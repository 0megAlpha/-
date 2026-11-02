from dataclasses import dataclass,asdict
from pathlib import Path
import json,sqlite3,hashlib,time,subprocess
@dataclass
class Node:
    id:str
    parent:str|None
    kind:str
    status:str
    evidence:str=""
@dataclass
class Candidate:
    id:str
    parent:str
    change:str
    tests:list[str]
def sid(*x): return hashlib.sha256("|".join(x).encode()).hexdigest()[:16]
class DiscoveryTree:
    def __init__(self,db):
        self.db=db; db.mkdir(parents=True,exist_ok=True)
        self.c=db/"state.db"; self.cx=sqlite3.connect(self.c)
        self.cx.execute("create table if not exists nodes(id text primary key,parent text,kind text,status text,evidence text)")
        self.cx.commit()
    def add(self,n):
        self.cx.execute("insert or replace into nodes values(?,?,?,?,?)",(n.id,n.parent,n.kind,n.status,n.evidence)); self.cx.commit()
    def nodes(self): return [Node(*r) for r in self.cx.execute("select * from nodes")]
class VerificationGate:
    def run(self,root):
        checks=[("compile",["python3","-m","compileall","-q",str(root)]),("git-diff-check",["git","-C",str(root),"diff","--check"])]
        out={}
        for k,c in checks:
            p=subprocess.run(c,capture_output=True,text=True); out[k]=p.returncode==0
        return out
class ProviderRegistry:
    providers=["openai","openai_compatible","anthropic","google","azure_openai","aws_bedrock","vertex_ai","deepseek","qwen","mistral","xai","groq","together","fireworks","openrouter","ollama","litellm"]
    def ready(self,env):
        generic_url = env.get("OPENAI_COMPATIBLE_BASE_URL") or env.get("OPENAI_BASE_URL")
        generic_key = env.get("OPENAI_COMPATIBLE_API_KEY") or env.get("OPENAI_API_KEY")
        out = {}
        for p in self.providers:
            if p == "openai_compatible":
                out[p] = bool(generic_url or generic_key)
            elif p == "openai":
                out[p] = bool(env.get("OPENAI_API_KEY") or env.get("OPENAI_BASE_URL") or env.get("OPENAI_COMPATIBLE_BASE_URL"))
            else:
                out[p] = bool(env.get(p.upper()+"_API_KEY") or env.get(p.upper()+"_BASE_URL") or p=="litellm")
        return out
class EvolutionEngine:
    def __init__(self,tree): self.tree=tree
    def candidate(self,parent,change):
        c=Candidate(sid(parent,change),parent,change,["compile","regression","security"])
        self.tree.add(Node(c.id,parent,"candidate","proposed")); return c
class Harness:
    def __init__(self,root):
        self.root=Path(root); self.tree=DiscoveryTree(self.root/".evolution")
    def bootstrap(self):
        root=sid("ROOT","portable-observable-self-validating")
        self.tree.add(Node(root,None,"root","active","invariant core"))
        for kind in ["state-machine","tool-registry","memory","mcp","browser-e2e","evaluation","provider-gateway","deployment-gate","observability"]:
            self.tree.add(Node(sid(root,kind),root,kind,"ready","registered"))
        return root
