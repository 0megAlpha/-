import argparse,json,os
from pathlib import Path
from .core import Harness,VerificationGate,ProviderRegistry
def main():
 p=argparse.ArgumentParser(); p.add_argument("cmd",choices=["bootstrap","status","verify","providers"]); a=p.parse_args()
 h=Harness(Path(__file__).resolve().parents[2]); h.bootstrap()
 if a.cmd=="status": print(json.dumps([x.__dict__ for x in h.tree.nodes()],indent=2))
 elif a.cmd=="verify": print(json.dumps(VerificationGate().run(h.root.parent.parent),indent=2))
 elif a.cmd=="providers": print(json.dumps(ProviderRegistry().ready(os.environ),indent=2))
 else: print("SEE_BOOTSTRAP_OK")
if __name__=="__main__": main()
