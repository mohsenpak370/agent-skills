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

For backend, Python, and Django work:

- Use `django-backend-development` for Django apps, Django REST Framework,
  models, ORM queries, migrations, views, serializers, forms, settings,
  management commands, Django tests, performance, security, and deployment.
  Combine it with the Python, backend architecture, API design, PostgreSQL,
  auth, testing, security, and observability skills that match the task.
- Use `python-development-uv-package-manager` when setting up Python versions,
  virtual environments, dependencies, or `uv` workflows.
- Use `python-development-python-project-structure` when creating or reorganizing
  Python packages, Django apps, modules, public APIs, or test layout.
- Use `python-development-python-configuration` for environment variables,
  typed settings, secrets, and environment-specific behavior.
- Use `python-development-python-code-style` for Python style, naming, linting,
  formatting, docstrings, and project standards.
- Use `python-development-python-type-safety` for type annotations, protocols,
  generics, and mypy or pyright configuration.
- Use `python-development-python-error-handling` for validation, exception
  strategy, robust API failures, and partial failure handling.
- Use `python-development-python-testing-patterns` for pytest, fixtures, mocks,
  and Python-specific test structure. Use `test-driven-development` alongside it
  when the task is about the red-green-refactor workflow.
- Use `backend-development-architecture-patterns` for backend service boundaries,
  dependency direction, layered architecture, domain logic placement, and avoiding
  business logic in Django views or framework adapters. Apply it proportionally;
  do not introduce microservice, CQRS, event-sourcing, or heavy DDD complexity
  unless the project requirements justify it.
- Use `backend-development-api-design-principles` for REST or GraphQL resource
  design, endpoint naming, status codes, pagination, filtering, versioning, and
  API documentation. Use `api-and-interface-design` alongside it for broader
  contracts between frontend, backend, SDKs, or external consumers.
- Use `database-design-postgresql` when designing or reviewing PostgreSQL schemas,
  migrations, constraints, indexes, data types, query access paths, and database
  performance risks.
- Use `developer-essentials-auth-implementation-patterns` for authentication,
  authorization, sessions, OAuth, JWT, RBAC, resource ownership, and securing
  APIs. Use `security-and-hardening` alongside it for security-sensitive changes.

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
