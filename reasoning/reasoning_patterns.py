"""
Reasoning Patterns for AGI Agents
ReAct (Reason + Act), CoT (Chain-of-Thought), ToT (Tree-of-Thoughts), etc.
"""

from typing import Dict, Any, List, Optional, Tuple
from dataclasses import dataclass, field
from datetime import datetime
import logging
import json

logger = logging.getLogger(__name__)


@dataclass
class ThoughtStep:
    """A single reasoning step"""
    step_num: int
    content: str
    reasoning_type: str  # 'hypothesis', 'analysis', 'decision', 'reflection'
    confidence: float = 0.5
    timestamp: datetime = field(default_factory=datetime.now)


@dataclass
class ReasoningChain:
    """Chain of reasoning steps"""
    chain_id: str
    steps: List[ThoughtStep] = field(default_factory=list)
    conclusion: Optional[str] = None
    success: bool = False
    num_branches: int = 1  # For Tree-of-Thoughts
    
    def add_step(self, step: ThoughtStep):
        """Add a reasoning step"""
        self.steps.append(step)
    
    def to_string(self) -> str:
        """Convert chain to readable string"""
        result = f"Chain {self.chain_id}:\n"
        for step in self.steps:
            result += f"  Step {step.step_num} [{step.reasoning_type}]: {step.content}\n"
        if self.conclusion:
            result += f"  Conclusion: {self.conclusion}\n"
        return result


class ReAct:
    """ReAct Pattern: Reasoning + Acting"""
    
    def __init__(self, max_iterations: int = 10):
        self.max_iterations = max_iterations
        self.chains: List[ReasoningChain] = []
        
    def reason_and_act(self, task: str, tools: Dict[str, Any]) -> ReasoningChain:
        """Execute ReAct: alternately reason and act"""
        chain = ReasoningChain(chain_id=f"react_{datetime.now().timestamp()}")
        
        logger.info(f"Starting ReAct for task: {task}")
        
        for i in range(self.max_iterations):
            # Step 1: Reason
            thought = ThoughtStep(
                step_num=i,
                content=f"Reasoning about next action for: {task[:50]}",
                reasoning_type='hypothesis'
            )
            chain.add_step(thought)
            logger.debug(f"ReAct Thought {i}: {thought.content}")
            
            # Step 2: Act (simulate tool calling)
            action_thought = ThoughtStep(
                step_num=i,
                content=f"Action: Would call tool to progress",
                reasoning_type='decision'
            )
            chain.add_step(action_thought)
            
            # Step 3: Observe & Reflect
            observation = ThoughtStep(
                step_num=i,
                content="Observation: Action completed",
                reasoning_type='analysis'
            )
            chain.add_step(observation)
            
            # Check if done
            if i > 1:  # For demo: stop after 2 iterations
                chain.conclusion = f"Completed task through {i+1} reasoning+action cycles"
                chain.success = True
                break
        
        self.chains.append(chain)
        logger.info(f"ReAct completed: {chain.conclusion}")
        return chain


class ChainOfThought:
    """Chain-of-Thought Reasoning"""
    
    def __init__(self):
        self.chains: List[ReasoningChain] = []
    
    def reason(self, problem: str) -> ReasoningChain:
        """Execute CoT: step-by-step reasoning"""
        chain = ReasoningChain(chain_id=f"cot_{datetime.now().timestamp()}")
        
        logger.info(f"Starting CoT for problem: {problem}")
        
        # Break down problem into steps
        steps_breakdown = [
            ("Understanding", f"Breaking down: {problem}"),
            ("Analysis", f"Analyzing relevant information"),
            ("Solution", f"Deriving solution path"),
            ("Verification", f"Verifying conclusion")
        ]
        
        for idx, (step_type, step_content) in enumerate(steps_breakdown):
            thought = ThoughtStep(
                step_num=idx,
                content=step_content,
                reasoning_type='analysis',
                confidence=0.7 + (idx * 0.05)
            )
            chain.add_step(thought)
            logger.debug(f"CoT {step_type}: {step_content}")
        
        chain.conclusion = "Reasoning chain completed"
        chain.success = True
        
        self.chains.append(chain)
        return chain


