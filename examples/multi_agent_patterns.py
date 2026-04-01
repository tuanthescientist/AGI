"""
Comprehensive Example: Multi-Agent System Patterns
====================================================

This demonstrates advanced patterns:
1. Sequential communication
2. Hierarchical coordination
3. Parallel execution
4. Debate-based consensus
"""

import sys
sys.path.insert(0, '.')

from memory.hybrid_memory import HybridMemorySystem
from reasoning.reasoning_patterns import ReasoningSelector, ReAct
from agents.base_agent import (
    ResearcherAgent, PlannerAgent, ExecutorAgent, CriticAgent, MonitorAgent
)
from agents.crew import Crew, CrewBuilder, CommunicationPattern


def example_sequential_crew():
    """Chain-of-agents: output of agent i → input of agent i+1"""
    print("\n" + "=" * 70)
    print("Pattern 1: Sequential Communication (Pipeline)")
    print("=" * 70)
    print("Input → Researcher → Planner → Executor → Output")
    
    builder = CrewBuilder("Sequential Pipeline", CommunicationPattern.SEQUENTIAL)
    
    builder.add_agent(ResearcherAgent(name="Researcher"), "research")
    builder.add_agent(PlannerAgent(name="Planner"), "planning")
    builder.add_agent(ExecutorAgent(name="Executor"), "execution")
    
    crew = builder.build()
    
    task = {
        "description": "End-to-end ML pipeline: research problem → plan solution → execute implementation",
        "input": "Build a sentiment analysis system for customer reviews"
    }
    
    result = crew.execute_task(task)
    
    print(f"\nSequential Execution:")
    print(f"  Total steps: {result['execution_steps']}")
    print(f"  Status: {result['status']}")
    print(f"  Communication: Each agent processed the output of previous agent")
    

def example_hierarchical_crew():
    """Supervisor coordinates agents with explicit delegation"""
    print("\n" + "=" * 70)
    print("Pattern 2: Hierarchical Coordination")
    print("=" * 70)
    print("Supervisor → [Researcher, Planner, Executor] → Synthesis")
    
    builder = CrewBuilder("Research Hub", CommunicationPattern.HIERARCHICAL)
    
    builder.add_agent(ResearcherAgent(name="ResearchSpecialist"), "research")
    builder.add_agent(PlannerAgent(name="ArchitectureDesigner"), "planning")
    builder.add_agent(ExecutorAgent(name="DevelopmentLead"), "execution")
    
    supervisor = PlannerAgent(name="ProjectManager", role="Research Supervisor")
    builder.set_supervisor(supervisor)
    
    crew = builder.build()
    
    task = {
        "description": "Coordinate research, planning, and execution for complex system",
        "input": "Design and prototype a multi-modal AGI system"
    }
    
    result = crew.execute_task(task)
    
    print(f"\nHierarchical Execution:")
    print(f"  Supervisor: ProjectManager")
    print(f"  Execution steps: {result['execution_steps']}")
    print(f"  Status: {result['status']}")
    print(f"  Coordination: Supervisor analyzed problem → delegated to specialists → synthesized results")


def example_parallel_crew():
    """All agents work independently on subtasks"""
    print("\n" + "=" * 70)
    print("Pattern 3: Parallel Execution")
    print("=" * 70)
    print("[Researcher] ↓")
    print("[Planner]    ↓ (independent) → Aggregation")
    print("[Executor]   ↓")
    
    builder = CrewBuilder("Parallel Task Force", CommunicationPattern.PARALLEL)
    
    builder.add_agent(ResearcherAgent(name="DataResearcher"), "research")
    builder.add_agent(PlannerAgent(name="MethodPlanner"), "planning")
    builder.add_agent(ExecutorAgent(name="ImplementationExpert"), "execution")
    
    crew = builder.build()
    
    task = {
        "description": "Explore solution space in parallel: research options, plan alternatives, prototype implementations",
        "input": "What are the best approaches for few-shot learning in LLMs?"
    }
    
    result = crew.execute_task(task)
    
    print(f"\nParallel Execution:")
    print(f"  Total agents: 3")
    print(f"  Execution steps: {result['execution_steps']}")
    print(f"  Status: {result['status']}")
    print(f"  Coordination: All 3 agents worked independently → results aggregated")


def example_debate_crew():
    """Multi-round debate: proposals → critiques → consensus"""
    print("\n" + "=" * 70)
    print("Pattern 4: Debate-Based Consensus")
    print("=" * 70)
    print("Round 1 (Proposals) → Round 2 (Critiques) → Round 3 (Consensus)")
    
    builder = CrewBuilder("Debate Committee", CommunicationPattern.DEBATE)
    
    builder.add_agent(ResearcherAgent(name="ProponentA"), "research")
    builder.add_agent(PlannerAgent(name="ProponentB"), "planning")
    builder.add_agent(CriticAgent(name="Critic"), "critique")
    
    crew = builder.build()
    
    task = {
        "description": "Debate trade-offs: accuracy vs interpretability in deep learning",
        "input": "Black-box deep learning models achieve better accuracy but lack interpretability. White-box models are interpretable but less accurate. Which approach is better for healthcare applications?"
    }
    
    result = crew.execute_task(task)
    
    print(f"\nDebate Execution:")
    print(f"  Execution steps: {result['execution_steps']}")
    print(f"  Status: {result['status']}")
    print(f"  Debate rounds: 3 complete")
    print(f"  Consensus reached: {result.get('consensus', 'Yes')}")


