# Research: Book & Chatbot Integration

**Feature**: 004-book-chatbot-integration
**Date**: 2025-12-16
**Status**: Complete

## Research Tasks

### 1. GitHub Pages Iframe Embedding

**Question**: Will GitHub Pages allow iframe embedding from a different domain?

**Decision**: GitHub Pages allows iframe embedding by default

**Rationale**:
- GitHub Pages does not set restrictive X-Frame-Options headers by default
- The `X-Frame-Options` header is not set unless explicitly configured
- Modern browsers will allow embedding if no CSP frame-ancestors directive blocks it

**Alternatives Considered**:
- Migrate book to same domain: Rejected (adds complexity, loses GitHub Pages benefits)
- Use proxy API: Rejected (unnecessary overhead, CORS issues)

**Verification**:
```javascript
// Test by loading in iframe
const iframe = document.createElement('iframe');
iframe.src = 'https://nadeemsangrasi.github.io/humanoid-and-robotic-book/';
// If loads without error, embedding works
```

**Fallback**: Provide "Open in new tab" link if iframe fails to load

---

### 2. Next.js App Router Structure for New Routes

**Question**: How to structure `/book` and `/chat` routes in Next.js 15 App Router?

**Decision**: Use standard App Router file-based routing with route groups

**Rationale**:
- `/book` - Public route, no protection needed
- `/chat` - Protected route under existing middleware
- Leverage existing `(auth)` and `(protected)` route groups

**Implementation**:
```text
app/
├── book/
│   └── page.tsx        # Public book iframe
├── chat/
│   └── page.tsx        # Protected chat (inherits from middleware)
└── page.tsx            # Public landing page
```

**Alternatives Considered**:
- Route groups for book: Rejected (unnecessary, book is simple single page)
- Dynamic routes: Rejected (not needed for static pages)

---

### 3. Theme System Architecture

**Question**: How to implement dark/light theme across Next.js app?

**Decision**: CSS Custom Properties + Tailwind dark mode + localStorage persistence

**Rationale**:
- CSS Custom Properties enable instant theme switching without re-renders
- Tailwind's `dark:` modifier integrates well with existing setup
- localStorage provides persistence across sessions
- `prefers-color-scheme` media query for system preference detection

**Implementation**:
```typescript
// hooks/useTheme.ts
export function useTheme() {
  const [theme, setTheme] = useState<'light' | 'dark'>('light');

  useEffect(() => {
    const stored = localStorage.getItem('theme');
    const systemPreference = window.matchMedia('(prefers-color-scheme: dark)').matches;
    setTheme(stored || (systemPreference ? 'dark' : 'light'));
  }, []);

  const toggleTheme = () => {
    const newTheme = theme === 'light' ? 'dark' : 'light';
    setTheme(newTheme);
    localStorage.setItem('theme', newTheme);
    document.documentElement.classList.toggle('dark', newTheme === 'dark');
  };

  return { theme, toggleTheme };
}
```

**Alternatives Considered**:
- next-themes package: Rejected (adds dependency for simple use case)
- Context only: Rejected (CSS vars more performant for style changes)

---

### 4. Floating Action Button (FAB) Best Practices

**Question**: How to implement accessible, responsive FAB for instant chat?

**Decision**: Fixed positioning + Framer Motion animations + Radix Dialog

**Rationale**:
- Fixed position bottom-right (24px from edges) is standard FAB placement
- Framer Motion provides smooth slide-up animation
- Radix Dialog ensures accessibility (focus trap, escape key, screen readers)
- Hide on `/chat` page via usePathname() hook

**Implementation**:
```tsx
// components/instant-chat/FloatingChatButton.tsx
"use client";

import { useState } from "react";
import { usePathname } from "next/navigation";
import { MessageCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";

export function FloatingChatButton() {
  const pathname = usePathname();
  const [isOpen, setIsOpen] = useState(false);

  // Hide on chat page
  if (pathname === "/chat") return null;

  return (
    <>
      <motion.button
        className="fixed bottom-6 right-6 w-14 h-14 rounded-full bg-gradient-to-br from-primary to-secondary shadow-lg z-50"
        whileHover={{ scale: 1.05 }}
        whileTap={{ scale: 0.95 }}
        onClick={() => setIsOpen(true)}
      >
        <MessageCircle className="w-6 h-6 text-white mx-auto" />
      </motion.button>

      <AnimatePresence>
        {isOpen && <InstantChatModal onClose={() => setIsOpen(false)} />}
      </AnimatePresence>
    </>
  );
}
```

**Alternatives Considered**:
- Headless UI: Rejected (Radix has better animation support)
- Custom modal: Rejected (accessibility is hard to get right)

---

### 5. Chat Sidebar with Conversation History

**Question**: How to implement collapsible sidebar with conversation grouping?

**Decision**: Flexbox layout + date-based grouping + localStorage for collapse state

