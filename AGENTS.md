# Agent Instructions

When a user request matches an installed skill, use the `skill` tool before
acting.

## Skill Use Rules

- Always check whether an installed skill applies before acting.
- If a skill clearly applies, use the `skill` tool before proceeding.
- Do not skip required workflows from a loaded skill.
- Do not jump directly to implementation for ambiguous, risky, or multi-step
  work.
- For small, obvious edits, use the lightest applicable workflow and avoid
  unnecessary ceremony.

Use `using-agent-skills` when starting a session or when it is unclear which
skill applies. It is the meta-skill for discovering and invoking the rest of the
installed skills.

Use `frontend-ui-engineering` for building or modifying user-facing interfaces,
including React, Nuxt 4, Vue, Tailwind CSS 4, accessibility, component
architecture, layout, and design-system work.

For broader engineering work, select the matching lifecycle or specialty skill:

- New feature or unclear requirements: `spec-driven-development`
- Planning a known change: `planning-and-task-breakdown`
- Multi-file implementation: `incremental-implementation`
- Writing or running tests: `test-driven-development`
- Debugging failures: `debugging-and-error-recovery`
- Reviewing changes: `code-review-and-quality`
- API design: `api-and-interface-design`
- Security-sensitive work: `security-and-hardening`
- Performance work: `performance-optimization`
- Git, commits, and branching: `git-workflow-and-versioning`
- Documentation or ADRs: `documentation-and-adrs`
- CI/CD automation: `ci-cd-and-automation`
- Shipping or launch work: `shipping-and-launch`

Before writing framework-specific UI code, load the relevant skill reference and
follow the existing project conventions unless the user explicitly asks for a
different direction.

Do not force heavyweight lifecycle workflows for small, obvious edits. Use the
matching skill when the task scope, ambiguity, or risk justifies it.
