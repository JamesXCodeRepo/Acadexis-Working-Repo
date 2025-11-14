 # AI Dev Team Framework Template

A reusable, language‑agnostic template for building an “AI dev team” that can plan, code, review, and (optionally) deploy across multiple projects and repos.

---

## 1. Architecture Overview

Structure the system into three main layers:

- **Orchestrator** – Manages workflows, task state, and routing between agents.
- **Agents** – Role‑specialized workers (Planner, Architect, Coder, Reviewer, Ops).
- **Tools / Adapters** – Concrete actions like reading/writing code, running tests, opening PRs, or triggering deployments.

### Suggested Project Layout

Adapt names and file types to your stack (e.g., `.ts`, `.py`):

- `orchestrator/`
  - `workflow_engine.*` – State machine / graph runner
  - `task_router.*` – Maps tasks → workflows
- `agents/`
  - `planner_agent.*`
  - `architect_agent.*`
  - `coder_agent.*`
  - `reviewer_agent.*`
  - `ops_agent.*`
- `tools/`
  - `codebase_adapter.*` – File system, git, search
  - `command_runner.*` – Tests/builds/linters
  - `repo_host_adapter.*` – GitHub/GitLab API
  - `ci_cd_adapter.*`
- `configs/`
  - `projects.yaml` – Per‑repo configuration
  - `workflows.yaml` – Reusable workflows
  - `standards/` – Style, security, architecture guides
- `runtime/`
  - `task_state_store.*`
  - `logs/`

---

## 2. Core Data Models (Conceptual)

These abstractions should exist in your chosen language as interfaces/classes.

### Task

Represents an incoming work item (issue, feature, etc.):

```text
Task {
  id: string
  projectId: string
  type: "bugfix" | "feature" | "refactor" | "chore" | ...
  title: string
  description: string
  source: "manual" | "github_issue" | "gitlab_issue" | "cli" | ...
  metadata: Map<string, any>  // labels, priority, tags, etc.
}
```

### Artifact

Represents things agents produce and share:

```text
Artifact {
  id: string
  type: "spec" | "design" | "plan" | "patch" | "pr" | "review" | "deployment" | "log" | "note"
  taskId: string
  content: any           // text, JSON, diff, etc.
  createdBy: AgentRef
  createdAt: DateTime
}
```

### Agent

Role‑specialized worker that uses tools to act on artifacts:

```text
Agent {
  id: string
  role: "planner" | "architect" | "coder" | "reviewer" | "ops"
  capabilities: string[]    // "plan", "design", "edit_code", "run_tests", ...
  run(input: AgentInput) -> AgentOutput
}

AgentInput {
  task: Task
  artifacts: Artifact[]
  context: ExecutionContext
}

AgentOutput {
  newArtifacts: Artifact[]
  nextAction: "continue" | "handoff" | "done" | "needs_human"
  handoffTo?: AgentRef | WorkflowStepId
}
```

### Tool

Abstracts concrete actions (code, commands, CI, etc.):

```text
Tool {
  id: string
  type: "codebase" | "command" | "repo_host" | "ci_cd" | ...
  call(params: ToolParams) -> ToolResult
}
```

### ExecutionContext

Standard context passed to every agent:

```text
ExecutionContext {
  project: ProjectConfig
  tools: ToolRegistry
  standards: StandardsConfig
  logger: Logger
}
```

---

## 3. Workflow / State Machine Template

Define workflows as graphs of steps that bind roles to actions, so you can reuse them across projects.

### Workflow Schema

```text
Workflow {
  id: string
  name: string
  applicableTaskTypes: string[]    // e.g. ["bugfix", "feature"]
  steps: WorkflowStep[]
}

WorkflowStep {
  id: string
  name: string                     // "Plan", "Design", "Implement", ...
  agentRole: "planner" | "architect" | "coder" | "reviewer" | "ops"
  inputSelector: (Task, Artifact[]) -> AgentInput
  transition: (AgentOutput) -> NextStepDecision
}

NextStepDecision {
  nextStepId: string | null
  status: "in_progress" | "blocked" | "waiting_human" | "completed"
}
```

### Standard Dev Workflow

Default step sequence you can reuse for new or existing projects:

1. **Plan** (`planner`)
   - Turn vague task into a clear spec + acceptance criteria.
