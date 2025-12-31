/**
 * Dashboard Layout
 * Protected layout for authenticated users
 *
 * Spec Reference:
 * - specs/features/authentication.md (UI/UX Requirements - Protected Routes)
 * - specs/ui/components.md (Dashboard Layout)
 */

"use client";

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  const router = useRouter();
  const [isAuthenticated, setIsAuthenticated] = useState(false);
  const [userEmail, setUserEmail] = useState("");

  useEffect(() => {
    // Check for JWT token
    const token = localStorage.getItem("jwt_token");
    const expiry = localStorage.getItem("token_expiry");
    const email = localStorage.getItem("user_email");

    if (!token || !expiry) {
      // No token - redirect to login
      router.push("/");
      return;
    }

    const expiryTime = parseInt(expiry, 10);
    if (Date.now() >= expiryTime) {
      // Token expired - clear and redirect
      localStorage.removeItem("jwt_token");
      localStorage.removeItem("token_expiry");
      localStorage.removeItem("user_email");
      router.push("/");
      return;
    }

    // Token valid
    setIsAuthenticated(true);
    setUserEmail(email || "");
  }, [router]);

  const handleLogout = () => {
    // Clear token from localStorage
    localStorage.removeItem("jwt_token");
    localStorage.removeItem("token_expiry");
    localStorage.removeItem("user_email");

    // Redirect to login
    router.push("/");
  };

  // Don't render until authentication is verified
  if (!isAuthenticated) {
    return null;
  }

  return (
    <div className="min-h-screen" style={{ background: '#f5f0eb' }}>
      {/* Top Navigation */}
      <nav className="bg-white shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex justify-between items-center h-20">
            {/* Left side - Logo/Title */}
            <div className="flex items-center">
              <Link href="/dashboard" className="flex items-center space-x-1 hover:opacity-80 transition-opacity">
                <h1 className="text-4xl font-bold tracking-tight">
                  <span className="text-gray-600">TO</span>
                  <span className="text-[#e08b3d]">DO</span>
                  <span className="inline-flex items-center justify-center w-10 h-10 ml-1 rounded-full bg-[#e08b3d] text-white">
                    <svg className="h-6 w-6" fill="none" viewBox="0 0 24 24" stroke="currentColor" strokeWidth={3}>
                      <path strokeLinecap="round" strokeLinejoin="round" d="M5 13l4 4L19 7" />
                    </svg>
                  </span>
                </h1>
              </Link>
            </div>

            {/* Right side - User menu */}
            <div className="flex items-center space-x-4">
              <span className="text-sm text-gray-600">
                {userEmail}
              </span>
              <button
                onClick={handleLogout}
                className="px-4 py-2 text-sm font-medium rounded-lg text-white bg-[#e08b3d] hover:bg-[#d17a2f] transition-colors"
              >
                Logout
              </button>
            </div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="max-w-6xl mx-auto py-8 px-4 sm:px-6 lg:px-8">
        {children}
      </main>
    </div>
  );
}
