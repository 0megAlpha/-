/* ============================================================
 * Ai-agent-skill — Agent Collaboration Monitor（修復 4）
 * 接入 Qdrant 向量庫與 Hermes 的「真實」數據：
 *   - Hermes  /health、/v1/agents/status（Agent 狀態 + 任務進度）
 *   - Qdrant  /collections、/collections/{name}（記憶統計）
 *   - Qdrant  POST /collections/{name}/points/scroll（最新記憶檢索）
 * 任何端點失敗 → 如實顯示 offline / unknown，不假造數據。
 * ============================================================ */

const DEFAULTS = { hermes: 'http://100.126.48.60:8642', qdrant: 'http://100.126.48.60:6333', key: '' };
let cfg = { ...DEFAULTS, ...JSON.parse(localStorage.getItem('aask_cfg') || '{}') };
let latestMemories = [];   // {collection, payload}

function authHeaders() { return cfg.key ? { 'Authorization': 'Bearer ' + cfg.key } : {}; }

async function fetchJSON(url, opts = {}) {
  try {
    const res = await fetch(url, { ...opts, headers: { 'Content-Type': 'application/json', ...authHeaders(), ...(opts.headers || {}) } });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (e) { return { __error: String(e && e.message ? e.message : e) }; }
}

function saveConfig() {
  cfg.hermes = document.getElementById('cfg-hermes').value.trim() || DEFAULTS.hermes;
  cfg.qdrant = document.getElementById('cfg-qdrant').value.trim() || DEFAULTS.qdrant;
  cfg.key = document.getElementById('cfg-key').value.trim();
  localStorage.setItem('aask_cfg', JSON.stringify(cfg));
  pollAll();
}

/* ---------- Agent 協作狀態（Hermes） ---------- */
async function pollAgents() {
  const tbody = document.getElementById('agent-tbody');
  const d = await fetchJSON(cfg.hermes + '/v1/agents/status');
  if (d.__error || !Array.isArray(d.agents)) {
    tbody.innerHTML = '<tr><td colspan="3" class="off">Hermes /v1/agents/status 不可用（' +
      (d.__error || '未提供 agents 陣列') + '）</td></tr>';
    return;
  }
  tbody.innerHTML = d.agents.map(a =>
    `<tr><td>${a.name}</td>` +
    `<td class="${a.status === 'online' ? 'on' : a.status ? 'off' : 'warn'}">${a.status || 'unknown'}</td>` +
    `<td>${a.current_task || a.task || '—'}</td></tr>`).join('');
}

/* ---------- 記憶庫統計（Qdrant） ---------- */
async function pollMemory() {
  const tbody = document.getElementById('mem-tbody');
  const note = document.getElementById('mem-note');
  const q = await fetchJSON(cfg.qdrant + '/collections');
  if (q.__error) {
    tbody.innerHTML = '<tr><td colspan="3" class="off">Qdrant 不可用：' + q.__error + '</td></tr>';
    return;
  }
  const cols = (q.result && q.result.collections) || [];
  if (!cols.length) { tbody.innerHTML = '<tr><td colspan="3" class="warn">尚無 collection</td></tr>'; return; }
  const rows = [];
  latestMemories = [];
  for (const c of cols) {
    const info = await fetchJSON(cfg.qdrant + '/collections/' + encodeURIComponent(c.name));
    if (info.__error) { rows.push(`<tr><td>${c.name}</td><td>—</td><td class="off">讀取失敗</td></tr>`); continue; }
    const points = info.result ? (info.result.points_count || 0) : '—';
    const status = info.result ? (info.result.status || 'green') : 'unknown';
    rows.push(`<tr><td>${c.name}</td><td>${points}</td><td class="${status === 'green' ? 'on' : 'warn'}">${status}</td></tr>`);
    await scrollMemories(c.name);
  }
  tbody.innerHTML = rows.join('');
  note.textContent = '共 ' + cols.length + ' 個 collections；最新記憶共載入 ' + latestMemories.length + ' 筆。';
}

/* ---------- 最新記憶檢索（Qdrant scroll，真實資料） ---------- */
async function scrollMemories(collection) {
  const r = await fetchJSON(cfg.qdrant + '/collections/' + encodeURIComponent(collection) + '/points/scroll', {
    method: 'POST',
    body: JSON.stringify({ limit: 20, with_payload: true })
  });
  if (r.__error) return;
  const points = (r.result && r.result.points) || [];
  for (const p of points) {
    latestMemories.push({ collection, payload: p.payload || {} });
  }
}

function renderMemories() {
  const kw = document.getElementById('mem-filter').value.trim().toLowerCase();
  const list = document.getElementById('mem-list');
  const filtered = kw
    ? latestMemories.filter(m => JSON.stringify(m.payload).toLowerCase().includes(kw))
    : latestMemories;
  if (!filtered.length) {
    list.innerHTML = '<div class="note">（無資料：Qdrant 尚未寫入記憶，或 collection 為空）</div>';
    return;
  }
  list.innerHTML = filtered.slice(0, 50).map(m => {
    const p = m.payload || {};
    const ts = p.timestamp || '—';
    const task = (p.task || p.content || '').toString().slice(0, 120);
    const result = (p.result || p.shortcut || '').toString().slice(0, 160);
    return `<div class="mem"><div>${task || '（無摘要）'}</div>` +
           (result ? `<div class="meta">→ ${result}</div>` : '') +
           `<div class="meta">[${m.collection}] ${ts}</div></div>`;
  }).join('');
}

/* ---------- 主循環 ---------- */
function pollAll() { pollAgents(); pollMemory().then(renderMemories); }
document.getElementById('cfg-hermes').value = cfg.hermes;
document.getElementById('cfg-qdrant').value = cfg.qdrant;
document.getElementById('cfg-key').value = cfg.key;
pollAll();
setInterval(pollAll, 15000);
