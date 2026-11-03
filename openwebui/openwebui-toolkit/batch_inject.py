import os, requests, glob

OWUI_URL = os.getenv("OWUI_URL", "http://localhost:8080")
OWUI_KEY = os.getenv("OWUI_API_KEY", "your-owui-api-key")
HEADERS = {"Authorization": f"Bearer {OWUI_KEY}"}

# 自動掃描所有 .py 插件並上傳
for py_file in glob.glob("**/*.py", recursive=True):
    if "batch_inject" in py_file: continue
    with open(py_file, "r") as f:
        content = f.read()
    payload = {"id": os.path.basename(py_file).replace(".py",""), "content": content}
    try:
        requests.post(f"{OWUI_URL}/api/v1/functions/create", json=payload, headers=HEADERS)
        print(f"[+] 注入成功: {py_file}")
    except Exception as e:
        print(f"[-] 注入失敗: {py_file} ({e})")
