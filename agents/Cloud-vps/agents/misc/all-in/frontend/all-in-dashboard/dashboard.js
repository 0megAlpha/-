/* ============================================================
 * All-in Dashboard — 真實數據接入（2026.08.16 修復 4）
 * 資料來源（全部為真實 fetch，失敗即降級顯示，不假造數據）：
 *   1) Hermes /health、/v1/agents/status、/v1/chat/completions、/v1/sesm/state
 *   2) Qdrant /collections 與 /collections/{name}（記憶點數）
 * 端點不存在或 CORS 未開時 → 面板顯示 offline / unknown。
 * ============================================================ */

const DEFAULT_HERMES = '/api/hent/hermes';
const DEFAULT_QDRANT = '/api/hent/qdrant';
const FALLBACK_AGENTS = ['hermes','openhands','opencode','kilo-code','goose','aider',
                         'crush','continue','mini-swe-agent','swe-agent','claude-code','kimi-code'];

let cfg = {
  hermes: localStorage.getItem('allin_hermes_base') || DEFAULT_HERMES,
  qdrant: localStorage.getItem('allin_qdrant_base') || DEFAULT_QDRANT,
  key:   ''
};

function authHeaders() {
  return cfg.key ? { 'Authorization': 'Bearer ' + cfg.key } : {};
}

