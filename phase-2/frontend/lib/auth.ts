/**
 * Better Auth Configuration
 * Connects to FastAPI backend with JWT authentication
 */

import { betterAuth } from "better-auth";
import { nextCookies } from "better-auth/next-js";

const API_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export const auth = betterAuth({
  // Email/password authentication via FastAPI
  emailAndPassword: {
    enabled: true,

    async signUp(data) {
      const res = await fetch(`${API_URL}/api/auth/register`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "Registration failed");
      }

      const user = await res.json();

      return {
        id: user.id.toString(),
        email: user.email,
        name: user.email.split("@")[0],
        emailVerified: false,
      };
    },

    async signIn(data) {
      const res = await fetch(`${API_URL}/api/auth/login`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(data),
      });

      if (!res.ok) {
        const error = await res.json();
        throw new Error(error.detail || "Login failed");
      }

      const token = await res.json();

      return {
        user: {
          id: "jwt",
          email: data.email,
          name: data.email.split("@")[0],
          emailVerified: false,
        },
        session: {
          token: token.access_token,
          expiresAt: new Date(Date.now() + token.expires_in * 1000),
        },
      };
    },
  },

  plugins: [nextCookies()],

  // REQUIRED in production (Vercel)
  trustHost: true,

  // REQUIRED secret (you already fixed this)
  secret: process.env.BETTER_AUTH_SECRET!,

  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",
});
