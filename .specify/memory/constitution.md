<!--
Sync Impact Report:
Version change: 1.1.1 → 1.2.0
List of modified principles:
  - Added Backend Technology Requirements (New)
  - Added RAG Chatbot Integration (New)
  - Added Deployment Constraints (New)
  - Updated Technical Stack (Expanded to include RAG, Qdrant, Gemini)
Added sections:
  - 2.1 Backend Services & RAG Integration
  - 6.4 RAG & Vector Database Standards
  - 12.IV Deployment Constraints
Modified sections:
  - Section 2: Expanded scope to include backend services
  - Section 12.I: Updated technology stack to include backend components
  - Section 12.III: Updated to include RAG-specific constraints
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - CLAUDE.md: ✅ already updated
Follow-up TODOs: None
-->
# Project Constitution: Physical AI & Humanoid Robotics Textbook

## 1. Purpose

This project creates an **AI-native, Docusaurus-based textbook** for the course *Physical AI & Humanoid Robotics*.
It will be written using **Spec-Kit Plus** and **Claude Code**, with documentation retrieval done via **Context7 MCP Server**.

This constitution defines how the book will be structured, authored, and maintained, including the backend RAG chatbot functionality.

---

## 1.1 Core Technical Principles

### I. Technical Accuracy & Verifiability
All technical claims and data MUST be accurate, technically sound, and verifiable against primary robotics and AI sources or through direct demonstration.

### II. Pedagogical Clarity
Content MUST be structured and written for optimal student comprehension, prioritizing clarity, progressive difficulty, and practical application for engineering and computer science students.

### III. Executable by Design
All demonstrations MUST be minimal and validated in the specified target environments (Ubuntu 22.04, ROS 2 Humble, Isaac Sim, Unity).

### IV. No Hypotheticals
Invented robotics systems, hallucinated parameters, or fictional sensors are strictly forbidden. All examples MUST correspond to real-world or industry-standard systems.

---

## 2. Scope (Book + Backend Services)

This constitution covers:

*   Writing the **textbook content** using Spec-Kit Plus
*   Organizing chapters under Docusaurus
*   Defining structure, standards, guidelines
*   Using Context7 MCP for all Docusaurus documentation lookups
*   Backend services: FastAPI + Uvicorn + OpenAI Agent SDK with Google Gemini models
*   Vector database: Qdrant (free tier) for book content embedding
*   Embedding: Google free embedding model via Langchain
*   RAG chatbot integration with OpenAI ChatKit UI
*   Frontend authentication: Better Auth with PostgreSQL Neon DB and Drizzle ORM
*   Database: PostgreSQL Neon DB (free tier) with Drizzle ORM for user data management
*   Authentication: Better Auth for frontend authentication and user management
*   Deployment: Docker (multi-stage) + Hugging Face Spaces (Docker mode) only
*   Preparing content so that later RAG integration is easy

---

## 2.1 Backend Services & RAG Integration

### I. RAG Architecture Requirements
The backend MUST implement a RAG (Retrieval-Augmented Generation) system that allows users to ask questions about the textbook content using an embedded chatbot. The system MUST use Google Gemini models (gemini-2.5-flash or gemini-1.5-flash) via OpenAI Agent SDK compatibility layer.

### II. Vector Database Integration
All textbook content MUST be embedded using Google's free embedding model via Langchain and stored in Qdrant vector database for efficient retrieval during RAG operations.

### III. Frontend-Backend Separation
The frontend UI MUST use OpenAI ChatKit ONLY for the chatbot interface. NO OpenAI models are permitted for backend inference; only Google Gemini models are allowed on the backend.

### IV. Authentication & Database Integration
The frontend MUST implement Better Auth for user authentication with PostgreSQL Neon DB as the backend database and Drizzle ORM for database operations. User data and session management MUST be handled securely through this stack.

---

## 3. Authoring Workflow

All writing must follow this workflow:

1.  **Use Spec-Kit Plus** to generate:

    *   Chapter specs
    *   Section outlines
    *   Diagram prompts

