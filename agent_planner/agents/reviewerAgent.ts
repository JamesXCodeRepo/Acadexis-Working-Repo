import { AgentInput, AgentOutput, AgentRole, AgentSpec } from './types';
import { BaseAgent } from './baseAgent';

export class ReviewerAgent extends BaseAgent {
  constructor(spec: AgentSpec) {
    super('reviewer', 'reviewer' as AgentRole, spec);
  }

  async run(input: AgentInput): Promise<AgentOutput> {
    // Integration point for code review and standards enforcement.
    throw new Error('ReviewerAgent.run is not implemented. Integrate with your LLM/orchestrator here.');
  }
}

