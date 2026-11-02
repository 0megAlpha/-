import os
import io
import json
import uuid
import subprocess
import shutil
import urllib.parse
import urllib.request
from datetime import datetime
from flask import Flask, request, jsonify, send_file, send_from_directory
from flask_cors import CORS

BASE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(BASE)
UPLOADS = os.path.join(ROOT, "uploads")
OUTPUTS = os.path.join(ROOT, "outputs")
os.makedirs(UPLOADS, exist_ok=True)
os.makedirs(OUTPUTS, exist_ok=True)

app = Flask(__name__, static_folder=os.path.join(ROOT, "frontend"), static_url_path="")
CORS(app)

HISTORY_FILE = os.path.join(ROOT, "history.json")

def load_history():
    if not os.path.exists(HISTORY_FILE):
        return []
    try:
        with open(HISTORY_FILE) as f:
            return json.load(f)
    except Exception:
        return []

def save_history(entry):
    h = load_history()
    h.insert(0, entry)
    h = h[:500]
    with open(HISTORY_FILE, "w") as f:
        json.dump(h, f, ensure_ascii=False, indent=2)

def run_cmd(cmd, timeout=180):
    try:
        r = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return r.returncode, r.stdout, r.stderr
    except Exception as e:
        return 1, "", str(e)

@app.route("/")
def index():
    return send_from_directory(os.path.join(ROOT, "frontend"), "index.html")

@app.route("/api/health")
def health():
    return jsonify({"status": "ok", "time": datetime.now().isoformat()})

@app.route("/api/tools")
def tools():
    return jsonify({
        "ffmpeg": shutil.which("ffmpeg") is not None,
        "convert": shutil.which("convert") is not None,
        "pandoc": shutil.which("pandoc") is not None,
        "7z": shutil.which("7z") is not None or shutil.which("7za") is not None,
        "zip": shutil.which("zip") is not None,
        "unzip": shutil.which("unzip") is not None
    })

@app.route("/api/convert", methods=["POST"])
def convert():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    target = request.form.get("target", "").lower()
    f = request.files["file"]
    ext = os.path.splitext(f.filename)[1].lower().lstrip(".")
    uid = uuid.uuid4().hex[:12]
    src = os.path.join(UPLOADS, uid + "_" + f.filename)
    f.save(src)

    img_formats = ["png", "jpg", "jpeg", "webp", "svg", "bmp", "tiff"]
    audio_formats = ["mp3", "wav", "aac", "flac", "ogg", "m4a"]
    video_formats = ["mp4", "mov", "webm", "mkv", "avi"]
    doc_formats = ["pdf", "docx", "txt", "md", "html", "odt"]
    arc_formats = ["zip", "7z", "tar", "gz"]
    data_formats = ["json", "yaml", "yml", "csv", "xml"]

    out_ext = target if target else "out"
    out_name = uid + "." + out_ext
    out_path = os.path.join(OUTPUTS, out_name)

    rc = 1
    stderr = ""

    if target in img_formats and shutil.which("convert"):
        rc, so, stderr = run_cmd(["convert", src, out_path])
    elif target in audio_formats and shutil.which("ffmpeg"):
        rc, so, stderr = run_cmd(["ffmpeg", "-y", "-i", src, out_path])
    elif target in video_formats and shutil.which("ffmpeg"):
        rc, so, stderr = run_cmd(["ffmpeg", "-y", "-i", src, out_path])
    elif target in doc_formats and shutil.which("pandoc") and ext in doc_formats:
        rc, so, stderr = run_cmd(["pandoc", src, "-o", out_path])
    elif target in arc_formats and shutil.which("7z"):
        rc, so, stderr = run_cmd(["7z", "a", out_path, src])
    elif target in data_formats:
        try:
            if ext == "json":
                with open(src) as fh:
                    data = json.load(fh)
            elif ext in ["yaml", "yml"]:
                import yaml
                with open(src) as fh:
                    data = yaml.safe_load(fh)
            elif ext == "csv":
                import csv
                with open(src) as fh:
                    data = [row for row in csv.DictReader(fh)]
            else:
                data = {"raw": open(src).read()}
            if target == "json":
                with open(out_path, "w") as fh:
                    json.dump(data, fh, ensure_ascii=False, indent=2)
                rc = 0
            else:
                rc = 1
                stderr = "no converter for target " + target
        except Exception as e:
            rc = 1
            stderr = str(e)
    else:
        stderr = "unsupported conversion " + ext + " to " + target

    if rc != 0 or not os.path.exists(out_path):
        return jsonify({"error": "conversion failed", "detail": stderr[:500]}), 500

    size = os.path.getsize(out_path)
    entry = {
        "id": uid,
        "type": "convert",
        "src": f.filename,
        "dst": out_name,
        "from": ext,
        "to": target,
        "size": size,
        "time": datetime.now().isoformat()
    }
    save_history(entry)
    return jsonify({"status": "ok", "file": out_name, "size": size, "url": "/api/download/" + out_name})

