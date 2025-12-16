# Quickstart Guide: Book & Chatbot Integration

**Feature**: 004-book-chatbot-integration
**Date**: 2025-12-16

## Prerequisites

- Node.js 18+ installed
- Existing frontend setup from 002-auth-frontend-integration
- Access to PostgreSQL Neon DB (existing)
- GitHub Pages book deployed at: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/

## Quick Setup

### 1. Install New Dependencies

```bash
cd frontend
npm install lucide-react framer-motion @radix-ui/react-dialog clsx tailwind-merge
```

### 2. Environment Variables

No new environment variables required. Ensure existing `.env.local` has:

```env
# Database (existing)
DATABASE_URL=your_neon_db_url

# Better Auth (existing)
BETTER_AUTH_SECRET=your_secret
BETTER_AUTH_URL=http://localhost:3000

# Backend API (existing)
NEXT_PUBLIC_BACKEND_URL=your_backend_url
```

### 3. Start Development Server

```bash
npm run dev
```

### 4. Verify Setup

1. Open http://localhost:3000 - Should see landing page (after implementation)
2. Navigate to http://localhost:3000/book - Should see embedded textbook
3. Navigate to http://localhost:3000/chat - Should redirect to login (if not authenticated)

## File Structure to Create

```
frontend/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── book/
│   │   └── page.tsx                # Book iframe
│   └── chat/
│       └── page.tsx                # Chat with sidebar
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx
│   │   ├── Footer.tsx
│   │   └── ThemeToggle.tsx
│   ├── landing/
│   │   ├── Hero.tsx
│   │   ├── Features.tsx
│   │   ├── BookPreview.tsx
│   │   └── ChatbotDemo.tsx
│   ├── chat/
│   │   ├── ChatLayout.tsx
│   │   ├── ChatSidebar.tsx
│   │   ├── ChatHeader.tsx
│   │   ├── ChatMessages.tsx
│   │   ├── ChatMessage.tsx
│   │   ├── ChatInput.tsx
│   │   └── ChatTypingIndicator.tsx
│   └── instant-chat/
│       ├── FloatingChatButton.tsx
│       ├── InstantChatModal.tsx
│       └── LoginPromptModal.tsx
├── hooks/
│   └── useTheme.ts
└── lib/
    └── constants/
        └── theme.ts
```

## Implementation Order

### Phase 1: Core Infrastructure (Start Here)
1. Create `lib/constants/theme.ts` - Theme configuration
2. Create `hooks/useTheme.ts` - Theme hook
3. Create `components/layout/ThemeToggle.tsx`
4. Create `components/layout/Navbar.tsx`
5. Update `app/layout.tsx` - Add Navbar
6. Create `app/book/page.tsx` - Book iframe
7. Update `middleware.ts` - Update route protection

### Phase 2: Floating Chat
1. Create `components/instant-chat/FloatingChatButton.tsx`
2. Create `components/instant-chat/LoginPromptModal.tsx`
3. Create `components/instant-chat/InstantChatModal.tsx`
4. Update `app/layout.tsx` - Add FloatingChatButton

### Phase 3: Landing Page
1. Create `components/landing/Hero.tsx`
2. Create `components/landing/Features.tsx`
3. Create `components/landing/BookPreview.tsx`
4. Create `components/landing/ChatbotDemo.tsx`
5. Create `components/layout/Footer.tsx`
6. Update `app/page.tsx` - Compose landing page

### Phase 4: Chat UI Enhancement
1. Create `components/chat/ChatLayout.tsx`
2. Create `components/chat/ChatSidebar.tsx`
3. Create `components/chat/ChatHeader.tsx`
4. Create `components/chat/ChatMessage.tsx`
5. Create `components/chat/ChatMessages.tsx`
6. Create `components/chat/ChatInput.tsx`
7. Create `components/chat/ChatTypingIndicator.tsx`
8. Create `app/chat/page.tsx` - New chat page

### Phase 5: Theme Polish
1. Update `app/globals.css` - CSS custom properties
2. Update all components for dark mode support
3. Test and refine animations

## Key Code Snippets

### Book Iframe Page
```tsx
// app/book/page.tsx
"use client";

import { useState } from "react";

const BOOK_URL = "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/";

export default function BookPage() {
  const [isLoading, setIsLoading] = useState(true);
  const [hasError, setHasError] = useState(false);

  return (
    <div className="h-[calc(100vh-64px)] w-full">
      {isLoading && !hasError && (
        <div className="flex items-center justify-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
        </div>
      )}
      {hasError && (
        <div className="flex flex-col items-center justify-center h-full gap-4">
          <p>Unable to load the textbook.</p>
          <a href={BOOK_URL} target="_blank" className="text-primary underline">
            Open in new tab
          </a>
        </div>
      )}
      <iframe
        src={BOOK_URL}
        className={`w-full h-full border-0 ${isLoading || hasError ? 'hidden' : 'block'}`}
        onLoad={() => setIsLoading(false)}
        onError={() => { setIsLoading(false); setHasError(true); }}
        title="Physical AI & Humanoid Robotics Textbook"
        allow="fullscreen"
      />
    </div>
  );
}
```

### Theme Hook
```tsx
// hooks/useTheme.ts
"use client";

import { useState, useEffect } from "react";

type Theme = 'light' | 'dark';

export function useTheme() {
  const [theme, setThemeState] = useState<Theme>('light');
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
    const stored = localStorage.getItem('theme') as Theme | null;
    const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const initialTheme = stored || (systemPreference ? 'dark' : 'light');
    setThemeState(initialTheme);
    document.documentElement.classList.toggle('dark', initialTheme === 'dark');
  }, []);

  const setTheme = (newTheme: Theme) => {
    setThemeState(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  const toggleTheme = () => setTheme(theme === 'light' ? 'dark' : 'light');

  return { theme, setTheme, toggleTheme, mounted };
}
```

### Middleware Update
```typescript
// middleware.ts (key changes)
const protectedRoutes = ["/chat", "/history", "/profile", "/settings"];
const publicRoutes = ["/", "/book", "/login", "/register", "/api/auth"];

// Remove root route redirect to /chat
// Let landing page render at /
```

## Testing

```bash
# Run unit tests
npm run test

# Run tests with UI
npm run test:ui

# Run specific test file
npm run test -- components/layout/Navbar.test.tsx
```

## Deployment

```bash
# Build for production
npm run build

# Deploy to Vercel (auto-deploys on push to main)
git push origin 004-book-chatbot-integration
# Then create PR to merge to main
```

## Verification Checklist

- [ ] Landing page loads at `/`
- [ ] Book iframe loads at `/book`
- [ ] Chat page loads at `/chat` (requires auth)
- [ ] FAB appears on landing and book pages
- [ ] FAB hidden on chat page
- [ ] Theme toggle works
- [ ] Mobile navigation works
- [ ] Auth flow works for chat access