**Rationale**:
- Existing `ConversationList` component provides history data
- Group by date using date-fns (already installed)
- Sidebar width: 280px desktop, full-width drawer on mobile
- Collapsible via hamburger icon (preserved in localStorage)

**Implementation**:
```typescript
// Group conversations by date
function groupByDate(conversations: ChatSession[]) {
  const today = startOfToday();
  const yesterday = subDays(today, 1);
  const lastWeek = subDays(today, 7);

  return {
    today: conversations.filter(c => isToday(new Date(c.createdAt))),
    yesterday: conversations.filter(c => isSameDay(new Date(c.createdAt), yesterday)),
    lastWeek: conversations.filter(c =>
      new Date(c.createdAt) > lastWeek &&
      !isToday(new Date(c.createdAt)) &&
      !isSameDay(new Date(c.createdAt), yesterday)
    ),
    older: conversations.filter(c => new Date(c.createdAt) <= lastWeek),
  };
}
```

**Alternatives Considered**:
- Virtual scrolling: Defer (only needed if >100 conversations)
- Infinite scroll: Defer (existing pagination sufficient)

---

### 6. ChatKit Integration Strategy

**Question**: How to integrate existing ChatKitPanel with new UI components?

**Decision**: Wrap ChatKitPanel in new ChatLayout, extract styling, preserve functionality

**Rationale**:
- ChatKitPanel handles complex OpenAI ChatKit integration
- Don't rewrite - wrap and enhance
- New ChatLayout provides sidebar + header
- Style overrides via CSS custom properties

**Implementation**:
```tsx
// app/chat/page.tsx
export default function ChatPage() {
  return (
    <ChatLayout>
      <ChatKitPanel
        theme={theme}
        onWidgetAction={handleWidgetAction}
        onResponseEnd={handleResponseEnd}
        onThemeRequest={setTheme}
      />
    </ChatLayout>
  );
}
```

**Alternatives Considered**:
- Rewrite ChatKitPanel: Rejected (high effort, low value)
- Use ChatKit directly in new components: Rejected (loses existing customizations)

---

### 7. Landing Page Animation Strategy

**Question**: What animation approach for landing page sections?

**Decision**: Framer Motion with Intersection Observer for scroll-triggered animations

**Rationale**:
- Framer Motion's `useInView` hook simplifies scroll detection
- Staggered children for feature cards
- Subtle fade-up animations (opacity + translateY)
- Respect reduced-motion preference

**Implementation**:
```tsx
// components/landing/Features.tsx
import { motion, useInView } from "framer-motion";

const containerVariants = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: { staggerChildren: 0.1 }
  }
};

const itemVariants = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
};

export function Features() {
  const ref = useRef(null);
  const isInView = useInView(ref, { once: true, margin: "-100px" });

  return (
    <motion.section
      ref={ref}
      variants={containerVariants}
      initial="hidden"
      animate={isInView ? "visible" : "hidden"}
    >
      {features.map((feature) => (
        <motion.div key={feature.title} variants={itemVariants}>
          {/* Feature card */}
        </motion.div>
      ))}
    </motion.section>
  );
}
```

**Alternatives Considered**:
- CSS-only animations: Rejected (harder to control timing)
- react-intersection-observer: Rejected (Framer's built-in is sufficient)

---

### 8. Middleware Route Protection Updates

**Question**: How to update middleware for new route structure?

**Decision**: Add `/book` to public routes, keep `/chat` protected, make `/` public

**Rationale**:
- Current middleware redirects `/` to `/chat` (needs change for landing page)
- `/book` should be public (no auth required)
- `/chat` remains protected
- Instant chat modal handles its own auth check

**Implementation**:
```typescript
// middleware.ts changes
const protectedRoutes = ["/chat", "/history", "/profile", "/settings"];
const publicRoutes = ["/", "/book", "/login", "/register", "/api/auth"];
```

**Alternatives Considered**:
- Route groups for protection: Works but middleware is cleaner
- Client-side only protection: Rejected (security risk)

---

## Summary of Decisions

| Topic | Decision |
|-------|----------|
| Iframe embedding | GitHub Pages allows; fallback to new tab |
| Route structure | App Router file-based, standard patterns |
| Theme system | CSS vars + Tailwind dark mode + localStorage |
| FAB implementation | Framer Motion + Radix Dialog |
| Chat sidebar | Flexbox + date-fns grouping |
| ChatKit integration | Wrap existing panel in new layout |
| Landing animations | Framer Motion + useInView |
| Route protection | Update middleware for new public routes |

## Dependencies Confirmed

```json
{
  "existing": [
    "@openai/chatkit-react",
    "better-auth",
    "drizzle-orm",
    "date-fns"
  ],
  "to-add": [
    "lucide-react",
    "framer-motion",
    "@radix-ui/react-dialog",
    "clsx",
    "tailwind-merge"
  ]
}
```

## Research Status: COMPLETE

All technical questions resolved. Ready for Phase 1 design artifacts.
