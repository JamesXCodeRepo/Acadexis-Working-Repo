import { AgentInput, AgentOutput, AgentRole, AgentSpec } from './types';
import { BaseAgent } from './baseAgent';

export class ArchitectAgent extends BaseAgent {
  constructor(spec: AgentSpec) {
    super('architect', 'architect' as AgentRole, spec);
  }

  async run(input: AgentInput): Promise<AgentOutput> {
    // Integration point for design‑level reasoning.
    throw new Error('ArchitectAgent.run is not implemented. Integrate with your LLM/orchestrator here.');
  }
}

