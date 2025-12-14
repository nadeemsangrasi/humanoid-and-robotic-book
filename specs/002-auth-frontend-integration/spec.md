# Feature Specification: Authentication & Frontend-Backend Integration

**Feature Branch**: `002-auth-frontend-integration`
**Created**: 2025-12-14
**Status**: Draft
**Input**: Authentication (Better Auth + Neon + Drizzle) and ChatKit-FastAPI integration with chat history for the Physical AI & Humanoid Robotics textbook chatbot

---

## Overview

This specification defines the authentication system and frontend-backend integration for the Physical AI & Humanoid Robotics textbook chatbot. It covers:

1. **User Authentication**: Registration, login, session management, and logout functionality
2. **ChatKit Backend Adapter**: Customizing the ChatKit UI to communicate with the existing FastAPI RAG backend instead of OpenAI workflows
3. **Chat History Persistence**: Storing and retrieving user conversations across sessions
4. **Protected Routes**: Ensuring authenticated access to the chat interface

The goal is to transform the current ChatKit-based frontend from using OpenAI workflows to using the custom RAG-powered FastAPI backend while adding user authentication and conversation persistence.

---

## User Scenarios & Testing

### User Story 1 - New User Registration (Priority: P1)

A new visitor to the textbook chatbot wants to create an account so they can access the AI-powered Q&A feature and have their conversations saved for future reference.

**Why this priority**: Registration is the entry point for all users. Without account creation, users cannot access any authenticated features. This is the foundation for all other functionality.

**Independent Test**: Can be fully tested by completing the registration flow and verifying the user can subsequently log in. Delivers immediate value by enabling account access.

**Acceptance Scenarios**:

1. **Given** a visitor on the chatbot page without an account, **When** they click "Sign Up" and provide valid email, name, and password, **Then** an account is created and they are automatically logged in
2. **Given** a visitor attempting to register, **When** they provide an email already associated with an existing account, **Then** they see a clear error message indicating the email is already registered
3. **Given** a visitor attempting to register, **When** they provide a password that doesn't meet requirements, **Then** they see a clear message explaining the password requirements

---

### User Story 2 - Returning User Login (Priority: P1)

A returning user wants to log into their existing account to access the chatbot and view their previous conversations.

**Why this priority**: Login enables returning users to access their accounts. Without login, the registration feature has no follow-through value.

**Independent Test**: Can be fully tested by logging in with valid credentials and verifying access to the chat interface. Delivers immediate value by granting account access.

**Acceptance Scenarios**:

1. **Given** a registered user on the login page, **When** they enter correct email and password, **Then** they are logged in and redirected to the chat interface
2. **Given** a user attempting to log in, **When** they enter an incorrect password, **Then** they see a generic error message (not revealing which field is wrong for security)
3. **Given** a user attempting to log in, **When** they enter an email that doesn't exist, **Then** they see the same generic error message

---

### User Story 3 - Ask Questions via Authenticated Chat (Priority: P1)

An authenticated user wants to ask questions about humanoid robotics and physical AI topics using the chat interface, receiving answers powered by the textbook's RAG system.

**Why this priority**: This is the core value proposition of the entire application. Users come to ask questions and get intelligent answers from the textbook content.

**Independent Test**: Can be fully tested by sending a question through the chat interface and verifying a relevant response is returned from the backend. Delivers the primary value of the chatbot.

**Acceptance Scenarios**:

1. **Given** an authenticated user on the chat page, **When** they type a question and submit it, **Then** the message is sent to the FastAPI backend and a response appears in the chat
2. **Given** an authenticated user, **When** the backend returns a response with citations, **Then** the citations are displayed clearly in the chat interface
3. **Given** an authenticated user, **When** they submit a question, **Then** they see a loading indicator while waiting for the response

---

### User Story 4 - Session Persistence Across Refreshes (Priority: P1)

A logged-in user wants their session to persist when they refresh the page or close and reopen the browser tab, so they don't have to log in repeatedly.

**Why this priority**: Session persistence is essential for usability. Without it, users would need to log in on every page refresh, creating a frustrating experience.

**Independent Test**: Can be fully tested by logging in, refreshing the page, and verifying the user remains authenticated. Delivers immediate value by preserving authentication state.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they refresh the browser page, **Then** they remain logged in and can continue using the chat
2. **Given** a logged-in user, **When** they close the browser tab and reopen it within the session timeout period, **Then** they remain logged in
3. **Given** a logged-in user, **When** their session expires due to inactivity, **Then** they are prompted to log in again on their next action

