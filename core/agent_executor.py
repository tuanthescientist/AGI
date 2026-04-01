"""
Graph-Based Agent Executor (LangGraph-inspired)
State machine orchestration for agent workflows
"""

from typing import Dict, Any, Optional, Callable, List, Tuple
from dataclasses import dataclass, field
from enum import Enum
import logging
import json
from datetime import datetime

logger = logging.getLogger(__name__)


class NodeType(Enum):
    """Node types in execution graph"""
    START = "start"
    REASONING = "reasoning"
    TOOL_CALL = "tool_call"
    ACTION = "action"
    DECISION = "decision"
    REFLECTION = "reflection"
    END = "end"


@dataclass
class Node:
    """Execution node in the graph"""
    id: str
    node_type: NodeType
    description: str
    executor: Optional[Callable] = None
    config: Dict[str, Any] = field(default_factory=dict)


@dataclass
class Edge:
    """Transition between nodes"""
    source: str
    target: str
    condition: Optional[Callable] = None  # Returns True to follow this edge
    label: str = ""


@dataclass
class ExecutionState:
    """Current execution state"""
    node_id: str
    state_data: Dict[str, Any] = field(default_factory=dict)
    history: List[Dict[str, Any]] = field(default_factory=list)
    step_count: int = 0
    is_final: bool = False
    timestamp: datetime = field(default_factory=datetime.now)


class StateGraph:
    """Directed graph for agent execution"""
    
    def __init__(self, start_node_id: str):
        self.start_node = start_node_id
        self.nodes: Dict[str, Node] = {}
        self.edges: List[Edge] = []
        self.end_nodes: set = set()
        
    def add_node(self, node: Node):
        """Add node to graph"""
        self.nodes[node.id] = node
        logger.debug(f"Added node: {node.id}")
    
    def add_edge(self, source: str, target: str, condition: Optional[Callable] = None,
                label: str = ""):
        """Add edge between nodes"""
        edge = Edge(source=source, target=target, condition=condition, label=label)
        self.edges.append(edge)
        logger.debug(f"Added edge: {source} -> {target}")
    
    def add_end_node(self, node_id: str):
        """Mark node as end node"""
        self.end_nodes.add(node_id)
    
    def get_next_nodes(self, current_node_id: str, state: ExecutionState) -> List[str]:
        """Get possible next nodes from current state"""
        next_nodes = []
        
        for edge in self.edges:
            if edge.source == current_node_id:
                # Check condition
                if edge.condition is None or edge.condition(state):
                    next_nodes.append(edge.target)
        
        return next_nodes
    
    def compile(self) -> 'CompiledGraph':
        """Compile graph for execution"""
        return CompiledGraph(self)


class CompiledGraph:
    """Compiled and executable graph"""
    
    def __init__(self, state_graph: StateGraph):
        self.graph = state_graph
        self.execution_traces: List[Dict[str, Any]] = []
        
    def execute(self, initial_state: Dict[str, Any], max_steps: int = 100) -> ExecutionState:
        """Execute the graph"""
        state = ExecutionState(
            node_id=self.graph.start_node,
            state_data=initial_state.copy()
        )
        
        execution_trace = {
            'start_time': datetime.now(),
            'initial_state': initial_state,
            'steps': []
        }
        
        logger.info(f"Starting graph execution from node: {self.graph.start_node}")
        
        while not state.is_final and state.step_count < max_steps:
            current_node = self.graph.nodes.get(state.node_id)
            
            if current_node is None:
                logger.error(f"Node {state.node_id} not found")
                state.is_final = True
                break
            
            # Execute node
            step_log = {
                'step': state.step_count,
                'node_id': state.node_id,
                'node_type': current_node.node_type.value,
                'timestamp': datetime.now().isoformat()
            }
            
            try:
                if current_node.executor:
                    result = current_node.executor(state)
                    state.state_data['last_result'] = result
                    step_log['result'] = str(result)
                else:
                    step_log['result'] = "no_executor"
                
                state.history.append(step_log)
                execution_trace['steps'].append(step_log)
                
            except Exception as e:
                logger.error(f"Error executing node {state.node_id}: {e}")
                step_log['error'] = str(e)
                state.state_data['error'] = str(e)
                state.history.append(step_log)
                
                # Try to navigate to error handler if exists
                next_nodes = self.graph.get_next_nodes(state.node_id, state)
                if next_nodes:
                    state.node_id = next_nodes[0]
                else:
                    state.is_final = True
                    break
            
            # Determine next node
            next_nodes = self.graph.get_next_nodes(state.node_id, state)
            
            if not next_nodes:
                # No outgoing edges - check if end node
                if state.node_id in self.graph.end_nodes:
                    state.is_final = True
                    logger.info(f"Reached end node: {state.node_id}")
                else:
                    logger.warning(f"Node {state.node_id} has no outgoing edges and is not marked as end")
                    state.is_final = True
            else:
                # Move to next node (choose first for now - could be random/priority)
                state.node_id = next_nodes[0]
            
            state.step_count += 1
        
        execution_trace['end_time'] = datetime.now()
        execution_trace['total_steps'] = state.step_count
        execution_trace['is_final'] = state.is_final
        
        self.execution_traces.append(execution_trace)
        logger.info(f"Graph execution completed: {state.step_count} steps, final={state.is_final}")
        
        return state
    
    def get_execution_trace(self) -> List[Dict[str, Any]]:
        """Get all execution traces"""
        return self.execution_traces
    
    def save_trace(self, filepath: str):
        """Save execution trace to file"""
        with open(filepath, 'w') as f:
            json.dump(self.execution_traces, f, indent=2, default=str)
        logger.info(f"Execution trace saved to {filepath}")


