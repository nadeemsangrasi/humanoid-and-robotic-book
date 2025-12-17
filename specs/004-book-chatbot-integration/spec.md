# Feature Specification: Book & Chatbot Integration

**Feature Branch**: `004-book-chatbot-integration`
**Created**: 2025-12-16
**Status**: Draft
**Input**: User description: "Integrate existing static Docusaurus book (deployed on GitHub Pages) with Next.js chatbot frontend using iframe strategy to create unified educational platform"

## Overview

This feature integrates the existing Physical AI & Humanoid Robotics textbook (static Docusaurus site on GitHub Pages) with the Next.js chatbot frontend to create a unified educational platform. Users can seamlessly read the textbook and interact with an AI assistant for questions and guidance.

### Current Deployments
- **Book (Docusaurus)**: https://nadeemsangrasi.github.io/humanoid-and-robotic-book/
- **Chatbot (Next.js)**: https://rag-chatbot-teal-two.vercel.app

### Architecture Decision
- Book remains static on GitHub Pages (no migration needed)
- Next.js frontend acts as the unified shell
- Iframe loads book content seamlessly
- Single deployment for chatbot + landing page on Vercel

---

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Seamless Book Access (Priority: P1)

As a reader, I want to click "Book" in the navbar and see the textbook loaded seamlessly so that the book feels like a native part of the application.

**Why this priority**: Core functionality - without book access, the platform has no educational content to offer. This is the foundation of the unified experience.

**Independent Test**: Can be fully tested by navigating to /book route and verifying the Docusaurus site loads within an iframe without visible borders, with responsive sizing on all devices.

**Acceptance Scenarios**:

1. **Given** a user on any page of the platform, **When** they click "Book" in the navbar, **Then** they are navigated to `/book` route showing the full textbook in an iframe
2. **Given** a user on the `/book` page, **When** the iframe is loading, **Then** they see a loading spinner until content is ready
3. **Given** a user viewing the book, **When** they click internal book links, **Then** navigation works normally within the iframe
4. **Given** a user on any device (mobile/tablet/desktop), **When** viewing the book page, **Then** the iframe scales responsively to fill available viewport
5. **Given** an unauthenticated user, **When** they access `/book`, **Then** they can view the book without needing to log in

---

### User Story 2 - Navigation Between Book and Chat (Priority: P1)

As a user, I want to easily switch between the Book and Chat sections so that I can read content and ask questions seamlessly.

**Why this priority**: Critical for user workflow - users need to move between learning (book) and asking questions (chat) fluidly.

**Independent Test**: Can be tested by verifying navbar contains both "Book" and "Chat" links, and navigation between them works with appropriate auth protection for chat.

**Acceptance Scenarios**:

1. **Given** a user on the landing page, **When** they view the navbar, **Then** they see "Book", "Chat", and authentication options clearly visible
2. **Given** an authenticated user, **When** they click "Chat", **Then** they are taken to `/chat` with the full chatbot interface
3. **Given** an unauthenticated user, **When** they click "Chat", **Then** they are redirected to login with a callback URL to return to chat after authentication
4. **Given** a user on mobile, **When** they open the menu, **Then** they see a hamburger menu with Book and Chat options
5. **Given** a user navigating between sections, **When** they switch from Book to Chat or vice versa, **Then** the active nav item is visually highlighted

---

### User Story 3 - Modern Landing Page (Priority: P2)

As a visitor, I want a modern, cohesive landing page so that I understand the product and can access the book or chatbot easily.

**Why this priority**: First impression for new users - establishes credibility and guides users to primary actions.

**Independent Test**: Can be tested by visiting the root URL and verifying all sections render correctly with CTAs functioning properly.

**Acceptance Scenarios**:

1. **Given** a visitor lands on the homepage, **When** they view the hero section, **Then** they see a compelling headline, subheadline about the textbook + AI assistant, and two CTA buttons ("Read the Book" and "Try the Chatbot")
2. **Given** a visitor scrolling the landing page, **When** they reach the features section, **Then** they see 4 feature cards: 13-Week Curriculum, AI Chat Assistant, Code Examples, and Capstone Project
3. **Given** a visitor viewing the landing page, **When** they scroll to preview sections, **Then** they see book preview and chatbot demo sections
4. **Given** a visitor on any device, **When** viewing the landing page, **Then** all sections are fully responsive and readable
5. **Given** a visitor scrolling, **When** sections come into view, **Then** smooth fade-in animations enhance the experience

---

### User Story 4 - Instant Chat Floating Button (Priority: P2)