---

### User Story 5 - View and Continue Previous Conversations (Priority: P2)

A returning user wants to view their previous chat conversations and continue where they left off, maintaining context from earlier discussions.

**Why this priority**: Conversation history adds significant value by allowing users to build on previous interactions, but the chatbot is still functional without it.

**Independent Test**: Can be fully tested by logging in as a user with previous conversations and verifying they can view and continue past chats. Delivers value by preserving conversation context.

**Acceptance Scenarios**:

1. **Given** a user with previous conversations, **When** they log in, **Then** they can see a list of their past conversation sessions
2. **Given** a user viewing their conversation history, **When** they select a previous conversation, **Then** the full conversation loads and they can continue chatting in that context
3. **Given** a new user with no conversation history, **When** they access the chat, **Then** they see an empty state with a prompt to start a new conversation

---

### User Story 6 - User Logout (Priority: P2)

A user wants to securely log out of their account, ensuring their session is invalidated and no one else can access their account on the same device.

**Why this priority**: Logout is important for security, especially on shared devices, but users can work around it by clearing cookies or waiting for session expiry.

**Independent Test**: Can be fully tested by logging out and verifying the user cannot access protected pages without logging in again. Delivers security value.

**Acceptance Scenarios**:

1. **Given** a logged-in user, **When** they click the logout button, **Then** their session is invalidated and they are redirected to the login page
2. **Given** a user who just logged out, **When** they try to access the chat interface directly via URL, **Then** they are redirected to the login page
3. **Given** a user who logged out, **When** they use the browser back button, **Then** they cannot access previously viewed protected content

---

### User Story 7 - Protected Routes Redirect (Priority: P2)

An unauthenticated visitor trying to access the chat interface directly should be redirected to login, with their intended destination preserved.

**Why this priority**: Protected routes are essential for security but are a supporting mechanism for the core authentication flow.

**Independent Test**: Can be fully tested by accessing the chat URL without authentication and verifying redirection to login, then logging in and being redirected to the original destination.

**Acceptance Scenarios**:

1. **Given** an unauthenticated visitor, **When** they navigate directly to the chat URL, **Then** they are redirected to the login page
2. **Given** a visitor redirected to login, **When** they successfully log in, **Then** they are redirected to the page they originally requested
3. **Given** an authenticated user with an expired session, **When** they try to send a chat message, **Then** they are prompted to log in again

---

### User Story 8 - OAuth Social Login (Priority: P3)

A user wants to sign up or log in using their existing Google or GitHub account for convenience, without creating a separate password.

**Why this priority**: OAuth is a convenience feature that improves user experience but is not essential for core functionality. Email/password authentication provides full access.

**Independent Test**: Can be fully tested by completing OAuth flow with a social provider and verifying account creation/login. Delivers convenience value.

**Acceptance Scenarios**:

1. **Given** a visitor on the login page, **When** they click "Sign in with Google/GitHub", **Then** they are redirected to the OAuth provider's authorization page
2. **Given** a new user completing OAuth, **When** they authorize the application, **Then** an account is created using their provider profile and they are logged in
3. **Given** an existing user who registered via email, **When** they try to log in via OAuth with the same email, **Then** their accounts are linked appropriately

---

### User Story 9 - Delete Chat History (Priority: P3)

A user wants to delete their chat history for privacy reasons, removing all stored conversations permanently.

**Why this priority**: This is a privacy feature that some users may want but is not essential for core chatbot functionality.

**Independent Test**: Can be fully tested by deleting chat history and verifying conversations are no longer accessible. Delivers privacy control value.

**Acceptance Scenarios**:

1. **Given** a user with conversation history, **When** they choose to delete all chat history, **Then** they see a confirmation prompt warning this action is irreversible
2. **Given** a user who confirms deletion, **When** the deletion completes, **Then** all their conversations are permanently removed and they see an empty conversation list
3. **Given** a user who deletes their history, **When** they start a new conversation, **Then** it is saved normally for future sessions

---

### Edge Cases

**Authentication Edge Cases**:
- User tries to register with an email address that already exists in the system
- User enters incorrect password multiple consecutive times (rate limiting applies)
- User's session expires while they are actively typing a chat message
- User attempts to access a protected route with an expired or invalid session token
- OAuth provider is temporarily unavailable during login attempt
- User tries to register with an invalid email format
- User clears browser cookies while logged in

