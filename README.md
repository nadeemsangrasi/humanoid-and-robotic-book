# Physical AI & Humanoid Robotics Textbook

**A comprehensive educational resource on Physical AI and Humanoid Robotics built with Docusaurus**

---

## Overview

This repository contains a complete textbook on **Physical AI & Humanoid Robotics**, structured as a Docusaurus-based website. The textbook is designed as a 13-week curriculum covering the fundamental concepts, technologies, and applications in humanoid robotics and physical artificial intelligence.

## Course Structure

The textbook is organized into four progressive modules:

1. **Module 1: The Robotic Nervous System (ROS 2)**
   - ROS 2 architecture, nodes, topics, and services
   - Bridging Python agents to ROS controllers using `rclpy`
   - URDF (Unified Robot Description Format) for humanoid robots

2. **Module 2: The Digital Twin (Gazebo & Unity)**
   - Physics simulation and environment construction
   - Gazebo physics: gravity, collisions, constraints
   - Unity rendering & Human-Robot Interaction (HRI)
   - Sensor simulation: LiDAR, depth cameras, IMUs

3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)**
   - NVIDIA Isaac Sim: photorealistic simulation and synthetic data generation
   - Isaac ROS: hardware-accelerated perception
   - Nav2 for bipedal humanoid navigation

4. **Module 4: Vision-Language-Action (VLA)**
   - Whisper for voice-to-command pipeline
   - LLM-based cognitive planning (natural language to ROS 2 action graph)
   - Capstone: Autonomous humanoid executing voice commands

## Features

- **13-week curriculum** with structured learning path
- **Interactive documentation** built with Docusaurus v3
- **Mermaid diagrams** for visual explanations
- **Conceptual code examples** in Python and ROS 2
- **Comprehensive glossary** of robotics and AI terms
- **GitHub Pages deployment** for easy access
- **RAG-powered chatbot** for interactive Q&A with the textbook content

## RAG Chatbot Backend

The textbook includes an AI-powered chatbot that answers questions based on the textbook content using Retrieval-Augmented Generation (RAG).

### Backend Architecture

```
User Question → Embedding (Gemini) → Vector Search (Qdrant) → AI Response (Gemini)
```

| Component | Technology | Purpose |
|-----------|------------|---------|
| Web Framework | FastAPI | Async HTTP API with auto-docs |
| Embeddings | Google Gemini text-embedding-004 | Convert text to 768D vectors |
| Vector DB | Qdrant Cloud | Semantic similarity search |
| LLM | Google Gemini 2.0 Flash | Answer generation with citations |
| Agent Framework | OpenAI Agent SDK | Tool-calling AI orchestration |
| Deployment | Docker + Hugging Face Spaces | Free hosting |

### Frontend Architecture

| Component | Technology | Purpose |
|-----------|------------|---------|
| UI Framework | Next.js 15 + React 19 | Modern web application with App Router |
| Chat UI | OpenAI ChatKit | Pre-built chat interface components |
| Authentication | Better Auth | User authentication and session management |
| Database | PostgreSQL Neon + Drizzle ORM | User data and chat history storage |
| Styling | Tailwind CSS + Custom CSS | Responsive design with theme support |
| Theme System | CSS Custom Properties | Light/dark mode with localStorage persistence |
| Deployment | Vercel (frontend), Hugging Face Spaces (backend) | Static hosting for frontend, container hosting for backend |

### API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/health` | GET | Health check for monitoring |
| `/api/v1/chat` | POST | Ask questions about the textbook |
| `/docs` | GET | Swagger UI documentation |

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

### Environment Variables

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
```

See [`backend/README.md`](./backend/README.md) for detailed backend documentation.

## Frontend Setup

### Quick Start (Frontend)

```bash
cd frontend

# Install dependencies
npm install

# Start development server
npm run dev

# Build for production
npm run build
```

### Frontend Environment Variables

Create a `.env.local` file in the `frontend/` directory:

```bash
# Better Auth Configuration
NEXT_PUBLIC_BETTER_AUTH_URL=http://localhost:3000
BETTER_AUTH_SECRET=your_secret_key_here

