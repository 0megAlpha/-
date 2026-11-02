#!/usr/bin/env bash
set -euo pipefail
ROOT=/root/AI-Agent-Skill
python3 - <<'PY'
import json, urllib.request, urllib.error, socket, subprocess
from pathlib import Path
env={}
for line in Path('/root/.agent.env').read_text().splitlines():
 s=line.strip()
 if s and not s.startswith('#') and '=' in s:
  k,v=s.split('=',1); env[k]=v.strip().strip('"').strip("'")
key=env.get('LITELLM_MASTER_KEY','')
assert len(key)>=32, 'missing/short gateway key'
def readj(p): return json.loads(Path(p).read_text())
def request(url,token=None):
 headers={}
 if token: headers['Authorization']='Bearer '+token
 req=urllib.request.Request(url,headers=headers)
 try:
  with urllib.request.urlopen(req,timeout=8) as r:
   body=r.read()
   try: data=json.loads(body)
   except: data={}
   return r.status,data
 except urllib.error.HTTPError as e: return e.code,{}
def post_json(url, token, payload, timeout=20):
 req=urllib.request.Request(url,data=json.dumps(payload).encode(),headers={'Authorization':'Bearer '+token,'Content-Type':'application/json'})
 try:
  with urllib.request.urlopen(req,timeout=timeout) as r: return r.status,json.loads(r.read())
 except urllib.error.HTTPError as e:
  try: data=json.loads(e.read())
  except: data={}
  return e.code,data
for name,url in [('gateway','http://127.0.0.1:4000/v1/models'),('openhands-bridge','http://10.0.0.1:4001/v1/models')]:
 status,data=request(url,key)
 ids=[x.get('id') for x in data.get('data',[]) if isinstance(x,dict)]
 assert status==200, f'{name} authenticated model catalog HTTP {status}'
 for model in ['my-model','deepseek-free','nvidia/meta/llama-3.1-8b-instruct','nvidia/deepseek-ai/deepseek-r1','nvidia/qwen/qwen3-32b']:
  assert model in ids, f'{name} missing model alias {model}'
 noauth,_=request(url)
 assert noauth in (401,403), f'{name} unauthenticated model catalog returned {noauth}'
 print('PASS',name,'authenticated model catalog',len(ids),'aliases; unauthenticated rejected')
# Verify actual generation and one complete function-tool round-trip through both public seams.
for name,url in [('gateway','http://127.0.0.1:4000/v1/chat/completions'),('openhands-bridge','http://10.0.0.1:4001/v1/chat/completions')]:
 status,data=post_json(url,key,{'model':'my-model','messages':[{'role':'user','content':'Reply exactly INFERENCE-OK.'}],'max_tokens':16,'temperature':0})
 assert status==200, f'{name} generation HTTP {status}: {str(data)[:200]}'
 msg=data.get('choices',[{}])[0].get('message',{})
 assert 'INFERENCE-OK' in str(msg.get('content') or ''), f'{name} generation returned no expected content'
 tool_payload={'model':'my-model','messages':[{'role':'user','content':'Call ping with value OK. Do not answer in text.'}],'tools':[{'type':'function','function':{'name':'ping','description':'Return a value to the caller','parameters':{'type':'object','properties':{'value':{'type':'string'}},'required':['value'],'additionalProperties':False}}}],'tool_choice':'required','max_tokens':128,'temperature':0}
 status,data=post_json(url,key,tool_payload)
 assert status==200, f'{name} tool-call request HTTP {status}: {str(data)[:200]}'
 msg=data.get('choices',[{}])[0].get('message',{}); calls=msg.get('tool_calls') or []
 assert calls and calls[0].get('function',{}).get('name')=='ping', f'{name} did not emit ping tool call'
 args=json.loads(calls[0]['function'].get('arguments') or '{}')
 assert args.get('value')=='OK', f'{name} tool arguments mismatch: {args}'
 tool_id=calls[0].get('id')
 messages=tool_payload['messages']+[msg,{'role':'tool','tool_call_id':tool_id,'content':'pong: OK'}]
 status,final=post_json(url,key,{'model':'my-model','messages':messages,'max_tokens':24,'temperature':0})
 assert status==200, f'{name} tool-result continuation HTTP {status}: {str(final)[:200]}'
 answer=final.get('choices',[{}])[0].get('message',{}).get('content') or ''
 assert 'OK' in answer, f'{name} failed to continue after tool result: {answer!r}'
 print('PASS',name,'live inference + function tool call + tool-result continuation')
