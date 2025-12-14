/**
 * Login Page
 *
 * User login page using the LoginForm component.
 * Part of the (auth) route group for consistent auth page layouts.
 * Supports callbackUrl query parameter for post-login redirect.
 *
 * Route: /login
 * Query params: ?callbackUrl=/path (optional)
 */

import { Suspense } from "react";
import { LoginForm } from "@/components/auth/LoginForm";

/**
 * Page metadata
 */
export const metadata = {
  title: "Sign In | Physical AI & Humanoid Robotics",
  description: "Sign in to access the Physical AI & Humanoid Robotics textbook chatbot.",
};

/**
 * Loading fallback for form
 */
function FormSkeleton() {
  return (
    <div className="w-full max-w-md mx-auto">
      <div className="bg-white dark:bg-gray-800 shadow-lg rounded-lg p-8 animate-pulse">
        <div className="h-8 bg-gray-200 dark:bg-gray-700 rounded w-3/4 mx-auto mb-4" />
        <div className="h-4 bg-gray-200 dark:bg-gray-700 rounded w-1/2 mx-auto mb-8" />
        <div className="space-y-6">
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded" />
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded" />
          <div className="h-10 bg-blue-200 dark:bg-blue-800 rounded" />
        </div>
      </div>
    </div>
  );
}

/**
 * Login Page Component
 *
 * Wrapped in Suspense because LoginForm uses useSearchParams hook
 * which requires client-side rendering.
 */
export default function LoginPage() {
  return (
    <Suspense fallback={<FormSkeleton />}>
      <LoginForm />
    </Suspense>
  );
}
