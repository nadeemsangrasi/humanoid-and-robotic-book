# API Contracts: Book & Chatbot Integration

**Feature**: 004-book-chatbot-integration
**Date**: 2025-12-16

## Overview

This feature is primarily **frontend-only** and reuses existing API endpoints. No new backend APIs are required.

## Existing APIs Used

### Authentication (Better Auth)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/auth/get-session` | GET | Get current session |
| `/api/auth/sign-in` | POST | Sign in user |
| `/api/auth/sign-up` | POST | Register user |
| `/api/auth/sign-out` | POST | Sign out user |

### Chat History (Existing)

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/chat/history` | GET | List user's chat sessions |
| `/api/chat/history` | POST | Create new chat session |
| `/api/chat/history/[sessionId]` | GET | Get session details |
| `/api/chat/history/[sessionId]` | DELETE | Delete session |
| `/api/chat/history/[sessionId]/messages` | GET | Get session messages |
| `/api/chat/history/[sessionId]/messages` | POST | Add message to session |

### Chat Completion (Backend RAG)

| Endpoint | Method | Description |
|----------|--------|-------------|
| External Backend API | POST | Send message, get RAG response |

## Route Contracts (Frontend)

### Public Routes

| Route | Component | Auth Required |
|-------|-----------|---------------|
| `/` | Landing Page | No |
| `/book` | Book Iframe | No |
| `/login` | Login Form | No |
| `/register` | Register Form | No |

### Protected Routes

| Route | Component | Auth Required |
|-------|-----------|---------------|
| `/chat` | Chat Interface | Yes |
| `/history` | Chat History | Yes |

## Component Props Contracts

### Navbar
```typescript
interface NavbarProps {
  // No props - uses hooks internally
}
```

### ThemeToggle
```typescript
interface ThemeToggleProps {
  className?: string;
}
```

### FloatingChatButton
```typescript
interface FloatingChatButtonProps {
  // No props - uses pathname and auth hooks
}
```

### InstantChatModal
```typescript
interface InstantChatModalProps {
  isOpen: boolean;
  onClose: () => void;
}
```

### LoginPromptModal
```typescript
interface LoginPromptModalProps {
  isOpen: boolean;
  onClose: () => void;
  callbackUrl?: string;
}
```

### ChatLayout
```typescript
interface ChatLayoutProps {
  children: React.ReactNode;
}
```

### ChatSidebar
```typescript
interface ChatSidebarProps {
  conversations: ChatSession[];
  activeSessionId?: string;
  onSelectConversation: (id: string) => void;
  onNewChat: () => void;
  onDeleteConversation: (id: string) => void;
  collapsed?: boolean;
  onToggleCollapse?: () => void;
}
```

### ChatMessage
```typescript
interface ChatMessageProps {
  message: {
    id: string;
    role: 'user' | 'assistant';
    content: string;
    citations?: Citation[];
    createdAt: Date;
  };
  showTimestamp?: boolean;
}
```

### Hero
```typescript
interface HeroProps {
  // No props - content is static
}
```

### Features
```typescript
interface FeaturesProps {
  // No props - content is static
}
```

### BookPreview
```typescript
interface BookPreviewProps {
  // No props - content is static
}
```

### ChatbotDemo
```typescript
interface ChatbotDemoProps {
  // No props - content is static
}
```

### Footer
```typescript
interface FooterProps {
  // No props - content is static
}
```

## Hook Contracts

### useTheme
```typescript
interface UseThemeReturn {
  theme: 'light' | 'dark';
  setTheme: (theme: 'light' | 'dark') => void;
  toggleTheme: () => void;
  systemTheme: 'light' | 'dark';
}
```

### useAuth (Existing)
```typescript
interface UseAuthReturn {
  user: User | null;
  session: Session | null;
  isLoading: boolean;
  isAuthenticated: boolean;
}
```

### useChatHistory (Existing)
```typescript
interface UseChatHistoryReturn {
  sessions: ChatSession[];
  isLoading: boolean;
  error: Error | null;
  createSession: () => Promise<ChatSession>;
  deleteSession: (id: string) => Promise<void>;
  refresh: () => void;
}
```

## Constants

### Book URL
```typescript
const BOOK_URL = "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/";
```

### Theme Colors
```typescript
const THEME_COLORS = {
  primary: '#667eea',
  primaryDark: '#5a67d8',
  secondary: '#764ba2',
  accent: '#25c2a0',
  accentDark: '#1fa88c',
};
```

### Navbar Height
```typescript
const NAVBAR_HEIGHT = 64; // pixels
```

## Error Responses

All API errors follow existing Better Auth error format:

```typescript
interface APIError {
  error: string;
  message: string;
  statusCode: number;
}
```

## No New Backend APIs Required

This feature operates entirely on the frontend by:
1. Reusing existing auth APIs
2. Reusing existing chat history APIs
3. Using the existing ChatKitPanel for RAG interactions
4. Storing UI preferences in localStorage
