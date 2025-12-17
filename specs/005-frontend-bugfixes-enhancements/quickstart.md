# Quickstart: Frontend Bug Fixes & Enhancements

**Feature**: 005-frontend-bugfixes-enhancements
**Date**: 2025-12-17

## Prerequisites

- Node.js 18+ installed
- Frontend dependencies installed (`npm install` in `frontend/`)
- Development server running (`npm run dev`)
- Access to Docusaurus book source (for theme parameter handling)

## Quick Verification Steps

### 1. Check Duplicate Headers Bug
```bash
# Start dev server
cd frontend && npm run dev

# Open browser and navigate to:
# - /chat - Should show only ONE header (navbar)
# - /login - Should NOT show navbar (clean auth UI)
# - /register - Should NOT show navbar
```

### 2. Check Chat Component Overlap
```bash
# Navigate to /chat
# Verify chat content does not overlap navbar
# Navbar should remain visible and accessible
```

### 3. Check Modal Blur Bug
```bash
# Navigate to any page (e.g., /, /book)
# Click floating chat button to open instant chat
# Minimize the modal
# Un-minimize the modal
# Verify: background is NOT blurred after un-minimize
```

### 4. Check Hover States
```bash
# Inspect interactive elements:
# - Navbar links
# - Buttons
# - Chat history items
# Verify: visible hover feedback on all
```

### 5. Check Theme Consistency
```bash
# Toggle theme using theme button
# Verify ALL components update:
# - Navbar
# - Landing page
# - Chat interface
# - Instant chat modal
```

### 6. Check Theme Sync with Book
```bash
# Navigate to /book
# Toggle theme
# Verify: iframe URL includes ?theme=dark or ?theme=light
# Note: Docusaurus book must implement parameter reading
```

### 7. Check Instant Chat History
```bash
# Open instant chat modal
# Send a message and receive response
# Navigate to /chat
# Verify: conversation appears in history sidebar
```

## Development Workflow

### Bug Fix Pattern
```typescript
// 1. Identify the component with the bug
// 2. Check related files (layout, styles, hooks)
// 3. Make minimal change to fix
// 4. Test in dev server
// 5. Verify no regressions
```

### File Locations

| Bug/Enhancement | Primary File |
|-----------------|--------------|
| Duplicate headers | `app/layout.tsx`, `app/(auth)/layout.tsx` |
| Chat overlap | `app/(protected)/chat/page.tsx` |
| Modal blur | `components/instant-chat/InstantChatModal.tsx` |
| Hover states | `app/globals.css`, individual components |
| Theme consistency | `hooks/useTheme.ts`, `app/globals.css` |
| Theme sync | `app/book/page.tsx` |
| History loading | `app/(protected)/chat/page.tsx` |
| Instant chat history | `components/instant-chat/InstantChatModal.tsx` |

### Testing Commands
```bash
# Run type check
npm run build

# Run linter
npm run lint

# Run tests
npm run test
```

## Documentation Updates

### Files to Update
```bash
# RAG chatbot specs - Update auth documentation
specs/003-rag-chatbot-backend/spec.md

# Parent README - Comprehensive update
README.md

# Frontend guide
frontend/GUIDE.md
```

### Documentation Checklist
- [ ] Update auth approach (JWT → email header)
- [ ] Add architecture overview
- [ ] Document frontend setup
- [ ] Document backend setup
- [ ] Document deployment process

## Quick Reference

### Z-Index Hierarchy
```css
/* Established order */
navbar: z-40
content: auto
modal-backdrop: z-50
modal-content: z-51
toast: z-60
```

### Theme CSS Variables
```css
/* Key variables to use */
var(--background)
var(--foreground)
var(--primary)
var(--hover-bg)
var(--border)
```

### Conditional Navbar Rendering
```typescript
// Pattern for hiding navbar on specific routes
const hideNavbarRoutes = ['/login', '/register'];
const pathname = usePathname();
const showNavbar = !hideNavbarRoutes.some(route => pathname?.startsWith(route));
```

## Troubleshooting

### Theme Not Persisting
- Check localStorage: `localStorage.getItem('theme')`
- Verify `useTheme` hook is being used
- Check for hydration mismatch warnings

### Blur Stuck
- Check AnimatePresence exit animation
- Verify overlay unmount timing
- Check isMinimized state transitions

### History Not Saving
- Check network tab for API calls
- Verify session creation response
- Check console for errors
