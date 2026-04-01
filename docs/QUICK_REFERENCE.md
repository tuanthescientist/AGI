# Quick Reference: AGI Framework v0.2

**Cheat Sheet for Common Operations**

## Memory Operations

```python
from memory.hybrid_memory import HybridMemorySystem

memory = HybridMemorySystem()

# Store & retrieve semantic facts
memory.store_semantic("key", "value", metadata={})
results = memory.search_similar("query", k=5)

# Knowledge graphs
memory.store_knowledge("Entity", {"attr": "value"})
memory.add_relationship("A", "relates_to", "B")

# Experiences
memory.record_experience("ep_123", steps=[...], outcome="success")
successes = memory.retrieve_by_outcome("success")

# Skills registry
memory.register_skill("task", "tool", success_rate=0.9)
best = memory.get_best_tools("task_type")

# Status
status = memory.get_memory_status()
```

## Agent Operations

```python
from agents.base_agent import (
    ResearcherAgent, PlannerAgent, ExecutorAgent, CriticAgent, MonitorAgent
)

# Create agent
agent = ResearcherAgent(name="Bot", role="Researcher")

# Process task
result = agent.process_task({
    "description": "...",
    "input": "..."
})

# Send/receive messages
agent.send_message(other_agent, "message")
msg = agent.receive_message()

# Access result
reasoning = result["reasoning"]
action = result["action"]
reflection = result["reflection"]
status = result["status"]
```

## Crew Operations

```python
from agents.crew import CrewBuilder, CommunicationPattern

# Create crew
builder = CrewBuilder("TeamName", CommunicationPattern.SEQUENTIAL)
builder.add_agent(ResearcherAgent(), "research")
builder.add_agent(PlannerAgent(), "planning")
crew = builder.build()

# Execute task
result = crew.execute_task({
    "description": "...",
    "input": "..."
})

# Crew patterns:
# - SEQUENTIAL: pipeline (output of i → input of i+1)
# - HIERARCHICAL: supervisor + delegation
# - PARALLEL: all agents work independently
# - DEBATE: multi-round consensus building
```

## Reasoning Patterns

```python
from reasoning.reasoning_patterns import ReasoningSelector

selector = ReasoningSelector()

# Automatic selection
chain = selector.select_and_reason(
    problem_type="analytical",  # sequential/analytical/exploratory
    problem="...",
    context="..."
)

# Manual use
from reasoning.reasoning_patterns import ReAct, ChainOfThought

cot = ChainOfThought()
chain = cot.reason(problem="...", context="...")

react = ReAct()
chain = react.reason_and_act(problem="...", tools={...})
```

## Tracing & Observability

```python
from infrastructure.observability import Tracer

tracer = Tracer(name="MyAgent", export_json=True)

# Start trace
tracer.start_trace("task_id")

# Log operations
tracer.log_reasoning(thought="...", step=1, confidence=0.8)
tracer.log_action(action="act", tool="tool_name")
tracer.log_tool_call("tool", {"arg": "val"}, result={})
tracer.log_decision("choice", alternatives=["alt1"], reasoning="...")
tracer.log_reflection("reflection text", success=True)
tracer.log_memory_operation("store", "key")

# End trace
result = tracer.end_trace()

# Query traces
summary = tracer.get_summary()
trace = tracer.get_trace("task_id")
all_traces = tracer.get_all_traces()
```

## Evaluation

```python
from evaluation.benchmarks import Evaluator, Benchmark, BenchmarkSuite

# Setup evaluator
evaluator = Evaluator("MyEval")
evaluator.setup_default_suite()

# Custom benchmark
def test_fn(output):
    return output.get("success")

benchmark = Benchmark("test", test_fn, expected_output=True)

# Evaluate
result = evaluator.evaluate_task(agent_output)
score = result.get_average_score()

# Summary
summary = evaluator.get_summary()
```

## Common Patterns

