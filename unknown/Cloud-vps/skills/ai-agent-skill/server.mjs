#!/usr/bin/env node
/**
 * Google-ai Mobile Dashboard Backend (zero-dependency, Node >= 18)
 * ================================================================
 * - GET  /api/status      -> 服務健康檢查 + 任務佇列狀態
 * - POST /api/chat        -> 輪流呼叫（round-robin）多模型/多 agent 對話
 * - GET  /api/queue       -> 任務佇列
 * - GET  /api/models      -> 目前啟用的模型輪播清單
 *
 * 啟動: node /root/Google-ai/server.mjs   (監聽 127.0.0.1:8090)
 * systemd: google-ai-web.service (Restart=always)
 */
import http from "node:http";
import fs from "node:fs";
import path from "node:path";
import net from "node:net";
import { fileURLToPath } from "node:url";

const __dirname = path.dirname(fileURLToPath(import.meta.url));
const PORT = 8090;
const QUEUE_FILE = path.join(__dirname, "tasks", "queue.json");

// ---- 統一模擬 API 設定（sim-api :4010，含 ollama 保底）----
const LLM_BASE = "http://127.0.0.1:4010/v1";
const ROTATION_MODELS = [
  "glm-5.2",
  "nvidia/meta/llama-3.1-8b-instruct",
  "nvidia/deepseek-ai/deepseek-v4-flash-0731",
  "nvidia/qwen/qwen3-32b",
];
const AGENT_LABELS = ["openhands", "devin-sim", "claude-code", "cline"];

// 從 .sim-key 讀取 master key（sim-api 統一認證）
function loadApiKey() {
  for (const p of ["/root/Google-ai/.sim-key", "/root/工作流部署/01-模擬API/.sim-key"]) {
    try { const k = fs.readFileSync(p, "utf8").trim(); if (k) return k; } catch {}
  }
  return "";
}
const API_KEY = process.env.LITELLM_API_KEY || loadApiKey();

// ---- 服務健康檢查 ----
const SERVICES = [
  { name: "LiteLLM 閘道", port: 4000, path: "/health/liveliness" },
  { name: "OpenCode Server", port: 4096, path: "/" },
  { name: "OpenHands", port: 18000, path: "/" },
  { name: "n8n", port: 5678, path: "/healthz" },
  { name: "Ollama", port: 11434, path: "/" },
  { name: "Redis", port: 6379, path: "" },
  { name: "Neo4j", port: 7474, path: "/" },
  { name: "SonarQube", port: 9000, path: "/" },
  { name: "Dashboard(8080)", port: 8080, path: "/" },
  { name: "WebUI API(8090)", port: PORT, path: "/api/status" },
];

function checkService(svc) {
  return new Promise((resolve) => {
    // 自我檢查直接回 up，避免 /api/status 無限遞迴
    if (svc.port === PORT) return resolve("up");
    if (svc.port === 6379) {
      // Redis 簡易檢查：raw TCP ping
    const s = net.connect(svc.port, "127.0.0.1", () => {
      s.write("*1\r\n$4\r\nPING\r\n");
    });
    let buf = "";
    s.on("data", (d) => {
      buf += d.toString();
      if (buf.includes("PONG")) {
        s.destroy();
        resolve("up");
      }
    });
    s.on("error", () => resolve("down"));
    s.setTimeout(5000, () => {
      s.destroy();
      resolve("timeout");
    });
      return;
    }
    const req = http.get(
      { host: "127.0.0.1", port: svc.port, path: svc.path, timeout: 5000 },
      (res) => {
        res.resume();
        resolve(res.statusCode ? "up" : "down");
      }
    );
    req.on("timeout", () => {
      req.destroy();
      resolve("timeout");
    });
    req.on("error", () => resolve("down"));
  });
}

// ---- 任務佇列 ----
function readQueue() {
  try {
    return JSON.parse(fs.readFileSync(QUEUE_FILE, "utf8"));
  } catch {
    return [];
  }
}
function writeQueue(q) {
  fs.mkdirSync(path.dirname(QUEUE_FILE), { recursive: true });
  fs.writeFileSync(QUEUE_FILE, JSON.stringify(q, null, 2));
}

// ---- 輪流呼叫模型 ----
let cursor = 0;
function nextModel() {
  const m = ROTATION_MODELS[cursor % ROTATION_MODELS.length];
  cursor += 1;
  return m;
}

