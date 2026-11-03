#!/usr/bin/env python3
import argparse,json,os,re,subprocess,urllib.parse,urllib.request
UA="Ai-Agent-Skill-research-gateway/1.0"
def fetch(url,headers=None):
    h={"User-Agent":UA,"Accept":"text/html,application/json"}; h.update(headers or {})
    with urllib.request.urlopen(urllib.request.Request(url,headers=h),timeout=12) as r:return r.status,r.read().decode("utf-8","replace")
def web(q):
    s,h=fetch("https://html.duckduckgo.com/html/?"+urllib.parse.urlencode({"q":q}))
    out=[]
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>',hlre.S):
        out.append({"title":re.sub("<.*?>","",m.group(2)).strip(),"url":urllib.parse.unquote(m.group(1))})
        if len(out)>=8:break
    return {"engine":"duckduckgo-html","query":q,"results":out,"http_status":s}
def github(q):
    s,b=fetch("https://api.github.com/search/repositories?"+urllib.parse.urlencode({"q":q,"per_page":8}),{"Accept":"application/vnd.github+json"})
    d=json.loads(b);return {"engine":"github-rest","query":q,"results":[{"name":x.get("full_name"),"url":x.get("html_url"),"description":x.get("description")} for x in d.get("items",[])],"http_status":s}
def repo(path,pattern=""):
    root=os.path.realpath(path)
    if not os.path.isdir(os.path.join(root,".git")):raise ValueError("not a git repository")
    a=["git","-C",root,"grep","-nI","-E",pattern,"--","*.py","*.js","*.ts","*.yaml","*.yml","*.md"] if pattern else ["git","-C",root,"ls-files"]
    p=subprocess.run(a,capture_output=True,text=True,timeout=15);return {"engine":"git-local","path":root,"results":p.stdout.splitlines()[:50],"returncode":p.returncode}
p=argparse.ArgumentParser();s=p.add_subparsers(dest="op", required=True)
for n in ("web-search","github-search"):s.add_parser(n); s.add_parser(n).add_argument("query")
x=s.add_parser("repo-search");x.add_argument("path");x.add_argument("pattern",nargs="?")
a=p.parse_args()
r=web(a.query) if a.op=="web-search" else github(a.query) if a.op=="github-search" else repo(a.path,a.pattern or "")
print(json.dumps({"ok":True,"result":s}, ensure_ascii=False,indent=2))
