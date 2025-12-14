/**
 * Chat Proxy API Route
 *
 * Proxies chat requests to the FastAPI backend with authentication.
 * Validates the user session and forwards the request with proper authorization.
 *
 * @module app/api/chat/route
 */

import { NextRequest, NextResponse } from "next/server";
import { auth } from "@/lib/auth";
import { headers } from "next/headers";
import { BACKEND_URL } from "@/lib/config";

/**
 * Request body for chat endpoint
 */
interface ChatRequestBody {
  message: string;
  session_id?: string;
}

/**
 * POST /api/chat
 *
 * Forwards chat messages to the FastAPI backend with user authentication.
 * The backend URL is configured via NEXT_PUBLIC_BACKEND_URL environment variable.
 */
export async function POST(request: NextRequest): Promise<NextResponse> {
  try {
    // Get the session from Better Auth
    const session = await auth.api.getSession({
      headers: await headers(),
    });

    // Check if user is authenticated
    if (!session || !session.user) {
      return NextResponse.json(
        {
          error: "Unauthorized",
          detail: "You must be logged in to use the chat feature",
        },
        { status: 401 }
      );
    }

    // Parse the request body
    let body: ChatRequestBody;
    try {
      body = await request.json();
    } catch {
      return NextResponse.json(
        {
          error: "Bad Request",
          detail: "Invalid JSON in request body",
        },
        { status: 400 }
      );
    }

    // Validate the message
    if (!body.message || typeof body.message !== "string") {
      return NextResponse.json(
        {
          error: "Bad Request",
          detail: "Message is required and must be a string",
        },
        { status: 400 }
      );
    }

    const trimmedMessage = body.message.trim();
    if (trimmedMessage.length === 0) {
      return NextResponse.json(
        {
          error: "Bad Request",
          detail: "Message cannot be empty",
        },
        { status: 400 }
      );
    }

    // Prepare the request to the backend
    const backendRequestBody = {
      message: trimmedMessage,
      ...(body.session_id && { session_id: body.session_id }),
    };

    // Build headers for backend request
    const backendHeaders: HeadersInit = {
      "Content-Type": "application/json",
    };

    // Add user context to the request via custom header
    // The backend can use this for user-specific features
    backendHeaders["X-User-ID"] = session.user.id;
    if (session.user.email) {
      backendHeaders["X-User-Email"] = session.user.email;
    }

    // If the session has a token, include it for backend authentication
    // Note: Better Auth uses session cookies, but we can generate a token
    // for backend services if needed
    if (session.session?.token) {
      backendHeaders["Authorization"] = `Bearer ${session.session.token}`;
    }

    // Forward the request to the FastAPI backend
    const backendResponse = await fetch(`${BACKEND_URL}/api/v1/chat`, {
      method: "POST",
      headers: backendHeaders,
      body: JSON.stringify(backendRequestBody),
    });

    // Get the response text
    const responseText = await backendResponse.text();

    // Parse the response
    let responseData;
    try {
      responseData = JSON.parse(responseText);
    } catch {
      console.error("[Chat API] Invalid JSON from backend:", responseText);
      return NextResponse.json(
        {
          error: "Backend Error",
          detail: "Invalid response from chat backend",
        },
        { status: 502 }
      );
    }

    // If the backend returned an error, forward it
    if (!backendResponse.ok) {
      const errorDetail =
        responseData.detail ||
        responseData.error ||
        responseData.message ||
        "An error occurred while processing your request";

      return NextResponse.json(
        {
          error: "Backend Error",
          detail: errorDetail,
        },
        { status: backendResponse.status }
      );
    }

    // Return the successful response
    return NextResponse.json(responseData);
  } catch (error) {
    console.error("[Chat API] Unexpected error:", error);

    // Handle network errors to the backend
    if (error instanceof TypeError && error.message.includes("fetch")) {
      return NextResponse.json(
        {
          error: "Service Unavailable",
          detail:
            "Unable to reach the chat backend. Please try again later.",
        },
        { status: 503 }
      );
    }

    return NextResponse.json(
      {
        error: "Internal Server Error",
        detail: "An unexpected error occurred",
      },
      { status: 500 }
    );
  }
}

/**
 * GET /api/chat
 *
 * Health check endpoint for the chat proxy
 */
export async function GET(): Promise<NextResponse> {
  return NextResponse.json({
    status: "ok",
    backend_url: BACKEND_URL,
    message: "Chat proxy is running. Use POST to send messages.",
  });
}
