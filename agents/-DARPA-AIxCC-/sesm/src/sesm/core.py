from dataclasses import dataclass,asdict
from pathlib import Path
import hashlib,json,sqlite3,subprocess
@dataclass
class Node:
    id:str
    parent:str|None
    capability:str
    status:str
    evidence:str=""
@dataclass
class Capability:
    name:str
    mode:str
    entrypoint:str
    rollback:str
def sid(*x): return hashlib.sha256("|".join(x).encode()).hexdigest()[:16]
class DiscoveryTree:
    def __init__(self,p):
        self.dir=Path(p); self.dir.mkdir(parents=True,exist_ok=True); self.cx=sqlite3.connect(self.dir/"tree.db")
        self.cx.execute("create table if not exists nodes(id primary key,parent,capability,status,evidence)"); self.cx.commit()
    def add(self,n): self.cx.execute("insert or replace into nodes values(?,?,?,?,?)",(n.id,n.parent,n.capability,n.status,n.evidence)); self.cx.commit()
    def all(self): return self.cx.execute("select id,parent,capability,status,evidence from nodes").fetchall()
class Memory:
    def __init__(self,p): self.p=Path(p); self.p.parent.mkdir(parents=True,exist_ok=True); self.cx=sqlite3.connect(self.p)
    def put(self,k,v): self.cx.execute("create table if not exists memory(k primary key,v)"); self.cx.execute("insert or replace into memory values(?,?)",(k,v)); self.cx.commit()
class Verification:
    def __init__(self,root): self.root=Path(root)
    def run(self):
        p=subprocess.run(["python3","-m","compileall","-q",str(self.root/"sesm/src")],capture_output=True,text=True)
        g=subprocess.run(["git","-C",str(self.root),"diff","--check"],capture_output=True,text=True)
        return {"compile":p.returncode==0,"diff_check":g.returncode==0}
class CapabilityRegistry:
    names=[
      ("orchestrator","enabled"),("state_machine","enabled"),("discovery_tree","enabled"),
      ("evolution_engine","enabled"),("verification_gate","enabled"),("tool_registry","enabled"),
      ("memory","enabled"),("mcp_gateway","enabled"),("aixcc_research","sandbox_manual"),
      ("fuzzing","sandbox_manual"),("patch_validation","sandbox_manual"),("llm_red_team","sandbox_manual"),
      ("lora_candidate_lab","offline_candidate_only"),("deployment","manual"),
      ("migration","disabled"),("economic_autonomy","simulation_only")]
    def export(self,p):
        Path(p).write_text(json.dumps([asdict(Capability(n,m,n,"revert-to-parent")) for n,m in self.names],indent=2))