function callLiteLLM(model, messages, timeoutMs = 45000) {
  return new Promise((resolve, reject) => {
    const body = JSON.stringify({
      model,
      messages,
      temperature: 0.5,
      max_tokens: 1500,
    });
    const req = http.request(
      {
        host: "127.0.0.1",
        port: 4000,
        path: "/v1/chat/completions",
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${API_KEY}`,
          "Content-Length": Buffer.byteLength(body),
        },
        timeout: timeoutMs,
      },
      (res) => {
        let data = "";
        res.on("data", (c) => (data += c));
        res.on("end", () => {
          try {
            const j = JSON.parse(data);
            const content = j.choices?.[0]?.message?.content;
            if (!content || !content.trim()) reject(new Error("模型回覆為空，切換下一模型"));
            else resolve(content);
          } catch {
            reject(new Error(`閘道回應異常: ${data.slice(0, 300)}`));
          }
        });
      }
    );
    req.on("timeout", () => req.destroy(new Error("閘道逾時，切換下一模型")));
    req.on("error", (e) => reject(new Error(`閘道錯誤，切換下一模型 (${e.message})`)));
    req.write(body);
    req.end();
  });
}

// ---- HTTP 伺服器 ----
const server = http.createServer(async (req, res) => {
  res.setHeader("Access-Control-Allow-Origin", "*");
  res.setHeader("Access-Control-Allow-Methods", "GET,POST,OPTIONS");
  res.setHeader("Access-Control-Allow-Headers", "Content-Type");
  res.setHeader("Content-Type", "application/json; charset=utf-8");
  if (req.method === "OPTIONS") return res.end("ok");

  const url = new URL(req.url, `http://127.0.0.1:${PORT}`);

  try {
    if (url.pathname === "/api/status" && req.method === "GET") {
      const results = await Promise.all(SERVICES.map((s) => checkService(s)));
      const services = SERVICES.map((s, i) => ({
        name: s.name,
        port: s.port,
        status: results[i],
      }));
      return res.end(
        JSON.stringify({ ok: true, services, queue: readQueue().length, updatedAt: new Date().toISOString() })
      );
    }

    if (url.pathname === "/api/models" && req.method === "GET") {
      return res.end(JSON.stringify({ ok: true, models: ROTATION_MODELS, agents: AGENT_LABELS }));
    }

    if (url.pathname === "/api/queue" && req.method === "GET") {
      return res.end(JSON.stringify({ ok: true, queue: readQueue().slice(-20) }));
    }

    if (url.pathname === "/api/chat" && req.method === "POST") {
      let raw = "";
      for await (const chunk of req) raw += chunk;
      const { agent, task } = JSON.parse(raw || "{}");
      if (!task) return res.end(JSON.stringify({ ok: false, error: "task 必填" }));

      const model = nextModel();
      const q = readQueue();
      const entry = {
        id: Date.now(),
        agent: agent || "auto",
        model,
        task,
        ts: new Date().toISOString(),
        status: "running",
      };
      q.push(entry);
      writeQueue(q);

      // 實際呼叫模型（LiteLLM 閘道，輪播重試最多 3 個模型）
      const sysMsg = { role: "system", content: "你是多 agent 自動化軟體公司的執行引擎。直接、精準、可執行的回答。" };
      let reply;
      let lastErr = "";
      for (let attempt = 0; attempt < 3; attempt += 1) {
        const m = nextModel();
        try {
          reply = await callLiteLLM(m, [sysMsg, { role: "user", content: task }]);
          entry.model = m;
          entry.status = "done";
          break;
        } catch (e) {
          lastErr = e.message;
          entry.model = m;
        }
      }
      if (!reply) {
        entry.status = "error";
        entry.error = lastErr;
        reply = `[模型閘道] 嘗試 3 個模型皆失敗: ${lastErr}`;
      }
      entry.reply = reply.slice(0, 4000);
      writeQueue(q);

      return res.end(
        JSON.stringify({ ok: true, model, agent: entry.agent, reply, queueId: entry.id })
      );
    }

    res.statusCode = 404;
    res.end(JSON.stringify({ ok: false, error: "not found" }));
  } catch (e) {
    res.statusCode = 500;
    res.end(JSON.stringify({ ok: false, error: String(e && e.message || e) }));
  }
});

server.listen(PORT, "127.0.0.1", () => {
  console.log(`[google-ai-web] listening on http://127.0.0.1:${PORT}`);
});
