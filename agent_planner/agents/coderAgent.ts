import { AgentInput, AgentOutput, AgentRole, AgentSpec } from './types';
import { BaseAgent } from './baseAgent';

export class CoderAgent extends BaseAgent {
  constructor(spec: AgentSpec) {
    super('coder', 'coder' as AgentRole, spec);
  }

  async run(input: AgentInput): Promise<AgentOutput> {
    // Integration point for code editing, test execution, etc.
    throw new Error('CoderAgent.run is not implemented. Integrate with your LLM/orchestrator here.');
  }
}