assert request('http://127.0.0.1:4000/health/readiness')[0]==200
assert subprocess.run(['systemctl','is-active','--quiet','litellm.service']).returncode==0
assert subprocess.run(['systemctl','is-active','--quiet','openhands-litellm-bridge.service']).returncode==0
assert subprocess.run(['systemctl','is-active','--quiet','hermes-api.service']).returncode==0
assert subprocess.run(['systemctl','is-active','--quiet','dsh-agent.service']).returncode==0
assert subprocess.run(['systemctl','is-active','--quiet','litellm-agent.service']).returncode!=0
# The container network must reach the bridge; HTTP model discovery above verifies the host side.
s=socket.socket(); s.settimeout(3); rc=s.connect_ex(('10.0.0.1',4001)); s.close()
assert rc==0, f'OpenHands bridge TCP not reachable: {rc}'
h=readj('/root/.hermes/config.json'); d=readj('/root/.dsh/agent-config.json')
o=readj('/root/.openhands/settings.json'); oc=readj('/root/.config/opencode/opencode.json'); cl=readj('/root/.claude/settings.json')
assert h['llm']['model']=='my-model' and h['llm']['api_key']==key
assert d['llm']['model']=='my-model' and d['llm']['api_key']==key
ollm=o['agent_settings']['llm']
assert ollm['base_url']=='http://host.docker.internal:4001/v1' and ollm['api_key']==key and ollm['model']=='openai/my-model'
prov=oc['provider']['litellm']
assert prov['options']['baseURL']=='http://127.0.0.1:4000/v1' and prov['options']['apiKey']==key
assert oc['model']=='litellm/my-model' and 'my-model' in prov['models']
assert cl['env']['ANTHROPIC_BASE_URL']=='http://127.0.0.1:4000' and cl['env']['ANTHROPIC_AUTH_TOKEN']==key and cl['model']=='my-model'
print('PASS agent configuration consistency: Hermes, DSH, OpenCode, Claude Code, OpenHands host settings')
print('PASS gateway readiness, single active LiteLLM service, bridge network')
# Verify OpenHands runtime env without printing credentials.
r=subprocess.run(['docker','exec','openhands','python3','-c',"import os,socket; assert os.environ.get('LLM_MODEL')=='openai/my-model'; assert os.environ.get('LLM_BASE_URL')=='http://host.docker.internal:4001/v1'; assert bool(os.environ.get('LLM_API_KEY')); s=socket.socket(); s.settimeout(3); rc=s.connect_ex(('host.docker.internal',4001)); s.close(); assert rc==0"],capture_output=True,text=True,timeout=10)
assert r.returncode==0, 'OpenHands runtime LLM env or bridge check failed'
print('PASS OpenHands live container has LLM model/base/key and bridge TCP')
# Cline already has an OpenAI-compatible provider; preserve it instead of overwriting its NVIDIA connection.
cline=readj('/root/.cline/data/settings/providers.json')
cp=cline['providers']['openai-compatible']['settings']
assert cp.get('provider')=='openai-compatible' and cp.get('apiKey') and cp.get('baseUrl')
print('PASS Cline existing OpenAI-compatible provider remains configured')
# OpenWebUI already has provider connections; verify the existing set remains intact.
import sqlite3
db=sqlite3.connect('file:/opt/open-webui/data/webui.db?mode=ro',uri=True)
def webui_get(k):
 row=db.execute('select value from config where "key"=?',(k,)).fetchone()
 return json.loads(row[0]) if row else None
urls=webui_get('openai.api_base_urls') or []
keys=webui_get('openai.api_keys') or []
configs=webui_get('openai.api_configs') or {}
assert len(urls)>=14 and len(urls)==len(keys)==len(configs)
print('PASS OpenWebUI existing provider connections preserved:',len(urls))
db.close()
# A broken duplicate Docker gateway must stay stopped; systemd litellm.service is canonical.
r=subprocess.run(['docker','inspect','--format','{{.State.Status}}|{{.HostConfig.RestartPolicy.Name}}','litellm-proxy'],capture_output=True,text=True,timeout=5)
if r.returncode == 0:
    assert r.stdout.strip() == 'exited|no', 'duplicate Docker LiteLLM proxy should remain stopped'
    print('PASS duplicate Docker gateway disabled; single systemd gateway active')
else:
    inventory=subprocess.run(['docker','container','ls','-a','--format','{{.Names}}'],capture_output=True,text=True,timeout=5)
    assert inventory.returncode == 0, 'unable to verify Docker container inventory'
    assert 'litellm-proxy' not in inventory.stdout.splitlines(), 'duplicate Docker LiteLLM proxy exists but inspect failed'
    print('PASS duplicate Docker gateway container absent; single systemd gateway active')
print('PASS live model inference and function-tool round-trip tested on gateway and OpenHands bridge.')
PY
bash -n "$ROOT/All-in/tests/verify_agent_api_compat.sh"
echo "PASS shell syntax"