def example_memory_augmented_crew():
    """Crew with persistent memory across executions"""
    print("\n" + "=" * 70)
    print("Advanced: Memory-Augmented Crew (Learning Loop)")
    print("=" * 70)
    
    memory = HybridMemorySystem()
    
    builder = CrewBuilder("Learning Crew", CommunicationPattern.HIERARCHICAL)
    builder.add_agent(ResearcherAgent(name="Learner"), "research")
    builder.add_agent(ExecutorAgent(name="Practitioner"), "execution")
    supervisor = CriticAgent(name="Evaluator", role="Team Supervisor")
    builder.set_supervisor(supervisor)
    
    crew = builder.build()
    
    print("\nSimulating 3-iteration learning loop:")
    
    for iteration in range(1, 4):
        print(f"\n  Iteration {iteration}:")
        
        task = {
            "description": f"Learn and improve approach (iteration {iteration})",
            "input": f"Task variant {iteration}: Optimize model performance with constraint"
        }
        
        # Execute
        result = crew.execute_task(task)
        
        # Store lessons learned
        memory.record_experience(
            episode_id=f"crew_iter_{iteration}",
            steps=[
                {"action": "research_approach", "result": "completed"},
                {"action": "execute_implementation", "result": "completed"},
                {"action": "critic_feedback", "result": f"iteration {iteration} feedback"}
            ],
            outcome="success" if iteration % 2 == 0 else "partial_success",
            reflection=f"Learned approach for constraint handling in iteration {iteration}"
        )
        
        # Retrieve lessons
        success_rate = memory.get_episodic_memory().get_success_rate()
        procedural_skills = len(memory.get_procedural_memory().skills)
        
        print(f"    Status: {result['status']}")
        print(f"    Memory - Success rate: {success_rate:.1%}, Skills learned: {procedural_skills}")
    
    print("\n  Final memory state:")
    print(f"    {memory.get_memory_status()}")


def example_multi_crew_orchestration():
    """Two crews working together: research crew → execution crew"""
    print("\n" + "=" * 70)
    print("Advanced: Multi-Crew Orchestration")
    print("=" * 70)
    print("Research Crew (discoveries) → Execution Crew (implementation)")
    
    # Crew 1: Research
    print("\n  Step 1: Research Crew (hierarchical)")
    research_builder = CrewBuilder("Research Crew", CommunicationPattern.HIERARCHICAL)
    research_builder.add_agent(ResearcherAgent(name="InfoGatherer"), "research")
    research_builder.add_agent(PlannerAgent(name="PatternAnalyzer"), "planning")
    research_supervisor = PlannerAgent(name="ResearchLead", role="Research Supervisor")
    research_builder.set_supervisor(research_supervisor)
    research_crew = research_builder.build()
    
    research_task = {
        "description": "Research state-of-the-art approaches",
        "input": "What are latest breakthroughs in efficient training methods?"
    }
    research_result = research_crew.execute_task(research_task)
    print(f"    Research findings ready: {research_result['status']}")
    
    # Crew 2: Execution
    print("\n  Step 2: Execution Crew (sequential, consuming research output)")
    exec_builder = CrewBuilder("Execution Crew", CommunicationPattern.SEQUENTIAL)
    exec_builder.add_agent(PlannerAgent(name="ImplementationPlanner"), "planning")
    exec_builder.add_agent(ExecutorAgent(name="Engineer"), "execution")
    exec_builder.add_agent(CriticAgent(name="Validator"), "validation")
    exec_crew = exec_builder.build()
    
    exec_task = {
        "description": "Implement based on research findings",
        "input": f"Implement approach from research phase: {research_result['status']}"
    }
    exec_result = exec_crew.execute_task(exec_task)
    print(f"    Implementation ready: {exec_result['status']}")
    
    print(f"\n  Multi-crew orchestration complete!")
    print(f"    Research phase: {research_result['execution_steps']} steps")
    print(f"    Execution phase: {exec_result['execution_steps']} steps")
    print(f"    Total pipeline: Research → Execution (knowledge transfer)")


def main():
    """Run all multi-agent examples"""
    print("\n" + "🚀" * 35)
    print("AGI Framework - Multi-Agent System Patterns")
    print("🚀" * 35)
    
    try:
        example_sequential_crew()
        example_hierarchical_crew()
        example_parallel_crew()
        example_debate_crew()
        example_memory_augmented_crew()
        example_multi_crew_orchestration()
        
        print("\n" + "✓" * 70)
        print("\n✅ All multi-agent examples completed successfully!")
        print("\nKey takeaways:")
        print("  ✓ Sequential: Linear pipeline for dependent tasks")
        print("  ✓ Hierarchical: Supervisor coordinates specialists")
        print("  ✓ Parallel: Independent agents explore solution space")
        print("  ✓ Debate: Multi-round consensus for trade-off decisions")
        print("  ✓ Memory-Augmented: Crews learn from experience")
        print("  ✓ Multi-Crew: Complex pipelines with knowledge transfer")
        print("\nNext: Read docs/deepdive/ for architecture and best practices!")
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
