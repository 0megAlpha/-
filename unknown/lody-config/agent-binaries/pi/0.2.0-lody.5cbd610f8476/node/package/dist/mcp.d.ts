import type { ExtensionAPI } from "@earendil-works/pi-coding-agent";
export declare const MCP_CONFIG_ENV = "LODY_PI_MCP_CONFIG";
/** Loaded in Pi: native tools own calls and cancellation; the SDK owns transport. */
export declare function registerMcpTools(pi: ExtensionAPI): Promise<void>;
