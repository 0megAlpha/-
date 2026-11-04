import type { PiStream } from "./types.js";
/** Only LF delimits records; Unicode line separators belong to JSON strings. */
export declare class PiTransport {
    private readonly onEvent;
    private readonly onFailure;
    private readonly writer;
    private readonly pending;
    private sequence;
    private failure?;
    private events;
    constructor(stream: PiStream, onEvent: (event: Record<string, unknown>) => Promise<void>, onFailure: (error: Error) => void);
    send(value: Record<string, unknown>): Promise<void>;
    request(command: string, fields?: Record<string, unknown>): Promise<unknown>;
    drain(): Promise<void>;
    assertOpen(): void;
    close(): void;
    private fail;
    private read;
}
