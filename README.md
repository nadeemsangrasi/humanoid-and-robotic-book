# Physical AI & Humanoid Robotics Textbook

**A comprehensive educational resource on Physical AI and Humanoid Robotics built with Docusaurus, featuring an AI-powered RAG chatbot for interactive learning**

---

## Table of Contents

- [Overview](#overview)
- [Course Structure](#course-structure)
- [Features](#features)
- [System Architecture](#system-architecture)
- [RAG Chatbot Backend](#rag-chatbot-backend)
- [Frontend Application](#frontend-application)
- [Prerequisites](#prerequisites)
- [Getting Started](#getting-started)
- [Project Structure](#project-structure)
- [Deployment](#deployment)
- [Contributing](#contributing)

---

## Overview

This repository contains a complete textbook on **Physical AI & Humanoid Robotics**, structured as a Docusaurus-based website with an integrated **RAG-powered chatbot** for interactive Q&A. The textbook is designed as a 13-week curriculum covering the fundamental concepts, technologies, and applications in humanoid robotics and physical artificial intelligence.

The chatbot allows users to ask questions about the textbook content and receive AI-generated answers with source citations, making it an invaluable study companion.

---

## Course Structure

The textbook is organized into four progressive modules:

### Module 1: The Robotic Nervous System (ROS 2)
- ROS 2 architecture, nodes, topics, and services
- Bridging Python agents to ROS controllers using `rclpy`
- URDF (Unified Robot Description Format) for humanoid robots

### Module 2: The Digital Twin (Gazebo & Unity)
- Physics simulation and environment construction
- Gazebo physics: gravity, collisions, constraints
- Unity rendering & Human-Robot Interaction (HRI)
- Sensor simulation: LiDAR, depth cameras, IMUs

### Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- NVIDIA Isaac Sim: photorealistic simulation and synthetic data generation
- Isaac ROS: hardware-accelerated perception
- Nav2 for bipedal humanoid navigation

### Module 4: Vision-Language-Action (VLA)
- Whisper for voice-to-command pipeline
- LLM-based cognitive planning (natural language to ROS 2 action graph)
- Capstone: Autonomous humanoid executing voice commands

---

## Features

### Textbook Features
- **13-week curriculum** with structured learning path
- **Interactive documentation** built with Docusaurus v3
- **Mermaid diagrams** for visual explanations
- **Conceptual code examples** in Python and ROS 2
- **Comprehensive glossary** of robotics and AI terms
- **GitHub Pages deployment** for easy access

### RAG Chatbot Features
- **AI-powered Q&A** based on textbook content
- **Source citations** with direct links to relevant sections
- **User authentication** with email/password and OAuth (Google, GitHub)
- **Chat history** with persistent conversation storage
- **Light/dark theme** synchronized with the textbook
- **Responsive design** for desktop and mobile

---

## System Architecture

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              User Browser                                    │
│  ┌─────────────────────────┐  ┌─────────────────────────────────────────┐  │
│  │   Docusaurus Textbook   │  │         Next.js Frontend                │  │
│  │   (GitHub Pages)        │  │   - ChatKit UI                          │  │
│  │                         │  │   - Better Auth                         │  │
│  │   ┌───────────────────┐ │  │   - Chat History                        │  │
│  │   │ Embedded Chatbot  │◄┼──┤   - OAuth (Google/GitHub)               │  │
│  │   │ (iframe)          │ │  │                                         │  │
│  │   └───────────────────┘ │  │                                         │  │
│  └─────────────────────────┘  └──────────────────┬──────────────────────┘  │
└───────────────────────────────────────────────────┼─────────────────────────┘
                                                    │
                    ┌───────────────────────────────┴───────────────────┐
                    ▼                                                   ▼
        ┌─────────────────────────┐                     ┌─────────────────────────┐
        │   Neon PostgreSQL       │                     │   FastAPI Backend       │
        │   (User Data)           │                     │   (Hugging Face Spaces) │
        │   - users               │                     │                         │
        │   - sessions            │                     │   ┌─────────────────┐   │
        │   - chat_sessions       │                     │   │  OpenAI Agent   │   │
        │   - chat_messages       │                     │   │  SDK + Gemini   │   │
        └─────────────────────────┘                     │   └────────┬────────┘   │
                                                        │            │            │
                                                        │   ┌────────▼────────┐   │
                                                        │   │  Qdrant Cloud   │   │
                                                        │   │  (Vector DB)    │   │
                                                        │   └─────────────────┘   │
                                                        └─────────────────────────┘
```

---

## RAG Chatbot Backend

The textbook includes an AI-powered chatbot that answers questions based on the textbook content using Retrieval-Augmented Generation (RAG).

### How It Works

```
User Question → Embedding (Gemini) → Vector Search (Qdrant) → Context Retrieval → AI Response (Gemini) → Citations
```

### Backend Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Framework | FastAPI + Uvicorn | Async HTTP API with auto-generated docs |
| Embeddings | Google Gemini text-embedding-004 | Convert text to 768D vectors |
| Vector DB | Qdrant Cloud (free tier) | Semantic similarity search |
| LLM | Google Gemini 2.0 Flash | Answer generation with citations |
| Agent Framework | OpenAI Agent SDK | Tool-calling AI orchestration |
| Deployment | Docker + Hugging Face Spaces | Free container hosting |

### Backend API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | API information and documentation links |
| `/health` | GET | Health check for monitoring |
| `/api/v1/chat` | POST | Ask questions about the textbook |
| `/docs` | GET | Swagger UI documentation |
| `/redoc` | GET | ReDoc documentation |

### Quick Start (Backend)

```bash
cd backend

# Option 1: Docker (recommended)
docker compose up --build

# Option 2: Local development
python -m venv .venv
source .venv/bin/activate  # or .venv\Scripts\activate on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload --port 7860
```

### Backend Environment Variables

Create a `.env` file in the `backend/` directory:

```bash
# Required
GOOGLE_API_KEY=your_google_api_key      # From https://aistudio.google.com/
QDRANT_URL=https://xxx.cloud.qdrant.io  # From https://cloud.qdrant.io/
QDRANT_API_KEY=your_qdrant_api_key

# Optional (with defaults)
LLM_MODEL=gemini-2.0-flash
COLLECTION_NAME=book_chunks
SCORE_THRESHOLD=0.7
LOG_LEVEL=INFO
```

See [`backend/README.md`](./backend/README.md) for detailed backend documentation.

---

## Frontend Application

The frontend provides a modern chat interface with user authentication, chat history, and theme synchronization.

### Frontend Technology Stack

| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Framework | Next.js 15 + React 19 | Modern web application with App Router |
| Chat UI | OpenAI ChatKit | Pre-built chat interface components |
| Authentication | Better Auth | Email/password + OAuth (Google, GitHub) |
| Database | PostgreSQL Neon + Drizzle ORM | User data and chat history storage |
| Session Management | JWT tokens in httpOnly cookies | Secure session handling |
| Styling | Tailwind CSS | Responsive design with theme support |
| Theme System | CSS Custom Properties | Light/dark mode with localStorage |
| Deployment | Vercel | Static hosting for frontend |

### Frontend Features

- **User Authentication**: Email/password registration and login with OAuth support
- **Session Management**: JWT tokens stored in httpOnly cookies for security
- **Chat Interface**: ChatKit UI integrated with FastAPI RAG backend
- **Chat History**: Persistent conversation storage with Neon PostgreSQL
- **Route Protection**: Middleware-based access control for protected pages
- **Theme Sync**: Theme synchronized between chat UI and embedded textbook iframe

### Database Schema

| Table | Purpose |
|-------|---------|
| `user` | User accounts (email, name, password hash) |
| `session` | Active login sessions |
| `account` | OAuth provider accounts (Google, GitHub) |
| `verification` | Email verification tokens |
| `chat_session` | Chat conversation metadata |
| `chat_message` | Individual messages with role and content |

### Quick Start (Frontend)

```bash
cd frontend

# Install dependencies (use --legacy-peer-deps if needed)
npm install --legacy-peer-deps

# Copy environment template
cp .env.example .env.local

# Run database migrations
npx drizzle-kit generate
npx drizzle-kit migrate

# Start development server
npm run dev
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# =============================================================================
# Database Configuration (Required)
# =============================================================================
DATABASE_URL=postgresql://user:password@ep-xxx.region.aws.neon.tech/neondb?sslmode=require

# =============================================================================
# Better Auth Configuration (Required)
# =============================================================================
BETTER_AUTH_SECRET=your-secret-key-min-32-characters-here  # Generate with: openssl rand -base64 32
BETTER_AUTH_URL=http://localhost:3000

# =============================================================================
# Backend Configuration (Required for Chat)
# =============================================================================
NEXT_PUBLIC_BACKEND_URL=http://localhost:7860

# =============================================================================
# OAuth Providers (Optional)
# =============================================================================
GOOGLE_CLIENT_ID=your_google_client_id
GOOGLE_CLIENT_SECRET=your_google_client_secret
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
```

### Frontend API Routes

| Route | Method | Description |
|-------|--------|-------------|
| `/api/auth/sign-up/email` | POST | Register with email/password |
| `/api/auth/sign-in/email` | POST | Login with email/password |
| `/api/auth/sign-out` | POST | Sign out (clear session) |
| `/api/auth/session` | GET | Get current session |
| `/api/auth/callback/google` | GET | Google OAuth callback |
| `/api/auth/callback/github` | GET | GitHub OAuth callback |
| `/api/chat` | POST | Send message to RAG backend |
| `/api/chat/history` | GET/POST | List or create chat sessions |
| `/api/chat/history/[sessionId]` | GET/DELETE | Get or delete session |
| `/api/chat/history/[sessionId]/messages` | GET/POST | Get or add messages |

### Setting Up OAuth Providers

**Google OAuth:**
1. Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
2. Create a new OAuth 2.0 Client ID
3. Set authorized redirect URI: `{BETTER_AUTH_URL}/api/auth/callback/google`
4. Copy Client ID and Secret to `.env.local`

**GitHub OAuth:**
1. Go to [GitHub Developer Settings](https://github.com/settings/developers)
2. Create a new OAuth App
3. Set authorization callback URL: `{BETTER_AUTH_URL}/api/auth/callback/github`
4. Copy Client ID and Secret to `.env.local`

See [`frontend/GUIDE.md`](./frontend/GUIDE.md) for comprehensive frontend documentation.

---

## Prerequisites

### For Textbook (Docusaurus)
- Node.js v18.x or higher
- npm (Node Package Manager)

### For Frontend Application
- Node.js v18.x or higher
- npm (Node Package Manager)
- PostgreSQL Neon account (free tier available)

### For RAG Chatbot Backend
- Python 3.11+
- Docker (recommended) or local Python environment
- Google AI API key (from [Google AI Studio](https://aistudio.google.com/))
- Qdrant Cloud account (free tier available)

### Knowledge Prerequisites (for studying the textbook)
- Basic programming experience (preferably Python)
- Understanding of linear algebra and calculus
- Familiarity with basic physics concepts

---

## Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/nadeemsangrasi/humanoid-and-robotic-book.git
cd humanoid-and-robotic-book
```

### 2. Run the Textbook (Docusaurus)

```bash
# Install dependencies
npm install

# Start development server
npm start
```
The textbook will be available at `http://localhost:3000/humanoid-robotic-book/`

### 3. Run the Backend (FastAPI + RAG)

```bash
cd backend

# Copy environment template and configure
cp .env.example .env
# Edit .env with your API keys

# Run with Docker (recommended)
docker compose up --build

# Or run locally
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 7860
```
The API will be available at `http://localhost:7860`

### 4. Run the Frontend (Next.js + ChatKit)

```bash
cd frontend

# Install dependencies
npm install --legacy-peer-deps

# Copy environment template and configure
cp .env.example .env.local
# Edit .env.local with your credentials

# Run database migrations
npx drizzle-kit generate
npx drizzle-kit migrate

# Start development server
npm run dev
```
The frontend will be available at `http://localhost:3000`

### 5. Build for Production

```bash
# Textbook
npm run build

# Frontend
cd frontend && npm run build

# Backend (Docker)
cd backend && docker build -t rag-chatbot .
```

---

## Project Structure

```
humanoid-robotic-book/
│
├── docs/                          # Textbook content (Docusaurus)
│   ├── introduction/              # Course introduction
│   ├── quarter-overview/          # 13-week curriculum overview
│   ├── module-1-ros2/             # ROS 2 fundamentals
│   ├── module-2-gazebo-unity/     # Simulation environments
│   ├── module-3-nvidia-isaac/     # Advanced simulation
│   ├── module-4-vla/              # Vision-Language-Action models
│   ├── capstone/                  # Final project
│   └── glossary.md                # Robotics terminology
│
├── backend/                       # RAG Chatbot Backend (FastAPI)
│   ├── app/
│   │   ├── main.py                # FastAPI application entry point
│   │   ├── config.py              # Environment configuration
│   │   ├── routers/               # API endpoints (chat, health)
│   │   ├── schemas/               # Pydantic request/response models
│   │   ├── services/
│   │   │   ├── agent/             # OpenAI Agent SDK + Gemini orchestration
│   │   │   ├── embedding/         # Google Gemini embeddings
│   │   │   └── retrieval/         # Qdrant vector search
│   │   └── utils/                 # Logging utilities
│   ├── scripts/                   # Ingestion and deployment scripts
│   ├── tests/                     # Pytest test suite
│   ├── Dockerfile                 # Multi-stage production build
│   ├── docker-compose.yml         # Local development setup
│   ├── requirements.txt           # Production dependencies
│   └── README.md                  # Backend documentation
│
├── frontend/                      # Chat Frontend (Next.js + ChatKit)
│   ├── app/
│   │   ├── (auth)/                # Public auth routes (login, register)
│   │   ├── (protected)/           # Protected routes (chat, history)
│   │   ├── api/                   # API routes (auth, chat, history)
│   │   ├── book/                  # Embedded book with chat
│   │   ├── layout.tsx             # Root layout
│   │   └── page.tsx               # Home page
│   ├── components/
│   │   ├── auth/                  # Auth components (LoginForm, RegisterForm)
│   │   ├── chat/                  # Chat components (CitationDisplay, ConversationList)
│   │   └── ChatKitPanel.tsx       # Main chat interface
│   ├── hooks/                     # Custom React hooks
│   ├── lib/
│   │   ├── api/                   # Backend adapter, chat history API
│   │   ├── db/                    # Database schema and connection
│   │   ├── auth.ts                # Better Auth server config
│   │   └── auth-client.ts         # Better Auth client config
│   ├── drizzle/                   # Database migration files
│   ├── middleware.ts              # Route protection middleware
│   ├── GUIDE.md                   # Comprehensive frontend guide
│   └── README.md                  # Frontend documentation
│
├── specs/                         # Project specifications (SDD)
├── src/                           # Custom Docusaurus components
├── static/                        # Static assets
├── docusaurus.config.ts           # Docusaurus configuration
├── sidebars.ts                    # Navigation sidebar configuration
├── package.json                   # Root project dependencies
└── README.md                      # This file
```

---

## Deployment

### Textbook (Docusaurus)

Deployed on **GitHub Pages**:
- URL: [https://nadeemsangrasi.github.io/humanoid-and-robotic-book/](https://nadeemsangrasi.github.io/humanoid-and-robotic-book/)
- Automatic deployment via GitHub Actions on push to main branch

### Frontend Application (Next.js)

Deployed on **Vercel**:
- Build command: `npm run build`
- Output directory: `.next/`
- Environment variables: Configure in Vercel dashboard (see Frontend Environment Variables)
- Domain allowlist: Add your domain to [ChatKit Domain Allowlist](https://platform.openai.com/settings/organization/security/domain-allowlist)

### Backend API (FastAPI)

Deployed on **Hugging Face Spaces** (Docker mode):
- SDK: Docker
- App port: 7860
- Environment secrets: Configure in Space settings (GOOGLE_API_KEY, QDRANT_URL, QDRANT_API_KEY)

### Complete Architecture Flow

```
┌─────────────┐     ┌─────────────────┐     ┌────────────────────────┐
│   User      │────▶│  Vercel         │────▶│  Hugging Face Spaces   │
│   Browser   │     │  (Frontend)     │     │  (Backend API)         │
└─────────────┘     └─────────────────┘     └───────────┬────────────┘
                            │                           │
                            ▼                           ▼
                    ┌───────────────┐          ┌───────────────────┐
                    │ Neon Postgres │          │  Qdrant Cloud     │
                    │ (User Data)   │          │  (Vector DB)      │
                    └───────────────┘          └───────────────────┘
                                                        │
                                                        ▼
                                               ┌───────────────────┐
                                               │  Google Gemini    │
                                               │  (Embeddings+LLM) │
                                               └───────────────────┘
```

---

## Testing

### Frontend Tests

```bash
cd frontend

# Run all tests
npm run test

# Run tests with UI
npm run test:ui

# Run tests once (CI mode)
npm run test:run

# Run with coverage
npm run test:coverage
```

### Backend Tests

```bash
cd backend

# Install dev dependencies
pip install -r requirements-dev.txt

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

---

## Troubleshooting

### Common Issues

| Issue | Solution |
|-------|----------|
| "Database connection failed" | Verify `DATABASE_URL` in `.env.local` and ensure Neon project is active |
| "Invalid session" or "Unauthorized" | Check `BETTER_AUTH_SECRET` matches, clear cookies, verify `BETTER_AUTH_URL` |
| "CORS error" when calling backend | Ensure FastAPI CORS settings allow your frontend URL |
| "OAuth callback failed" | Verify redirect URI matches `{BETTER_AUTH_URL}/api/auth/callback/{provider}` |
| "Module not found: better-auth" | Run `npm install --legacy-peer-deps` |
| Backend returns 500 error | Check API keys are valid and not placeholder values |

See [`frontend/GUIDE.md`](./frontend/GUIDE.md) for detailed troubleshooting steps.

---

## Contributing

This project uses **Spec-Driven Development (SDD)** methodology with:
- Detailed specifications in the `specs/` directory
- Structured task management in `specs/*/tasks.md`
- Architectural planning in `specs/*/plan.md`
- Prompt History Records in `history/prompts/`

### Development Workflow

1. Create a feature specification in `specs/<feature>/spec.md`
2. Generate an implementation plan in `specs/<feature>/plan.md`
3. Break down into tasks in `specs/<feature>/tasks.md`
4. Implement following the task list
5. Create PR with reference to the spec

---

## License

This project is licensed under the ISC License.

---

## Links

- **Textbook**: [https://nadeemsangrasi.github.io/humanoid-and-robotic-book/](https://nadeemsangrasi.github.io/humanoid-and-robotic-book/)
- **Frontend Guide**: [`frontend/GUIDE.md`](./frontend/GUIDE.md)
- **Backend Docs**: [`backend/README.md`](./backend/README.md)
- **Better Auth Docs**: [https://www.better-auth.com/docs](https://www.better-auth.com/docs)
- **Drizzle ORM Docs**: [https://orm.drizzle.team/docs/overview](https://orm.drizzle.team/docs/overview)
- **Next.js App Router**: [https://nextjs.org/docs/app](https://nextjs.org/docs/app)
- **ChatKit Library**: [http://openai.github.io/chatkit-js/](http://openai.github.io/chatkit-js/)

---

**Keywords:** robotics, humanoid robotics, physical AI, ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA, textbook, docusaurus, simulation, artificial intelligence, RAG, chatbot, FastAPI, Qdrant, Google Gemini, vector search, embeddings, Next.js, Better Auth, Drizzle ORM, PostgreSQL, authentication, chat history