2.  **Use Claude Code** to convert Spec-Kit specs → `.md` files.

3.  All documentation lookups for Docusaurus must use:
    **Context7 MCP (docasaurus provider)**
    → This is the default and prioritized source for all official references.

4.  Commit generated chapters to GitHub with clear semantic messages.

5.  Content changes MUST be compatible with the RAG indexing system via `scripts/ingest-book.py`.

---

## 4. Book Structure (Based on Quarter & Modules)

The Docusaurus `docs/` folder will follow this structure:

```
/docs
  ├── 00-introduction/
  ├── 01-quarter-overview/
  ├── 02-module-1-ros2/
  ├── 03-module-2-gazebo-unity/
  ├── 04-module-3-nvidia-isaac/
  ├── 05-module-4-vla/
  ├── 06-capstone/
  └── glossary.md
```
The `glossary.md` file will serve as a living document to define key robotics and AI terms consistently used throughout the textbook. New terms and definitions will be added as they appear in content.

Each chapter will be generated using a Spec-Kit spec.

---

## 5. Core Content Definitions

The book content is structured around the quarter and its four modules:

### **Quarter Overview Chapter**

*   Why Physical AI matters
*   From digital AI → embodied intelligence
*   Overview of simulation + real-world robotics
*   Hardware and software ecosystem
*   Humanoid robotics landscape

---

## 6. Style & Quality Standards

To ensure high-quality, AI-native book content:

*   Clear, structured, modular writing.
*   Each chapter includes:
    *   Learning objectives
    *   Concept explanations
    *   Mermaid diagrams
    *   Step-by-step tutorials
    *   Common errors + troubleshooting
    *   Exercises
*   Use American English.
*   Avoid overly long paragraphs.
*   Make content chunk-friendly for future RAG indexing.

### 6.1 Docusaurus Formatting & Linking
All output MUST conform to Docusaurus-compatible Markdown. All pages MUST include required front-matter fields. All code blocks MUST specify language (e.g., using ````python` or ````cpp` for fenced code blocks) and build without breaking the MDX pipeline. Internal links, sidebar ordering, and slugs MUST follow Docusaurus routing rules. All diagrams and images MUST be in supported formats (e.g., SVG, PNG, JPG) and referenced using relative paths.

### 6.2 Mathematical & Diagram Standards
All diagrams MUST be generated or verified from accurate robotics models (URDF, kinematic chains, transforms). Mathematical expressions MUST use consistent LaTeX formatting supported by Docusaurus math plugins. Every chapter MUST include at least one practical applied robotics exercise. Exercises should focus on hands-on application of concepts in simulation or hardware, with clear objectives and expected outcomes.

### 6.3 Terminology & Symbol Consistency
All terminology, symbols, units, and coordinate frames MUST be strictly consistent across the entire textbook and align with established robotics and AI conventions.

### 6.4 RAG & Vector Database Standards
All content MUST be structured in a way that supports RAG indexing and retrieval. Content chunks SHOULD be semantically coherent and self-contained for effective embedding and retrieval. All content MUST be suitable for RAG-based Q&A functionality where users can ask questions about specific sections or the entire book.

---

## 7. File Naming Rules

*   Folders: **kebab-case** only
*   Files: numeric prefix + descriptive title
    Example:

```
01-ros2-basics.md
02-ros2-nodes-and-topics.md
03-ros2-services.md
```

---

## 8. MCP (Context7) Documentation Priority

All Docusaurus documentation used during development **must** come from:

**Primary Source:**

*   **Context7 MCP Docusaurus Docs Provider**

**Reason:**

*   Ensures consistent, version-correct docs
*   Supports AI-autocomplete inside Claude Code
*   Guarantees reproducible setups for hackathon evaluation

---

## 9. Versioning Rules

*   Each major addition = version bump
*   Use semantic versioning:
    `v1.0.0 → v1.1.0 → v1.2.0 → v2.0.0`
*   Every chapter update must include a CHANGELOG entry

---

## 10. License

Recommended:

**CC BY 4.0 International License**

---

## 11. Success Criteria

