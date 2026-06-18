# Skills

Project-level agent skills and instructions for opencode.

## Contents

- `AGENTS.md`: Root agent instructions for when and how to use installed skills.
- `.agents/skills/`: Installed agent skills.
- `skills-lock.json`: Installed skill lockfile.

## Usage

Open this repository in opencode. When a request matches an installed skill, the
agent should load that skill before acting.

Use natural language. The root `AGENTS.md` tells the agent to choose the right
skill based on the task, such as:

- `using-agent-skills` when it needs to discover which skill applies
- `spec-driven-development` for unclear requirements or significant new features
- `planning-and-task-breakdown` for turning a known change into tasks
- `incremental-implementation` for multi-file implementation work
- `test-driven-development` for writing or running tests
- `debugging-and-error-recovery` for failures and regressions
- `code-review-and-quality` for review work
- `git-workflow-and-versioning` for commits, branches, and versioning

## Agent Expectations

- The agent checks whether an installed skill applies before acting.
- Matching skills are loaded with the `skill` tool.
- Required workflows from loaded skills should be followed.
- Significant work should go through the appropriate define, plan, build,
  verify, review, or ship phase.
- Small, obvious edits should use the lightest applicable workflow.

## Lifecycle Mapping

The development lifecycle is handled implicitly through skills. Use natural
language instead of slash commands; the agent maps the work to the right skill.

| Phase | Skill |
| --- | --- |
| DEFINE | `spec-driven-development` |
| PLAN | `planning-and-task-breakdown` |
| BUILD | `incremental-implementation` + `test-driven-development` |
| VERIFY | `debugging-and-error-recovery` |
| REVIEW | `code-review-and-quality` |
| SHIP | `shipping-and-launch` |

For frontend work, the agent should use `frontend-ui-engineering` for:

- React or TSX UI work
- Nuxt 4 or Vue single-file components
- Tailwind CSS 4 styling
- Accessibility and responsive layout work
- Component architecture and design-system implementation

For Vue and Nuxt work, Vue-specific skills may be loaded alongside
`frontend-ui-engineering`. Use the frontend skill for UI quality and design
system concerns, and Vue-specific skills for framework correctness, composables,
Pinia, testing, and debugging.

Use `nuxt` for Nuxt 3 and Nuxt 4 routing, data fetching, server routes,
middleware, Nitro, modules, layers, and rendering modes. The Nuxt skill is based
on Nuxt 3.x, so verify version-specific features against the project's installed
Nuxt version.

Use VueUse when an existing composable fits browser APIs, storage, sensors,
async state, animation, or common reactive utilities. Keep Nuxt server-aware data
fetching on `useFetch` or `useAsyncData` unless client-only fetch behavior is
intended.

Use `nuxt-ui` only when `@nuxt/ui` / Nuxt UI is installed in the target project,
or when the task is explicitly to add, install, configure, theme, or use Nuxt UI.
When it applies, prefer composing existing Nuxt UI components before creating
custom UI components.

For backend, Python, and Django work, combine the focused skills that match the
task:

| Area | Skills |
| --- | --- |
| Django | `django-backend-development` |
| Python setup | `python-development-uv-package-manager` |
| Python structure | `python-development-python-project-structure` |
| Python config | `python-development-python-configuration` |
| Python style | `python-development-python-code-style` |
| Python typing | `python-development-python-type-safety` |
| Python errors | `python-development-python-error-handling` |
| Python resources | `python-development-python-resource-management` |
| Python resilience | `python-development-python-resilience` |
| Python observability | `python-development-python-observability` |
| Python testing | `python-development-python-testing-patterns` |
| Backend architecture | `backend-development-architecture-patterns` |
| API design | `backend-development-api-design-principles`, `api-and-interface-design` |
| PostgreSQL | `database-design-postgresql` |
| SQL optimization | `developer-essentials-sql-optimization-patterns`, `database-design-postgresql` |
| E2E testing | `developer-essentials-e2e-testing-patterns` |
| Auth and authorization | `developer-essentials-auth-implementation-patterns`, `security-and-hardening` |

For Django work, load `django-backend-development` first, then combine it with
the Python, backend architecture, API design, PostgreSQL, auth, testing,
security, and observability skills that match the task. Apply architecture
guidance proportionally: avoid putting business logic in Django views, but do not
force microservice, CQRS, event-sourcing, or heavy DDD patterns unless the product
requirements justify them.

Having multiple focused skills is expected. It becomes a problem only when skill
descriptions overlap without routing guidance or when heavyweight workflows are
forced for small edits. `AGENTS.md` defines the routing rules to avoid that.

## Installed Skills

This repository currently includes skills for:

- API and interface design
- Backend API design principles
- Backend architecture patterns
- Browser testing with DevTools
- CI/CD and automation
- CI/CD deployment pipeline design
- CI/CD GitHub Actions templates
- CI/CD secrets management
- Code review and quality
- Code simplification
- Context engineering
- Database design with PostgreSQL
- Debugging and error recovery
- Deprecation and migration
- Developer auth implementation patterns
- Developer E2E testing patterns
- Developer SQL optimization patterns
- Django backend development
- Documentation and ADRs
- OpenAPI spec generation
- Doubt-driven development
- Frontend UI engineering
- Git workflow and versioning
- Idea refinement
- Incremental implementation
- Interview-driven clarification
- Nuxt framework guidance
- Nuxt UI component and theming guidance
- Observability and instrumentation
- SLO implementation
- Performance optimization
- Planning and task breakdown
- Python code style
- Python configuration
- Python error handling
- Python observability
- Python project structure
- Python resilience
- Python resource management
- Python testing patterns
- Python type safety
- Python uv package management
- Security and hardening
- SAST configuration
- Security requirement extraction
- Threat mitigation mapping
- Shipping and launch
- Source-driven development
- Spec-driven development
- Test-driven development
- Using agent skills
- Vue adaptable composables
- Vue best practices
- Vue debugging guides
- Vue Pinia best practices
- Vue testing best practices
- VueUse functions

## References

The frontend skill points agents to focused references:

- `references/react-ui.md` for React UI patterns
- `references/nuxt4-tailwind4.md` for Nuxt 4, Vue, and Tailwind CSS 4 patterns
- `references/nuxt-focused-components.md` for explicit Nuxt bad/good component split examples
- `references/accessibility-checklist.md` for accessibility checks

## Maintenance

Keep skill descriptions specific and action-oriented so opencode can select the
right skill automatically. If you add a new skill, place it under
`.agents/skills/<skill-name>/SKILL.md` and include clear frontmatter with `name`
and `description`.

Restart opencode after changing `AGENTS.md`, skill files, or references so new
sessions pick up the updated instructions.