class TreeOfThoughts:
    """Tree-of-Thoughts: exploring multiple reasoning branches"""
    
    def __init__(self, branching_factor: int = 3, max_depth: int = 3):
        self.branching_factor = branching_factor
        self.max_depth = max_depth
        self.trees: List[Dict[str, Any]] = []
    
    def explore(self, problem: str) -> Tuple[ReasoningChain, Dict[str, Any]]:
        """Explore problem through tree structure"""
        logger.info(f"Starting ToT for problem: {problem}")
        
        # Create root chain
        root_chain = ReasoningChain(chain_id=f"tot_{datetime.now().timestamp()}")
        root_chain.num_branches = self.branching_factor
        
        # Simulate expanding tree
        tree_structure = {
            'root': problem,
            'depth': 0,
            'branches': []
        }
        
        # Expand to depth 1
        for branch_idx in range(self.branching_factor):
            branch_thought = ThoughtStep(
                step_num=branch_idx,
                content=f"Approach {branch_idx+1}: {problem[:30]}",
                reasoning_type='hypothesis'
            )
            root_chain.add_step(branch_thought)
            
            tree_structure['branches'].append({
                'branch_id': branch_idx,
                'approach': f"Approach {branch_idx+1}",
                'confidence': 0.6 + (branch_idx * 0.1)
            })
        
        # Select best branch (simulated)
        best_branch = max(tree_structure['branches'], key=lambda x: x['confidence'])
        root_chain.conclusion = f"Selected best approach: {best_branch['approach']}"
        root_chain.success = True
        
        self.trees.append(tree_structure)
        logger.info(f"ToT exploration complete: {len(tree_structure['branches'])} branches explored")
        
        return root_chain, tree_structure


class GraphOfThoughts:
    """Graph-of-Thoughts: reasoning with explicit dependencies"""
    
    def __init__(self):
        self.graphs: List[Dict[str, Any]] = []
    
    def reason_with_graph(self, problem: str, dependencies: Optional[List[Tuple[str, str]]] = None) -> ReasoningChain:
        """Reason using a DAG of thoughts"""
        chain = ReasoningChain(chain_id=f"got_{datetime.now().timestamp()}")
        
        logger.info(f"Starting GoT for problem: {problem}")
        
        # Create thought nodes
        thoughts = [
            ("Premise1", "Statement A"),
            ("Premise2", "Statement B"),
            ("Inference", "Conclusion from A and B"),
            ("Verification", "Verify conclusion")
        ]
        
        # Default dependencies if not provided
        if dependencies is None:
            dependencies = [
                ("Premise1", "Inference"),
                ("Premise2", "Inference"),
                ("Inference", "Verification")
            ]
        
        graph_struct = {
            'problem': problem,
            'nodes': [],
            'edges': dependencies
        }
        
        # Add thought nodes
        for idx, (name, content) in enumerate(thoughts):
            thought = ThoughtStep(
                step_num=idx,
                content=content,
                reasoning_type='analysis'
            )
            chain.add_step(thought)
            
            graph_struct['nodes'].append({
                'id': name,
                'content': content,
                'type': 'premise' if 'Premise' in name else 'inference'
            })
        
        chain.conclusion = "Graph-based reasoning complete"
        chain.success = True
        
        self.graphs.append(graph_struct)
        logger.info(f"GoT exploration complete: {len(graph_struct['nodes'])} nodes, {len(dependencies)} edges")
        
        return chain


class SelfReflection:
    """Self-Reflection pattern: agent critiques its own reasoning"""
    
    def __init__(self):
        self.reflections: List[Dict[str, Any]] = []
    
    def reflect_on_reasoning(self, reasoning_chain: ReasoningChain) -> Dict[str, Any]:
        """Agent critiques its own reasoning"""
        reflection = {
            'timestamp': datetime.now(),
            'chain_id': reasoning_chain.chain_id,
            'critique': {},
            'improvements': []
        }
        
        # Critique
        reflection['critique'] = {
            'num_steps': len(reasoning_chain.steps),
            'avg_confidence': sum(s.confidence for s in reasoning_chain.steps) / len(reasoning_chain.steps) if reasoning_chain.steps else 0,
            'success': reasoning_chain.success,
            'effectiveness': 'high' if reasoning_chain.success else 'low'
        }
        
        # Identify improvements
        if len(reasoning_chain.steps) < 3:
            reflection['improvements'].append("Add more reasoning steps")
        
        if reflection['critique']['avg_confidence'] < 0.7:
            reflection['improvements'].append("Increase confidence in reasoning")
        
        if not reasoning_chain.success:
            reflection['improvements'].append("Review reasoning strategy")
        
        self.reflections.append(reflection)
        logger.info(f"Reflection complete: {reflection['critique']['effectiveness']}, improvements: {len(reflection['improvements'])}")
        
        return reflection


