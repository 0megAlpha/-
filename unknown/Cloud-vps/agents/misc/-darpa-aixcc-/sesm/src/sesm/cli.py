import argparse,json
from pathlib import Path
from .core import *
def main():
 p=argparse.ArgumentParser(); p.add_argument("cmd",choices=["bootstrap","status","verify","capabilities"]); a=p.parse_args()
 root=Path(__file__).resolve().parents[3]; t=DiscoveryTree(root/".evolution"); rid=sid("sesm","portable-aixcc")
 t.add(Node(rid,None,"root","active","security-research engineering platform"))
 for n,m in CapabilityRegistry.names: t.add(Node(sid(rid,n),rid,n,m,"registry"))
 CapabilityRegistry().export(root/"sesm/config/capabilities.json")
 if a.cmd=="status": print(json.dumps(t.all(),indent=2))
 elif a.cmd=="capabilities": print(Path(root/"sesm/config/capabilities.json").read_text())
 elif a.cmd=="verify": print(json.dumps(Verification(root).run(),indent=2))
 else: print("SESM_BOOTSTRAP_OK")
if __name__=="__main__": main()
