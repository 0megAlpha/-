import { z } from "zod";
const envelope = z.object({ type: z.string() }).passthrough();
const response = z.object({
    type: z.literal("response"),
    id: z.string(),
    command: z.string(),
    success: z.boolean(),
    data: z.unknown().optional(),
    error: z.string().optional(),
});
const MAX_RECORD_CHARACTERS = 16 * 1024 * 1024;
/** Only LF delimits records; Unicode line separators belong to JSON strings. */
export class PiTransport {
    onEvent;
    onFailure;
    writer;
    pending = new Map();
    sequence = 0;
    failure;
    events = Promise.resolve();
    constructor(stream, onEvent, onFailure) {
        this.onEvent = onEvent;
        this.onFailure = onFailure;
        this.writer = stream.writable.getWriter();
        void this.read(stream.readable).catch((error) => this.fail(error));
    }
    async send(value) {
        this.assertOpen();
        try {
            await this.writer.write(new TextEncoder().encode(JSON.stringify(value) + "\n"));
        }
        catch (error) {
            this.fail(error);
            throw this.failure;
        }
    }
    request(command, fields = {}) {
        if (this.failure)
            return Promise.reject(this.failure);
        const id = String(++this.sequence);
        const result = new Promise((resolve, reject) => {
            this.pending.set(id, { command, resolve, reject });
        });
        void this.send({ ...fields, id, type: command }).catch((error) => this.fail(error));
        return result;
    }
    async drain() {
        await this.events;
        this.assertOpen();
    }
    assertOpen() {
        if (this.failure)
            throw this.failure;
    }
    close() {
        this.fail(new Error("Pi connection closed"));
    }
    fail(error) {
        if (this.failure)
            return;
        this.failure =
            error instanceof Error ? error : new Error("Pi RPC connection closed");
        for (const request of this.pending.values())
            request.reject(this.failure);
        this.pending.clear();
        this.onFailure(this.failure);
    }
    async read(readable) {
        const reader = readable.getReader();
        const decoder = new TextDecoder("utf-8", { fatal: true });
        let buffer = "";
        try {
            while (true) {
                const { done, value } = await reader.read();
                if (done)
                    break;
                buffer += decoder.decode(value, { stream: true });
                let end;
                while ((end = buffer.indexOf("\n")) !== -1) {
                    if (end > MAX_RECORD_CHARACTERS)
                        throw new Error("Pi RPC record exceeds the size limit");
                    const line = buffer.slice(0, end).replace(/\r$/, "");
                    buffer = buffer.slice(end + 1);
                    if (!line)
                        continue;
                    const event = envelope.parse(JSON.parse(line));
                    if (event.type === "response") {
                        const reply = response.parse(event);
                        const pending = this.pending.get(reply.id);
                        if (!pending)
                            continue;
                        if (reply.command !== pending.command)
                            throw new Error("Pi RPC response command mismatch");
                        this.pending.delete(reply.id);
                        if (reply.success)
                            pending.resolve(reply.data);
                        else
                            pending.reject(new Error(reply.error ?? `Pi ${reply.command} failed`));
                    }
                    else {
                        // Replies remain readable while a notification is being applied to history.
                        this.events = this.events.then(() => this.onEvent(event));
                        void this.events.catch((error) => this.fail(error));
                    }
                }
                if (buffer.length > MAX_RECORD_CHARACTERS)
                    throw new Error("Pi RPC record exceeds the size limit");
            }
            buffer += decoder.decode();
            // Reject pending requests before waiting on events: an event may itself await a reply.
            throw new Error(buffer.trim()
                ? "Pi RPC disconnected with an incomplete record"
                : "Pi RPC connection closed");
        }
        finally {
            reader.releaseLock();
        }
    }
}
