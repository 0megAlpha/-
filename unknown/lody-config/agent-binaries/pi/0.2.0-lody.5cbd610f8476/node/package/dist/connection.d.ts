import * as acp from "@agentclientprotocol/sdk";
import { type SessionUsageUpdate } from "acp-extension-core";
import type { AgentConnection, PiStream } from "./types.js";
type Host = {
    subagentEvents?: boolean;
    configureMcp: (servers: acp.McpServer[]) => Promise<void>;
    update: (notification: acp.SessionNotification) => Promise<void>;
    extension: (method: string, params: Record<string, unknown>) => Promise<void>;
    usage: (usage: SessionUsageUpdate) => void;
    question: (request: acp.CreateElicitationRequest) => Promise<acp.CreateElicitationResponse>;
};
/** Translates the ACP control contract to the pinned Pi JSONL runtime. */
export declare class PiRpcConnection implements AgentConnection {
    private readonly host;
    private readonly subagentRuns;
    private subagents;
    private readonly rpc;
    private sessionId;
    private cwd;
    private active?;
    private configuring;
    private readonly questions;
    private readonly controls;
    private pendingPlan?;
    /** Live per-response usage of this activation. Pi stats are a sum over the
     * current context, not a counter: compaction, retries and branching lower them
     * and resume restores history, so they never feed accounting. */
    private usageLedger;
    private compactions;
    private lastModelKey?;
    private steerCommand;
    private pendingSteer?;
    constructor(stream: PiStream, host: Host);
    initialize: AgentConnection["initialize"];
    close(): void;
    newSession: AgentConnection["newSession"];
    resumeSession: AgentConnection["resumeSession"];
    loadSession: AgentConnection["loadSession"];
    private open;
    private prepare;
    /** Replays the native branch Pi will continue from, using Pi's own tool call ids. */
    private replayHistory;
    private configOptions;
    private setOption;
    setSessionConfigOption: AgentConnection["setSessionConfigOption"];
    prompt: AgentConnection["prompt"];
    private finishRun;
    private refreshConfigOptions;
    cancel: AgentConnection["cancel"];
    private cancelRun;
    private abort;
    private promptContent;
    private update;
    private notice;
    private observeSession;
    private readState;
    private assertReady;
    private event;
    private startActivity;
    private endActivity;
    private recordUsage;
    /** Context occupancy and the /status text come from Pi stats; accounting does not. */
    private reportUsage;
    private tool;
    private toolCall;
    private question;
    private cancelQuestions;
    private configure;
    private assertIdle;
    private waitForSettledRun;
    private assertSession;
    request: AgentConnection["request"];
}
export declare function initializeResponse(): acp.InitializeResponse;
export {};
