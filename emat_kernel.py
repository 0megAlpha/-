#!/usr/bin/env python3
import os,sys,json,subprocess
from pathlib import Path
import requests
BASE="http://127.0.0.1:4000/v1";KEY=os.environ.get("LITELLM_MASTER_KEY","");MODEL=os.environ.get("EMAT_MODEL","deepseek-v4-flash");WS=Path(os.environ.get("EMAT_WS","./workspace"))
def llm(s,u,t=0.6):
    r=requests.post(f"{BASE}/chat/completions",headers={"Authorization":f"Bearer {KEY}"},json={"model":MODEL,"temperature":t,"messages":[{"role":"system","content":s},{"role":"user","content":u}]},timeout=180)
    r.raise_for_status();return r.json()["choices"][0]["message"]["content"]
def builder(p,task):
    files="\n".join(f"--- {f.name} ---\n{f.read_text()}"for f in WS.glob("*.py"))
    return llm("只輸出完整可執行代碼。",f"代碼:\n{files}\n規則:{json.dumps(p.get('rules',[]))}\n任務:{task}")
def breaker(c):return llm("找崩潰點。沒問題輸出 CLEAN。",c,0.9)
def magistrate(c,r,p):
    out=llm('只輸出 JSON: {"verdict":"PASS|REJECT","reason":"...","new_rule":"..."}',f"報告:{r}\n代碼:{c}\n規則:{json.dumps(p.get('rules',[]))}",0.2)
    try:return json.loads(out[out.index("{"):out.rindex("}")+1])
    except:return{"verdict":"REJECT","reason":"unparseable","new_rule":None}
def loop(task,max_gen=10):
    WS.mkdir(parents=True,exist_ok=True);plan={"gen":0,"rules":[]}
    for g in range(1,max_gen+1):
        cand=builder(plan,task)
        files={}
        if"### FILE:"in cand:
            for chunk in cand.split("### FILE:")[1:]:
                name,_,body=chunk.partition("\n");files[name.strip()]=body.strip()
        else:files["main.py"]=cand.strip()
        for n,b in files.items():(WS/n).write_text(b)
        ok=True
        for n in files:
            if n.endswith(".py"):
                r=subprocess.run([sys.executable,"-m","py_compile",str(WS/n)],capture_output=True,text=True,timeout=30)
                if r.returncode!=0:ok=False;plan["rules"].append(f"gen{g}: syntax");break
        if not ok:continue
        rep=breaker(cand)
        if"CLEAN"not in rep.upper():
            v=magistrate(cand,rep,plan)
            if v["verdict"]!="PASS":
                if v.get("new_rule"):plan["rules"].append(v["new_rule"])
                continue
        plan["gen"]=g;print(f"PASS gen {g}");return
    print("max gen")
if __name__=="__main__":loop(sys.argv[1]if len(sys.argv)>1 else"寫一個帶 SQLite 的 REST API。")
