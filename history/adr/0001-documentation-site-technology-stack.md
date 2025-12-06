# ADR-0001: Documentation Site Technology Stack

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-06
- **Feature:** 001-physical-ai-textbook
- **Context:** The project requires building a static textbook site for "Physical AI & Humanoid Robotics" with features like content management, navigation, and deployment capabilities.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Docusaurus v3 (Node.js/React framework) is chosen as the primary technology stack.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

Leverage Docusaurus's built-in features for documentation, strong community support, extensibility, and good performance for static sites.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

Dependency on Docusaurus ecosystem, potential learning curve for new contributors unfamiliar with Docusaurus/React.

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Hugo: Fast, but Go-based templating might be less familiar to JavaScript/React developers.
- Gatsby/Next.js for docs: More flexible but might be overkill for a pure documentation site, potentially higher complexity.
- Custom static site generator: High development effort, maintenance overhead.

<!-- Group alternatives by cluster:
     Alternative Stack A: Remix + styled-components + Cloudflare
     Alternative Stack B: Vite + vanilla CSS + AWS Amplify
     Why rejected: Less integrated, more setup complexity
-->

## References

- Feature Spec: /specs/001-physical-ai-textbook/spec.md
- Implementation Plan: /specs/001-physical-ai-textbook/plan.md
- Related ADRs: null
- Evaluator Evidence: null