**Chat Integration Edge Cases**:
- FastAPI backend is unavailable or returns a 5xx error during chat
- Backend returns an error response (4xx) for malformed requests
- Backend response takes longer than expected (timeout handling)
- User sends a new message while a previous response is still streaming/loading
- Backend returns a response without any citations
- Network connection drops mid-response

**Chat History Edge Cases**:
- User has no previous chat history (first-time user)
- Database is temporarily unavailable when loading chat history
- User deletes their account (cascade deletion of all history)
- User has extensive chat history causing slow load times
- Two browser tabs with the same session sending messages simultaneously
- User tries to continue a conversation that was deleted in another session

---

## Requirements

### Functional Requirements - Authentication

- **FR-001**: System MUST allow new users to register with email address, display name, and password
- **FR-002**: System MUST validate that email addresses are unique across all accounts
- **FR-003**: System MUST validate email format before accepting registration
- **FR-004**: System MUST enforce password requirements: minimum 8 characters, at least one uppercase letter, one lowercase letter, and one number
- **FR-005**: System MUST securely hash passwords before storage using bcrypt algorithm with appropriate cost factor
- **FR-006**: System MUST allow registered users to log in with email and password
- **FR-007**: System MUST issue a JWT token upon successful login stored in an httpOnly cookie, with a mechanism to extract token for Authorization header in API calls
- **FR-008**: System MUST allow users to log out, invalidating their current session
- **FR-009**: System MUST automatically expire sessions after 7 days of inactivity
- **FR-010**: System MUST implement rate limiting on authentication endpoints to prevent brute force attacks (maximum 5 failed attempts per 15 minutes)
- **FR-011**: System MUST protect against CSRF attacks on all authentication endpoints

### Functional Requirements - Database

- **FR-012**: System MUST persist user account information including email, display name, and hashed password
- **FR-013**: System MUST validate JWT tokens via middleware on the backend without database lookup (stateless validation)
- **FR-014**: System MUST support database migrations for schema changes
- **FR-015**: System MUST use connection pooling for efficient database access
- **FR-016**: System MUST cascade delete all user data when an account is deleted

### Functional Requirements - ChatKit Customization

- **FR-017**: System MUST provide an adapter layer that transforms chat messages from the frontend format to the FastAPI backend format
- **FR-018**: System MUST transform backend responses to the format expected by the ChatKit UI components
- **FR-019**: System MUST display source citations returned by the backend in a clear, readable format within chat messages
- **FR-020**: System MUST include JWT token in all requests to the backend using `Authorization: Bearer <jwt>` header format
- **FR-021**: System MUST display appropriate loading indicators while waiting for backend responses
- **FR-022**: System MUST handle backend errors gracefully, displaying user-friendly error messages
- **FR-023**: System MUST allow users to retry failed messages without re-typing

### Functional Requirements - Chat History

- **FR-024**: System MUST save all chat messages to persistent storage associated with the user's account
- **FR-025**: System MUST load the user's conversation history upon login
- **FR-026**: System MUST allow users to create new conversation sessions
- **FR-027**: System MUST allow users to continue previous conversation sessions
- **FR-028**: System MUST allow users to delete individual conversations
- **FR-029**: System MUST allow users to delete all their chat history

### Functional Requirements - Protected Routes

- **FR-030**: System MUST restrict access to the chat interface to authenticated users only
- **FR-031**: System MUST redirect unauthenticated users to the login page when accessing protected routes
- **FR-032**: System MUST preserve the user's intended destination URL and redirect them there after successful login
- **FR-033**: System MUST handle expired sessions gracefully, prompting users to re-authenticate

### Functional Requirements - OAuth (P3)

- **FR-034**: System SHOULD support OAuth authentication via Google
- **FR-035**: System SHOULD support OAuth authentication via GitHub
- **FR-036**: System SHOULD link OAuth accounts to existing email-based accounts when email addresses match

### Key Entities

- **User**: An authenticated individual with an account in the system. Contains profile information (email, display name), authentication credentials, and relationships to sessions and conversations.

- **Session/JWT Token**: A stateless JWT token representing an authenticated connection. Contains user ID, expiry timestamp, and signature. Validated cryptographically via backend middleware without database lookup.

- **Account**: A connection between a user and an external authentication provider (for OAuth). Stores provider-specific identifiers and tokens.

- **ChatSession**: A conversation thread representing a series of exchanges between a user and the chatbot. Groups related messages together and maintains conversation context.

