/* Agent Fleet Monitor — 對所有已知服務做真實健康探測（修復 4 配套）
 * 每 10 秒輪詢一次；HTTP 非 200 或 fetch 失敗如實顯示，不假造。 */
const DEFAULT_TS = 'http://100.126.48.60';
let TS = localStorage.getItem('allin_ts_base') || DEFAULT_TS;

const SERVICES = () => [
  { name: 'Hermes',     url: TS + ':8642/health' },
  { name: 'Qdrant',     url: TS + ':6333/healthz' },
  { name: 'Open WebUI', url: TS + ':3000/health' },
  { name: 'Mem0',       url: TS + ':8000/health' },
  { name: 'OpenHands',  url: TS + ':18000/health' },
  { name: 'OpenCode',   url: TS + ':8743/health' },
  { name: 'LiteLLM',    url: TS + ':4000/health/liveliness' },
  { name: 'n8n',        url: TS + ':5678/healthz' }
];

function saveBase() {
  TS = document.getElementById('ts-base').value.trim().replace(/\/+$/, '') || DEFAULT_TS;
  localStorage.setItem('allin_ts_base', TS);
  logEvent('基底 URL 更新為 ' + TS);
  poll();
}

async function ping(svc) {
  const t0 = performance.now();
  try {
    const res = await fetch(svc.url, { mode: 'cors' });
    return { ok: res.ok, code: res.status, ms: Math.round(performance.now() - t0) };
  } catch (e) {
    return { ok: false, code: 0, ms: 0, err: String(e && e.message ? e.message : e) };
  }
}

function logEvent(msg) {
  const el = document.getElementById('log');
  const time = new Date().toLocaleTimeString();
  el.innerHTML = `<div>[${time}] ${msg}</div>` + el.innerHTML;
}

async function poll() {
  const tbody = document.querySelector('#svc-table tbody');
  const rows = [];
  for (const svc of SERVICES()) {
    const r = await ping(svc);
    const cls = r.ok ? 'on' : 'off';
    const status = r.ok ? 'online' : 'unreachable';
    rows.push(`<tr><td>${svc.name}</td><td class="${cls}">${status}</td><td class="${cls}">${r.code || '—'}</td><td>${r.ok ? r.ms + ' ms' : '—'}</td></tr>`);
    if (!r.ok && r.err) logEvent(`${svc.name} 探測失敗：${r.err}`);
  }
  tbody.innerHTML = rows.join('');
}

document.getElementById('ts-base').value = TS;
poll();
setInterval(poll, 10000);
