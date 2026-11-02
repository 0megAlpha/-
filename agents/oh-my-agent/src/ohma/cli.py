import argparse,json
from pathlib import Path
from .core import *
def main():
 p=argparse.ArgumentParser(); p.add_argument("cmd",choices=["bootstrap","status","verify","providers"]); a=p.parse_args()
 root=Path(__file__).resolve().parents[2]; t=Tree(root/".evolution"); r=Registry(root/"config/agents.json")
 rootid=sid("oh-my-agent","invariant"); t.add(Node(rootid,None,"root","active","portable multi-agent evolution"))
 for b in ["statem-execution","hyperagents-meta-planning","dgm-candidate-evolution","harness-evaluation","mcp-gateway","agent-registry","memory","security-gate","observability","provider-gateway"]:
  t.add(Node(sid(rootid,b),rootid,b,"ready","registered"))
 for agent in [Agent("openhands",["code","terminal","browser"],"openhands"),Agent("hermes",["orchestration"],"hermes"),Agent("opencode",["code"],"opencode"),Agent("dsh",["code","web","sandbox"],"dsh"),Agent("cline",["code","acp"],"cline"),Agent("cuga",["browser","agent"],"cuga"),Agent("pentestgpt",["security-research"],"pentestgpt")]: r.add(agent)
 if a.cmd=="status": print(json.dumps(t.all(),indent=2))
 elif a.cmd=="providers": print(json.dumps(ProviderMatrix().status(),indent=2))
 elif a.cmd=="verify": print(json.dumps(Verifier(root).run(),indent=2))
 else: print("OH_MY_AGENT_BOOTSTRAP_OK")
if __name__=="__main__": main()