- **ChatMessage**: An individual message within a conversation, either from the user or the assistant. Contains the message content, timestamp, and role indicator.

- **Citation**: A source reference returned by the RAG backend, indicating which parts of the textbook were used to generate a response. Contains source title, URL, and relevant excerpt.

- **APIAdapter**: The interface layer responsible for transforming requests and responses between the frontend ChatKit format and the FastAPI backend format.

---

## Success Criteria

### Measurable Outcomes - Authentication

- **SC-001**: Users can complete registration (email, name, password entry, and account creation) in under 30 seconds
- **SC-002**: Users can complete login (email, password entry, and session creation) in under 15 seconds
- **SC-003**: 100% of protected routes correctly redirect unauthenticated users to the login page
- **SC-004**: Sessions persist correctly across page refreshes with zero unexpected logouts during active use
- **SC-005**: Zero credentials, tokens, or sensitive authentication data exposed in browser console, network logs, or client-side code
- **SC-006**: Failed login attempts are rate-limited after 5 consecutive failures within 15 minutes

### Measurable Outcomes - Chat Integration

- **SC-007**: Chat messages reach the FastAPI backend and return responses with less than 500ms additional latency compared to direct API calls
- **SC-008**: 100% of RAG citations returned by the backend display correctly in the chat UI with clickable links where applicable
- **SC-009**: Chat functionality works seamlessly after the ChatKit-to-FastAPI adapter integration, with no regression in user experience
- **SC-010**: Backend errors are handled gracefully with user-friendly messages in 100% of error scenarios

### Measurable Outcomes - Chat History

- **SC-011**: Users see their previous conversations within 2 seconds of logging in (for up to 100 conversations)
- **SC-012**: Chat history persists correctly across browser sessions with 100% data integrity
- **SC-013**: Users can create, continue, and delete conversations with immediate UI feedback

### Measurable Outcomes - Development

- **SC-014**: Local development environment setup completes in under 10 minutes with documented steps
- **SC-015**: All Context7 MCP documentation for required technologies is fetched and referenced before implementation begins
- **SC-016**: Zero TypeScript compilation errors in the final implementation
- **SC-017**: All functional requirements have corresponding test coverage

---

## Constraints

### Technical Constraints

- **C-001**: Authentication MUST use Better Auth library - no custom authentication implementations or alternative libraries
- **C-002**: Database MUST be PostgreSQL hosted on Neon (free tier) - no alternative database providers
- **C-003**: ORM MUST be Drizzle ORM - no Prisma, TypeORM, Sequelize, or raw SQL queries
- **C-004**: Frontend MUST use existing OpenAI ChatKit React components - no building chat UI from scratch
- **C-005**: All backend API calls MUST include user authentication context (user ID or session token)
- **C-006**: All secrets, credentials, and service URLs MUST be stored in environment variables - never hardcoded in source code. Backend URL configured via `NEXT_PUBLIC_BACKEND_URL`
- **C-007**: All API calls in production MUST use HTTPS

### Documentation Constraint (Critical)

- **C-008**: Before implementing ANY technology (Better Auth, Drizzle, Neon, ChatKit customization), developers MUST use Context7 MCP server to retrieve up-to-date official documentation. NO implementation without MCP-verified documentation first.

### Agent Assignment Constraints

- **C-009**: ChatKit UI customization tasks MUST use `UI-and-ChatKit-customization-agent`
- **C-010**: Authentication configuration tasks MUST use `Auth-Integration-Agent`
- **C-011**: Database schema and Drizzle setup MUST reference Context7 documentation for Drizzle ORM
- **C-012**: Better Auth setup MUST reference Context7 documentation for Better Auth

---

## Dependencies

### External Dependencies

- **FastAPI Backend**: Already deployed RAG chatbot API on Hugging Face Spaces with POST /api/v1/chat and GET /health endpoints
- **Neon PostgreSQL**: Free tier account required for database hosting
- **Better Auth**: Authentication library for Next.js
- **Drizzle ORM**: TypeScript ORM for database operations
- **OpenAI ChatKit React**: Existing UI components in frontend/

### Internal Dependencies

- **Existing Frontend**: Next.js application with ChatKit already integrated (frontend/ folder)
- **Existing Backend**: FastAPI service with RAG capabilities already operational
- **Textbook Content**: Docusaurus site at https://nadeemsangrasi.github.io/humanoid-and-robotic-book/ already indexed in vector database