class MetaReasoning:
    """Meta-Reasoning: reasoning about reasoning"""
    
    def __init__(self):
        self.meta_analyses: List[Dict[str, Any]] = []
    
    def analyze_reasoning_strategies(self, chains: List[ReasoningChain]) -> Dict[str, Any]:
        """Analyze and compare reasoning strategies"""
        analysis = {
            'timestamp': datetime.now(),
            'num_chains_analyzed': len(chains),
            'strategies': {},
            'best_strategy': None,
            'success_rate': 0
        }
        
        if not chains:
            return analysis
        
        # Analyze each chain
        success_count = sum(1 for c in chains if c.success)
        analysis['success_rate'] = success_count / len(chains)
        
        # Group by reasoning type
        for chain in chains:
            for step in chain.steps:
                if step.reasoning_type not in analysis['strategies']:
                    analysis['strategies'][step.reasoning_type] = {'count': 0, 'avg_confidence': 0}
                analysis['strategies'][step.reasoning_type]['count'] += 1
        
        # Find best performing strategy
        if analysis['strategies']:
            best = max(analysis['strategies'].items(), key=lambda x: x[1]['count'])
            analysis['best_strategy'] = best[0]
        
        self.meta_analyses.append(analysis)
        logger.info(f"Meta-analysis: {analysis['num_chains_analyzed']} chains, success rate: {analysis['success_rate']:.2%}")
        
        return analysis


class ReasoningSelector:
    """Selects best reasoning pattern for a given problem"""
    
    def __init__(self):
        self.react = ReAct()
        self.cot = ChainOfThought()
        self.tot = TreeOfThoughts()
        self.got = GraphOfThoughts()
        self.reflection = SelfReflection()
        self.meta = MetaReasoning()
    
    def select_and_reason(self, problem: str, problem_type: str = "generic") -> Dict[str, Any]:
        """Select reasoning pattern and execute"""
        logger.info(f"Selecting reasoning pattern for {problem_type} problem")
        
        result = {
            'problem': problem,
            'problem_type': problem_type,
            'reasoning_chains': []
        }
        
        # Select based on problem type
        if problem_type == "sequential":
            # Use ReAct for sequential action problems
            chain = self.react.reason_and_act(problem, {})
            result['selected_pattern'] = 'ReAct'
        
        elif problem_type == "analytical":
            # Use CoT for analytical problems
            chain = self.cot.reason(problem)
            result['selected_pattern'] = 'CoT'
        
        elif problem_type == "exploratory":
            # Use ToT for problems needing exploration
            chain, _ = self.tot.explore(problem)
            result['selected_pattern'] = 'ToT'
        
        else:
            # Default to CoT
            chain = self.cot.reason(problem)
            result['selected_pattern'] = 'CoT'
        
        result['reasoning_chains'].append(chain)
        
        # Self-reflect
        reflection = self.reflection.reflect_on_reasoning(chain)
        result['self_reflection'] = reflection
        
        logger.info(f"Reasoning complete using {result['selected_pattern']}")
        return result


if __name__ == "__main__":
    # Test different reasoning patterns
    selector = ReasoningSelector()
    
    # Test ReAct
    print("=== ReAct Example ===")
    result = selector.select_and_reason("Solve a complex problem", "sequential")
    print(result['reasoning_chains'][0].to_string())
    
    # Test CoT
    print("\n=== CoT Example ===")
    result = selector.select_and_reason("Analyze data", "analytical")
    print(result['reasoning_chains'][0].to_string())
