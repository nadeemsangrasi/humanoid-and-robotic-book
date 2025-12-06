# ADR-0004: Conceptual Code Blocks and Mermaid Diagrams Strategy

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-06
- **Feature:** 001-physical-ai-textbook
- **Context:** The project's `constitution.md` has been updated to remove "runnable code examples" and "100% real APIs" to focus on conceptual explanations and reduce maintenance overhead. A clear strategy for representing code and diagrams is needed.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

The textbook will provide conceptual code blocks (e.g., Python `rclpy` code for ROS 2 concepts) that are syntactically correct but not necessarily intended for direct execution. Diagrams illustrating concepts, architectures, or robot kinematics will be generated using Mermaid syntax directly within MDX files. Specific visual assets (e.g., Isaac Sim screenshots) will be pre-generated externally and stored as static images.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

Reduces maintenance burden associated with runnable code examples, prevents broken code from frequent API changes, focuses on conceptual understanding, leverages Mermaid for editable diagrams.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

Students cannot directly run code examples from the textbook, requiring them to implement code independently for hands-on experience, potential limitations of Mermaid for highly complex diagrams.

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Fully runnable code examples: High maintenance burden, frequent breakage, requires a stable execution environment for verification.
- Other diagramming tools (e.g., PlantUML): Requires different syntax/tooling, potentially less integrated with MDX.
- All diagrams as static images: Less editable, harder to version control changes to diagrams.

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: /specs/001-physical-ai-textbook/spec.md
- Implementation Plan: /specs/001-physical-ai-textbook/plan.md
- Related ADRs: null
- Evaluator Evidence: null <!-- link to eval notes/PHR showing graders and outcomes -->
