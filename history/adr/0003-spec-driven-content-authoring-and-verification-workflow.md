# ADR-0003: Spec-Driven Content Authoring and Verification Workflow

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-06
- **Feature:** 001-physical-ai-textbook
- **Context:** Need a structured and verifiable workflow for generating high-quality, technically accurate, and Docusaurus-compatible content for the textbook, aligning with the "Zero Hallucination" principle.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Implement a workflow using Spec-Kit Plus for granular specifications, Claude Code for MDX content generation from specs, and Context7 MCP Server as the authoritative source for Docusaurus-specific syntax, best practices, and verification during MDX generation.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

Ensures consistency, technical accuracy, Docusaurus compatibility, reduces "hallucinations," provides an auditable content generation process, leverages AI for efficiency.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

Introduces a multi-tool workflow, potential overhead in maintaining specifications, dependency on AI agent capabilities.

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Manual MDX authoring: Higher risk of inconsistencies, errors, and Docusaurus incompatibility; labor-intensive.
- Other AI content generation without structured specs/verification: Higher risk of "hallucinations" and lack of control over output quality.
- Using general web search for Docusaurus documentation: Less authoritative and consistent than a dedicated MCP server.

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
