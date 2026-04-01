"""
Quickstart Example: Basic AGI Usage (< 2 minutes)
================================================

This demonstrates the core features:
1. Memory system
2. Reasoning patterns
3. Single agent task processing
4. Multi-agent crew execution
"""

import sys
sys.path.insert(0, '.')

from memory.hybrid_memory import HybridMemorySystem
from reasoning.reasoning_patterns import ReasoningSelector
from agents.base_agent import ResearcherAgent, PlannerAgent, ExecutorAgent
from agents.crew import Crew, CrewBuilder, CommunicationPattern


def quickstart_basic_agent():
    """Example 1: Single agent processing a task"""
    print("=" * 60)
    print("Example 1: Basic Agent Task Processing")
    print("=" * 60)
    
    # Create an agent
    agent = ResearcherAgent(name="ResearchBot", role="Information Researcher")
    
    # Process a task
    task = {
        "description": "Research machine learning basics",
        "input": "What is transfer learning?"
    }
    
    result = agent.process_task(task)
    print(f"\n✓ Agent: {result['agent_name']}")
    print(f"  Status: {result['status']}")
    print(f"  Thought: {result['reasoning'][:100]}...")
    print(f"  Action taken: {result['action'][:80]}...")
    

def quickstart_memory():
    """Example 2: Hybrid memory system"""
    print("\n" + "=" * 60)
    print("Example 2: Hybrid Memory System")
    print("=" * 60)
    
    memory = HybridMemorySystem()
    
    # Store semantic knowledge
    memory.store_semantic(
        key="transfer_learning",
        value="Transfer learning reuses pre-trained models for new tasks",
        metadata={"source": "research", "confidence": 0.95}
    )
    
    # Store knowledge graph
    memory.store_knowledge(
        entity="Transfer Learning",
        attributes={
            "definition": "Using pre-trained models for new tasks",
            "benefits": ["Faster training", "Better performance", "Less data needed"],
            "use_cases": ["NLP", "Computer Vision", "Speech"]
        }
    )
    
    # Record an episode
    memory.record_experience(
        episode_id="exp_001",
        steps=[
            {"action": "load_pretrained_model", "result": "success"},
            {"action": "finetune_on_new_data", "result": "success"}
        ],
        outcome="success",
        reflection="Transfer learning significantly improved model performance"
    )
    
    # Get memory status
    status = memory.get_memory_status()
    print(f"\n✓ Memory Status:")
    print(f"  {status}")


def quickstart_reasoning():
    """Example 3: Automatic reasoning pattern selection"""
    print("\n" + "=" * 60)
    print("Example 3: Reasoning Pattern Selection")
    print("=" * 60)
    
    selector = ReasoningSelector()
    
    # Problem 1: Analytical problem
    chain = selector.select_and_reason(
        problem_type="analytical",
        problem="Analyze the impact of transfer learning on model training speed",
        context="Comparing with training from scratch"
    )
    print(f"\n✓ Analytical Problem:")
    print(f"  Pattern used: {chain.pattern}")
    print(f"  Steps: {len(chain.steps)}")
    print(f"  Conclusion: {chain.conclusion[:80]}...")
    
    # Problem 2: Exploratory problem
    chain = selector.select_and_reason(
        problem_type="exploratory",
        problem="What are all possible applications of transfer learning?",
        context="Brainstorm new use cases"
    )
    print(f"\n✓ Exploratory Problem:")
    print(f"  Pattern used: {chain.pattern}")
    print(f"  Branches explored: {len(chain.steps)}")
    

def quickstart_crew():
    """Example 4: Multi-agent crew execution"""
    print("\n" + "=" * 60)
    print("Example 4: Multi-Agent Crew (Hierarchical)")
    print("=" * 60)
    
    # Build crew
    builder = CrewBuilder("Research Team", CommunicationPattern.HIERARCHICAL)
    
    builder.add_agent(ResearcherAgent(name="Researcher"), "research")
    builder.add_agent(PlannerAgent(name="Planner"), "planning")
    builder.add_agent(ExecutorAgent(name="Executor"), "execution")
    
    supervisor = PlannerAgent(name="Supervisor", role="Research Supervisor")
    builder.set_supervisor(supervisor)
    
    crew = builder.build()
    
    # Execute task
    task = {
        "description": "Research and implement transfer learning solution",
        "input": "Create a transfer learning pipeline for image classification"
    }
    
    result = crew.execute_task(task)
    print(f"\n✓ Crew Execution Summary:")
    print(f"  Pattern: {result['pattern']}")
    print(f"  Steps executed: {result['execution_steps']}")
    print(f"  Status: {result['status']}")
    print(f"  Timestamp: {result['timestamp']}")


def quickstart_self_improvement():
    """Example 5: Self-improving loop (basic)"""
    print("\n" + "=" * 60)
    print("Example 5: Self-Improving Loop")
    print("=" * 60)
    
    memory = HybridMemorySystem()
    agent = ExecutorAgent(name="LearningBot", role="Executor")
    
    print("\nSimulating 3 iterations of task execution + learning:")
    
    for iteration in range(1, 4):
        # Task
        task = {
            "description": f"Iteration {iteration}: Solve classification task",
            "input": f"Classify image {iteration}"
        }
        
        # Execute
        result = agent.process_task(task)
        
        # Store experience
        memory.record_experience(
            episode_id=f"iter_{iteration}",
            steps=[
                {"action": "classify", "result": result['action']}
            ],
            outcome="success" if iteration % 2 == 0 else "partial_success",
            reflection=f"Iteration {iteration}: Accuracy improved, timeout decreased"
        )
        
        print(f"  Iteration {iteration}: status={result['status']}, learned & stored")
    
    # Check consolidation
    status = memory.get_memory_status()
    print(f"\n✓ After learning loop:")
    print(f"  {status}")


def main():
    """Run all examples"""
    print("\n" + "🚀" * 30)
    print("AGI Framework - Quickstart Examples")
    print("🚀" * 30)
    
    try:
        quickstart_basic_agent()
        quickstart_memory()
        quickstart_reasoning()
        quickstart_crew()
        quickstart_self_improvement()
        
        print("\n" + "✓" * 60)
        print("\n✅ All examples completed successfully!")
        print("\nNext steps:")
        print("  1. Explore examples/ for more advanced patterns")
        print("  2. Review README.md for architecture overview")
        print("  3. Run tests/ with: pytest tests/")
        print("  4. Integrate with your own tasks!")
        
    except Exception as e:
        print(f"\n❌ Error during execution: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()