# Backend API Configuration
NEXT_PUBLIC_BACKEND_URL=http://localhost:7860
```

### Frontend Architecture

The frontend is built with Next.js 15 using the App Router and includes:

- **Authentication**: Better Auth for user management
- **Database**: PostgreSQL Neon DB with Drizzle ORM for user data
- **Chat Interface**: OpenAI ChatKit components for conversation UI
- **Theme System**: CSS custom properties with light/dark mode support
- **Responsive Design**: Mobile-first approach with Tailwind CSS

## Prerequisites

### For Textbook (Docusaurus)
- Node.js v18.x or higher
- npm (Node Package Manager)

### For RAG Chatbot Backend
- Python 3.11+
- Docker (recommended) or local Python environment
- API keys: Google AI (Gemini) and Qdrant Cloud

### Knowledge Prerequisites
- Basic programming experience (preferably Python)
- Understanding of linear algebra and calculus
- Familiarity with basic physics concepts

## Getting Started

1. **Clone the repository:**
   ```bash
   git clone https://github.com/nadeemsangrasi/humanoid-and-robotic-book.git
   cd humanoid-and-robotic-book
   ```

2. **Install dependencies:**
   ```bash
   npm install
   ```

3. **Run the development server:**
   ```bash
   npm start
   ```
   The textbook will be available at `http://localhost:3000/humanoid-robotic-book/`

4. **Build the static site:**
   ```bash
   npm run build
   ```

## Project Structure

```
├── docs/                    # Textbook content
│   ├── introduction/        # Course introduction
│   ├── quarter-overview/    # 13-week curriculum overview
│   ├── module-1-ros2/       # ROS 2 fundamentals
│   ├── module-2-gazebo-unity/ # Simulation environments
│   ├── module-3-nvidia-isaac/ # Advanced simulation
│   ├── module-4-vla/        # Vision-Language-Action models
│   ├── capstone/            # Final project
│   └── glossary.md          # Robotics terminology
├── backend/                 # RAG Chatbot Backend
│   ├── app/
│   │   ├── main.py          # FastAPI application entry point
│   │   ├── config.py        # Environment configuration
│   │   ├── routers/         # API endpoints (chat, health)
│   │   ├── schemas/         # Pydantic request/response models
│   │   ├── services/        # Business logic
│   │   │   ├── agent/       # OpenAI Agent SDK + Gemini orchestration
│   │   │   ├── embedding/   # Google Gemini embeddings
│   │   │   └── retrieval/   # Qdrant vector search
│   │   └── utils/           # Logging utilities
│   ├── tests/               # Pytest test suite
│   ├── scripts/             # Ingestion and deployment scripts
│   ├── Dockerfile           # Multi-stage production build
│   ├── docker-compose.yml   # Local development setup
│   └── requirements.txt     # Python dependencies
├── specs/                   # Project specifications
├── src/                     # Custom Docusaurus components
├── static/                  # Static assets
├── docusaurus.config.ts     # Docusaurus configuration
├── sidebars.ts              # Navigation sidebar configuration
└── package.json             # Project dependencies and scripts
```

## Deployment

### Textbook (Docusaurus)
The textbook is deployed on GitHub Pages at: [https://nadeemsangrasi.github.io/humanoid-and-robotic-book/](https://nadeemsangrasi.github.io/humanoid-and-robotic-book/)

### Frontend Application
The chatbot frontend is deployed on Vercel:
- Build command: `npm run build`
- Output directory: `out/`
- Environment variables required (see Frontend Environment Variables section)

### Backend API
The RAG chatbot backend is deployed on Hugging Face Spaces (Docker mode):
- Dockerfile included in backend/
- Environment variables configured in Hugging Face secrets
- Free tier deployment with Docker container

### Architecture Overview
```
User → Vercel Frontend → Hugging Face Backend → Qdrant Vector DB → Google Gemini APIs
```

## Contributing

This project uses Spec-Driven Development (SDD) methodology with:
- Detailed specifications in the `specs/` directory
- Structured task management in `specs/001-physical-ai-textbook/tasks.md`
- Architectural planning in `specs/001-physical-ai-textbook/plan.md`

## License

This project is licensed under the ISC License.

---

**Keywords:** robotics, humanoid robotics, physical AI, ROS 2, Gazebo, Unity, NVIDIA Isaac, VLA, textbook, docusaurus, simulation, artificial intelligence, RAG, chatbot, FastAPI, Qdrant, Google Gemini, vector search, embeddings