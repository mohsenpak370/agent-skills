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

Having multiple focused skills is expected. It becomes a problem only when skill
descriptions overlap without routing guidance or when heavyweight workflows are
forced for small edits. `AGENTS.md` defines the routing rules to avoid that.

## Installed Skills

This repository currently includes skills for:

- API and interface design
- Browser testing with DevTools
- CI/CD and automation
- Code review and quality
- Code simplification
- Context engineering
- Debugging and error recovery
- Deprecation and migration
- Documentation and ADRs
- Doubt-driven development
- Frontend UI engineering
- Git workflow and versioning
- Idea refinement
- Incremental implementation
- Interview-driven clarification
- Nuxt framework guidance
- Observability and instrumentation
- Performance optimization
- Planning and task breakdown
- Security and hardening
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
