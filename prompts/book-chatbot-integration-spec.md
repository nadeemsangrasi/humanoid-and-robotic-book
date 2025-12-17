# Physical AI & Humanoid Robotics - Book & Chatbot Integration Specification

## Project Overview

Integrate the existing static Docusaurus book (deployed on GitHub Pages) with the Next.js chatbot frontend using an iframe strategy. The goal is to create a unified educational platform where users can read the textbook and interact with an AI assistant.

### Current Deployments
- **Book (Docusaurus):** https://nadeemsangrasi.github.io/humanoid-and-robotic-book/
- **Chatbot (Next.js):** https://rag-chatbot-teal-two.vercel.app

### Architecture Decision
**Strategy:** Iframe embedding for book content
- Book remains static on GitHub Pages (no migration needed)
- Next.js frontend acts as the unified shell
- Iframe loads book content seamlessly
- Single deployment for chatbot + landing page on Vercel

---

## User Stories

---

### US-1: Book Navigation with Seamless Iframe Integration

**As a** reader
**I want** to click "Book" in the navbar and see the textbook loaded seamlessly
**So that** the book feels like a native part of the application

#### Acceptance Criteria

- [ ] Navbar contains "Book" navigation item
- [ ] Clicking "Book" navigates to `/book` route
- [ ] `/book` page renders full-width iframe containing the Docusaurus book
- [ ] Iframe should:
  - Take full viewport height (minus navbar)
  - Have no visible borders or scrollbars (use book's internal scrolling)
  - Feel like a native part of the app (seamless integration)
  - Handle responsive sizing on all screen sizes
- [ ] Loading state shown while iframe loads
- [ ] Iframe navigation within book works normally (internal links)
- [ ] Book is accessible **without authentication** (public)

#### Technical Implementation

```tsx
// app/book/page.tsx
"use client";

import { useState } from "react";

const BOOK_URL = "https://nadeemsangrasi.github.io/humanoid-and-robotic-book/";

export default function BookPage() {
  const [isLoading, setIsLoading] = useState(true);

  return (
    <div className="h-[calc(100vh-64px)] w-full">
      {isLoading && (
        <div className="flex items-center justify-center h-full">
          <div className="animate-spin rounded-full h-12 w-12 border-b-2 border-primary" />
        </div>
      )}
      <iframe
        src={BOOK_URL}
        className={`w-full h-full border-0 ${isLoading ? 'hidden' : 'block'}`}
        onLoad={() => setIsLoading(false)}
        title="Physical AI & Humanoid Robotics Textbook"
        allow="fullscreen"
      />
    </div>
  );
}
```

#### Styling Requirements

```css
/* Remove iframe artifacts */
iframe {
  border: none;
  outline: none;
}

/* Ensure seamless height */
.book-container {
  height: calc(100vh - var(--navbar-height));
  overflow: hidden;
}
```

#### Edge Cases
- Handle iframe load errors with fallback message + direct link
- Ensure X-Frame-Options on GitHub Pages allows embedding (usually allowed)
- Test cross-origin messaging if needed for theme sync

---

### US-2: Navigate Between Book and Chat

**As a** user
**I want** to easily switch between the Book and Chat sections
**So that** I can read content and ask questions seamlessly

#### Acceptance Criteria

- [ ] Navbar displays both "Book" and "Chat" navigation items
- [ ] Active nav item is visually highlighted
- [ ] "Book" → `/book` (iframe with Docusaurus)
- [ ] "Chat" → `/chat` (existing chatbot page)
- [ ] Chat page renders the existing ChatKitPanel component
- [ ] **Chat requires authentication** - redirect to login if not authenticated
- [ ] Smooth transitions between routes
- [ ] Mobile: Hamburger menu with both options

#### Navigation Structure

```
┌─────────────────────────────────────────────────────────────────┐
│  [Logo] Physical AI & Robotics    │  Book  │  Chat  │  Login   │
└─────────────────────────────────────────────────────────────────┘
```

When authenticated:
```
┌─────────────────────────────────────────────────────────────────┐
│  [Logo] Physical AI & Robotics    │  Book  │  Chat  │ [Avatar] │
└─────────────────────────────────────────────────────────────────┘
```

#### Auth Flow for Chat

```typescript
// middleware.ts or route protection
if (pathname.startsWith('/chat') && !isAuthenticated) {
  redirect(`/login?callbackUrl=${encodeURIComponent(pathname)}`);
}
```

---

### US-3: Instant Chat Floating Button

**As a** reader
**I want** a floating chat button at the bottom of the screen
**So that** I can quickly ask questions without leaving the current page

#### Acceptance Criteria

- [ ] Floating Action Button (FAB) fixed at bottom-right corner
- [ ] Visible on all pages (landing, book, etc.) except `/chat` page
- [ ] Click opens instant chat modal/drawer
- [ ] **Requires authentication:**
  - If logged out: Show login prompt modal instead of chat
  - If logged in: Open chat interface
- [ ] Chat modal features:
  - Slide-up animation from bottom
  - Close button (X) in header
  - Minimize button to collapse back to FAB
  - Resizable height (drag handle)
  - Chat input and message history
- [ ] Chat context preserved when closing/reopening modal
- [ ] Mobile: Full-screen modal

#### Visual Design

```
┌─────────────────────────────────────────────────┐
│                                                 │
│              [Page Content]                     │
│                                                 │
│                                                 │
│                                                 │
│                                          ┌────┐ │
│                                          │ 💬 │ │
│                                          └────┘ │
└─────────────────────────────────────────────────┘

When clicked (authenticated):
┌─────────────────────────────────────────────────┐
│              [Page Content]                     │
│                                                 │
├─────────────────────────────────────────────────┤
│  Instant Chat                        [−] [×]   │
├─────────────────────────────────────────────────┤
│                                                 │
│  [Chat Messages]                                │
│                                                 │
├─────────────────────────────────────────────────┤
│  [Type a message...]              [Send]        │
└─────────────────────────────────────────────────┘

When clicked (not authenticated):
┌─────────────────────────────────────────────────┐
│              [Page Content]                     │
│                                                 │
├─────────────────────────────────────────────────┤
│  🔐 Login Required                      [×]    │
├─────────────────────────────────────────────────┤
│                                                 │
│  Please log in to use the AI assistant.        │
│                                                 │
│  [Login]  [Sign Up]                            │
│                                                 │
└─────────────────────────────────────────────────┘
```

#### Component Structure

```
components/
├── instant-chat/
│   ├── FloatingChatButton.tsx    # FAB component
│   ├── InstantChatModal.tsx      # Modal wrapper
│   ├── InstantChatContent.tsx    # Chat UI inside modal
│   └── LoginPromptModal.tsx      # Auth prompt for logged-out users
```

#### FAB Styling

```css
.floating-chat-btn {
  position: fixed;
  bottom: 24px;
  right: 24px;
  width: 56px;
  height: 56px;
  border-radius: 50%;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  box-shadow: 0 4px 12px rgba(102, 126, 234, 0.4);
  cursor: pointer;
  transition: transform 0.2s, box-shadow 0.2s;
  z-index: 50;
}

.floating-chat-btn:hover {
  transform: scale(1.05);
  box-shadow: 0 6px 20px rgba(102, 126, 234, 0.5);
}

/* Pulse animation for attention */
.floating-chat-btn::after {
  content: '';
  position: absolute;
  inset: 0;
  border-radius: 50%;
  animation: pulse 2s infinite;
}

@keyframes pulse {
  0% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0.4); }
  70% { box-shadow: 0 0 0 10px rgba(102, 126, 234, 0); }
  100% { box-shadow: 0 0 0 0 rgba(102, 126, 234, 0); }
}
```

---

### US-4: Modern Landing Page

**As a** visitor
**I want** a modern, cohesive landing page
**So that** I understand the product and can access the book or chatbot easily

#### Acceptance Criteria

- [ ] Hero section with:
  - Compelling headline about Physical AI & Robotics
  - Subheadline describing the textbook + AI assistant
  - Two CTA buttons: "Read the Book" + "Try the Chatbot"
  - Gradient background or animated visual
- [ ] Navigation bar:
  - Logo + "Physical AI & Robotics" title
  - "Book" link
  - "Chat" link
  - "Login" / "Sign Up" buttons (or user avatar when logged in)
- [ ] Features section showcasing:
  - 13-Week Comprehensive Curriculum
  - AI-Powered Learning Assistant
  - Hands-on Code Examples & Diagrams
  - Capstone Project
- [ ] Book preview section (screenshot or animated preview)
- [ ] Chatbot demo section (screenshot or mini demo)
- [ ] Footer with links and copyright
- [ ] Fully responsive (mobile-first)
- [ ] Smooth scroll animations (fade-in on scroll)

#### Visual Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  NAVBAR: [Logo] Physical AI & Robotics   Book  Chat  Login     │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                         HERO SECTION                            │
│           "Master Physical AI & Humanoid Robotics"              │
│      "A comprehensive textbook with AI-powered assistant"       │
│                                                                 │
│              [Read the Book]    [Try Chatbot]                   │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                      FEATURES SECTION                           │
│   ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐       │
│   │ 13-Week  │  │ AI Chat  │  │ Code     │  │ Capstone │       │
│   │Curriculum│  │Assistant │  │ Examples │  │ Project  │       │
│   └──────────┘  └──────────┘  └──────────┘  └──────────┘       │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                    BOOK PREVIEW SECTION                         │
│            [Screenshot/mockup of the textbook]                  │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│                   CHATBOT DEMO SECTION                          │
│         [Screenshot/animation of chatbot interface]             │
│                                                                 │
├─────────────────────────────────────────────────────────────────┤
│                         FOOTER                                  │
│          Links  |  GitHub  |  © 2025 Physical AI                │
└─────────────────────────────────────────────────────────────────┘
```

#### Color Palette (Unified Theme)

```css
:root {
  /* Primary Gradient */
  --gradient-primary: linear-gradient(135deg, #667eea 0%, #764ba2 100%);

  /* Primary Colors */
  --color-primary: #667eea;
  --color-primary-dark: #5a67d8;
  --color-secondary: #764ba2;

  /* Accent */
  --color-accent: #25c2a0;
  --color-accent-dark: #1fa88c;

  /* Neutrals - Light Theme */
  --color-bg: #ffffff;
  --color-bg-secondary: #f8fafc;
  --color-bg-tertiary: #f1f5f9;
  --color-text-primary: #0f172a;
  --color-text-secondary: #475569;
  --color-text-muted: #94a3b8;
  --color-border: #e2e8f0;

  /* Neutrals - Dark Theme */
  --color-bg-dark: #0f172a;
  --color-bg-secondary-dark: #1e293b;
  --color-bg-tertiary-dark: #334155;
  --color-text-primary-dark: #f8fafc;
  --color-text-secondary-dark: #cbd5e1;
  --color-border-dark: #334155;
}
```

---

### US-5: Modern Chatbot UI with Sidebar History

**As a** user
**I want** a modern chatbot interface with conversation history sidebar
**So that** I can manage past conversations and have a great chat experience

#### Acceptance Criteria

- [ ] **Sidebar (Left Panel):**
  - "New Chat" button at top
  - List of past conversations
  - Each conversation shows:
    - Title (auto-generated from first message)
    - Date/time
    - Delete option (hover reveal)
  - Search/filter conversations
  - Collapsible sidebar (toggle button)
  - Mobile: Slide-out drawer

- [ ] **Chat Area (Main Panel):**
  - Header with:
    - Current conversation title
    - Theme toggle (light/dark)
    - Sidebar toggle (mobile)
  - Message list:
    - User messages: Right-aligned, primary gradient background
    - Bot messages: Left-aligned, subtle background
    - Avatar icons for user/bot
    - Timestamps on hover
    - Copy message button
    - Markdown rendering for bot responses
    - Code block syntax highlighting
  - Typing indicator animation
  - Scroll to bottom button (when scrolled up)

- [ ] **Input Area (Bottom):**
  - Multi-line text input (auto-expand)
  - Send button with icon
  - Character count (optional)
  - Keyboard shortcut hint (Enter to send, Shift+Enter for newline)

- [ ] **Loading & Error States:**
  - Skeleton loading for messages
  - Error message with retry button
  - Connection status indicator

#### Layout

```
┌─────────────────────────────────────────────────────────────────┐
│  NAVBAR: [Logo] Physical AI & Robotics   Book  Chat  [Avatar]  │
├────────────────┬────────────────────────────────────────────────┤
│   SIDEBAR      │              CHAT AREA                         │
│                │  ┌──────────────────────────────────────────┐  │
│  [+ New Chat]  │  │ Chat Title                    🌙  ≡     │  │
│                │  └──────────────────────────────────────────┘  │
│  Today         │                                                │
│  ├ Conv 1      │  ┌──────────────────────────────────────────┐  │
│  └ Conv 2      │  │                                          │  │
│                │  │  [User message bubble - right aligned]   │  │
│  Yesterday     │  │                                          │  │
│  ├ Conv 3      │  │  [Bot message bubble - left aligned]     │  │
│  └ Conv 4      │  │                                          │  │
│                │  │  [User message bubble]                   │  │
│  Last 7 days   │  │                                          │  │
│  └ Conv 5      │  │  [Bot typing indicator...]               │  │
│                │  │                                          │  │
│                │  └──────────────────────────────────────────┘  │
│  [Collapse ◀]  │  ┌──────────────────────────────────────────┐  │
│                │  │ [Type your message...]         [Send ➤]  │  │
│                │  └──────────────────────────────────────────┘  │
└────────────────┴────────────────────────────────────────────────┘
```

#### Component Structure

```
components/
├── chat/
│   ├── ChatLayout.tsx           # Main layout with sidebar + chat
│   ├── ChatSidebar.tsx          # Conversation history sidebar
│   ├── ChatHeader.tsx           # Title, theme toggle, controls
│   ├── ChatMessages.tsx         # Message list container
│   ├── ChatMessage.tsx          # Individual message bubble
│   ├── ChatInput.tsx            # Input area with send button
│   ├── ChatTypingIndicator.tsx  # Animated typing dots
│   ├── ConversationItem.tsx     # Sidebar conversation entry
│   └── NewChatButton.tsx        # New conversation button
```

#### Message Bubble Styles

```css
/* User message */
.message-user {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
  border-radius: 18px 18px 4px 18px;
  margin-left: auto;
  max-width: 70%;
}

/* Bot message */
.message-bot {
  background: var(--color-bg-secondary);
  color: var(--color-text-primary);
  border-radius: 18px 18px 18px 4px;
  margin-right: auto;
  max-width: 70%;
}

/* Dark theme bot message */
[data-theme='dark'] .message-bot {
  background: var(--color-bg-secondary-dark);
  color: var(--color-text-primary-dark);
}
```

---

### US-6: Unified Modern Theme

**As a** user
**I want** a consistent, modern theme across landing page, book, and chatbot
**So that** the entire platform feels cohesive and professional

#### Acceptance Criteria

- [ ] **Unified Color Scheme:**
  - Primary gradient: Purple (#667eea → #764ba2)
  - Accent: Teal (#25c2a0)
  - Consistent neutral tones

- [ ] **Typography:**
  - Modern sans-serif font (Inter or system font stack)
  - Consistent heading sizes
  - Readable body text (16px base)

- [ ] **Components:**
  - Consistent button styles (primary, secondary, ghost)
  - Consistent card styles with subtle shadows
  - Consistent form inputs
  - Consistent icons (use a single icon library - Lucide or Heroicons)

- [ ] **Dark/Light Theme:**
  - Theme toggle in navbar
  - Persist preference in localStorage
  - Smooth transition between themes
  - Apply to landing page, chat, and instant chat modal

- [ ] **Book Styling (Docusaurus):**
  - Update `/src/css/custom.css` in Docusaurus to match theme
  - Update primary colors to match gradient
  - Ensure dark mode matches Next.js dark theme

- [ ] **Animations:**
  - Subtle hover effects on buttons and cards
  - Smooth page transitions
  - Loading animations consistent throughout

#### Docusaurus Theme Update

Update `/src/css/custom.css`:

```css
:root {
  /* Match Next.js theme */
  --ifm-color-primary: #667eea;
  --ifm-color-primary-dark: #5a67d8;
  --ifm-color-primary-darker: #4c51bf;
  --ifm-color-primary-darkest: #434190;
  --ifm-color-primary-light: #7c87ec;
  --ifm-color-primary-lighter: #9098ee;
  --ifm-color-primary-lightest: #a8adf1;

  --ifm-font-family-base: 'Inter', system-ui, -apple-system, sans-serif;
  --ifm-code-font-size: 95%;
}

[data-theme='dark'] {
  --ifm-color-primary: #7c87ec;
  --ifm-color-primary-dark: #667eea;
  --ifm-color-primary-darker: #5a67d8;
  --ifm-color-primary-darkest: #4c51bf;
  --ifm-color-primary-light: #9098ee;
  --ifm-color-primary-lighter: #a8adf1;
  --ifm-color-primary-lightest: #c0c4f5;

  --ifm-background-color: #0f172a;
  --ifm-background-surface-color: #1e293b;
}

/* Hero gradient to match */
.hero {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
}
```

#### Tailwind Theme Extension

```typescript
// tailwind.config.ts
export default {
  theme: {
    extend: {
      colors: {
        primary: {
          DEFAULT: '#667eea',
          dark: '#5a67d8',
          light: '#7c87ec',
        },
        secondary: {
          DEFAULT: '#764ba2',
          dark: '#6b4190',
          light: '#8b5cb5',
        },
        accent: {
          DEFAULT: '#25c2a0',
          dark: '#1fa88c',
          light: '#3cd4b2',
        },
      },
      backgroundImage: {
        'gradient-primary': 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
      },
    },
  },
};
```

---

## Implementation Phases

### Phase 1: Infrastructure & Navigation (US-1, US-2)
1. Create `/book` route with iframe
2. Update navbar with Book and Chat links
3. Implement auth middleware for `/chat` route
4. Test iframe loading and responsiveness

### Phase 2: Floating Chat (US-3)
1. Create FloatingChatButton component
2. Create InstantChatModal component
3. Implement auth check for instant chat
4. Create LoginPromptModal for unauthenticated users
5. Add to root layout (exclude from `/chat` page)

### Phase 3: Landing Page (US-4)
1. Design and implement hero section
2. Create features section
3. Add book preview section
4. Add chatbot demo section
5. Implement footer
6. Add scroll animations

### Phase 4: Chatbot UI Enhancement (US-5)
1. Create new ChatLayout with sidebar
2. Implement ChatSidebar with history
3. Redesign ChatMessages and ChatMessage
4. Update ChatInput styling
5. Add typing indicator
6. Implement conversation management (new, delete, switch)

### Phase 5: Theme Unification (US-6)
1. Define Tailwind theme tokens
2. Update all components to use theme tokens
3. Implement theme toggle
4. Update Docusaurus custom.css
5. Test dark/light modes across all pages
6. Polish animations and transitions

---

## File Structure

```
frontend/
├── app/
│   ├── page.tsx                    # Landing page
│   ├── layout.tsx                  # Root layout with navbar
│   ├── book/
│   │   └── page.tsx                # Book iframe page
│   ├── chat/
│   │   └── page.tsx                # Full chatbot page
│   ├── login/
│   │   └── page.tsx                # Login page
│   └── register/
│       └── page.tsx                # Register page
├── components/
│   ├── layout/
│   │   ├── Navbar.tsx              # Main navigation
│   │   ├── Footer.tsx              # Footer component
│   │   └── ThemeToggle.tsx         # Dark/light toggle
│   ├── landing/
│   │   ├── Hero.tsx                # Hero section
│   │   ├── Features.tsx            # Features grid
│   │   ├── BookPreview.tsx         # Book screenshot/preview
│   │   └── ChatbotDemo.tsx         # Chatbot preview
│   ├── chat/
│   │   ├── ChatLayout.tsx          # Sidebar + chat layout
│   │   ├── ChatSidebar.tsx         # Conversation history
│   │   ├── ChatMessages.tsx        # Message list
│   │   ├── ChatMessage.tsx         # Message bubble
│   │   ├── ChatInput.tsx           # Input area
│   │   └── ChatTypingIndicator.tsx # Typing animation
│   ├── instant-chat/
│   │   ├── FloatingChatButton.tsx  # FAB
│   │   ├── InstantChatModal.tsx    # Modal wrapper
│   │   └── LoginPromptModal.tsx    # Auth prompt
│   └── ui/
│       ├── Button.tsx              # Styled button
│       ├── Card.tsx                # Card component
│       ├── Input.tsx               # Form input
│       └── Modal.tsx               # Modal base
├── lib/
│   ├── auth.ts                     # Auth utilities
│   ├── theme.ts                    # Theme utilities
│   └── constants.ts                # App constants
├── styles/
│   └── globals.css                 # Global styles + theme vars
└── middleware.ts                   # Auth middleware
```

---

## Auth Flow Summary

| Route | Auth Required | Behavior |
|-------|---------------|----------|
| `/` | No | Public landing page |
| `/book` | No | Public book iframe |
| `/chat` | Yes | Redirect to login if not authenticated |
| `/login` | No | Public login page |
| `/register` | No | Public register page |
| Floating Chat | Yes | Show login prompt modal if not authenticated |

---

## Success Criteria

- [ ] Book loads seamlessly in iframe without visible borders
- [ ] Navigation between Book and Chat is smooth
- [ ] Chat is protected behind authentication
- [ ] Floating chat button appears on all pages except `/chat`
- [ ] Instant chat shows login prompt for unauthenticated users
- [ ] Landing page is modern, responsive, and cohesive
- [ ] Chatbot has sidebar with conversation history
- [ ] Theme is consistent across landing, chat, and book
- [ ] Dark/light mode works across all components
- [ ] Mobile responsive at all breakpoints
- [ ] Vercel deployment succeeds
- [ ] GitHub Pages book remains functional

---

## Dependencies to Add

```bash
# UI Components
npm install lucide-react           # Icons
npm install framer-motion          # Animations
npm install @radix-ui/react-dialog # Modal primitives
npm install @radix-ui/react-dropdown-menu # Dropdown

# Optional enhancements
npm install react-intersection-observer # Scroll animations
npm install clsx                   # Conditional classes
npm install tailwind-merge         # Merge Tailwind classes
```

---

## Notes

- Iframe may have limitations with theme sync - accept that book uses its own theme toggle
- Test X-Frame-Options headers on GitHub Pages
- Consider adding a "Open in new tab" option for book if iframe causes issues
- Keep existing ChatKitPanel as base, enhance with new styling
- Preserve all existing authentication logic from Better Auth
