#!/usr/bin/env python3
from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlparse,parse_qs
from pathlib import Path
import json,os,platform,shutil,socket,subprocess,time
ROOT=Path(__file__).resolve().parents[1]
HOST=os.getenv("AGENT_THRONE_HOST","127.0.0.1")
PORT=int(os.getenv("AGENT_THRONE_PORT","8787"))
URL=os.getenv("AGENT_THRONE_PROVIDER_URL","").rstrip("/")
MODEL=os.getenv("AGENT_THRONE_MODEL","")
KEY=os.getenv("AGENT_THRONE_API_KEY","")
AGENTS=["Hermes","OpenHands","DSH","OpenCode","Cline","OpenWebUI","Lody","Conduit"]
SAFE={"status":["bash","-lc","hostname; uptime -p 2>/dev/null; cut -d' ' -f1-3 /proc/loadavg"],"ps":["bash","-lc","ps -eo pid,comm,%cpu,%mem,args --sort=-%cpu | head -35"],"ports":["bash","-lc","ss -lntup 2>/dev/null | head -80"],"git":["bash","-lc","for d in /root/ai-agent-skill /root/open-hands /root/007-hermes /root/opencode; do [ -d \"$d/.git\" ] || continue; echo [$d]; git -C \"$d\" status --short --branch 2>/dev/null | head -5; done"]}
def mem():
 m={x.split(":")[0]:int(x.split()[1]) for x in Path("/proc/meminfo").read_text().splitlines()}
 return round((1-m["MemAvailable"]/m["MemTotal"])*100,1)
def status():
 u=shutil.disk_usage("/")
 cpu=min(100,round(os.getloadavg()[0]/(os.cpu_count() or 1)*100,1))
 return {"host":socket.gethostname(),"platform":platform.platform(),"uptime":subprocess.run(["uptime","-p"],capture_output=True,text=True).stdout.strip(),"cpu":cpu,"ram":mem(),"disk":round(u.used/u.total*100,1),"agents":AGENTS}
def observe(k):
 if k not in SAFE: raise ValueError("unsupported observation")
 p=subprocess.run(SAFE[k],capture_output=True,text=True,timeout=4)
 return {"kind":k,"output":p.stdout[-12000:],"returncode":p.returncode}
def chat(msg,agent,session):
 if not URL:return {"reply":"LOCAL ROUTER: "+agent+" / session "+session[:8]+" / provider adapter ready; no endpoint configured."}
 import urllib.request
 body=json.dumps({"model":MODEL or "local","messages":[{"role":"user","content":msg}],"metadata":{"agent":agent,"session":session}}).encode(); h={"Content-Type":"application/json"};h.update({"Authorization":"Bearer "+KEY} if KEY else {})
 q=urllib.request.Request(URL+"/chat/completions",data=body,headers=h)
 with urllib.request.urlopen(q,timeout=45) as r:d=json.loads(r.read().decode())
 return {"reply":d.get("choices",[{}])[0].get("message",{}).get("content",""),"provider":"openai-compatible"}
class H(BaseHTTPRequestHandler):
 def out(self,x,code=200,ctype="application/json"):
  b=x if isinstance(x,bytes) else json.dumps(x,ensure_ascii=False).encode()
  self.send_response(code);self.send_header("Content-Type",ctype);self.send_header("Content-Length",str(len(b)));self.send_header("Cache-Control","no-store");self.end_headers();self.wfile.write(b)
 def do_GET(self):
  p=urlparse(self.path)
  if p.path=="/api/status":return self.out(status())
  if p.path=="/api/observe":
   try:return self.out(observe(parse_qs(p.query).get("kind",["status"])[0]))
   except Exception as e:return self.out({"error":str(e)},400)
  if p.path=="/api/health":return self.out({"ok":True,"service":"agent-throne"})
  if p.path=="/api/agents":return self.out({"agents":AGENTS})
  rel=p.path.lstrip("/") or "index.html";f=(ROOT/"portal"/rel).resolve();base=(ROOT/"portal").resolve()
  if not str(f).startswith(str(base)) or not f.is_file():f=base/"index.html"
  ct="text/html; charset=utf-8" if f.suffix==".html" else "text/plain; charset=utf-8"
  if f.suffix==".js":ct="application/javascript"
  if f.suffix==".css":ct="text/css"
  if f.suffix==".svg":ct="image/svg+xml"
  return self.out(f.read_bytes(),200,ct)
 def do_POST(self):
  if urlparse(self.path).path!="/api/chat":return self.out({"error":"not found"},404)
  try:
   n=int(self.headers.get("Content-Length","0"));d=json.loads(self.rfile.read(n));msg=str(d.get("message","")).strip()
   if not msg or len(msg)>12000:raise ValueError("invalid message")
   return self.out(chat(msg,str(d.get("agent","router")),str(d.get("session",""))))
  except Exception as e:return self.out({"error":str(e)},502)
 def log_message(self,*a):pass
if __name__=="__main__":
 print("AGENT//THRONE http://"+HOST+":"+str(PORT))
 ThreadingHTTPServer((HOST,PORT),H).serve_forever()