### Single Agent + Memory + Tracing
```python
tracer = Tracer("agent", export_json=True)
memory = HybridMemorySystem()
agent = ResearcherAgent()

tracer.start_trace("task_001")
result = agent.process_task({"input": "..."})
tracer.log_reasoning(thought=result["reasoning"])
memory.record_experience("ep_001", steps=[...], outcome="success")
tracer.end_trace()
```

### Multi-Agent Debate
```python
builder = CrewBuilder("Debate", CommunicationPattern.DEBATE)
builder.add_agent(ResearcherAgent(), "pro")
builder.add_agent(PlannerAgent(), "con")
builder.add_agent(CriticAgent(), "judge")
crew = builder.build()

result = crew.execute_task({"input": "Trade-off question"})
```

### Self-Improving Loop
```python
memory = HybridMemorySystem()
agent = ExecutorAgent()

for i in range(5):
    result = agent.process_task(task)
    memory.record_experience(f"iter_{i}", steps=[...], outcome="success")
    best_tools = memory.get_best_tools("task")
    # Apply learnings...
```

### Hierarchical Team
```python
builder = CrewBuilder("Team", CommunicationPattern.HIERARCHICAL)
builder.add_agent(ResearcherAgent(), "research")
builder.add_agent(PlannerAgent(), "planning")
builder.set_supervisor(CriticAgent())
crew = builder.build()

result = crew.execute_task(task)
```

## File Structure Reference

```
d:\Data Science\AGI\
├── memory/
│   └── hybrid_memory.py         # 5 memory types + consolidation
├── reasoning/
│   └── reasoning_patterns.py    # ReAct, CoT, ToT, GoT, SelfReflection, MetaReasoning
├── agents/
│   ├── base_agent.py            # BaseAgent + 5 archetypes
│   └── crew.py                  # Multi-agent orchestration (4 patterns)
├── infrastructure/
│   └── observability.py         # Tracer, ExecutionTrace, ObservableEvent
├── evaluation/
│   └── benchmarks.py            # Evaluator, BenchmarkSuite, Metrics
├── examples/
│   ├── quickstart.py            # < 2 minutes to get started
│   └── multi_agent_patterns.py  # 6 advanced patterns
├── docs/
│   └── deepdive/
│       └── MODULE_REFERENCE.md  # Complete reference guide
└── ...
```

## Result Structure Reference

### Agent Result
```python
{
    "agent_name": "ResearcherBot",
    "status": "success",  # success/failure/partial_success
    "reasoning": "Analytical reasoning process...",
    "action": "Generated output or action...",
    "reflection": "Evaluation and learnings...",
    "execution_history": [...]
}
```

### Crew Result
```python
{
    "pattern": "hierarchical",  # sequential/hierarchical/parallel/debate
    "execution_steps": 3,
    "status": "success",
    "timestamp": "2024-10-01T...",
    "agents_involved": ["agent1", "agent2"]
}
```

### Evaluation Result
```python
{
    "task_id": "task_001",
    "agent_name": "Evaluator",
    "success": True,
    "average_score": 0.85,  # 0-1
    "metrics": [
        {
            "name": "accuracy",
            "type": "accuracy",
            "value": 0.9
        }
    ]
}
```

## Quick Troubleshooting

| Issue | Solution |
|-------|----------|
| "No module named" | Check `__init__.py` files exist, add to `sys.path` |
| Memory bloat | Memory consolidates auto every 100 ops |
| Tracing not saved | Set `export_json=True`, check `./traces/` folder |
| Crew not executing | Check `all agents added`, supervisor set for hierarchical |
| Reasoning timeout | Reduce max iterations, use simpler pattern |
| Evaluation score low | Check benchmark expectations, trace agent output |

## Configuration

### AgentConfig
```python
from agents.base_agent import AgentConfig

config = AgentConfig(
    model="gpt-4",
    temperature=0.7,
    max_tokens=2048,
    reasoning_pattern="CoT",
    memory_size=100
)
```

### TraceConfig
```python
tracer = Tracer(
    name="MyAgent",
    export_json=True,
    export_path="./traces"
)
```

---

**For complete reference, see `/docs/deepdive/MODULE_REFERENCE.md`**
