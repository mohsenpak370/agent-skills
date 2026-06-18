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

For Vue and Nuxt work:

- Use `nuxt` for Nuxt apps, server routes, middleware, `useFetch`,
  `useAsyncData`, Nitro, file-based routing, modules, layers, or hybrid
  rendering. The `nuxt` skill is based on Nuxt 3.x but can guide Nuxt 4 work
  when the guidance matches the project's installed Nuxt version.
- Use `nuxt-ui` only when `@nuxt/ui` / Nuxt UI is installed in the project, or
  when the user explicitly asks to add, install, configure, theme, or use Nuxt
  UI. Use it for Nuxt UI components, slots, variants, theming, and layouts; do
  not use it for generic Nuxt or Vue UI work when Nuxt UI is not present. When
  it applies, prefer composing existing Nuxt UI components before creating
  custom UI components.
- Use `vue-best-practices` for any Vue, `.vue`, Vue Router, Pinia, or Vue/Vite
  task.
- Use `frontend-ui-engineering` alongside it when the task affects user-facing
  UI, layout, accessibility, responsive behavior, or design-system behavior.
- Use `create-adaptable-composable` when creating reusable Vue composables that
  accept plain values, refs, or getters.
- Use `vueuse-functions` for VueUse composables in Vue/Nuxt work. Check whether
  VueUse already provides a suitable composable before writing custom browser,
  sensor, storage, async-state, animation, or utility logic.
- Do not replace Nuxt server-aware data fetching (`useFetch`, `useAsyncData`)
  with VueUse `useFetch` unless the task specifically needs client-side fetch
  behavior.
- Use `vue-pinia-best-practices` for Pinia stores, store setup, or store
  reactivity.
- Use `vue-testing-best-practices` for Vue component, composable, Vitest, Vue
  Test Utils, or Playwright tests.
- Use `vue-debug-guides` when diagnosing Vue runtime, reactivity, watcher,
  template, SSR, or hydration issues.

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
