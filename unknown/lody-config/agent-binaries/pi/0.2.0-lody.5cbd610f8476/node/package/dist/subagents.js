import { spawn } from "node:child_process";
import { randomUUID } from "node:crypto";
import { fileURLToPath } from "node:url";
import { join } from "node:path";
import { z } from "zod";
import { PI_EXTENSIONS_ENV } from "./extensions.js";
const MAX_OUTPUT = 64 * 1024;
/** The process owner supplies identity, terminal status and cancellation to Lody. */
export function registerSubagents(pi, emit) {
    const tasks = new Map();
    pi.on("session_shutdown", async () => {
        await Promise.all([...tasks.values()].map((task) => task.cancel()));
        tasks.clear();
    });
    pi.registerTool({
        name: "subagent",
        label: "Subagent",
        description: "Delegate a focused task to an isolated Pi agent and wait for its result. It cannot ask the user or spawn further subagents; return missing information to the main agent.",
        parameters: {
            type: "object",
            properties: { task: { type: "string" }, description: { type: "string" } },
            required: ["task", "description"],
        },
        async execute(parentToolCallId, input, signal, _update, ctx) {
            const args = z
                .object({ task: z.string().min(1), description: z.string().min(1) })
                .parse(input);
            if (signal?.aborted)
                throw new Error("Subagent cancelled before launch");
            if (!ctx.model)
                throw new Error("Select a model before starting a subagent");
            const id = randomUUID();
            const entry = fileURLToPath(new URL("./bundle/cli.js", import.meta.resolve("@earendil-works/pi-coding-agent")));
            const extensions = JSON.parse(process.env[PI_EXTENSIONS_ENV] ?? "[]");
            const proc = spawn(process.execPath, [
                entry,
                "--mode",
                "json",
                "-p",
                "--no-session",
                "--no-extensions",
                ...extensions.flatMap((path) => ["-e", path]),
                "--model",
                `${ctx.model.provider}/${ctx.model.id}`,
                "--thinking",
                pi.getThinkingLevel(),
                "--append-system-prompt",
                "You are a subagent. Complete the delegated task. If information is missing, report it to the parent; do not ask the user. Do not start other agents.",
                "--",
                args.task,
            ], {
                cwd: ctx.cwd,
                stdio: ["ignore", "pipe", "pipe"],
                // Stay in the parent Pi process group so adapter shutdown also kills
                // children if Pi cannot finish its cooperative shutdown hook.
                detached: false,
                windowsHide: true,
            });
            let finish;
            let cancellation;
            let forced;
            let failed = false;
            let buffer = "";
            let messageId = randomUUID();
            let lastToolName;
            const info = {
                taskId: id,
                description: args.description,
                status: "running",
                modelId: `${ctx.model.provider}/${ctx.model.id}`,
                startedAtEpochSeconds: Date.now() / 1000,
                endedAtEpochSeconds: null,
            };
            const publish = (event = "updated") => {
                const meta = {
                    version: 1,
                    taskId: id,
                    kind: "subagent",
                    parentToolCallId,
                    description: info.description,
                    modelId: info.modelId,
                    status: info.status === "running"
                        ? "in_progress"
                        : info.status === "completed"
                            ? "completed"
                            : "failed",
                    startedAtEpochSeconds: info.startedAtEpochSeconds,
                    ...(info.endedAtEpochSeconds === null
                        ? {}
                        : { endedAtEpochSeconds: info.endedAtEpochSeconds }),
                    ...(info.stopReason ? { error: info.stopReason } : {}),
                    ...(lastToolName ? { lastToolName } : {}),
                };
                emit(ctx, {
                    type: "lody_subagent",
                    event,
                    task: meta,
                    state: info.status,
                });
            };
            const kill = (force) => {
                if (proc.exitCode !== null || proc.signalCode !== null || !proc.pid)
                    return;
                if (process.platform === "win32") {
                    const killer = spawn(join(process.env.SystemRoot ?? "C:\\Windows", "System32", "taskkill.exe"), ["/pid", String(proc.pid), "/T", ...(force ? ["/F"] : [])], { stdio: "ignore", windowsHide: true });
                    killer.on("error", () => proc.kill(force ? "SIGKILL" : "SIGTERM"));
                }
                else {
                    try {
                        proc.kill(force ? "SIGKILL" : "SIGTERM");
                    }
                    catch {
                        /* Already exited. */
                    }
                }
            };
            const task = {
                info,
                output: "",
                finished: new Promise((resolve) => {
                    finish = resolve;
                }),
                cancel: () => {
                    if (info.status !== "running")
                        return task.finished;
                    cancellation ??= (async () => {
                        kill(false);
                        forced = setTimeout(() => kill(true), 1000);
                        await task.finished;
                    })();
                    return cancellation;
                },
            };
            tasks.set(id, task);
            publish("started");
            const append = (text) => {
                task.output = (task.output + text).slice(-MAX_OUTPUT);
            };
            proc.stderr.on("data", (chunk) => append(String(chunk)));
            proc.stdout.setEncoding("utf8");
            proc.stdout.on("data", (chunk) => {
                buffer += chunk;
                if (buffer.length > 16 * 1024 * 1024) {
                    failed = true;
                    void task.cancel();
                    return;
                }
                let index;
                while ((index = buffer.indexOf("\n")) >= 0) {
                    const line = buffer.slice(0, index);
                    buffer = buffer.slice(index + 1);
                    if (!line.trim())
                        continue;
                    try {
                        const event = JSON.parse(line);
                        if (event.type === "message_start")
                            messageId = randomUUID();
                        if ([
                            "message_update",
                            "tool_execution_start",
                            "tool_execution_update",
                            "tool_execution_end",
                        ].includes(event.type)) {
                            emit(ctx, {
                                type: "lody_subagent_output",
                                taskId: id,
                                messageId,
                                event,
                            });
                        }
                        if (event.type === "message_update" &&
                            event.assistantMessageEvent?.type === "text_delta") {
                            append(String(event.assistantMessageEvent.delta ?? ""));
                        }
                        if (event.type === "tool_execution_start") {
                            lastToolName = String(event.toolName);
                            publish();
                        }
                        if (event.type === "message_end" &&
                            event.message?.role === "assistant") {
                            // Child usage is live-only (--no-session); forward just its accounting fields.
                            const { provider, model, responseId, timestamp, usage } = event.message;
                            emit(ctx, {
                                type: "lody_usage",
                                taskId: id,
                                message: {
                                    role: "assistant",
                                    provider,
                                    model,
                                    responseId,
                                    timestamp,
                                    usage,
                                },
                            });
                            append("\n");
                            failed = ["error", "aborted", "length"].includes(event.message.stopReason);
                            if (failed) {
                                info.stopReason =
                                    event.message.errorMessage ?? event.message.stopReason;
                            }
                            else
                                info.stopReason = undefined;
                        }
                    }
                    catch {
                        failed = true;
                        append("Invalid Pi subagent output\n");
                        void task.cancel();
                    }
                }
            });
            proc.on("error", (error) => {
                failed = true;
                info.stopReason = error.message;
            });
            const abort = () => {
                void task.cancel();
            };
            signal?.addEventListener("abort", abort, { once: true });
            if (signal?.aborted)
                abort();
            proc.once("close", (code) => {
                if (forced)
                    clearTimeout(forced);
                signal?.removeEventListener("abort", abort);
                info.status = cancellation
                    ? "killed"
                    : failed || code !== 0
                        ? "failed"
                        : "completed";
                info.endedAtEpochSeconds = Date.now() / 1000;
                if (info.status === "killed")
                    info.stopReason = "Cancelled";
                else if (info.status === "failed")
                    info.stopReason ??= `Pi exited with code ${code}`;
                publish();
                finish();
            });
            await task.finished;
            return {
                content: [
                    {
                        type: "text",
                        text: [info.stopReason, task.output].filter(Boolean).join("\n") ||
                            "Subagent completed without text output",
                    },
                ],
                details: {
                    taskId: id,
                    status: info.status,
                    isError: info.status !== "completed",
                },
            };
        },
    });
    pi.on("tool_result", (event) => {
        if (event.toolName === "subagent" &&
            event.details?.isError)
            return { isError: true };
    });
    return async (request) => {
        if (request.op === "list")
            return {
                tasks: [...tasks.values()]
                    .filter((task) => !request.activeOnly || task.info.status === "running")
                    .map((task) => task.info),
            };
        const task = tasks.get(request.taskId ?? "");
        if (!task)
            throw new Error("Unknown Pi subagent task");
        if (request.op === "cancel") {
            await task.cancel();
            return {};
        }
        if (request.op === "output")
            return {
                output: task.output.slice(-Math.max(1, Math.min(request.tail ?? MAX_OUTPUT, MAX_OUTPUT))),
            };
        throw new Error("Unsupported subagent operation");
    };
}
