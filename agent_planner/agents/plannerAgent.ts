import { AgentInput, AgentOutput, AgentRole, AgentSpec } from './types';
import { BaseAgent } from './baseAgent';

export class PlannerAgent extends BaseAgent {
  constructor(spec: AgentSpec) {
    super('planner', 'planner' as AgentRole, spec);
  }

  async run(input: AgentInput): Promise<AgentOutput> {
    // Integration point:
    // - Call your LLM with this.spec, input.task, project standards, and context
    // - Produce a "spec" Artifact matching the structure in agent_specs.json
    // For now, this is a placeholder that does not implement model calls.
    throw new Error('PlannerAgent.run is not implemented. Integrate with your LLM/orchestrator here.');
  }
}

