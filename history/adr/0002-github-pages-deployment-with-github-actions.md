# ADR-0002: GitHub Pages Deployment with GitHub Actions

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-06
- **Feature:** 001-physical-ai-textbook
- **Context:** The static Docusaurus textbook needs an automated and cost-effective deployment mechanism.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
     2) Alternatives: Multiple viable options considered with tradeoffs?
     3) Scope: Cross-cutting concern (not an isolated detail)?
     If any are false, prefer capturing as a PHR note instead of an ADR. -->

## Decision

Deploy to GitHub Pages using GitHub Actions for automated build and deployment to the `gh-pages` branch. The `baseUrl` in `docusaurus.config.js` will be set to `/humanoid-robotic-book/`.

<!-- For technology stacks, list all components:
     - Framework: Next.js 14 (App Router)
     - Styling: Tailwind CSS v3
     - Deployment: Vercel
     - State Management: React Context (start simple)
-->

## Consequences

### Positive

Free hosting, integrated CI/CD with GitHub, simplified deployment workflow, version control of deployment.

<!-- Example: Integrated tooling, excellent DX, fast deploys, strong TypeScript support -->

### Negative

GitHub Pages limitations (e.g., no server-side logic, custom domain complexities, potential build time limits for very large sites), dependency on GitHub infrastructure.

<!-- Example: Vendor lock-in to Vercel, framework coupling, learning curve -->

## Alternatives Considered

- Netlify/Vercel: Offer more features (e.g., preview deploys, serverless functions) but might introduce additional cost or third-party dependencies.
- AWS S3 + CloudFront: Highly scalable, but more complex setup and management, additional cost.
- Manual deployment: High human error risk, not scalable, lacks automation.

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
