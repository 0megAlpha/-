import type { ModelUsage } from "acp-extension-core";
import { z } from "zod";
/** Pi `Usage` of one model response. Input and cache buckets are disjoint;
 * `reasoning` is a subset of `output`. */
export declare const piUsageSchema: z.ZodObject<{
    input: z.ZodNumber;
    output: z.ZodNumber;
    cacheRead: z.ZodNumber;
    cacheWrite: z.ZodNumber;
    reasoning: z.ZodOptional<z.ZodNumber>;
    cost: z.ZodOptional<z.ZodObject<{
        total: z.ZodOptional<z.ZodNumber>;
    }, z.core.$strip>>;
}, z.core.$strip>;
/** The accounting fields of a Pi assistant message; content is never needed. */
export declare const piAssistantUsageSchema: z.ZodObject<{
    role: z.ZodLiteral<"assistant">;
    provider: z.ZodString;
    model: z.ZodString;
    responseId: z.ZodOptional<z.ZodString>;
    timestamp: z.ZodNumber;
    usage: z.ZodObject<{
        input: z.ZodNumber;
        output: z.ZodNumber;
        cacheRead: z.ZodNumber;
        cacheWrite: z.ZodNumber;
        reasoning: z.ZodOptional<z.ZodNumber>;
        cost: z.ZodOptional<z.ZodObject<{
            total: z.ZodOptional<z.ZodNumber>;
        }, z.core.$strip>>;
    }, z.core.$strip>;
}, z.core.$strip>;
export type PiAssistantUsage = z.infer<typeof piAssistantUsageSchema>;
/** Same `provider/id` spelling as the model config option. */
export declare const piModelKey: (provider: string, model: string) => string;
/** One response's own usage, keyed so a repeated report merges instead of adding. */
export declare const piResponseOperation: (message: PiAssistantUsage) => string;
export declare function toModelUsage(usage: z.infer<typeof piUsageSchema>): ModelUsage;