@app.route("/api/download/<name>")
def download(name):
    p = os.path.join(OUTPUTS, name)
    if not os.path.exists(p):
        return jsonify({"error": "not found"}), 404
    return send_file(p, as_attachment=True)

@app.route("/api/import/url", methods=["POST"])
def import_url():
    data = request.get_json() or {}
    url = data.get("url", "").strip()
    if not url:
        return jsonify({"error": "no url"}), 400

    parsed = urllib.parse.urlparse(url)
    filename = os.path.basename(parsed.path) or "import"
    uid = uuid.uuid4().hex[:12]
    out_name = uid + "_" + filename
    out_path = os.path.join(UPLOADS, out_name)

    kind = "unknown"
    lower = url.lower()
    if any(lower.endswith(x) for x in [".png", ".jpg", ".jpeg", ".webp", ".gif", ".svg"]):
        kind = "image"
    elif any(lower.endswith(x) for x in [".mp4", ".mov", ".webm", ".mkv"]):
        kind = "video"
    elif any(lower.endswith(x) for x in [".mp3", ".wav", ".aac", ".flac"]):
        kind = "audio"
    elif lower.endswith(".pdf"):
        kind = "pdf"
    elif "github.com" in lower:
        kind = "github"

    if kind == "github":
        clone_dir = os.path.join(ROOT, "repos", uid)
        os.makedirs(clone_dir, exist_ok=True)
        rc, so, se = run_cmd(["git", "clone", "--depth", "1", url, clone_dir], timeout=300)
        if rc != 0:
            return jsonify({"error": "clone failed", "detail": se[:500]}), 500
        save_history({"id": uid, "type": "github", "url": url, "dir": clone_dir, "time": datetime.now().isoformat()})
        return jsonify({"status": "ok", "kind": "github", "path": clone_dir})

    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=60) as resp:
            with open(out_path, "wb") as f:
                shutil.copyfileobj(resp, f)
        size = os.path.getsize(out_path)
        save_history({"id": uid, "type": "url", "url": url, "kind": kind, "file": out_name, "size": size, "time": datetime.now().isoformat()})
        return jsonify({"status": "ok", "kind": kind, "file": out_name, "size": size})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/api/history")
def history():
    return jsonify(load_history())

@app.route("/api/outputs")
def outputs():
    items = []
    for n in os.listdir(OUTPUTS):
        p = os.path.join(OUTPUTS, n)
        items.append({"name": n, "size": os.path.getsize(p), "time": datetime.fromtimestamp(os.path.getmtime(p)).isoformat()})
    items.sort(key=lambda x: x["time"], reverse=True)
    return jsonify(items)

@app.route("/api/media/repair", methods=["POST"])
def repair():
    if "file" not in request.files:
        return jsonify({"error": "no file"}), 400
    f = request.files["file"]
    action = request.form.get("action", "upscale")
    uid = uuid.uuid4().hex[:12]
    src = os.path.join(UPLOADS, uid + "_" + f.filename)
    f.save(src)
    ext = os.path.splitext(f.filename)[1].lower()
    out_name = uid + "_repaired" + ext
    out_path = os.path.join(OUTPUTS, out_name)

    if ext in [".png", ".jpg", ".jpeg", ".webp"] and shutil.which("convert"):
        if action == "upscale":
            rc, so, se = run_cmd(["convert", src, "-resize", "200%", "-sharpen", "0x1", out_path])
        elif action == "denoise":
            rc, so, se = run_cmd(["convert", src, "-enhance", "-despeckle", out_path])
        elif action == "grayscale":
            rc, so, se = run_cmd(["convert", src, "-colorspace", "Gray", out_path])
        else:
            rc, so, se = run_cmd(["convert", src, out_path])
    elif ext in [".mp4", ".mov", ".webm"] and shutil.which("ffmpeg"):
        rc, so, se = run_cmd(["ffmpeg", "-y", "-i", src, "-vf", "scale=iw*1.5:ih*1.5", "-c:v", "libx264", "-crf", "23", out_path])
    else:
        return jsonify({"error": "unsupported repair target"}), 400

    if rc != 0 or not os.path.exists(out_path):
        return jsonify({"error": "repair failed", "detail": se[:500]}), 500
    save_history({"id": uid, "type": "repair", "action": action, "src": f.filename, "dst": out_name, "time": datetime.now().isoformat()})
    return jsonify({"status": "ok", "file": out_name, "url": "/api/download/" + out_name})

