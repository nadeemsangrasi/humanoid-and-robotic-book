"use client";

/**
 * Protected Chat Page
 *
 * Main chat interface for authenticated users.
 * Integrates ChatKitPanel with user authentication context and chat history.
 *
 * Route: /chat (protected)
 * Requires: Authentication
 */

import { useState, useCallback, useEffect } from "react";
import { useSearchParams, useRouter } from "next/navigation";
import Link from "next/link";
import { ChatKitPanel, type FactAction } from "@/components/ChatKitPanel";
import { useColorScheme, type ColorScheme } from "@/hooks/useColorScheme";
import { useAuth } from "@/components/auth/AuthProvider";
import { useChatHistory } from "@/hooks/useChatHistory";
import { NewChatButtonCompact } from "@/components/chat/NewChatButton";

/**
 * Chat Page Metadata (client component - using document.title)
 * Note: For proper SEO, consider using a server component wrapper
 * or implementing metadata in layout.tsx
 */
const PAGE_TITLE = "Chat - Physical AI & Humanoid Robotics";

/**
 * Chat Page Component
 *
 * Features:
 * - ChatKit integration with Better Auth session
 * - Theme switching support
 * - Fact saving widget actions
 * - User-specific chat context
 * - Chat history persistence
 */
export default function ChatPage() {
  const { user } = useAuth();
  const router = useRouter();
  const searchParams = useSearchParams();
  const { scheme: colorScheme, setScheme: setColorScheme } = useColorScheme();
  const [savedFacts, setSavedFacts] = useState<string[]>([]);

  // Get session ID from URL if present
  const initialSessionId = searchParams.get("session");

  // Chat history management
  const {
    sessionId,
    session,
    messages: historyMessages,
    isLoading: historyLoading,
    clearSession,
    addMessage,
  } = useChatHistory({
    initialSessionId,
    autoSave: true,
    onSessionChange: (newSessionId) => {
      // Update URL when session changes
      if (newSessionId && newSessionId !== initialSessionId) {
        router.replace(`/chat?session=${newSessionId}`, { scroll: false });
      } else if (!newSessionId && initialSessionId) {
        router.replace("/chat", { scroll: false });
      }
    },
  });

  /**
   * Handle widget actions from ChatKit
   * Currently supports saving facts from the conversation
   */
  const handleWidgetAction = useCallback(async (action: FactAction) => {
    if (action.type === "save") {
      setSavedFacts((prev) => {
        // Avoid duplicates
        if (prev.includes(action.factId)) {
          return prev;
        }
        return [...prev, action.factId];
      });
      // In a full implementation, this would save to a backend
      console.log(`[ChatPage] Saved fact: ${action.factId} - ${action.factText}`);
    }
  }, []);

  /**
   * Handle response end events from ChatKit
   */
  const handleResponseEnd = useCallback(() => {
    // Analytics or logging could go here
    console.log("[ChatPage] Response completed");
  }, []);

  /**
   * Handle theme change requests from ChatKit
   */
  const handleThemeRequest = useCallback(
    (scheme: ColorScheme) => {
      setColorScheme(scheme);
    },
    [setColorScheme]
  );

  /**
   * Handle starting a new chat
   */
  const handleNewChat = useCallback(() => {
    clearSession();
    router.replace("/chat", { scroll: false });
  }, [clearSession, router]);

  /**
   * Handle saving messages to chat history
   */
  const handleSaveMessage = useCallback(
    async (
      role: "user" | "assistant",
      content: string,
      citations?: { title: string; url: string; excerpt?: string; score?: number }[]
    ) => {
      await addMessage(role, content, citations);
    },
    [addMessage]
  );

  // Set page title on client side
  useEffect(() => {
    if (typeof document !== "undefined") {
      document.title = session?.title
        ? `${session.title} - Chat`
        : PAGE_TITLE;
    }
  }, [session?.title]);

  return (
    <div className="flex-1 flex flex-col">
      {/* Page header with user greeting and history link */}
      <div className="px-4 py-2 bg-blue-50 dark:bg-blue-900/20 border-b border-blue-100 dark:border-blue-800">
        <div className="max-w-6xl mx-auto flex items-center justify-between">
          <div className="flex items-center gap-4">
            {user && (
              <p className="text-sm text-blue-700 dark:text-blue-300">
                Welcome back, <strong>{user.name}</strong>!
                {session?.title && (
                  <span className="ml-2 text-blue-600 dark:text-blue-400">
                    - {session.title}
                  </span>
                )}
              </p>
            )}
          </div>
          <div className="flex items-center gap-3">
            {sessionId && (
              <button
                onClick={handleNewChat}
                className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 flex items-center gap-1"
              >
                <svg
                  className="w-4 h-4"
                  fill="none"
                  stroke="currentColor"
                  viewBox="0 0 24 24"
                  aria-hidden="true"
                >
                  <path
                    strokeLinecap="round"
                    strokeLinejoin="round"
                    strokeWidth={2}
                    d="M12 4v16m8-8H4"
                  />
                </svg>
                New Chat
              </button>
            )}
            <Link
              href="/history"
              className="text-sm text-blue-600 hover:text-blue-700 dark:text-blue-400 dark:hover:text-blue-300 flex items-center gap-1"
            >
              <svg
                className="w-4 h-4"
                fill="none"
                stroke="currentColor"
                viewBox="0 0 24 24"
                aria-hidden="true"
              >
                <path
                  strokeLinecap="round"
                  strokeLinejoin="round"
                  strokeWidth={2}
                  d="M12 8v4l3 3m6-3a9 9 0 11-18 0 9 9 0 0118 0z"
                />
              </svg>
              History
            </Link>
          </div>
        </div>
      </div>

      {/* Loading state for session restoration */}
      {historyLoading && initialSessionId && (
        <div className="px-4 py-2 bg-yellow-50 dark:bg-yellow-900/20 border-b border-yellow-100 dark:border-yellow-800">
          <div className="max-w-6xl mx-auto">
            <p className="text-sm text-yellow-700 dark:text-yellow-300 flex items-center gap-2">
              <svg
                className="w-4 h-4 animate-spin"
                fill="none"
                viewBox="0 0 24 24"
                aria-hidden="true"
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
              Loading conversation...
            </p>
          </div>
        </div>
      )}

      {/* Main chat interface */}
      <div className="flex-1 p-4 max-w-6xl mx-auto w-full">
        <ChatKitPanel
          theme={colorScheme}
          onWidgetAction={handleWidgetAction}
          onResponseEnd={handleResponseEnd}
          onThemeRequest={handleThemeRequest}
          sessionId={sessionId}
          initialMessages={historyMessages}
          onSaveMessage={handleSaveMessage}
        />
      </div>

      {/* Saved facts indicator (optional) */}
      {savedFacts.length > 0 && (
        <div className="fixed bottom-20 right-4 bg-green-100 dark:bg-green-900 text-green-800 dark:text-green-200 px-3 py-1 rounded-full text-sm shadow-lg">
          {savedFacts.length} fact{savedFacts.length > 1 ? "s" : ""} saved
        </div>
      )}
    </div>
  );
}
