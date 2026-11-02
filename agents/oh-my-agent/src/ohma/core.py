from dataclasses import dataclass,asdict
from pathlib import Path
import hashlib,json,sqlite3,subprocess,os
@dataclass
class Agent:
    name:str
    capabilities:list[str]
    entrypoint:str
    policy:str="sandbox"
@dataclass
class Node:
    id:str
    parent:str|None
    branch:str
    status:str
    evidence:str=""
def sid(*v): return hashlib.sha256("|".join(v).encode()).hexdigest()[:16]
class Registry:
    def __init__(self,p): self.p=Path(p); self.p.parent.mkdir(parents=True,exist_ok=True)
    def load(self):
        if not self.p.exists(): return []
        return json.loads(self.p.read_text())
    def add(self,a):
        xs=self.load(); xs=[x for x in xs if x["name"]!=a.name]; xs.append(asdict(a)); self.p.write_text(json.dumps(xs,indent=2))
class Tree:
    def __init__(self,p):
        self.db=Path(p); self.db.mkdir(parents=True,exist_ok=True); self.cx=sqlite3.connect(self.db/"tree.db")
        self.cx.execute("create table if not exists nodes(id primary key,parent,branch,status,evidence)"); self.cx.commit()
    def add(self,n): self.cx.execute("insert or replace into nodes values(?,?,?,?,?)",(n.id,n.parent,n.branch,n.status,n.evidence)); self.cx.commit()
    def all(self): return self.cx.execute("select id,parent,branch,status,evidence from nodes").fetchall()
class Verifier:
    def __init__(self,root): self.root=Path(root)
    def run(self):
        p=subprocess.run(["python3","-m","compileall","-q",str(self.root/"src")],capture_output=True,text=True)
        g=subprocess.run(["git","-C",str(self.root),"diff","--check"],capture_output=True,text=True)
        return {"compile":p.returncode==0,"diff_check":g.returncode==0}
class Evolution:
    def __init__(self,tree): self.tree=tree
    def branch(self,parent,name):
        n=sid(parent,name); self.tree.add(Node(n,parent,name,"candidate","awaiting evaluation")); return n
class ProviderMatrix:
    names=["openai","anthropic","google","azure_openai","aws_bedrock","vertex_ai","deepseek","qwen","mistral","xai","groq","together","fireworks","openrouter","ollama","litellm"]
    def status(self): return {x:bool(os.getenv(x.upper()+"_API_KEY") or x=="litellm") for x in self.names}
