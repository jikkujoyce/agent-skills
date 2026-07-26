# Route Maps — entry points, spines, and runtime probes by project shape

Heuristics for finding where execution starts, which vertical slice to trace first, and how to get the runtime to grade predictions — by common project shape. Identify the shape from manifests and directory names during Phase 1 scouting, then use the matching map. Each map lists: identity clues, the entry point, the best first spine, landmarks worth a stop, a runtime probe, and prediction prompts that tend to work.

## Web backend / API server

- **Identity clues**: framework dependency (express, fastify, flask, fastapi, django, rails, spring-boot, gin, axum…), a `routes/` or `controllers/` directory, a Dockerfile exposing a port.
- **Entry**: the server bootstrap (`main`, `app`, `server` file) → where routes get registered.
- **Best first spine**: one authenticated CRUD endpoint — a single pass touches routing, middleware, auth, validation, business logic, persistence, and serialization.
- **Landmarks**: middleware chain and its order; where the DB connection or session lives; the error-handling convention.
- **Runtime probe**: breakpoint inside one handler plus one `curl`; or run the integration suite and read its setup — fixtures reveal the real dependency graph.
- **Prediction prompts**: "Which middleware do you think runs before this handler?" / "Where do you expect the SQL to actually execute?"

## Frontend SPA

- **Identity clues**: react/vue/svelte/angular dependency, `src/components`, an `index.html` with a mount node.
- **Entry**: the mount (`main.tsx`, `index.js`) → root component → router.
- **Best first spine**: one user interaction → state change → re-render; or one page's data-fetch lifecycle from navigation to painted data.
- **Landmarks**: the state-management approach (context, redux, signals, stores); the data-fetching layer; route-to-component mapping.
- **Runtime probe**: framework devtools open (component and state inspector) while stepping a breakpoint in one state transition.
- **Prediction prompts**: "When this button is clicked, what has to change before the UI updates?" / "Where do you think the loading state lives?"

## CLI tool

- **Identity clues**: a `bin` field in the manifest, argparse/clap/cobra/click dependency, a `main` that parses args.
- **Entry**: `main` → command dispatch.
- **Best first spine**: one subcommand end-to-end — flags in, output and exit code out.
- **Landmarks**: config resolution order (flags vs env vs config file); the output-formatting layer; how errors reach the terminal.
- **Runtime probe**: run one subcommand under a debugger; `--help` output is a free map of the dispatch table.
- **Prediction prompts**: "If the same option is set in the config file and as a flag, which wins — and where would that be decided?"

## Library / SDK

- **Identity clues**: no entry binary; an exported public API surface; README dominated by usage examples.
- **Entry**: the public API itself — start from the README's hello-world snippet and trace *that*.
- **Best first spine**: the canonical usage example, from the public call down to the core algorithm.
- **Landmarks**: the public/internal boundary (what's exported vs not); extension points and hooks; how backward compatibility is handled.
- **Runtime probe**: paste the README snippet into a REPL and step into it — the stack depth at the first real work *is* the architecture.
- **Prediction prompts**: "This one-liner in the README — how many layers deep do you think it goes before real work happens?"

## Data pipeline / batch jobs

- **Identity clues**: DAG definitions (airflow, dagster, prefect), a `jobs/` or `tasks/` directory, scheduler config, warehouse client dependencies.
- **Entry**: the DAG or schedule definition.
- **Best first spine**: one dataset from source to sink through its transforms.
- **Landmarks**: idempotency and retry handling; schema definitions; the backfill story.
- **Runtime probe**: run a single task locally on sample data — most frameworks have a one-task execution mode; find it before touching the DAG.
- **Prediction prompts**: "If this job runs twice for the same day, what happens — and where is that guaranteed?"

## Monorepo

- **Identity clues**: workspaces/packages configuration, multiple manifests, turborepo/nx/bazel/pants files.
- **First move**: map the package graph before anything else — which packages depend on which, and which shared core everything imports.
- **Best first spine**: one flow that crosses a package boundary, because in a monorepo the boundaries *are* the architecture.
- **Landmarks**: the shared core package; build orchestration; versioning policy between packages.
- **Runtime probe**: run one package's test suite in isolation, never the world's.
- **Scope hard**: tour one package plus its interface to the shared core, and name explicitly what you're skipping.

## Event-driven / message-based services

- **Identity clues**: broker dependencies (kafka, rabbitmq, sqs, nats), `consumers/` or `handlers/` directories, proto or schema registries.
- **Entry**: consumer registration — where handlers bind to topics or queues.
- **Best first spine**: one message type from producer through consumer to side effect.
- **Landmarks**: message schemas and their evolution; retry and dead-letter policy; ordering assumptions.
- **Runtime probe**: a local broker usually ships in docker-compose — publish one hand-crafted message and breakpoint the consumer.
- **Prediction prompts**: "If this consumer crashes mid-handler, what happens to the message?"

## When no shape fits

Fall back to universal heuristics, in rough order of yield:

1. Grep for a main-like entry point or ask the build system: what CI runs (`ci.yml`, `Makefile`, `justfile` targets) is executable truth about how the thing starts.
2. The most-imported source file is usually near the core — a quick import count often finds the center of gravity.
3. The largest test file at the highest level of abstraction describes the system's intended behavior better than the README.
4. The newest merged code shows the current idiom — old code may predate the conventions the team now enforces.
5. If anything runs at all, run it — a stack trace from one real invocation outranks every heuristic above.
