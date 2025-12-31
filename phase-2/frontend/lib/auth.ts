/**
 * Better Auth Configuration
 * Connects to FastAPI backend with JWT authentication
 *
 * Spec Reference: specs/features/authentication.md
 */

import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const auth = betterAuth({
  // Database not needed - we're using backend API
  database: undefined as any,

  // Email/password authentication
  emailAndPassword: {
    enabled: true,
    // Custom endpoints to use our FastAPI backend
    async signUp(data: { email: string; password: string }) {
      const response = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Registration failed");
      }

      const user = await response.json();
      return {
        id: user.id.toString(),
        email: user.email,
        name: user.email.split("@")[0],
        emailVerified: false,
      };
    },

    async signIn(data: { email: string; password: string }) {
      const response = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          email: data.email,
          password: data.password,
        }),
      });

      if (!response.ok) {
        const error = await response.json();
        throw new Error(error.detail || "Login failed");
      }

      const tokenData = await response.json();

      // Store JWT token for API requests
      if (typeof window !== "undefined") {
        localStorage.setItem("jwt_token", tokenData.access_token);
        localStorage.setItem("token_expiry", (Date.now() + tokenData.expires_in * 1000).toString());
      }

      return {
        user: {
          id: "temp", // Will be populated from JWT
          email: data.email,
          name: data.email.split("@")[0],
          emailVerified: false,
        },
        session: {
          token: tokenData.access_token,
          expiresAt: new Date(Date.now() + tokenData.expires_in * 1000),
        },
      };
    },
  },

  // Plugin for Next.js cookie handling
  plugins: [nextCookies()],

  // Secret for signing sessions
  secret: process.env.BETTER_AUTH_SECRET!,

  // Base URL
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});