### Tool Dependencies

- **Context7 MCP Server**: Required for fetching up-to-date documentation before implementation

---

## Assumptions

- FastAPI backend is stable, accessible, and will remain deployed on Hugging Face Spaces throughout development
- Neon PostgreSQL free tier provides sufficient capacity for expected user base (< 1000 users initially)
- User base will not exceed Neon free tier limits during initial deployment
- Better Auth supports all required authentication features (email/password, sessions, OAuth)
- ChatKit React components can be customized to work with non-OpenAI backends
- Network latency to Hugging Face Spaces backend is acceptable for chat use case
- Users have modern browsers with JavaScript enabled
- Single concurrent session per user is acceptable (no multi-device sync required for MVP)

---

## Clarifications

### Session 2025-12-14

- Q: How should user sessions be stored (database vs JWT vs hybrid)? → A: JWT tokens - stateless tokens stored client-side, validated cryptographically via middleware on backend
- Q: What format should be used for authentication headers to backend? → A: Bearer token - `Authorization: Bearer <jwt>` header (standard OAuth2/JWT pattern)
- Q: How should the frontend discover/configure the backend URL? → A: Environment variable - `NEXT_PUBLIC_BACKEND_URL` configurable per environment
- Q: Where should JWT tokens be stored client-side? → A: httpOnly cookie - most secure, immune to XSS attacks, with cookie-to-header extraction for API calls
- Q: Which password hashing algorithm should be used? → A: bcrypt - industry standard, built-in salting, widely supported by Better Auth

---

## Out of Scope

- Multi-factor authentication (MFA)
- Admin dashboard for user management
- User roles and permissions beyond authenticated/unauthenticated
- Real-time collaboration features (multiple users in same conversation)
- Mobile application authentication
- Payment or subscription features
- Email verification on registration (can be added later)
- Password reset functionality (can be added later)
- Account settings page (profile editing, email change)
- Conversation sharing or export features
- Analytics or usage tracking dashboard
- Offline mode or progressive web app features
- Multi-language support
- Accessibility compliance beyond basic requirements

---

## Implementation Phases (for Plan Generation)

### Phase 1: Database & Auth Foundation (Blocking)

1. Set up Neon PostgreSQL database and obtain connection credentials
2. Create Drizzle ORM schema for users, sessions, and accounts
3. Configure Drizzle migrations
4. Set up Better Auth with email/password authentication

### Phase 2: Frontend Auth Integration

1. Create auth context provider for React components
2. Build login and registration pages/forms
3. Add protected route wrapper component
4. Integrate auth state with existing UI layout

### Phase 3: ChatKit Backend Adapter

1. Create API adapter module for FastAPI backend communication
2. Transform request format (ChatKit to FastAPI)
3. Transform response format (FastAPI to ChatKit with citations)
4. Add authentication headers to backend requests

### Phase 4: Chat History

1. Add ChatSession and ChatMessage schemas to Drizzle
2. Implement save and load chat history functionality
3. Add conversation list UI component
4. Implement new chat and continue chat functionality

### Phase 5: Testing & Polish

1. Integration tests for authentication flow
2. E2E tests for chat functionality
3. Error handling refinement
4. Documentation and developer setup guide

---

## Agent and Skill Assignments for Implementation

| Task Area                 | Agent                              | Skill                        |
| ------------------------- | ---------------------------------- | ---------------------------- |
| Drizzle schema definition | backend-architect-and-sdk-agent    | drizzle-schema-generation    |
| Better Auth configuration | Auth-Integration-Agent             | better-auth-configuration    |
| Frontend auth components  | Auth-Integration-Agent             | frontend-auth-integration    |
| ChatKit customization     | UI-and-ChatKit-customization-agent | chatkit-backend-adapter      |
| UI theming and styling    | UI-and-ChatKit-customization-agent | ui-customization             |
| Selection-based Q&A       | UI-and-ChatKit-customization-agent | selection-qa                 |

---

## Context7 MCP Documentation Requirements

Before implementing any task, fetch documentation for:

1. **Better Auth**: `resolve-library-id` with "better-auth"
2. **Drizzle ORM**: `resolve-library-id` with "drizzle-orm"
3. **Neon PostgreSQL**: `resolve-library-id` with "neon postgres"
4. **Next.js App Router**: `resolve-library-id` with "nextjs"

This is MANDATORY per project constitution. No implementation without MCP-verified documentation.
