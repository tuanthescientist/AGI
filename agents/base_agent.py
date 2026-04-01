"""
Agent Framework: Base Agent and Agent Execution
"""

from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class AgentConfig:
    """Agent configuration"""
    name: str
    role: str = "general"
    reasoning_pattern: str = "cot"  # cot, react, tot, got
    memory_enabled: bool = True
    self_improvement_enabled: bool = True
    max_iterations: int = 10
    timeout: int = 300  # seconds
    metadata: Dict[str, Any] = field(default_factory=dict)


@dataclass
class AgentMessage:
    """Message in agent communication"""
    sender: str
    recipient: str
    content: str
    message_type: str = "task"  # task, result, feedback, query
    timestamp: datetime = field(default_factory=datetime.now)
    parent_id: Optional[str] = None


class BaseAgent:
    """Base Agent class with reasoning and memory"""
    
    def __init__(self, config: AgentConfig):
        self.config = config
        self.name = config.name
        self.role = config.role
        self.reasoning_pattern = config.reasoning_pattern
        
        self.memory = {}
        self.execution_history: List[Dict[str, Any]] = []
        self.task_queue: List[Dict[str, Any]] = []
        self.message_history: List[AgentMessage] = []
        
        logger.info(f"Initialized agent: {self.name} (role: {self.role})")
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process a task"""
        logger.info(f"[{self.name}] Processing task: {task.get('description', 'Unknown')}")
        
        execution_log = {
            'agent': self.name,
            'task': task,
            'start_time': datetime.now(),
            'steps': []
        }
        
        # Step 1: Reason
        reasoning_step = {
            'phase': 'reasoning',
            'pattern': self.reasoning_pattern,
            'input': task.get('input', '')
        }
        
        if self.reasoning_pattern == 'cot':
            reasoning_step['output'] = f"Reasoning through: {task.get('description')}"
        elif self.reasoning_pattern == 'react':
            reasoning_step['output'] = f"Plan and act on: {task.get('description')}"
        else:
            reasoning_step['output'] = f"Analyzing: {task.get('description')}"
        
        execution_log['steps'].append(reasoning_step)
        
        # Step 2: Act
        action_step = {
            'phase': 'action',
            'action_type': task.get('action', 'generic'),
            'result': f"Executed {task.get('action', 'action')}"
        }
        execution_log['steps'].append(action_step)
        
        # Step 3: Reflect (if enabled)
        if self.config.self_improvement_enabled:
            reflection_step = {
                'phase': 'reflection',
                'feedback': f"Task progress: {action_step['result']}"
            }
            execution_log['steps'].append(reflection_step)
        
        execution_log['end_time'] = datetime.now()
        execution_log['success'] = True
        
        self.execution_history.append(execution_log)
        
        result = {
            'agent': self.name,
            'success': True,
            'result': action_step['result'],
            'execution_log': execution_log
        }
        
        logger.info(f"[{self.name}] Task completed successfully")
        return result
    
    def send_message(self, recipient: str, content: str, message_type: str = "task") -> AgentMessage:
        """Send message to another agent"""
        message = AgentMessage(
            sender=self.name,
            recipient=recipient,
            content=content,
            message_type=message_type
        )
        self.message_history.append(message)
        logger.debug(f"[{self.name}] Message sent to {recipient}: {message_type}")
        return message
    
    def receive_message(self, message: AgentMessage):
        """Receive message from another agent"""
        self.message_history.append(message)
        logger.debug(f"[{self.name}] Message received from {message.sender}")
    
    def get_status(self) -> Dict[str, Any]:
        """Get agent status"""
        return {
            'name': self.name,
            'role': self.role,
            'reasoning_pattern': self.reasoning_pattern,
            'tasks_executed': len(self.execution_history),
            'messages_sent': len([m for m in self.message_history if m.sender == self.name]),
            'messages_received': len([m for m in self.message_history if m.recipient == self.name]),
            'timestamp': datetime.now()
        }


class SpecializedAgent(BaseAgent):
    """Specialized agent with specific role"""
    
    def __init__(self, config: AgentConfig, specialization: str):
        super().__init__(config)
        self.specialization = specialization
        logger.info(f"[{self.name}] Specialized as: {specialization}")
    
    def process_task(self, task: Dict[str, Any]) -> Dict[str, Any]:
        """Process task with specialization"""
        logger.info(f"[{self.name}:{self.specialization}] Processing task")
        
        # Add specialization context
        task_with_spec = {**task, 'specialization_context': self.specialization}
        
        result = super().process_task(task_with_spec)
        result['specialization'] = self.specialization
        
        return result


class ResearcherAgent(SpecializedAgent):
    """Agent specialized in research"""
    
    def __init__(self, name: str = "Researcher"):
        config = AgentConfig(
            name=name,
            role="research",
            reasoning_pattern="cot"
        )
        super().__init__(config, "research")
    
    def research(self, topic: str) -> Dict[str, Any]:
        """Conduct research on a topic"""
        task = {
            'description': f'Research topic: {topic}',
            'action': 'research',
            'input': topic
        }
        return self.process_task(task)


class PlannerAgent(SpecializedAgent):
    """Agent specialized in planning"""
    
    def __init__(self, name: str = "Planner"):
        config = AgentConfig(
            name=name,
            role="planning",
            reasoning_pattern="tot"
        )
        super().__init__(config, "planning")
    
    def plan(self, objective: str) -> Dict[str, Any]:
        """Create a plan"""
        task = {
            'description': f'Create plan for: {objective}',
            'action': 'plan',
            'input': objective
        }
        return self.process_task(task)


class ExecutorAgent(SpecializedAgent):
    """Agent specialized in execution"""
    
    def __init__(self, name: str = "Executor"):
        config = AgentConfig(
            name=name,
            role="execution",
            reasoning_pattern="react"
        )
        super().__init__(config, "execution")
    
    def execute(self, plan: str) -> Dict[str, Any]:
        """Execute a plan"""
        task = {
            'description': f'Execute plan: {plan}',
            'action': 'execute',
            'input': plan
        }
        return self.process_task(task)


class CriticAgent(SpecializedAgent):
    """Agent specialized in critique and feedback"""
    
    def __init__(self, name: str = "Critic"):
        config = AgentConfig(
            name=name,
            role="critique",
            reasoning_pattern="cot"
        )
        super().__init__(config, "critique")
    
    def critique(self, work: str) -> Dict[str, Any]:
        """Critique work"""
        task = {
            'description': f'Critique: {work}',
            'action': 'critique',
            'input': work
        }
        result = self.process_task(task)
        
        # Add critique feedback
        result['critique_feedback'] = {
            'strengths': ['Well-structured', 'Clear reasoning'],
            'weaknesses': ['Could be more detailed'],
            'suggestions': ['Add more context', 'Consider edge cases']
        }
        
        return result


class MonitorAgent(SpecializedAgent):
    """Agent specialized in monitoring and oversight"""
    
    def __init__(self, name: str = "Monitor"):
        config = AgentConfig(
            name=name,
            role="monitoring",
            reasoning_pattern="cot"
        )
        super().__init__(config, "monitoring")
    
    def monitor(self, agents: List[BaseAgent]) -> Dict[str, Any]:
        """Monitor team of agents"""
        monitoring_report = {
            'timestamp': datetime.now(),
            'agents_monitored': len(agents),
            'agent_statuses': []
        }
        
        for agent in agents:
            status = agent.get_status()
            monitoring_report['agent_statuses'].append(status)
        
        return monitoring_report


if __name__ == "__main__":
    # Example: Create different agents
    researcher = ResearcherAgent("Dr. Smith")
    planner = PlannerAgent("Strategic Planner")
    executor = ExecutorAgent("Action Taker")
    critic = CriticAgent("Quality Assurance")
    
    print("=== Agent Communication Example ===\n")
    
    # Research phase
    research_result = researcher.research("Advanced AI techniques")
    print(f"[Research] {researcher.name}: {research_result['result']}")
    
    # Planning phase
    plan_result = planner.plan(research_result['result'])
    print(f"[Planning] {planner.name}: {plan_result['result']}")
    
    # Execution phase
    exec_result = executor.execute(plan_result['result'])
    print(f"[Execution] {executor.name}: {exec_result['result']}")
    
    # Critique phase
    critique_result = critic.critique(exec_result['result'])
    print(f"[Critique] {critic.name}: {critique_result['result']}")
    
    # Get statuses
    print("\n=== Agent Statuses ===")
    for agent in [researcher, planner, executor, critic]:
        status = agent.get_status()
        print(f"{agent.name}: executed {status['tasks_executed']} tasks")
