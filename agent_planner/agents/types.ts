export type AgentRole = 'planner' | 'architect' | 'coder' | 'reviewer' | 'ops';

export interface Task {
  id: string;
  projectId: string;
  type: string;
  title: string;
  description: string;
  source?: string;
  metadata?: Record<string, unknown>;
}

export interface Artifact {
  id: string;
  taskId: string;
  artifactType: string;
  content: unknown;
  createdBy: AgentRef;
  createdAt: string;
}

export interface AgentRef {
  id: string;
  role: AgentRole;
}

export interface ExecutionContext {
  projectId: string;
  projectConfig: ProjectConfig;
  tools: ToolRegistry;
  standards: StandardsConfig;
  logger?: Logger;
}

export interface ProjectConfig {
  id: string;
  repo?: {
    host: string;
    owner: string;
    name: string;
    defaultBranch?: string;
  };
  commands?: {
    test?: string;
    lint?: string;
    build?: string;
    [key: string]: string | undefined;
  };
  paths?: {
    src?: string;
    tests?: string;
    [key: string]: string | undefined;
  };
  workflows?: Record<string, string>;
  standards?: StandardsConfig;
}

export interface StandardsConfig {
  styleGuide?: string;
  securityGuide?: string;
  architectureGuide?: string;
  [key: string]: unknown;
}

export interface Logger {
  debug(message: string, meta?: unknown): void;
  info(message: string, meta?: unknown): void;
  warn(message: string, meta?: unknown): void;
  error(message: string, meta?: unknown): void;
}

export interface ToolRegistry {
  getTool(id: string): Tool | undefined;
}

export interface Tool {
  id: string;
  type: 'codebase' | 'command' | 'repo_host' | 'ci_cd' | string;
  call(params: Record<string, unknown>): Promise<unknown>;
}

export interface AgentInput {
  task: Task;
  artifacts: Artifact[];
  context: ExecutionContext;
}

export interface AgentOutput {
  newArtifacts: Artifact[];
  nextAction: 'continue' | 'handoff' | 'done' | 'needs_human';
  handoffTo?: AgentRef | string;
}

export interface AgentSpec {
  name: string;
  role: AgentRole | string;
  description: string;
  input: Record<string, unknown>;
  output: unknown;
  tools_available?: string[];
  validation_rules?: string[];
  handoff_criteria?: unknown;
  failure_handling?: string[];
}

export interface AgentsSpecsFile {
  agents: Record<string, AgentSpec>;
  workflow_handoff?: {
    sequence?: string[];
    failure_loops?: Record<string, string>;
  };
}

