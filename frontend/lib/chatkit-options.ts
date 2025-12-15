import type { ChatKitOptions } from "@openai/chatkit";

/**
 * ChatKit Options Configuration
 * Generated from ChatKit Studio and customized for Physical AI & Humanoid Robotics textbook
 */
export const chatkitOptions: ChatKitOptions = {
  theme: {
    colorScheme: "light",
    radius: "pill",
    density: "normal",
    typography: {
      baseSize: 16,
      fontFamily:
        '"OpenAI Sans", system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, "Apple Color Emoji", "Segoe UI Emoji", "Noto Color Emoji", sans-serif',
      fontFamilyMono:
        'ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", "DejaVu Sans Mono", "Courier New", monospace',
      fontSources: [
        {
          family: "OpenAI Sans",
          src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Regular.woff2",
          weight: 400,
          style: "normal",
          display: "swap",
        },
        {
          family: "OpenAI Sans",
          src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Medium.woff2",
          weight: 500,
          style: "normal",
          display: "swap",
        },
        {
          family: "OpenAI Sans",
          src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-SemiBold.woff2",
          weight: 600,
          style: "normal",
          display: "swap",
        },
        {
          family: "OpenAI Sans",
          src: "https://cdn.openai.com/common/fonts/openai-sans/v2/OpenAISans-Bold.woff2",
          weight: 700,
          style: "normal",
          display: "swap",
        },
      ],
    },
  },
  composer: {
    attachments: {
      enabled: false,
    },
    tools: [
      {
        id: "search_docs",
        label: "Search docs",
        shortLabel: "Docs",
        placeholderOverride: "Search documentation",
        icon: "book-open",
        pinned: false,
      },
      {
        id: "ask_textbook",
        label: "Ask textbook",
        shortLabel: "Textbook",
        placeholderOverride: "Ask about Physical AI & Robotics",
        icon: "graduation-cap",
        pinned: true,
      },
    ],
  },
  startScreen: {
    greeting: "Physical AI & Humanoid Robotics Assistant",
    prompts: [
      {
        icon: "circle-question",
        label: "What is ChatKit?",
        prompt: "What is ChatKit?",
      },
      {
        icon: "robot",
        label: "Explain humanoid robotics",
        prompt: "What are the key components of humanoid robotics?",
      },
      {
        icon: "brain",
        label: "What is Physical AI?",
        prompt: "Explain Physical AI and its applications in robotics.",
      },
      {
        icon: "cog",
        label: "Robot kinematics",
        prompt: "Explain forward and inverse kinematics in robotics.",
      },
      {
        icon: "book-open",
        label: "ROS2 basics",
        prompt: "What are the fundamentals of ROS2 for robotics?",
      },
    ],
  },
};

/**
 * Get ChatKit options with dynamic color scheme
 */
export function getChatkitOptions(
  colorScheme: "light" | "dark" = "light"
): ChatKitOptions {
  return {
    ...chatkitOptions,
    theme: {
      ...chatkitOptions.theme,
      colorScheme,
    },
  };
}