class AgentGraphBuilder:
    """Builder for constructing agent execution graphs"""
    
    def __init__(self, agent_name: str):
        self.agent_name = agent_name
        self.graph = StateGraph("start")
        
    def add_thinking_node(self, node_name: str = "think"):
        """Add reasoning/thinking node"""
        def think_executor(state: ExecutionState) -> str:
            return f"Reasoning about: {state.state_data.get('input', 'No input')}"
        
        node = Node(
            id=node_name,
            node_type=NodeType.REASONING,
            description="Agent thinking/reasoning",
            executor=think_executor
        )
        self.graph.add_node(node)
        return self
    
    def add_tool_call_node(self, node_name: str = "tool_call"):
        """Add tool calling node"""
        def tool_executor(state: ExecutionState) -> str:
            tool_name = state.state_data.get('selected_tool', 'unknown')
            return f"Calling tool: {tool_name}"
        
        node = Node(
            id=node_name,
            node_type=NodeType.TOOL_CALL,
            description="Call external tools",
            executor=tool_executor
        )
        self.graph.add_node(node)
        return self
    
    def add_reflection_node(self, node_name: str = "reflect"):
        """Add reflection/critique node"""
        def reflect_executor(state: ExecutionState) -> str:
            return f"Reflecting on outcome: {state.state_data.get('last_result', 'No result')}"
        
        node = Node(
            id=node_name,
            node_type=NodeType.REFLECTION,
            description="Agent self-reflection",
            executor=reflect_executor
        )
        self.graph.add_node(node)
        return self
    
    def add_decision_node(self, node_name: str = "decide"):
        """Add decision node that routes to different branches"""
        def decide_executor(state: ExecutionState) -> str:
            # Just return the last result for now
            return state.state_data.get('last_result', 'continue')
        
        node = Node(
            id=node_name,
            node_type=NodeType.DECISION,
            description="Conditional routing",
            executor=decide_executor
        )
        self.graph.add_node(node)
        return self
    
    def connect(self, source: str, target: str, condition: Optional[Callable] = None):
        """Connect two nodes"""
        self.graph.add_edge(source, target, condition=condition)
        return self
    
    def set_end_nodes(self, node_ids: List[str]):
        """Set end nodes"""
        for node_id in node_ids:
            self.graph.add_end_node(node_id)
        return self
    
    def build(self) -> CompiledGraph:
        """Build and compile the graph"""
        logger.info(f"Building agent graph: {self.agent_name}")
        return self.graph.compile()


# Example: ReAct graph pattern
def create_react_graph() -> CompiledGraph:
    """Create a ReAct (Reasoning + Acting) graph"""
    builder = AgentGraphBuilder("ReAct Agent")
    
    builder.add_thinking_node("think")
    builder.add_tool_call_node("act")
    builder.add_reflection_node("observe")
    builder.add_decision_node("decide")
    
    # Connect nodes: start -> think -> decide -> act -> observe -> think (loop) or end
    builder.connect("start", "think")
    builder.connect("think", "decide", condition=lambda s: True)
    
    def should_call_tool(state: ExecutionState) -> bool:
        """Decide whether to call a tool"""
        return state.state_data.get('needs_tool', False)
    
    def should_continue(state: ExecutionState) -> bool:
        """Decide whether to continue or end"""
        return state.step_count < 5  # Max 5 steps
    
    builder.connect("decide", "act", condition=should_call_tool)
    builder.connect("decide", "end", condition=lambda s: not should_call_tool(s))
    builder.connect("act", "observe")
    builder.connect("observe", "think", condition=should_continue)
    builder.connect("observe", "end", condition=lambda s: not should_continue(s))
    
    builder.set_end_nodes(["end"])
    
    # Add start and end nodes
    builder.graph.add_node(Node(id="start", node_type=NodeType.START, description="Start"))
    builder.graph.add_node(Node(id="end", node_type=NodeType.END, description="End"))
    
    graph = builder.build()
    logger.info("ReAct graph created successfully")
    return graph


if __name__ == "__main__":
    # Test ReAct graph
    graph = create_react_graph()
    
    initial_state = {
        'input': 'Solve this problem',
        'needs_tool': True
    }
    
    state = graph.execute(initial_state)
    
    print(f"\nExecution completed:")
    print(f"  Final node: {state.node_id}")
    print(f"  Steps: {state.step_count}")
    print(f"  Final state data: {state.state_data}")
    print(f"  History length: {len(state.history)}")