2. **Design** (`architect`)
   - Propose design, APIs, data models, and file/function changes.
3. **Implement** (`coder`)
   - Edit code, add tests, run tools; produce patch/PR artifact.
4. **Review** (`reviewer`)
   - Review diff, check against standards, request changes or approve.
5. **Ops** (`ops`)
   - Deploy, or prepare a deployment plan that a human can run.

You can define alternate workflows, such as:

- `bugfix-fast-flow` (Plan → Implement → Review)
- `refactor-flow` (Plan → Design → Implement → Review)

---

## 4. Project Configuration Template

Configure everything that varies per repo/project in one place.

### Example `projects.yaml` (Conceptual)

```yaml
projects:
  my-web-app:
    id: my-web-app
    repo:
      host: github
      owner: my-org
      name: my-web-app
      defaultBranch: main
    tech_stack:
      languages: ["typescript"]
      frameworks: ["react", "node"]
    commands:
      test: "npm test"
      lint: "npm run lint"
      build: "npm run build"
    paths:
      src: "src/"
      tests: "tests/"
    workflows:
      default: "standard-dev-flow"
      bugfix: "bugfix-fast-flow"
    standards:
      styleGuide: "configs/standards/style_web.md"
      securityGuide: "configs/standards/security_default.md"
      architectureGuide: "configs/standards/arch_web.md"
```

For each new project:

- Add a `projectId`.
- Point to the repo and default branch.
- Define commands for `test`, `lint`, `build`, etc.
- Select appropriate workflows.
- Attach standards documents.

---

## 5. Agent Role Templates

Each agent has:

- **Inputs** – What they read (artifacts, standards, code).
- **Outputs** – What artifacts they must produce.
- **Checklists** – Explicit steps to raise quality and consistency.

You can encode these into prompts or function comments.

### Planner Agent

**Purpose:** Turn a vague issue into a clear, testable spec.

**Inputs:**

- `Task.description`, `Task.metadata`
- Relevant project standards (style/architecture/security)

**Outputs:**

- `Artifact(type="spec")` with:
  - Problem summary
  - Requirements (functional and non‑functional)
  - Non‑goals
  - Acceptance criteria (including negative cases)
  - Impact/risks
  - Suggested touched files or modules (if obvious)

**Checklist:**

- Clarify ambiguity by listing open questions.
- Provide at least one negative acceptance criterion.
- Propose a rough scope estimate (S/M/L).
- Identify obvious dependencies and risks.

---

### Architect Agent

**Purpose:** Turn spec into a concrete design and change plan.

**Inputs:**

- Spec artifact
- Project standards (especially architecture)
- Context about existing architecture (if documented)

**Outputs:**

- `Artifact(type="design")` with:
  - High‑level approach
  - API/data model changes (if any)
  - List of files/functions to add/modify
  - Edge cases and trade‑offs considered

**Checklist:**

- Respect existing architecture and conventions.
- Minimize surface area of changes.
- Call out potential performance/security implications.
- Flag breaking changes and migration needs.

---

### Coder Agent

**Purpose:** Implement design in code with tests and minimal diffs.

**Inputs:**

- Spec artifact
- Design artifact (if present)
- Codebase via `CodebaseAdapter`
- Commands via `CommandRunner`

**Outputs:**

- `Artifact(type="patch")`:
  - Diff, commit(s), or branch name containing changes.
- `Artifact(type="note")`:
  - Summary of changes
  - Tests added/updated
  - Manual test notes (if applicable)

**Checklist:**

- Keep changes minimal and localized.
- Update or add tests; don’t reduce coverage.
- Run `test`, `lint`, and `build` per `ProjectConfig`.
- Follow style and architecture guides.
- Avoid introducing new tech/deps without approval.

---

### Reviewer Agent

**Purpose:** Perform code review and enforce standards.

**Inputs:**

- Patch artifact
- Notes from coder
- Project standards (style, security, architecture)

**Outputs:**

- `Artifact(type="review")`:
  - Verdict: `approve` or `request_changes`
  - Comments grouped by category (correctness, tests, security, etc.)
  - Suggestions for improvement

**Checklist:**

