/**
 * Constants Index
 *
 * Central export for all application constants.
 *
 * @module lib/constants
 */

export * from "./errors";
export * from "./theme";

/**
 * External URLs
 */
export const BOOK_URL =
  process.env.NEXT_PUBLIC_BOOK_URL ||
  "https://danbiocchi.github.io/physical-ai-book/";

/**
 * API Configuration
 */
export const API_BASE_URL =
  process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";
