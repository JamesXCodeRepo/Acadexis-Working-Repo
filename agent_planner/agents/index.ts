// Factory wiring agent_specs.json into concrete agent instances.
import specsJson from '../agent_specs.json';
import { AgentsSpecsFile, AgentRole } from './types';
import { PlannerAgent } from './plannerAgent';
import { ArchitectAgent } from './architectAgent';
import { CoderAgent } from './coderAgent';
import { ReviewerAgent } from './reviewerAgent';
import { OpsAgent } from './opsAgent';
import { BaseAgent } from './baseAgent';

export type AgentMap = Record<AgentRole, BaseAgent>;

export function loadAgentSpecs(): AgentsSpecsFile {
  return specsJson as AgentsSpecsFile;
}

export function createAgentsFromSpecs(specs: AgentsSpecsFile = loadAgentSpecs()): AgentMap {
  const plannerSpec = specs.agents['planner'];
  const architectSpec = specs.agents['architect'];
  const coderSpec = specs.agents['coder'];
  const reviewerSpec = specs.agents['reviewer'];
  const opsSpec = specs.agents['ops'];

  if (!plannerSpec || !architectSpec || !coderSpec || !reviewerSpec || !opsSpec) {
    throw new Error('agent_specs.json is missing one or more required agent definitions.');
  }

  return {
    planner: new PlannerAgent(plannerSpec),
    architect: new ArchitectAgent(architectSpec),
    coder: new CoderAgent(coderSpec),
    reviewer: new ReviewerAgent(reviewerSpec),
    ops: new OpsAgent(opsSpec),
  };
}