- Validate logic and edge cases.
- Ensure tests cover core behavior and regression scenarios.
- Check error handling and input validation.
- Assess readability and complexity.
- Confirm adherence to standards and patterns.

---

### Ops Agent

**Purpose:** Handle deployment and operational aspects.

**Inputs:**

- Approved patch / PR artifact
- Project deployment config and CI/CD status

**Outputs:**

- `Artifact(type="deployment")`:
  - What was deployed, where, and how.
  - Links to pipelines/logs.
  - Verification steps.

**Checklist:**

- Ensure CI tests passed before deployment.
- Support feature flags or canary releases where possible.
- Provide rollback instructions or mechanisms.
- Confirm monitoring/alerting is in place for changes.

---

## 6. Tool Interface Templates

Standardize tool interfaces so agents can be reused across environments.

### Codebase Adapter

```text
CodebaseAdapter {
  readFile(path: string) -> string
  writeFile(path: string, content: string) -> void
  listFiles(pattern: string) -> string[]
  search(pattern: string, path: string) -> SearchResult[]
  createBranch(name: string, from: string) -> void
  diff(base: string, head: string) -> string
}
```

### Command Runner

```text
CommandRunner {
  run(command: string, cwd?: string, timeoutMs?: number) -> {
    exitCode: number
    stdout: string
    stderr: string
  }
}
```

### Repo Host Adapter

```text
RepoHostAdapter {
  createPullRequest(params) -> { url: string, id: string }
  commentOnPullRequest(prId: string, comment: string) -> void
  getIssue(externalId: string) -> Task
  updateIssue(externalId: string, fields: any) -> void
}
```

### CI/CD Adapter

```text
CiCdAdapter {
  triggerPipeline(ref: string) -> PipelineRun
  getPipelineStatus(id: string) -> PipelineStatus
}
```

---

## 7. Generic Orchestrator Flow

This flow is reusable for any task/project; only config differs.

```text
handleTask(taskId):

  task = loadTask(taskId)
  projectConfig = loadProjectConfig(task.projectId)
  workflow = selectWorkflow(task, projectConfig)

  state = loadOrInitWorkflowState(taskId, workflow)

  while state.status not in ["completed", "waiting_human"]:
    step = workflow.steps[state.currentStepId]

    inputArtifacts = selectArtifactsForStep(step, task)
    agent = getAgentByRole(step.agentRole)

    agentInput = {
      task,
      artifacts: inputArtifacts,
      context: buildExecutionContext(projectConfig)
    }

    output = agent.run(agentInput)
    persistArtifacts(output.newArtifacts)

    decision = step.transition(output)
    updateState(taskId, decision)

  return state
```

Key extension points:

- `selectWorkflow(task, projectConfig)` – choose `standard-dev-flow`, `bugfix-fast-flow`, etc.
- `selectArtifactsForStep` – e.g., for Review, gather spec, design, patch, notes.
- `step.transition` – decide whether to repeat step, move to next, or require human.

---

## 8. Applying This Template

### New Projects

1. Create a `ProjectConfig` entry:
   - Repo info, tech stack, commands, paths.
2. Attach standards documents:
   - Style, security, architecture.
3. Choose a default workflow:
   - Usually `standard-dev-flow`.
4. Run tasks through Plan → Implement → Review, with human final approval.

### Existing Projects

1. Add minimal config:
   - Repo host, project name, default branch.
   - Test/lint/build commands.
2. Start with limited scope:
   - Bugfixes or small refactors only.
3. Keep AI changes PR‑only:
   - No direct pushes to `main` or production.
4. Iterate:
   - Adjust checklists, workflows, and standards based on failures.

---

## 9. Next Steps for Implementation

To turn this template into a working system:

- Pick an implementation language (e.g., TypeScript or Python).
- Implement the core interfaces:
  - `Task`, `Artifact`, `Agent`, `Tool`, `ExecutionContext`.
- Implement a minimal `workflow_engine` using the schema here.
- Implement basic tools:
  - `CodebaseAdapter` for local git checkouts.
  - `CommandRunner` for running tests/linters.
- Implement at least two agents:
  - `CoderAgent` and `ReviewerAgent`.
- Add `ProjectConfig` for one repo and a `standard-dev-flow` workflow.

From there, you can expand roles (Planner, Architect, Ops) and sophistication over time.

---

