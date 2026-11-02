from __future__ import annotations
import hashlib, json, mimetypes, os, shutil, subprocess, tempfile, threading, time, uuid
from pathlib import Path
from typing import Any
from fastapi import FastAPI, File, HTTPException, UploadFile
from fastapi.responses import FileResponse, JSONResponse, PlainTextResponse
from pydantic import BaseModel

ROOT = Path(os.environ.get("FILE_CENTER_ROOT", Path(__file__).resolve().parents[1] / "storage")).resolve()
FILES = ROOT / "files"
JOBS = ROOT / "jobs"
FILES.mkdir(parents=True, exist_ok=True); JOBS.mkdir(parents=True, exist_ok=True)
app = FastAPI(title="AGENT//THRONE File & Conversion Center", version="0.1.0")
lock = threading.Lock()

OPS = {
    "inspect": [],
    "archive_extract": ["bsdtar", "7z", "unzip"],
    "media_transcode": ["ffmpeg"],
    "image_convert": ["magick", "convert"],
    "office_convert": ["libreoffice", "soffice"],
    "android_repack": ["zipalign", "apksigner"],
    "ipa_inspect": ["unzip"],
    "ipa_to_apk": [],
}

def tool(name: str) -> str | None:
    return shutil.which(name)

def now() -> float: return time.time()

