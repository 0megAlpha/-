export declare const PI_EXTENSIONS_ENV = "LODY_PI_EXTENSIONS";
export declare function parsePiLaunchArgs(args: string[]): {
    args: string[];
    extensions: string[];
};
export declare function discoverPiExtensions(): Promise<{
    version: 1;
    agentDir: string;
    extensions: Array<{
        path: string;
        name: string;
        source: "package" | "settings" | "directory";
    }>;
    warnings: string[];
}>;
