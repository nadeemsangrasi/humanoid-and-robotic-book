"use client";

/**
 * Protected Route Group Layout
 *
 * Layout for authenticated-only pages.
 * Provides server-side session validation and redirects unauthenticated users.
 *
 * Note: Primary protection is handled by middleware.ts
 * This layout provides an additional client-side check and
 * shared UI elements for protected pages.
 *
 * Route Group: (protected)
 * Applies to: /chat, /history, /profile, /settings
 */

import { useEffect, useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";
import { useAuth } from "@/components/auth/AuthProvider";
import { LogoutButton } from "@/components/auth/LogoutButton";

/**
 * Protected Layout Props
 */
interface ProtectedLayoutProps {
  children: React.ReactNode;
}

/**
 * Loading skeleton for protected pages
 */
function LoadingState() {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-50 dark:bg-gray-900">
      <div className="flex flex-col items-center">
        <svg
          className="animate-spin h-10 w-10 text-blue-600"
          xmlns="http://www.w3.org/2000/svg"
          fill="none"
          viewBox="0 0 24 24"
          aria-label="Loading"
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
        <p className="mt-4 text-gray-600 dark:text-gray-400">
          Verifying authentication...
        </p>
      </div>
    </div>
  );
}

/**
 * User menu component for header
 */
function UserMenu({
  userName,
  userEmail,
}: {
  userName: string | null;
  userEmail: string | null;
}) {
  return (
    <div className="flex items-center gap-4">
      <div className="hidden sm:flex flex-col items-end">
        {userName && (
          <span className="text-sm font-medium text-gray-900 dark:text-white">
            {userName}
          </span>
        )}
        {userEmail && (
          <span className="text-xs text-gray-500 dark:text-gray-400">
            {userEmail}
          </span>
        )}
      </div>
      <LogoutButton variant="button" className="text-sm" />
    </div>
  );
}

/**
 * Protected Layout Component
 *
 * Provides:
 * - Client-side auth verification (backup to middleware)
 * - Shared header with user info and logout
 * - Consistent styling for protected pages
 */
export default function ProtectedLayout({ children }: ProtectedLayoutProps) {
  const router = useRouter();
  const { user, isAuthenticated, isPending } = useAuth();

  // Track if user was ever authenticated to prevent unmounting during session refresh
  const [wasAuthenticated, setWasAuthenticated] = useState(false);

  // Update wasAuthenticated when user becomes authenticated
  useEffect(() => {
    if (isAuthenticated) {
      setWasAuthenticated(true);
    }
  }, [isAuthenticated]);

  // Client-side redirect for unauthenticated users
  // This is a backup to middleware protection
  // Only redirect if user was never authenticated (not just a temporary session refresh)
  useEffect(() => {
    if (!isPending && !isAuthenticated && !wasAuthenticated) {
      // Add a small delay to allow session state to settle after login redirect
      const timeoutId = setTimeout(() => {
        // Get current path for callback
        const currentPath = window.location.pathname;
        router.replace(`/login?callbackUrl=${encodeURIComponent(currentPath)}`);
      }, 200);
      return () => clearTimeout(timeoutId);
    }
  }, [isAuthenticated, isPending, wasAuthenticated, router]);

  // Show loading only on initial auth check, not during session refresh
  if (isPending && !wasAuthenticated) {
    return <LoadingState />;
  }

  // Show loading while redirecting unauthenticated users (only if never authenticated)
  if (!isAuthenticated && !wasAuthenticated) {
    return <LoadingState />;
  }

  return (
    <div className="min-h-screen flex flex-col bg-gray-50 dark:bg-gray-900">
      {/* Header with navigation and user menu */}
      <header className="sticky top-0 z-50 bg-white dark:bg-gray-800 border-b border-gray-200 dark:border-gray-700 shadow-sm">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex items-center justify-between h-16">
            {/* Logo and brand */}
            <Link
              href="/chat"
              className="flex items-center text-lg font-semibold text-gray-900 dark:text-white hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
            >
              <svg
                className="w-8 h-8 mr-2 text-blue-600"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                xmlns="http://www.w3.org/2000/svg"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M9.75 17L9 20l-1 1h8l-1-1-.75-3M3 13h18M5 17h14a2 2 0 002-2V5a2 2 0 00-2-2H5a2 2 0 00-2 2v10a2 2 0 002 2z"
                />
              </svg>
              <span className="hidden sm:inline">Physical AI & Humanoid Robotics</span>
              <span className="sm:hidden">AI Robotics</span>
            </Link>

            {/* Navigation (can be extended) */}
            <nav className="hidden md:flex items-center gap-6">
              <Link
                href="/chat"
                className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                Chat
              </Link>
              <Link
                href="/history"
                className="text-gray-600 dark:text-gray-300 hover:text-blue-600 dark:hover:text-blue-400 transition-colors"
              >
                History
              </Link>
            </nav>

            {/* User menu */}
            <UserMenu
              userName={user?.name ?? null}
              userEmail={user?.email ?? null}
            />
          </div>
        </div>
      </header>

      {/* Main content area */}
      <main className="flex-1 flex flex-col">
        {children}
      </main>

      {/* Footer */}
      <footer className="py-4 px-4 border-t border-gray-200 dark:border-gray-700 bg-white dark:bg-gray-800">
        <div className="max-w-7xl mx-auto text-center">
          <p className="text-sm text-gray-500 dark:text-gray-400">
            Interactive textbook chatbot for robotics education
          </p>
        </div>
      </footer>
    </div>
  );
}
