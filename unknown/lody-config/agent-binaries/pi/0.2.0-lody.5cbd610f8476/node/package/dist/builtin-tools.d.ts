import type { ExtensionAPI, ExtensionContext } from "@earendil-works/pi-coding-agent";
import { z } from "zod";
export declare const QUESTION_PREFIX = "lody-question:";
export declare const questionsSchema: z.ZodArray<z.ZodObject<{
    id: z.ZodString;
    question: z.ZodString;
    header: z.ZodDefault<z.ZodString>;
    options: z.ZodDefault<z.ZodArray<z.ZodObject<{
        label: z.ZodString;
        description: z.ZodOptional<z.ZodString>;
    }, z.core.$strip>>>;
    allowCustomAnswer: z.ZodDefault<z.ZodBoolean>;
}, z.core.$strip>>;
/** Packaged tools only: each execute returns all of its work to Pi's tool await. */
export declare function registerBuiltinTools(pi: ExtensionAPI, emit: (ctx: ExtensionContext, event: unknown) => void): void;