def job_path(jid: str) -> Path: return JOBS / f"{jid}.json"
def save_job(j: dict[str, Any]):
    tmp = job_path(j["id"]).with_suffix(".tmp")
    tmp.write_text(json.dumps(j, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(job_path(j["id"]))

def load_job(jid: str) -> dict[str, Any]:
    p = job_path(jid)
    if not p.exists(): raise HTTPException(404, "job not found")
    return json.loads(p.read_text(encoding="utf-8"))

def update_job(jid: str, **kw):
    with lock:
        j = load_job(jid); j.update(kw); j["event_seq"] = int(j.get("event_seq",0))+1; j["updated_at"] = now(); save_job(j)
        return j

def run_job(jid: str, file_path: Path, operation: str, options: dict[str, Any]):
    try:
        update_job(jid, state="running", progress=5, message="job started")
        if operation == "inspect":
            update_job(jid, state="completed", progress=100, result={"name":file_path.name,"size":file_path.stat().st_size,"mime":mimetypes.guess_type(file_path.name)[0] or "application/octet-stream"}, message="inspection complete")
            return
        if operation == "ipa_to_apk":
            update_job(jid, state="completed", progress=100, result={"mode":"assessment","direct_binary_conversion":False,"reason":"IPA and APK are different application packaging/runtime targets; a real port requires source code and an Android build target.","next_step":"Provide source/project and select an Android build workflow."}, message="porting assessment complete")
            return
        candidates = OPS.get(operation, [])
        exe = next((tool(x) for x in candidates if tool(x)), None)
        if not exe:
            raise RuntimeError(f"required adapter unavailable: {candidates}")
        outdir = ROOT / "outputs" / jid; outdir.mkdir(parents=True, exist_ok=True)
        target_ext = options.get("extension")
        stem = file_path.stem
        if operation == "media_transcode":
            if not target_ext: raise ValueError("options.extension is required")
            out = outdir / f"{stem}.{target_ext.lstrip('.') }"
            cmd = [exe, "-y", "-i", str(file_path), str(out)]
        elif operation == "image_convert":
            if not target_ext: raise ValueError("options.extension is required")
            out = outdir / f"{stem}.{target_ext.lstrip('.') }"; cmd = [exe, str(file_path), str(out)]
        elif operation == "office_convert":
            fmt = options.get("format", "pdf"); cmd=[exe,"--headless","--convert-to",fmt,"--outdir",str(outdir),str(file_path)]; out = outdir / f"{stem}.{fmt}"
        elif operation == "archive_extract":
            out = outdir; cmd=[exe,"-xf",str(file_path),"-C",str(outdir)] if Path(exe).name in ("bsdtar","tar") else [exe,"x",str(file_path),f"-o{outdir}"]
        elif operation == "ipa_inspect":
            out = outdir; cmd=[exe,"-l",str(file_path)]
        else: raise ValueError("unsupported operation")
        update_job(jid, progress=20, message="adapter selected", adapter=exe)
        p = subprocess.run(cmd, capture_output=True, text=True, timeout=int(options.get("timeout_seconds",900)), cwd=str(outdir))
        if p.returncode != 0: raise RuntimeError((p.stderr or p.stdout)[-4000:])
        update_job(jid, state="completed", progress=100, result={"output":str(out),"stdout":p.stdout[-4000:],"stderr":p.stderr[-4000:]}, message="job complete")
    except Exception as e:
        update_job(jid, state="failed", progress=100, error=str(e), message="job failed")

class JobRequest(BaseModel):
    file_id: str
    operation: str
    options: dict[str, Any] = {}

@app.get("/health")
def health(): return {"ok":True,"service":"file-conversion-center","time":now()}

@app.get("/api/capabilities")
def capabilities():
    return {"operations": {k:{"available": (k=="ipa_to_apk" or all(tool(x) for x in v)),"tools":v} for k,v in OPS.items()}}

@app.post("/api/files")
async def upload(file: UploadFile = File(...)):
    fid = uuid.uuid4().hex; safe = Path(file.filename or "upload.bin").name; dest = FILES / f"{fid}__{safe}"
    h=hashlib.sha256(); size=0
    with dest.open("wb") as f:
        while True:
            chunk=await file.read(1024*1024)
            if not chunk: break
            size += len(chunk); h.update(chunk); f.write(chunk)
    meta={"id":fid,"name":safe,"path":str(dest),"size":size,"sha256":h.hexdigest(),"mime":file.content_type or mimetypes.guess_type(safe)[0] or "application/octet-stream","created_at":now()}
    (FILES/f"{fid}.json").write_text(json.dumps(meta,ensure_ascii=False,indent=2),encoding="utf-8")
    return meta

def meta(fid: str):
    p=FILES/f"{fid}.json"
    if not p.exists(): raise HTTPException(404,"file not found")
    return json.loads(p.read_text(encoding="utf-8"))

@app.get("/api/files/{fid}")
def get_file(fid: str): return meta(fid)

@app.get("/api/files/{fid}/download")
def download(fid: str):
    m=meta(fid); return FileResponse(m["path"],filename=m["name"],media_type=m["mime"])

@app.get("/api/files/{fid}/preview")
def preview(fid: str):
    m=meta(fid); p=Path(m["path"])
    if m["mime"].startswith("text/") or p.suffix.lower() in {".md",".json",".yaml",".yml",".log",".txt"}:
        return PlainTextResponse(p.read_text(errors="replace")[:200000])
    return {"preview":"metadata-only","name":m["name"],"mime":m["mime"],"size":m["size"]}

@app.post("/api/jobs")
def create_job(req: JobRequest):
    if req.operation not in OPS: raise HTTPException(400,"unknown operation")
    m=meta(req.file_id); jid=uuid.uuid4().hex
    j={"id":jid,"file_id":req.file_id,"operation":req.operation,"options":req.options,"state":"queued","progress":0,"event_seq":0,"created_at":now(),"updated_at":now()}; save_job(j)
    threading.Thread(target=run_job,args=(jid,Path(m["path"]),req.operation,req.options),daemon=True).start()
    return j

@app.get("/api/jobs/{jid}")
def get_job(jid: str): return load_job(jid)

@app.post("/api/jobs/{jid}/cancel")
def cancel_job(jid: str):
    j=load_job(jid)
    if j["state"] in {"queued","running"}: return update_job(jid,state="cancel_requested",message="cancellation requested")
    return j
