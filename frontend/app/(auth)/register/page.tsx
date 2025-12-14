/**
 * Register Page
 *
 * User registration page using the RegisterForm component.
 * Part of the (auth) route group for consistent auth page layouts.
 *
 * Route: /register
 */

import { Suspense } from "react";
import { RegisterForm } from "@/components/auth/RegisterForm";

/**
 * Page metadata
 */
export const metadata = {
  title: "Create Account | Physical AI & Humanoid Robotics",
  description: "Create a new account to access the Physical AI & Humanoid Robotics textbook chatbot.",
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
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded" />
          <div className="h-10 bg-gray-200 dark:bg-gray-700 rounded" />
          <div className="h-10 bg-blue-200 dark:bg-blue-800 rounded" />
        </div>
      </div>
    </div>
  );
}

/**
 * Register Page Component
 */
export default function RegisterPage() {
  return (
    <Suspense fallback={<FormSkeleton />}>
      <RegisterForm />
    </Suspense>
  );
}
