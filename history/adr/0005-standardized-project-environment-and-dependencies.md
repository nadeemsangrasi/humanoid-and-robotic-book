# ADR-0005: Standardized Project Environment and Dependencies

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-06
- **Feature:** 001-physical-ai-textbook
- **Context:** To ensure consistent development, reproducible builds, and smooth collaboration, a standardized environment and dependency management strategy is required.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

The project will standardize on Node.js v18.x or higher, use `npm` as the sole package manager, and maintain `package-lock.json` for lockfile strategy. Python v3.9 or higher will be assumed for conceptual Python code blocks.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

Ensures all developers and CI/CD environments use the same versions, minimizing "it works on my machine" issues; `package-lock.json` guarantees reproducible dependency installations.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

Requires developers to adhere to specific Node.js and Python versions, potentially conflicting with other projects on their local machines (mitigated by version managers like NVM/Pyenv).

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Other Node.js versions (e.g., latest LTS): Might introduce more frequent updates or compatibility issues with Docusaurus dependencies.
- Yarn/pnpm as package manager: Could be used, but standardizing on one (`npm`) simplifies tooling and consistency.
- No lockfile: Leads to non-reproducible builds due to floating dependency versions.

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
