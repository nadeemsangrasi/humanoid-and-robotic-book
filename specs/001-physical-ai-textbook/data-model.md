# Data Model: Physical AI & Humanoid Robotics Textbook

This document outlines the key entities for the Physical AI & Humanoid Robotics Textbook, based on the `spec.md`.

## Entities

### Module
-   **Description**: A top-level organizational unit containing multiple related chapters.
-   **Attributes**:
    -   `id`: Unique identifier (e.g., `01-module-name`)
    -   `title`: Title of the module (e.g., "The Robotic Nervous System (ROS 2)")
    -   `chapters`: List of associated chapters.

### Chapter
-   **Description**: A discrete section of the textbook covering a specific topic, part of a module.
-   **Attributes**:
    -   `id`: Unique identifier (e.g., `01-chapter-title`)
    -   `title`: Title of the chapter (e.g., "ROS 2 Nodes, Topics, and Services")
    -   `module_id`: Reference to the parent module.
    -   `content`: The actual text, diagrams, code blocks, and exercises.
    -   `learning_objectives`: Key takeaways for the student.
    -   `citations`: List of references used.

### Content
-   **Description**: Textual explanations, code examples, diagrams, exercises, and summaries within chapters.
-   **Attributes**:
    -   `type`: (e.g., `text`, `code_block`, `diagram`, `exercise`, `summary`)
    -   `value`: The actual content (Markdown, code, Mermaid syntax).
    -   `language`: (for code blocks, e.g., `python`, `cpp`)
    -   `alt_text`: (for diagrams/images)

### Citation
-   **Description**: A reference to an authoritative external source supporting technical claims.
-   **Attributes**:
    -   `text`: Full citation text (e.g., "Author, Title, Year, URL")
    -   `url`: Link to the source.

### Glossary Term
-   **Description**: A key robotics or AI term with its definition.
-   **Attributes**:
    -   `term`: The term itself (e.g., "URDF")
    -   `definition`: Concise explanation.