async function fetchJSON(url, opts = {}) {
  try {
    const res = await fetch(url, {
      ...opts,
      headers: { 'Content-Type': 'application/json', ...authHeaders(), ...(opts.headers || {}) }
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (e) {
    return { __error: String(e && e.message ? e.message : e) };
  }
}

/* ---------- 連線設定 ---------- */
function initConfigUI() {
  document.getElementById('cfg-base').value = cfg.hermes;
  document.getElementById('cfg-qdrant').value = cfg.qdrant;
  document.getElementById('cfg-key').value = cfg.key;
}
function saveConfig() {
  cfg.hermes = document.getElementById('cfg-base').value.trim() || DEFAULT_HERMES;
  cfg.qdrant = document.getElementById('cfg-qdrant').value.trim() || DEFAULT_QDRANT;
  cfg.key = document.getElementById('cfg-key').value.trim();
  localStorage.setItem('allin_hermes_base', cfg.hermes);
  localStorage.setItem('allin_qdrant_base', cfg.qdrant);
  // Credentials remain in memory only; never persist API keys in localStorage.
  document.getElementById('cfg-note').textContent =
    '設定已儲存至此分頁記憶體；API Key 不會寫入 localStorage，重新載入後需重新輸入。';
  pollAll();
}

/* ---------- Hermes 健康與 Agent 狀態 ---------- */
async function pollHermes() {
  const el = document.getElementById('hermes-status');
  const h = await fetchJSON(cfg.hermes + '/api/health');
  if (h.__error) {
    el.textContent = 'offline';
    el.className = 'status-offline';
    document.getElementById('hermes-decision').textContent = '—（檢查 8642 綁定 / CORS）';
    document.getElementById('connection-state').textContent = 'SYSTEM STATUS: HERMES UNREACHABLE';
    renderAgents(null);
    return;
  }
  el.textContent = 'online';
  el.className = 'status-online';
  document.getElementById('connection-state').textContent = 'SYSTEM STATUS: HERMES API REACHABLE · AUTHENTICATED AGENT STATUS UNKNOWN';
  const d = { __error: 'Agent status route is not verified; no synthetic agent status will be shown.' };
  if (!d.__error) {
    document.getElementById('hermes-decision').textContent =
      d.decision || d.current_decision || '（端點未提供 decision 欄位）';
    document.getElementById('hermes-memory').textContent =
      d.memory_hits != null ? (d.memory_hits + ' 筆記憶命中') : '（端點未提供 memory 欄位）';
  }
  renderAgents(d);
}

function renderAgents(d) {
  const list = document.getElementById('agent-list');
  const taskList = document.getElementById('task-list');
  if (d && !d.__error && Array.isArray(d.agents)) {
    list.replaceChildren();
    for (const a of d.agents) {
      const row = document.createElement('div'); row.className = 'agent-row';
      const name = document.createElement('span'); name.textContent = String(a.name || 'unnamed-agent');
      const status = document.createElement('span'); status.textContent = String(a.status || 'unknown');
      status.className = a.status === 'online' ? 'status-online' : (a.status === 'offline' ? 'status-offline' : 'status-warning');
      row.append(name, status); list.append(row);
    }
    taskList.replaceChildren();
    const tasks = d.tasks || [];
    if (!tasks.length) taskList.textContent = '目前無進行中任務';
    for (const t of tasks) {
      const row = document.createElement('div'); row.className = 'task-row';
      row.textContent = String(t.agent || 'agent') + ' — ' + String(t.description || t.title || t.objective || '未命名任務') + ' [' + String(t.status || 'unknown') + ']';
      taskList.append(row);
    }
    // 若端點有提供 verification 欄位則同步顯示
    const v = d.verification || {};
    if (v.tests)      document.getElementById('verify-tests').textContent = v.tests;
    if (v.typecheck)  document.getElementById('verify-type').textContent = v.typecheck;
    if (v.security)   document.getElementById('verify-sec').textContent = v.security;
    if (v.build)      document.getElementById('verify-build').textContent = v.build;
  } else {
    // 端點未實作 → 降級：顯示註冊表名單但標 unknown（不假造 online）
    list.replaceChildren();
    for (const a of FALLBACK_AGENTS) {
      const row = document.createElement('div'); row.className = 'agent-row';
      const name = document.createElement('span'); name.textContent = a;
      const status = document.createElement('span'); status.className = 'status-warning'; status.textContent = 'unknown（等待 /v1/agents/status）';
      row.append(name, status); list.append(row);
    }
  }
}

/* ---------- Qdrant 記憶統計 ---------- */
async function pollQdrant() {
  const el = document.getElementById('qdrant-points');
  const q = await fetchJSON(cfg.qdrant + '/collections');
  if (q.__error) { el.textContent = 'offline'; el.className = 'status-offline'; return; }
  const cols = (q.result && q.result.collections) || [];
  let total = 0;
  for (const c of cols) {
    const info = await fetchJSON(cfg.qdrant + '/collections/' + encodeURIComponent(c.name));
    if (!info.__error && info.result) total += info.result.points_count || 0;
  }
  el.textContent = total + ' points / ' + cols.length + ' collections';
  el.className = 'status-online';
}

/* ---------- SESM 狀態 ---------- */
async function pollSesm() {
  const s = await fetchJSON(cfg.hermes + '/api/status');
  if (!s.__error) {
    document.getElementById('sesm-state').textContent = s.current_state || s.state || '—';
    document.getElementById('sesm-version').textContent = s.version || '—';
    const rate = s.metrics && s.metrics.success_rate != null ? s.metrics.success_rate : 0;
    document.getElementById('sesm-rate').textContent = (Number(rate) * 100).toFixed(0) + '%';
  } else {
    document.getElementById('sesm-state').textContent = '未接線（Hermes 尚未提供 /v1/sesm/state）';
  }
}

/* ---------- CEO 下達目標 ---------- */
async function sendGoal() {
  const goal = document.getElementById('ceo-input').value.trim();
  if (!goal) return;
  const log = document.getElementById('ceo-log');
  log.textContent = '派發中: ' + goal;
  const r = await fetchJSON(cfg.hermes + '/api/chat', {
    method: 'POST',
    body: JSON.stringify({ messages: [{ role: 'user', content: '[CEO Goal] ' + goal }] })
  });
  log.textContent = r.__error
    ? '❌ ' + r.__error + '（檢查 Hermes 是否重啟完成 / CORS / API Key）'
    : '已收到 API 回應；此回應不代表任務已完成或工具已執行。回應摘要：' + JSON.stringify(r).slice(0, 260);
}

/* ---------- 主循環 ---------- */
function pollAll() { pollHermes(); pollQdrant(); pollSesm(); }
initConfigUI();
pollAll();
setInterval(pollHermes, 5000);
setInterval(() => { pollQdrant(); pollSesm(); }, 30000);