As a reader, I want a floating chat button at the bottom of the screen so that I can quickly ask questions without leaving the current page.

**Why this priority**: Enhances user experience by providing quick access to help while reading - reduces friction for asking questions.

**Independent Test**: Can be tested by verifying FAB appears on all pages except /chat, opens modal on click, and shows login prompt for unauthenticated users.

**Acceptance Scenarios**:

1. **Given** a user on any page except `/chat`, **When** they look at the bottom-right corner, **Then** they see a floating action button with chat icon
2. **Given** an authenticated user, **When** they click the FAB, **Then** a chat modal slides up from the bottom with full chat functionality
3. **Given** an unauthenticated user, **When** they click the FAB, **Then** a login prompt modal appears with "Login" and "Sign Up" buttons
4. **Given** a user with the chat modal open, **When** they click close or minimize, **Then** the modal collapses back to the FAB
5. **Given** a user on the `/chat` page, **When** they view the screen, **Then** the FAB is hidden (full chat is already visible)
6. **Given** a user on mobile, **When** they click the FAB, **Then** the chat opens as a full-screen modal

---

### User Story 5 - Modern Chatbot UI with Sidebar (Priority: P2)

As a user, I want a modern chatbot interface with conversation history sidebar so that I can manage past conversations and have a great chat experience.

**Why this priority**: Improves chat usability - users can reference previous conversations and maintain context across sessions.

**Independent Test**: Can be tested by logging in, starting conversations, and verifying sidebar shows history with new chat, delete, and search functionality.

**Acceptance Scenarios**:

1. **Given** an authenticated user on `/chat`, **When** they view the interface, **Then** they see a collapsible sidebar on the left with conversation history and main chat area on the right
2. **Given** a user viewing the sidebar, **When** they click "New Chat", **Then** a fresh conversation starts in the main chat area
3. **Given** a user with multiple conversations, **When** they view the sidebar, **Then** conversations are grouped by date (Today, Yesterday, Last 7 days) with titles auto-generated from first message
4. **Given** a user hovering over a conversation item, **When** they click delete, **Then** the conversation is removed from history
5. **Given** a user sending a message, **When** the bot is processing, **Then** they see an animated typing indicator
6. **Given** a user viewing messages, **When** they see bot responses, **Then** messages render with markdown formatting and code syntax highlighting

---

### User Story 6 - Unified Modern Theme (Priority: P3)

As a user, I want a consistent, modern theme across landing page, book, and chatbot so that the entire platform feels cohesive and professional.

**Why this priority**: Polish and professionalism - creates trust and pleasant user experience but not critical for core functionality.

**Independent Test**: Can be tested by verifying color scheme, typography, and component styles are consistent across all pages, with working dark/light theme toggle.

**Acceptance Scenarios**:

