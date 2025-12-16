/**
 * Theme Constants
 *
 * Color palette, gradients, and design tokens for the unified theme.
 * Used across landing page, chat, and all UI components.
 */

export const THEME_COLORS = {
  // Primary Gradient
  primary: "#667eea",
  primaryDark: "#5a67d8",
  primaryLight: "#7c87ec",

  // Secondary (Gradient end)
  secondary: "#764ba2",
  secondaryDark: "#6b4190",
  secondaryLight: "#8b5cb5",

  // Accent
  accent: "#25c2a0",
  accentDark: "#1fa88c",
  accentLight: "#3cd4b2",

  // Neutrals - Light Theme
  light: {
    bg: "#ffffff",
    bgSecondary: "#f8fafc",
    bgTertiary: "#f1f5f9",
    textPrimary: "#0f172a",
    textSecondary: "#475569",
    textMuted: "#94a3b8",
    border: "#e2e8f0",
  },

  // Neutrals - Dark Theme
  dark: {
    bg: "#0f172a",
    bgSecondary: "#1e293b",
    bgTertiary: "#334155",
    textPrimary: "#f8fafc",
    textSecondary: "#cbd5e1",
    textMuted: "#64748b",
    border: "#334155",
  },
} as const;

export const GRADIENTS = {
  primary: "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
  primaryHover: "linear-gradient(135deg, #5a67d8 0%, #6b4190 100%)",
  accent: "linear-gradient(135deg, #25c2a0 0%, #1fa88c 100%)",
} as const;

export const SHADOWS = {
  sm: "0 1px 2px 0 rgb(0 0 0 / 0.05)",
  md: "0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1)",
  lg: "0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1)",
  xl: "0 20px 25px -5px rgb(0 0 0 / 0.1), 0 8px 10px -6px rgb(0 0 0 / 0.1)",
  fab: "0 4px 12px rgba(102, 126, 234, 0.4)",
  fabHover: "0 6px 20px rgba(102, 126, 234, 0.5)",
} as const;

export const TRANSITIONS = {
  fast: "150ms ease",
  default: "200ms ease",
  slow: "300ms ease",
  theme: "300ms ease-in-out",
} as const;

export const BREAKPOINTS = {
  sm: "640px",
  md: "768px",
  lg: "1024px",
  xl: "1280px",
  "2xl": "1536px",
} as const;

export const NAVBAR_HEIGHT = 64;

export type ThemeMode = "light" | "dark" | "system";
