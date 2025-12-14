/**
 * Backend Adapter Service
 *
 * Transforms ChatKit requests to FastAPI backend format and vice versa.
 * Handles communication with the RAG chatbot backend deployed on Hugging Face Spaces.
 *
 * @module lib/api/backend-adapter
 */

import { BACKEND_URL } from "@/lib/config";

/**
 * Citation returned from the RAG backend
 */
export interface Citation {
  /** Title of the source document/chapter */
  title: string;
  /** URL path to the textbook section */
  url: string;
  /** Relevant text excerpt from the source */
  excerpt?: string;
  /** Relevance score (0-1) */
  score?: number;
}

/**
 * Request format expected by the FastAPI backend
 */
export interface BackendChatRequest {
  /** User's message/question */
  message: string;
  /** Optional session ID for conversation continuity */
  session_id?: string;
}

/**
 * Response format from the FastAPI backend
 */
export interface BackendChatResponse {
  /** Assistant's response text */
  response: string;
  /** Citations from the RAG retrieval */
  citations: Citation[];
  /** Session ID for conversation continuity */
  session_id: string;
}

/**
 * Error response from the backend
 */
export interface BackendErrorResponse {
  detail?: string;
  error?: string;
  message?: string;
}

/**
 * Result of a chat request including parsed citations
 */
export interface ChatResult {
  /** Success status */
  success: boolean;
  /** Response message from assistant */
  message: string;
  /** Citations from RAG retrieval */
  citations: Citation[];
  /** Session ID for conversation continuity */
  sessionId: string;
  /** Error message if request failed */
  error?: string;
}

/**
 * Transform ChatKit-style request to FastAPI backend format
 *
 * @param message - User's message text
 * @param sessionId - Optional session ID for conversation continuity
 * @returns Formatted request body for backend API
 */
export function transformToBackendRequest(
  message: string,
  sessionId?: string
): BackendChatRequest {
  return {
    message: message.trim(),
    ...(sessionId && { session_id: sessionId }),
  };
}

/**
 * Transform FastAPI backend response to ChatKit-compatible format
 *
 * @param response - Raw response from FastAPI backend
 * @returns Transformed result with citations parsed
 */
export function transformFromBackendResponse(
  response: BackendChatResponse
): ChatResult {
  return {
    success: true,
    message: response.response,
    citations: response.citations || [],
    sessionId: response.session_id,
  };
}

/**
 * Parse error response from backend
 *
 * @param errorData - Error response object
 * @param statusText - HTTP status text fallback
 * @returns Human-readable error message
 */
export function parseBackendError(
  errorData: BackendErrorResponse | unknown,
  statusText: string
): string {
  if (!errorData || typeof errorData !== "object") {
    return statusText || "An error occurred communicating with the backend";
  }

  const error = errorData as BackendErrorResponse;

  if (error.detail) {
    return typeof error.detail === "string"
      ? error.detail
      : JSON.stringify(error.detail);
  }

  if (error.error) {
    return error.error;
  }

  if (error.message) {
    return error.message;
  }

  return statusText || "An error occurred communicating with the backend";
}

/**
 * Send a chat message to the FastAPI backend
 *
 * @param message - User's message text
 * @param options - Request options
 * @param options.sessionId - Optional session ID for conversation continuity
 * @param options.token - JWT token for authentication
 * @param options.signal - AbortSignal for request cancellation
 * @returns Chat result with response and citations
 */
export async function sendChatMessage(
  message: string,
  options: {
    sessionId?: string;
    token?: string;
    signal?: AbortSignal;
  } = {}
): Promise<ChatResult> {
  const { sessionId, token, signal } = options;

  const requestBody = transformToBackendRequest(message, sessionId);

  const headers: HeadersInit = {
    "Content-Type": "application/json",
  };

  if (token) {
    headers["Authorization"] = `Bearer ${token}`;
  }

  try {
    const response = await fetch(`${BACKEND_URL}/api/v1/chat`, {
      method: "POST",
      headers,
      body: JSON.stringify(requestBody),
      signal,
    });

    const rawText = await response.text();
    let data: BackendChatResponse | BackendErrorResponse;

    try {
      data = JSON.parse(rawText);
    } catch {
      return {
        success: false,
        message: "",
        citations: [],
        sessionId: sessionId || "",
        error: "Invalid response from backend",
      };
    }

    if (!response.ok) {
      const errorMessage = parseBackendError(data, response.statusText);
      return {
        success: false,
        message: "",
        citations: [],
        sessionId: sessionId || "",
        error: errorMessage,
      };
    }

    return transformFromBackendResponse(data as BackendChatResponse);
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") {
      return {
        success: false,
        message: "",
        citations: [],
        sessionId: sessionId || "",
        error: "Request was cancelled",
      };
    }

    const errorMessage =
      error instanceof Error
        ? error.message
        : "Failed to communicate with backend";

    return {
      success: false,
      message: "",
      citations: [],
      sessionId: sessionId || "",
      error: errorMessage,
    };
  }
}

/**
 * Send a chat message through the local proxy endpoint
 * This route handles authentication and forwards to the backend
 *
 * @param message - User's message text
 * @param options - Request options
 * @param options.sessionId - Optional session ID for conversation continuity
 * @param options.signal - AbortSignal for request cancellation
 * @returns Chat result with response and citations
 */
export async function sendChatMessageViaProxy(
  message: string,
  options: {
    sessionId?: string;
    signal?: AbortSignal;
  } = {}
): Promise<ChatResult> {
  const { sessionId, signal } = options;

  try {
    const response = await fetch("/api/chat", {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        message: message.trim(),
        session_id: sessionId,
      }),
      signal,
      credentials: "include", // Include cookies for session
    });

    const rawText = await response.text();
    let data: BackendChatResponse | BackendErrorResponse;

    try {
      data = JSON.parse(rawText);
    } catch {
      return {
        success: false,
        message: "",
        citations: [],
        sessionId: sessionId || "",
        error: "Invalid response from server",
      };
    }

    if (!response.ok) {
      const errorMessage = parseBackendError(data, response.statusText);
      return {
        success: false,
        message: "",
        citations: [],
        sessionId: sessionId || "",
        error: errorMessage,
      };
    }

    return transformFromBackendResponse(data as BackendChatResponse);
  } catch (error) {
    if (error instanceof Error && error.name === "AbortError") {
      return {
        success: false,
        message: "",
        citations: [],
        sessionId: sessionId || "",
        error: "Request was cancelled",
      };
    }

    const errorMessage =
      error instanceof Error
        ? error.message
        : "Failed to communicate with server";

    return {
      success: false,
      message: "",
      citations: [],
      sessionId: sessionId || "",
      error: errorMessage,
    };
  }
}

/**
 * Format citations for display in chat UI
 *
 * @param citations - Array of citations from backend
 * @returns Formatted markdown string with citation links
 */
export function formatCitationsForDisplay(citations: Citation[]): string {
  if (!citations || citations.length === 0) {
    return "";
  }

  const citationLines = citations.map((citation, index) => {
    const scoreText = citation.score
      ? ` (relevance: ${Math.round(citation.score * 100)}%)`
      : "";
    return `${index + 1}. [${citation.title}](${citation.url})${scoreText}`;
  });

  return `\n\n**Sources:**\n${citationLines.join("\n")}`;
}

/**
 * Append citations to a response message
 *
 * @param message - Original response message
 * @param citations - Citations to append
 * @returns Message with formatted citations appended
 */
export function appendCitationsToMessage(
  message: string,
  citations: Citation[]
): string {
  const formattedCitations = formatCitationsForDisplay(citations);
  return `${message}${formattedCitations}`;
}
