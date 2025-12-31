/**
 * Better Auth API Route Handler
 * Handles authentication requests and proxies to FastAPI backend
 *
 * Spec Reference: specs/features/authentication.md
 */

import { auth } from "@/lib/auth";
import { toNextJsHandler } from "better-auth/next-js";

export const { GET, POST } = toNextJsHandler(auth);
