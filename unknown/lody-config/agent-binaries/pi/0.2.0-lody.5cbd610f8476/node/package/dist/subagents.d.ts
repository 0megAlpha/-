import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import type { LodySubagentTask } from "acp-extension-core";
/** The process owner supplies identity, terminal status and cancellation to Lody. */
export declare function registerSubagents(pi: ExtensionAPI, emit: (ctx: ExtensionContext, event: unknown) => void): (request: {
    op: string;
    taskId?: string;
    activeOnly?: boolean;
    tail?: number;
}) => Promise<{
    tasks: LodySubagentTask[];
    output?: undefined;
} | {
    tasks?: undefined;
    output?: undefined;
} | {
    output: string;
    tasks?: undefined;
}>;