@app.route("/api/automation/workflow", methods=["POST"])
def automation_workflow():
    data = request.get_json() or {}
    kind = data.get("kind", "n8n")
    name = data.get("name", "workflow")
    steps = data.get("steps", [])
    uid = uuid.uuid4().hex[:12]
    out_name = uid + "_" + name + ".json"
    out_path = os.path.join(OUTPUTS, out_name)

    if kind == "n8n":
        nodes = []
        connections = {}
        prev = None
        for i, s in enumerate(steps):
            node_id = "node" + str(i)
            nodes.append({
                "parameters": s.get("params", {}),
                "id": node_id,
                "name": s.get("name", "step" + str(i)),
                "type": s.get("type", "n8n-nodes-base.httpRequest"),
                "typeVersion": 1,
                "position": [250 + i * 200, 300]
            })
            if prev:
                connections[prev] = {"main": [[{"node": s.get("name", "step" + str(i)), "type": "main", "index": 0}]]}
            prev = s.get("name", "step" + str(i))
        wf = {"nodes": nodes, "connections": connections}
    elif kind == "github-actions":
        lines = ["name: " + name, "on:", "  push:", "    branches: [main]", "jobs:", "  build:", "    runs-on: ubuntu-latest", "    steps:"]
        lines.append("      - uses: actions/checkout@v4")
        for s in steps:
            lines.append("      - name: " + s.get("name", "step"))
            lines.append("        run: " + s.get("run", "echo step"))
        wf_text = "\n".join(lines)
        with open(out_path, "w") as f:
            f.write(wf_text)
        save_history({"id": uid, "type": "automation", "kind": kind, "file": out_name, "time": datetime.now().isoformat()})
        return jsonify({"status": "ok", "file": out_name, "url": "/api/download/" + out_name})
    else:
        wf = {"kind": kind, "name": name, "steps": steps}

    with open(out_path, "w") as f:
        json.dump(wf, f, ensure_ascii=False, indent=2)
    save_history({"id": uid, "type": "automation", "kind": kind, "file": out_name, "time": datetime.now().isoformat()})
    return jsonify({"status": "ok", "file": out_name, "url": "/api/download/" + out_name})

@app.route("/api/shortcut/generate", methods=["POST"])
def shortcut_generate():
    data = request.get_json() or {}
    name = data.get("name", "My Shortcut")
    steps = data.get("steps", [])
    uid = uuid.uuid4().hex[:12]
    out_name = uid + "_" + name.replace(" ", "_") + ".shortcut"
    out_path = os.path.join(OUTPUTS, out_name)

    actions_xml = []
    for s in steps:
        action_id = s.get("identifier", "is.workflow.actions.comment")
        params = s.get("params", {})
        param_xml = ""
        for k, v in params.items():
            param_xml += '<key>' + k + '</key><string>' + str(v) + '</string>'
        actions_xml.append(
            '<dict><key>WFWorkflowActionIdentifier</key><string>' + action_id + '</string>'
            '<key>WFWorkflowActionParameters</key><dict>' + param_xml + '</dict></dict>'
        )

    plist = (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<!DOCTYPE plist PUBLIC "-//Apple//DTD PLIST 1.0//EN" "http://www.apple.com/DTDs/PropertyList-1.0.dtd">\n'
        '<plist version="1.0"><dict>'
        '<key>WFWorkflowClientVersion</key><string>1200</string>'
        '<key>WFWorkflowMinimumClientVersionString</key><string>900</string>'
        '<key>WFWorkflowIcon</key><dict><key>WFWorkflowIconStartColor</key><integer>4282601983</integer><key>WFWorkflowIconGlyphNumber</key><integer>59511</integer></dict>'
        '<key>WFWorkflowImportQuestions</key><array/>'
        '<key>WFWorkflowTypes</key><array/>'
        '<key>WFWorkflowName</key><string>' + name + '</string>'
        '<key>WFWorkflowActions</key><array>' + "".join(actions_xml) + '</array>'
        '</dict></plist>'
    )

    with open(out_path, "w", encoding="utf-8") as f:
        f.write(plist)

    save_history({"id": uid, "type": "shortcut", "name": name, "file": out_name, "time": datetime.now().isoformat()})
    return jsonify({"status": "ok", "file": out_name, "url": "/api/download/" + out_name})

@app.route("/api/security/scan", methods=["POST"])
def security_scan():
    data = request.get_json() or {}
    target = data.get("target", "/root/AI-Agent-Skill")
    results = {}
    for tool, cmd in [
        ("trivy", ["trivy", "fs", "--quiet", target]),
        ("gitleaks", ["gitleaks", "detect", "--no-git", "-s", target]),
        ("semgrep", ["semgrep", "--config=auto", "--quiet", target])
    ]:
        if shutil.which(cmd[0]):
            rc, so, se = run_cmd(cmd, timeout=120)
            results[tool] = {"rc": rc, "out": so[:2000], "err": se[:1000]}
        else:
            results[tool] = {"missing": True}
    save_history({"id": uuid.uuid4().hex[:12], "type": "security_scan", "target": target, "time": datetime.now().isoformat()})
    return jsonify(results)

@app.route("/api/media/status")
def media_status():
    return jsonify({
        "uploads": len(os.listdir(UPLOADS)) if os.path.exists(UPLOADS) else 0,
        "outputs": len(os.listdir(OUTPUTS)) if os.path.exists(OUTPUTS) else 0,
        "history": len(load_history()),
        "time": datetime.now().isoformat()
    })

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8099, debug=False)
