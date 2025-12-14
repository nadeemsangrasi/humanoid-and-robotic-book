"use client";

/**
 * Auth Route Group Layout
 *
 * Shared layout for authentication pages (/login, /register).
 * Provides:
 * - Centered page layout
 * - Redirect for already authenticated users
 * - Consistent styling for auth pages
 *
 * Route Group: (auth)
 * Applies to: /login, /register
 */

import { useEffect } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";

/**
 * Auth Layout Props
 */
interface AuthLayoutProps {
  children: React.ReactNode;
}

/**
 * Loading spinner component
 */
function LoadingSpinner() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col items-center">
        <svg
          className="animate-spin h-8 w-8 text-blue-600"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
        >
          <circle
            className="opacity-25"
            cx="12"
            cy="12"
            r="10"
            stroke="currentColor"
            strokeWidth="4"
          />
          <path
            className="opacity-75"
            fill="currentColor"
            d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"
          />
        </svg>
        <p className="mt-4 text-gray-600 dark:text-gray-400">Loading...</p>
      </div>
    </div>
  );
}

/**
 * Auth Layout Component
 *
 * Redirects authenticated users away from auth pages to /chat.
 * Shows loading state while checking authentication.
 */
export default function AuthLayout({ children }: AuthLayoutProps) {
  const router = useRouter();
  const { isAuthenticated, isPending } = useAuth();

  // Redirect authenticated users away from auth pages
  useEffect(() => {
    if (!isPending && isAuthenticated) {
      router.replace("/chat");
    }
  }, [isAuthenticated, isPending, router]);

  // Show loading while checking auth state
  if (isPending) {
    return <LoadingSpinner />;
  }

  // If authenticated, show loading while redirecting
  if (isAuthenticated) {
    return <LoadingSpinner />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Header */}
      <header className="py-6 px-4">
        <div className="max-w-7xl mx-auto">
          <Link
            href="/"
            className="flex items-center text-xl font-semibold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
          >
            <svg
              className="w-8 h-8 mr-2 text-blue-600"
              fill="none"
              stroke="currentColor"
              viewBox="0 0 24 24"
              xmlns="http://www.w3.org/2000/svg"
            >
              <path
                strokeLinecap="round"
                strokeLinejoin="round"
                strokeWidth={2}
                d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
              />
            </svg>
            Physical AI & Humanoid Robotics
          </Link>
        </div>
      </header>

      {/* Main Content - Centered */}
      <main className="flex-1 flex items-center justify-center px-4 py-8">
        {children}
      </main>

      {/* Footer */}
      <footer className="py-6 px-4 border-t border-gray-200 dark:border-gray-700">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Interactive textbook chatbot for robotics education
          </p>
        </div>
      </footer>
    </div>
  );
}
