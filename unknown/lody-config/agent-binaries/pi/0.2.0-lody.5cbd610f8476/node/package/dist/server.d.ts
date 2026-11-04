import { AgentSideConnection, type Stream } from "@agentclientprotocol/sdk";
/** One runtime per ACP connection; Pi owns its native files and tool processes. */
export declare function serve(stream: Stream, piArgs?: string[]): {
    connection: AgentSideConnection;
    close: () => Promise<void>;
    closed: Promise<void>;
};