1. **Given** a user viewing any page, **When** they observe the UI, **Then** they see consistent purple gradient (#667eea to #764ba2) as primary color and teal (#25c2a0) as accent
2. **Given** a user clicking the theme toggle, **When** the theme changes, **Then** the entire interface smoothly transitions between light and dark modes
3. **Given** a user with a theme preference saved, **When** they return to the site, **Then** their preferred theme is automatically applied
4. **Given** a user viewing the Docusaurus book, **When** they toggle themes, **Then** the book's theme toggle independently controls its appearance (note: book uses its own theme system)
5. **Given** a user on any page, **When** they interact with buttons, cards, and inputs, **Then** all components follow the same design language with consistent styling

---

### Edge Cases

- **Iframe Load Failure**: If the GitHub Pages book fails to load, show a fallback message with a direct link to open the book in a new tab
- **X-Frame-Options**: GitHub Pages typically allows embedding; if blocked, provide "Open in new tab" fallback
- **Authentication Token Expiry**: If user's session expires while using instant chat, gracefully prompt re-login
- **Conversation History Limit**: Handle users with many conversations by implementing pagination or virtual scrolling
- **Offline Behavior**: Show appropriate offline indicators if network connection is lost
- **Theme Sync Limitation**: Accept that the embedded Docusaurus book manages its own theme independently

---

## Requirements *(mandatory)*

### Functional Requirements

**Navigation & Routing**
- **FR-001**: System MUST provide a navbar with "Book", "Chat", and authentication options visible on all pages
- **FR-002**: System MUST render the `/book` route with a full-viewport iframe containing the Docusaurus book
- **FR-003**: System MUST protect the `/chat` route, redirecting unauthenticated users to login with callback URL
- **FR-004**: System MUST display a mobile hamburger menu with all navigation options on small screens

**Landing Page**
- **FR-005**: System MUST display a hero section with headline, subheadline, and two CTA buttons on the landing page
- **FR-006**: System MUST display a features section with 4 feature cards (Curriculum, AI Assistant, Code Examples, Capstone)
- **FR-007**: System MUST include book preview and chatbot demo sections on the landing page
- **FR-008**: System MUST include a footer with links and copyright information

**Book Integration**
- **FR-009**: System MUST load the Docusaurus book URL in an iframe without visible borders
- **FR-010**: System MUST display a loading indicator while the iframe content loads
- **FR-011**: System MUST handle iframe load errors with a fallback message and direct link
- **FR-012**: System MUST allow the book to be accessible without authentication (public)

**Instant Chat (Floating Button)**
- **FR-013**: System MUST display a floating action button (FAB) on all pages except `/chat`
- **FR-014**: System MUST open a chat modal when authenticated users click the FAB
- **FR-015**: System MUST show a login prompt modal when unauthenticated users click the FAB
- **FR-016**: System MUST preserve chat context when users close and reopen the instant chat modal
- **FR-017**: System MUST render instant chat as full-screen modal on mobile devices

**Chatbot UI**
- **FR-018**: System MUST provide a collapsible sidebar showing conversation history
- **FR-019**: System MUST allow users to create new conversations via "New Chat" button
- **FR-020**: System MUST auto-generate conversation titles from the first user message
- **FR-021**: System MUST group conversations by date (Today, Yesterday, Last 7 days)
- **FR-022**: System MUST allow users to delete conversations from history
- **FR-023**: System MUST display user messages right-aligned with gradient background
- **FR-024**: System MUST display bot messages left-aligned with subtle background
- **FR-025**: System MUST render bot responses with markdown formatting and code syntax highlighting
- **FR-026**: System MUST display an animated typing indicator while bot is processing
- **FR-027**: System MUST provide a multi-line input with send button and keyboard shortcuts

**Theme & Styling**
- **FR-028**: System MUST implement a unified color scheme with purple gradient primary and teal accent
- **FR-029**: System MUST provide a theme toggle for dark/light mode in the navbar
- **FR-030**: System MUST persist theme preference in browser storage
- **FR-031**: System MUST apply smooth transitions when switching themes
- **FR-032**: System MUST use consistent typography (Inter or system font stack) across all pages

### Key Entities

- **Conversation**: Represents a chat session with unique ID, title (auto-generated), creation date, and list of messages
- **Message**: A single exchange containing sender type (user/bot), content, timestamp, and optional metadata (citations)
- **User Session**: Authenticated user's session state including preferences (theme) and active conversation reference
- **Navigation State**: Current active route and sidebar collapse state

---

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can access and read the textbook within 3 seconds of clicking "Book" (time to interactive)
- **SC-002**: 95% of users can successfully navigate between Book and Chat without confusion (task completion rate)
- **SC-003**: Landing page loads completely within 2 seconds on standard broadband connection
- **SC-004**: Instant chat modal opens within 500ms of FAB click
- **SC-005**: Users can find and resume previous conversations within 10 seconds using the sidebar
- **SC-006**: Theme toggle applies changes across all visible elements within 300ms
- **SC-007**: Platform maintains visual consistency score of 90%+ when audited against design system
- **SC-008**: Mobile users can complete all primary tasks (view book, use chat) without horizontal scrolling
- **SC-009**: Vercel deployment succeeds without errors
- **SC-010**: GitHub Pages book remains functional and accessible after integration

---

## Assumptions

- GitHub Pages allows iframe embedding (X-Frame-Options permits it)
- Existing Better Auth integration from previous feature (002-auth-frontend-integration) is functional
- Existing ChatKitPanel component can be reused and enhanced
- Users have modern browsers supporting CSS Grid, Flexbox, and CSS custom properties
- The Docusaurus book manages its own theme independently (no cross-origin theme sync required)

---

## Out of Scope

- Migrating the Docusaurus book to a different hosting platform
- Cross-origin theme synchronization between Next.js app and embedded book
- Real-time collaborative features
- Voice input for the chatbot
- Offline-first functionality with service workers
- Analytics and tracking implementation

---

## Dependencies

- **002-auth-frontend-integration**: Better Auth setup with login/register functionality
- **003-rag-chatbot-backend**: FastAPI backend with RAG chatbot functionality
- **External**: GitHub Pages hosting for Docusaurus book
- **External**: Vercel deployment for Next.js frontend
