"""
Multi-Agent Crew Orchestration
Supervisor-based team coordination
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


class CommunicationPattern(Enum):
    """Communication patterns for agent cooperation"""
    SEQUENTIAL = "sequential"
    PARALLEL = "parallel"
    HIERARCHICAL = "hierarchical"
    DEBATE = "debate"  # Multi-agent critique


@dataclass
class CrewConfig:
    """Configuration for agent crew"""
    name: str
    communication_pattern: CommunicationPattern = CommunicationPattern.HIERARCHICAL
    max_iterations: int = 3
    enable_reflection: bool = True
    enable_tool_sharing: bool = True


class Crew:
    """Team of cooperative agents supervised by a central controller"""
    
    def __init__(self, config: CrewConfig):
        self.config = config
        self.name = config.name
        self.agents: Dict[str, Any] = {}
        self.supervisor = None
        self.message_queue: List[Dict[str, Any]] = []
        self.execution_log: List[Dict[str, Any]] = []
        self.state: Dict[str, Any] = {}
        
        logger.info(f"Initialized Crew: {self.name} (pattern: {config.communication_pattern.value})")
    
    def add_agent(self, agent_name: str, agent: Any, role: Optional[str] = None):
        """Add agent to crew"""
        self.agents[agent_name] = {
            'agent': agent,
            'role': role or agent.role,
            'status': 'idle',
            'assigned_tasks': []
        }
        logger.info(f"Added agent: {agent_name} (role: {role})")
    
    def set_supervisor(self, supervisor_agent: Any):
        """Set supervisor agent"""
        self.supervisor = supervisor_agent
        logger.info(f"Supervisor set: {supervisor_agent.name}")
    
    def execute_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task with crew"""
        logger.info(f"[Crew:{self.name}] Executing task: {task.get('description', 'Unknown')}")
        
        execution = {
            'task': task,
            'start_time': datetime.now(),
            'crew_name': self.name,
            'communication_pattern': self.config.communication_pattern.value,
            'phases': []
        }
        
        if self.config.communication_pattern == CommunicationPattern.SEQUENTIAL:
            execution['phases'] = self._execute_sequential(task)
        
        elif self.config.communication_pattern == CommunicationPattern.HIERARCHICAL:
            execution['phases'] = self._execute_hierarchical(task)
        
        elif self.config.communication_pattern == CommunicationPattern.PARALLEL:
            execution['phases'] = self._execute_parallel(task)
        
        elif self.config.communication_pattern == CommunicationPattern.DEBATE:
            execution['phases'] = self._execute_debate(task)
        
        execution['end_time'] = datetime.now()
        execution['success'] = True
        
        self.execution_log.append(execution)
        logger.info(f"[Crew:{self.name}] Task completed")
        
        return execution
    
    def _execute_sequential(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute sequentially: each agent passes result to next"""
        phases = []
        current_input = task.get('input', '')
        
        for agent_name, agent_info in self.agents.items():
            phase = {
                'agent': agent_name,
                'role': agent_info['role'],
                'input': current_input,
                'position': len(phases)
            }
            
            # Simulate execution
            result = f"Output from {agent_name} on: {current_input[:30]}"
            phase['output'] = result
            phase['success'] = True
            
            phases.append(phase)
            current_input = result  # Chain result to next agent
            
            logger.debug(f"Sequential phase: {agent_name} completed")
        
        return phases
    
    def _execute_hierarchical(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute hierarchically: supervisor delegates to agents"""
        phases = []
        
        if not self.supervisor:
            logger.warning("No supervisor available for hierarchical execution")
            return phases
        
        # Phase 1: Supervisor analysis
        supervisor_phase = {
            'agent': self.supervisor.name,
            'phase_type': 'analysis',
            'action': 'Analyze task and create plan'
        }
        phases.append(supervisor_phase)
        
        # Phase 2: Distribute to agents
        num_agents = len(self.agents)
        for idx, (agent_name, agent_info) in enumerate(self.agents.items()):
            agent_phase = {
                'agent': agent_name,
                'role': agent_info['role'],
                'phase_type': 'execution',
                'subtask': f"Subtask {idx+1}/{num_agents}",
                'result': f"Completed by {agent_name}"
            }
            phases.append(agent_phase)
            logger.debug(f"Hierarchical delegation: {agent_name}")
        
        # Phase 3: Supervisor synthesis
        synthesis_phase = {
            'agent': self.supervisor.name,
            'phase_type': 'synthesis',
            'action': 'Aggregate results and finalize'
        }
        phases.append(synthesis_phase)
        
        return phases
    
    def _execute_parallel(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute in parallel: all agents work independently"""
        phases = []
        
        parallel_phase = {
            'type': 'parallel_execution',
            'agents': [],
            'start_time': datetime.now()
        }
        
        for agent_name, agent_info in self.agents.items():
            agent_task = {
                'agent': agent_name,
                'role': agent_info['role'],
                'assigned_task': f"{agent_name}'s subtask"
            }
            parallel_phase['agents'].append(agent_task)
            logger.debug(f"Parallel task: {agent_name}")
        
        parallel_phase['end_time'] = datetime.now()
        phases.append(parallel_phase)
        
        return phases
    
    def _execute_debate(self, task: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Execute with debate: agents critique each other's outputs"""
        phases = []
        
        # Round 1: Initial proposals
        round1 = {
            'round': 1,
            'type': 'initial_proposals',
            'proposals': []
        }
        
        for agent_name, agent_info in self.agents.items():
            proposal = {
                'agent': agent_name,
                'proposal': f"Proposal from {agent_name}",
                'confidence': 0.6 + (len(round1['proposals']) * 0.1)
            }
            round1['proposals'].append(proposal)
        
        phases.append(round1)
        
        # Round 2: Critique
        round2 = {
            'round': 2,
            'type': 'critique',
            'critiques': []
        }
        
        for i, proposal in enumerate(round1['proposals']):
            critique = {
                'proposal_author': proposal['agent'],
                'critique_by': list(self.agents.keys())[(i+1) % len(self.agents)],
                'feedback': f"Feedback on {proposal['agent']}'s proposal"
            }
            round2['critiques'].append(critique)
        
        phases.append(round2)
        
        # Round 3: Final agreement
        round3 = {
            'round': 3,
            'type': 'agreement',
            'consensus': f"Consensus reached after debate"
        }
        phases.append(round3)
        
        logger.debug("Debate execution completed")
        return phases
    
    def get_crew_status(self) -> Dict[str, Any]:
        """Get overall crew status"""
        status = {
            'crew_name': self.name,
            'num_agents': len(self.agents),
            'communication_pattern': self.config.communication_pattern.value,
            'agents': {},
            'total_tasks_executed': len(self.execution_log),
            'has_supervisor': self.supervisor is not None,
            'timestamp': datetime.now()
        }
        
        for agent_name, agent_info in self.agents.items():
            status['agents'][agent_name] = {
                'role': agent_info['role'],
                'status': agent_info['status'],
                'tasks_assigned': len(agent_info['assigned_tasks'])
            }
        
        return status
    
    def save_execution_log(self, filepath: str):
        """Save crew execution log"""
        with open(filepath, 'w') as f:
            json.dump(self.execution_log, f, indent=2, default=str)
        logger.info(f"Execution log saved to {filepath}")


class CrewBuilder:
    """Builder for constructing crews"""
    
    def __init__(self, crew_name: str, pattern: CommunicationPattern = CommunicationPattern.HIERARCHICAL):
        self.config = CrewConfig(
            name=crew_name,
            communication_pattern=pattern
        )
        self.agents_to_add: List[tuple] = []
        self.supervisor_agent = None
    
    def add_agent(self, agent: Any, role: Optional[str] = None):
        """Add agent to builder"""
        self.agents_to_add.append((agent.name, agent, role))
        return self
    
    def set_supervisor(self, supervisor_agent: Any):
        """Set supervisor"""
        self.supervisor_agent = supervisor_agent
        return self
    
    def build(self) -> Crew:
        """Build crew"""
        crew = Crew(self.config)
        
        for agent_name, agent, role in self.agents_to_add:
            crew.add_agent(agent_name, agent, role)
        
        if self.supervisor_agent:
            crew.set_supervisor(self.supervisor_agent)
        
        logger.info(f"Crew built: {self.config.name} with {len(self.agents_to_add)} agents")
        return crew


# Example crew configurations
def create_research_crew() -> Crew:
    """Create a research crew"""
    from agents.base_agent import ResearcherAgent, CriticAgent, PlannerAgent
    
    builder = CrewBuilder(
        "Research Team",
        CommunicationPattern.HIERARCHICAL
    )
    
    researcher = ResearcherAgent("Senior Researcher")
    critic = CriticAgent("Quality Advisor")
    planner = PlannerAgent("Research Planner")
    
    builder.add_agent(researcher, "research")
    builder.add_agent(planner, "planning")
    builder.add_agent(critic, "critique")
    builder.set_supervisor(planner)
    
    return builder.build()


def create_execution_crew() -> Crew:
    """Create an execution crew"""
    from agents.base_agent import PlannerAgent, ExecutorAgent, MonitorAgent
    
    builder = CrewBuilder(
        "Execution Team",
        CommunicationPattern.SEQUENTIAL
    )
    
    planner = PlannerAgent("Execution Planner")
    executor = ExecutorAgent("Task Executor")
    monitor = MonitorAgent("Execution Monitor")
    
    builder.add_agent(planner, "planning")
    builder.add_agent(executor, "execution")
    builder.add_agent(monitor, "monitoring")
    builder.set_supervisor(planner)
    
    return builder.build()


if __name__ == "__main__":
    # Test different crew patterns
    print("=== Hierarchical Crew ===")
    
    from agents.base_agent import ResearcherAgent, PlannerAgent, ExecutorAgent, CriticAgent
    
    builder = CrewBuilder("Test Crew", CommunicationPattern.HIERARCHICAL)
    builder.add_agent(ResearcherAgent("R1"), "research")
    builder.add_agent(PlannerAgent("P1"), "planning")
    builder.add_agent(ExecutorAgent("E1"), "execution")
    builder.add_agent(CriticAgent("C1"), "critique")
    
    supervisor = PlannerAgent("Supervisor")
    builder.set_supervisor(supervisor)
    
    crew = builder.build()
    
    task = {
        'description': 'Solve complex problem',
        'input': 'Given problem statement'
    }
    
    result = crew.execute_task(task)
    print(f"Crew Status: {crew.get_crew_status()['num_agents']} agents")
    print(f"Execution Phases: {len(result['phases'])} phases")