The project succeeds when:

*   All modules + capstone have full chapters
*   Docusaurus builds successfully
*   Backend RAG chatbot functions properly with textbook content
*   Content meets Spec-Kit quality guidelines
*   Navigation is clean and intuitive
*   Content is chunk-friendly for RAG used in next project phases
*   All backend services deploy successfully on Hugging Face Spaces

---

## 12. Constraints

### I. Restricted Technology Stack
Content and code examples MUST exclusively focus on ROS2, URDF, Gazebo/Isaac Sim, kinematics, dynamics, and control systems. Permitted programming languages include Python and C++. Backend services MUST use FastAPI, Uvicorn, OpenAI Agent SDK, Google Gemini models, and Qdrant vector database. Frontend authentication MUST use Better Auth with PostgreSQL Neon DB and Drizzle ORM. (Rationale: To maintain pedagogical focus, ensure consistent technical depth, and guarantee a reproducible learning environment.)

### II. Demonstrability & Verifiability
No content is allowed that cannot be demonstrated in ROS2, Gazebo, or Isaac Sim. All explanations and claims MUST be verifiable and supported by evidence. (Rationale: All claims and concepts MUST be grounded in practical application and verifiable evidence for student learning.)

### III. No Non-Robotics Content
The textbook MUST strictly avoid non-robotics related discussions, abstract AI theory without physical embodiment, or the introduction of invented frameworks, APIs, or tools. Content for RAG indexing MUST be exclusively from the textbook content. (Rationale: To preserve the core mission of the textbook and avoid diluting the focus with tangential or un-embodied AI concepts.)

### IV. Deployment Constraints
All backend services (especially RAG chatbot) MUST deploy as Docker container on Hugging Face Spaces free tier. NO alternatives permitted. NO other hosting (Vercel, Render, etc.) for production backend. (Rationale: To ensure consistent, accessible deployment that meets project requirements and constraints.)

---

## 13. Acceptance & Quality Gates

### I. Spec-Level Acceptance
Every Spec-Kit spec MUST be small, testable, implementable, and generate content cleanly without errors. It MUST explicitly define the expected outputs and behaviors.

### II. Chapter-Level Acceptance Checklist
All chapters and content modules MUST pass the following checks before integration:

*   [ ] Content is technically accurate and derived from primary robotics/AI sources.
*   [ ] Terminology, symbols, units, and coordinate frames align with established ROS2, URDF, and robotics conventions and are consistent throughout.
*   [ ] Demonstrations are verifiable in the specified environments.
*   [ ] Markdown passes a Docusaurus build without errors.
*   [ ] Chapter structure matches the required flow (learning objectives → theory → runnable example → diagram/pseudocode → summary → further reading).
*   [ ] No hallucinated parameters, robotics behaviors, or invented systems.
*   [ ] All new material includes a small, testable spec via Spec-Kit Plus.
*   [ ] All internal and external links resolve correctly within the Docusaurus site.
*   [ ] Diagrams are generated or verified from accurate robotics models.
*   [ ] Mathematical expressions use consistent LaTeX formatting.
*   [ ] Includes at least one practical applied robotics exercise.
*   [ ] Content is structured appropriately for RAG indexing and retrieval.
*   [ ] Content is suitable for embedding and Q&A functionality.

---

## 14. Governance

This Constitution supersedes all other project practices. Amendments REQUIRE a documented proposal (e.g., Markdown file), thorough review focusing on technical accuracy, pedagogical clarity, and constitution adherence, and explicit approval by the project architect. All content contributions MUST verify compliance with these principles, performing all acceptance checks before merging content.

### I. Architectural Decision Records (ADRs)
Any modifications to core terminology, chapter structure, core robotics assumptions, technology stack, or significant pedagogical approaches REQUIRE an ADR. Constitution changes REQUIRE explicit approval from the project architect and a logged update in `history/adr/`.

### II. Contributor Responsibilities
All contributors are responsible for adherence to this constitution and for running all specified acceptance checks prior to submitting work for review.

**Version**: 1.2.0 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-09