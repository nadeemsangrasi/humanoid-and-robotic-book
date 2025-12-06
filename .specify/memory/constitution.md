<!--
Sync Impact Report:
Version change: 1.0.0 → 1.1.1
List of modified principles:
  - Technical Accuracy & Verifiability (Added)
  - Pedagogical Clarity (Added)
  - Executable by Design (Added)
  - No Hypotheticals (Added)
Added sections:
  - 1.1 Core Technical Principles
  - 6.1 Docusaurus Formatting & Linking
  - 6.2 Mathematical & Diagram Standards
  - 6.3 Terminology & Symbol Consistency
  - 12. Constraints
  - 13. Acceptance & Quality Gates
  - 14. Governance (Expanded)
Modified sections:
  - Section 4: Added glossary purpose.
  - Section 6.1: Added example for code block language.
  - Section 6.2: Clarified exercise guidelines.
  - Section 12.I: Added rationale.
  - Section 12.II: Added rationale.
  - Section 12.III: Added rationale.
  - Section 14: Clarified review process.
Removed sections: None (sections were added/expanded within the existing structure)
Templates requiring updates:
  - .specify/templates/plan-template.md: ✅ updated
  - .specify/templates/spec-template.md: ✅ updated
  - .specify/templates/tasks-template.md: ✅ updated
  - .claude/commands/sp.adr.md: ✅ updated
  - .claude/commands/sp.analyze.md: ✅ updated
  - .claude/commands/sp.checklist.md: ✅ updated
  - .claude/commands/sp.clarify.md: ✅ updated
  - .claude/commands/sp.constitution.md: ✅ updated
  - .claude/commands/sp.git.commit_pr.md: ✅ updated
  - .claude/commands/sp.implement.md: ✅ updated
  - .claude/commands/sp.phr.md: ✅ updated
  - .claude/commands/sp.plan.md: ✅ updated
  - .claude/commands/sp.specify.md: ✅ updated
  - .claude/commands/sp.tasks.md: ✅ updated
  - CLAUDE.md: ✅ updated
Follow-up TODOs: None
-->
# Project Constitution: Physical AI & Humanoid Robotics Textbook

## 1. Purpose

This project creates an **AI-native, Docusaurus-based textbook** for the course *Physical AI & Humanoid Robotics*.
It will be written using **Spec-Kit Plus** and **Claude Code**, with documentation retrieval done via **Context7 MCP Server**.

This constitution defines how the book will be structured, authored, and maintained.

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

## 2. Scope (Book Only)

This constitution covers:

*   Writing the **textbook content** using Spec-Kit Plus
*   Organizing chapters under Docusaurus
*   Defining structure, standards, guidelines
*   Using Context7 MCP for all Docusaurus documentation lookups
*   Preparing content so that later RAG integration is easy
.

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
*   Content meets Spec-Kit quality guidelines
*   Navigation is clean and intuitive
*   Content is chunk-friendly for RAG used in next project phases

---

## 12. Constraints

### I. Restricted Technology Stack
Content and code examples MUST exclusively focus on ROS2, URDF, Gazebo/Isaac Sim, kinematics, dynamics, and control systems. Permitted programming languages include Python and C++. (Rationale: To maintain pedagogical focus, ensure consistent technical depth, and guarantee a reproducible learning environment.)

### II. Demonstrability & Verifiability
No content is allowed that cannot be demonstrated in ROS2, Gazebo, or Isaac Sim. All explanations and claims MUST be verifiable and supported by evidence. (Rationale: All claims and concepts MUST be grounded in practical application and verifiable evidence for student learning.)

### III. No Non-Robotics Content
The textbook MUST strictly avoid non-robotics related discussions, abstract AI theory without physical embodiment, or the introduction of invented frameworks, APIs, or tools. (Rationale: To preserve the core mission of the textbook and avoid diluting the focus with tangential or un-embodied AI concepts.)

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

---

## 14. Governance

This Constitution supersedes all other project practices. Amendments REQUIRE a documented proposal (e.g., Markdown file), thorough review focusing on technical accuracy, pedagogical clarity, and constitution adherence, and explicit approval by the project architect. All content contributions MUST verify compliance with these principles, performing all acceptance checks before merging content.

### I. Architectural Decision Records (ADRs)
Any modifications to core terminology, chapter structure, core robotics assumptions, technology stack, or significant pedagogical approaches REQUIRE an ADR. Constitution changes REQUIRE explicit approval from the project architect and a logged update in `history/adr/`.

### II. Contributor Responsibilities
All contributors are responsible for adherence to this constitution and for running all specified acceptance checks prior to submitting work for review.

**Version**: 1.1.1 | **Ratified**: 2025-12-05 | **Last Amended**: 2025-12-05