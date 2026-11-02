/* ================================================================
 * Memory Viewer — 真實 Qdrant 資料
 *   · 列出 collections + points_count
 *   · 選一個 collection 用 /points/scroll 拉最新 points（payload 為主）
 *   · 端點不可用 → 如實顯示 offline；沒有 fallback 假資料
 * ================================================================ */
'use strict';

const DEFAULT_QDRANT = 'http://100.126.48.60:6333';
let base = localStorage.getItem('qdrant_base') || DEFAULT_QDRANT;
let points = [];          // 目前 collection 的原始 points
let curCol = '';
let key = localStorage.getItem('qdrant_key') || '';

const $ = (id) => document.getElementById(id);
const esc = (s) => String(s == null ? '' : s)
  .replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');

async function qget(url, opts = {}) {
  try {
    const res = await fetch(url, {
      ...opts,
      headers: { 'Content-Type': 'application/json',
                 ...(key ? { 'api-key': key } : {}),
                 ...(opts.headers || {}) }
    });
    if (!res.ok) throw new Error('HTTP ' + res.status);
    return await res.json();
  } catch (e) { return { __error: String(e && e.message || e) }; }
}

function setOffline(msg) {
  $('s-status').textContent = 'offline';
  $('s-status').className = 'v offline';
  $('list').innerHTML = `<div class="empty">
    ⚠️ Qdrant 不可用：${esc(msg)}<br><br>
    請確認：<code>docker ps | grep qdrant</code>　或調整右上角「連線設定」<br>
    設定檔位置：<code>~/All-in/.env</code> 的 <code>QDRANT_URL</code>
  </div>`;
  $('qhost').textContent = base;
}

async function loadCollections() {
  const d = await qget(base.replace(/\/$/, '') + '/collections');
  if (d.__error) { setOffline(d.__error); return; }
  $('s-status').textContent = 'online';
  $('s-status').className = 'v';
  $('qhost').textContent = base;

  const cols = (d.result && d.result.collections) || [];
  $('s-cols').textContent = cols.length;

  let total = 0;
  const sel = $('col');
  sel.innerHTML = '<option value="">— 選擇 collection —</option>';
  for (const c of cols) {
    const info = await qget(base.replace(/\/$/, '') + '/collections/' + encodeURIComponent(c.name));
    const n = (info && info.result && info.result.points_count) || 0;
    total += n;
    const o = document.createElement('option');
    o.value = c.name; o.textContent = `${c.name}  (${n} pts)`;
    sel.appendChild(o);
  }
  $('s-points').textContent = total;
  if (cols.length && !curCol) { sel.value = cols[0].name; await loadPoints(cols[0].name); }
}

async function loadPoints(name) {
  curCol = name;
  if (!name) { points = []; render(); return; }
  const d = await qget(base.replace(/\/$/, '') + '/collections/' + encodeURIComponent(name) + '/points/scroll', {
    method: 'POST',
    body: JSON.stringify({ limit: 50, with_payload: true, with_vector: false })
  });
  if (d.__error) {
    points = [];
    $('list').innerHTML = `<div class="empty">⚠️ 讀取 ${esc(name)} 失敗：${esc(d.__error)}</div>`;
    $('s-shown').textContent = '0';
    return;
  }
  points = ((d.result && d.result.points) || []);
  render();
}

function payloadToText(p) {
  if (!p) return '(無 payload)';
  const pick = ['task', 'content', 'text', 'result', 'summary', 'description',
                'decision', 'solution', 'error', 'message'];
  for (const k of pick) if (p[k]) return String(p[k]);
  return JSON.stringify(p, null, 2).slice(0, 800);
}

function render() {
  const q = $('q').value.trim().toLowerCase();
  const rows = points.filter(p => {
    if (!q) return true;
    try { return JSON.stringify(p.payload || {}).toLowerCase().includes(q); }
    catch { return false; }
  });
  $('s-shown').textContent = rows.length;

  if (!rows.length) {
    $('list').innerHTML = `<div class="empty">${
      points.length ? '沒有符合關鍵字的記憶' :
      (curCol ? `collection <code>${esc(curCol)}</code> 目前沒有資料` : '請先選擇一個 collection')
    }</div>`;
    return;
  }
  $('list').innerHTML = rows.map(p => {
    const pl = p.payload || {};
    const ts = pl.timestamp || pl.ts || pl.created_at || '—';
    return `<div class="entry">
      <div class="meta">
        <span class="tag">${esc(curCol)}</span>
        <span>id ${esc(p.id)}</span>
        <span>${esc(ts)}</span>
        ${pl.agent ? `<span>agent: ${esc(pl.agent)}</span>` : ''}
        ${pl.type ? `<span>type: ${esc(pl.type)}</span>` : ''}
      </div>
      <div class="content">${esc(payloadToText(pl))}</div>
    </div>`;
  }).join('');
}

$('col').addEventListener('change', e => loadPoints(e.target.value));
$('q').addEventListener('input', render);
$('reload').addEventListener('click', () => { curCol = ''; loadCollections(); });
$('cfg').addEventListener('click', () => {
  const b = prompt('Qdrant Base URL', base);
  const k = prompt('Qdrant API Key（若啟用了 QDRANT__SERVICE__API_KEY，留空）', key);
  if (b) { base = b.trim().replace(/\/$/, ''); localStorage.setItem('qdrant_base', base); }
  key = (k || '').trim(); localStorage.setItem('qdrant_key', key);
  curCol = ''; loadCollections();
});

loadCollections();
setInterval(() => { if (curCol) loadPoints(curCol); }, 30000);