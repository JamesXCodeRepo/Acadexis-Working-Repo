import {
  AgentInput,
  AgentOutput,
  AgentRef,
  AgentRole,
  AgentSpec,
} from './types';

export interface Agent {
  id: string;
  role: AgentRole;
  spec: AgentSpec;
  run(input: AgentInput): Promise<AgentOutput>;
}

export abstract class BaseAgent implements Agent {
  id: string;
  role: AgentRole;
  spec: AgentSpec;

  protected constructor(id: string, role: AgentRole, spec: AgentSpec) {
    this.id = id;
    this.role = role;
    this.spec = spec;
  }

  abstract run(input: AgentInput): Promise<AgentOutput>;

  protected makeRef(): AgentRef {
    return { id: this.id, role: this.role };
  }
}

