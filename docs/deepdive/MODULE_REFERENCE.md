# Module Deep Dive: Complete Reference Guide

**Updated October 2024**  
**Author: Tuan Tran**

---

## Overview

This guide provides comprehensive documentation for AGI framework v0.2, including all modules, patterns, and best practices.

## Table of Contents

1. [Memory System](#memory-system)
2. [Reasoning Patterns](#reasoning-patterns)
3. [Agent Framework](#agent-framework)
4. [Multi-Agent Coordination](#multi-agent-coordination)
5. [Observability](#observability)
6. [Evaluation](#evaluation)
7. [Examples & Patterns](#examples--patterns)
8. [Best Practices](#best-practices)

---

## Memory System

### Overview

The hybrid memory system implements 5 memory types with automatic consolidation:

| Memory Type | Purpose | Access Pattern | Capacity |
|---|---|---|---|
| Vector Memory | Semantic knowledge | Embedding search | 1000 items |
| Graph Memory | Relationships | Node/edge traversal | 500 entities |
| Episodic Memory | Experiences | Success/failure filter | 100 episodes |
| Procedural Memory | Skills | Tool/task mapping | 200 skills |
| Working Memory | Context | FIFO | 20 items |

### Usage Examples

#### Store Semantic Knowledge
```python
from memory.hybrid_memory import HybridMemorySystem

memory = HybridMemorySystem()

# Store fact with metadata
memory.store_semantic(
    key="transformer_architecture",
    value="Uses attention mechanism for parallel processing",
    metadata={"source": "research", "confidence": 0.95}
)

# Search similar
results = memory.search_similar("attention mechanisms", k=3)
```

#### Store Knowledge Graph
```python
# Add entity with attributes
memory.store_knowledge(
    entity="TransformerModel",
    attributes={
        "architecture": "encoder-decoder",
        "attention": "multi-head",
        "applications": ["NLP", "CV", "Speech"]
    }
)

# Add relationships
memory.add_relationship("Transformer", "enables", "BERT")
memory.add_relationship("BERT", "improved", "NLP")

# Inference
neighbors = memory.get_neighbors("BERT", depth=2)
```

#### Record Experiences
```python
# Record episode with success/failure
memory.record_experience(
    episode_id="exp_001",
    steps=[
        {"action": "load_model", "result": "success"},
        {"action": "finetune", "result": "success"},
        {"action": "evaluate", "result": "success"}
    ],
    outcome="success",
    reflection="Finetuning on subset significantly improved performance"
)

# Retrieve successes
successes = memory.retrieve_by_outcome("success")
success_rate = memory.get_success_rate()  # 1.0 (100%)
```

#### Register Skills
```python
# Register skill with tool mapping
memory.register_skill(
    skill_name="image_classification",
    tool_name="ResNet50",
    success_rate=0.92
)

# Record tool usage
memory.record_tool_usage(
    tool_name="ResNet50",
    args={"image": "dog.jpg"},
    result={"class": "dog", "confidence": 0.98}
)

# Get best tools for task
best_tools = memory.get_best_tools("classification")
# [{"tool": "ResNet50", "success_rate": 0.92}, ...]
```

#### Working Context
```python
# Add current task context
working_mem = memory.get_working_memory()
working_mem.add("current_task", task_object)
working_mem.add("active_subtask", subtask_object)

# Get context
context = working_mem.get_context()
print(context)  # {"current_task": ..., "active_subtask": ...}

# Clear for new task
working_mem.clear()
```

#### Memory Status
```python
status = memory.get_memory_status()
# Returns:
# "Vector: 5/100 items | Graph: 3 entities, 2 relations | 
#  Episodic: 2 experiences (90% success) | 
#  Procedural: 1 skill, 3 tool usages | 
#  Working: 2 items | Next consolidation: 87 ops"
```

---

## Reasoning Patterns

### Overview

6 reasoning patterns for different problem types:

| Pattern | Best For | Cycles | Decision Style |
|---|---|---|---|
| ReAct | Interactive, tool-use | 1-10 | Iterative |
| Chain of Thought | Analytical | 4-5 steps | Deterministic |
| Tree of Thoughts | Exploratory | N branches | Confidence-weighted |
| Graph of Thoughts | Dependence graphs | DAG traversal | Topological |
| Self-Reflection | Meta-learning | 2 passes | Reflective |
| Meta-Reasoning | Strategy choice | Algorithm comparison | Quantitative |

### Pattern Details & Usage

#### 1. ReAct (Reason + Act + Observe)

**Best for:** Interactive tasks, real-time feedback, tool use

```python
from reasoning.reasoning_patterns import ReAct

react = ReAct()
chain = react.reason_and_act(
    problem="Find the best ML model for tabular data",
    tools={
        "search": lambda q: f"Results for {q}",
        "evaluate": lambda model: f"Performance: 0.95"
    }
)

print(f"Cycles: {len(chain.steps)}")  # 1-10
print(f"Conclusion: {chain.conclusion}")
```

**Execution Flow:**
1. Reason about problem
2. Decide action (tool call or answer)
3. Observe result
4. Loop (max 10 iterations)

#### 2. Chain of Thought (CoT)

**Best for:** Mathematical, logical, analytical reasoning

```python
from reasoning.reasoning_patterns import ChainOfThought

cot = ChainOfThought()
chain = cot.reason(
    problem="If a train travels 100km in 2 hours, what is its speed?",
    context="Need to include units"
)

print(f"Steps: {len(chain.steps)}")  # Usually 4-5
for i, step in enumerate(chain.steps, 1):
    print(f"  {i}. {step}")
print(f"Conclusion: {chain.conclusion}")
```

**Step Structure:**
- Understanding: Parse problem
- Analysis: Identify key information
- Solution: Apply reasoning
- Verification: Validate answer

#### 3. Tree of Thoughts (ToT)

**Best for:** Exploratory, solution space search

```python
from reasoning.reasoning_patterns import TreeOfThoughts

tot = TreeOfThoughts()
chain = tot.explore(
    problem="What are alternative architectures for AGI?",
    context="Compare design trade-offs"
)

print(f"Branches explored: {len(chain.steps)}")
print(f"Best branch selected: {chain.conclusion}")
```

**Characteristics:**
- Explores multiple branches
- Scores each branch (0-1 confidence)
- Prunes low-confidence branches
- Returns best path as conclusion

#### 4. Graph of Thoughts (GoT)

**Best for:** Problems with dependencies, constraint satisfaction

```python
from reasoning.reasoning_patterns import GraphOfThoughts

got = GraphOfThoughts()
chain = got.reason_with_graph(
    problem="Design microservice architecture with constraints",
    context="Must be scalable, fault-tolerant, and cost-efficient"
)

print(f"Nodes: {len(chain.steps)}")
print(f"Reasoning: {chain.conclusion}")
```

**Structure:**
- Models problem as DAG
- Tracks dependencies between reasoning steps
- Ensures prerequisites satisfied before proceeding

#### 5. Self-Reflection

**Best for:** Meta-learning, improving reasoning quality

```python
from reasoning.reasoning_patterns import SelfReflection

reflection = SelfReflection()
chain = reflection.reflect_on_reasoning(
    original_chain=[
        "Identified the problem",
        "Applied standard approach",
        "Got suboptimal result"
    ]
)

print(f"Critique: {chain.conclusion}")
# Suggests improvements, identifies weak points
```

#### 6. Meta-Reasoning

**Best for:** Comparing strategies, algorithm selection

```python
from reasoning.reasoning_patterns import MetaReasoning

meta = MetaReasoning()
result = meta.analyze_reasoning_strategies(
    strategies=[
        {"name": "CoT", "success_rate": 0.8},
        {"name": "ToT", "success_rate": 0.9},
        {"name": "ReAct", "success_rate": 0.75}
    ]
)

print(f"Best strategy: {result.conclusion}")
# Returns: "Use ToT (90% success rate)"
```

### Automatic Pattern Selection

```python
from reasoning.reasoning_patterns import ReasoningSelector

selector = ReasoningSelector()

# Selector automatically picks best pattern based on problem type
chain = selector.select_and_reason(
    problem_type="analytical",  # sequential/analytical/exploratory
    problem="Calculate ROI for investment",
    context="Include tax implications"
)

print(f"Pattern used: {chain.pattern}")  # e.g., "ChainOfThought"
print(f"Result: {chain.conclusion}")
```

---

## Agent Framework

### Agent Lifecycle

```
┌─────────────────────┐
│  Task Input         │
│  {description, ..}  │
└──────────┬──────────┘
           │
           ▼
┌─────────────────────────┐
│  REASONING Phase        │
│  - Select pattern       │
│  - Generate thoughts    │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  ACTION Phase           │
│  - Execute action       │
│  - Call tools           │
│  - Generate output      │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────────┐
│  REFLECTION Phase       │
│  - Evaluate result      │
│  - Store in memory      │
│  - Learn patterns       │
└──────────┬──────────────┘
           │
           ▼
┌─────────────────────┐
│  Result Output      │
└─────────────────────┘
```

### Agent Archetypes

#### ResearcherAgent
- **Role:** Information gathering, analysis
- **Reasoning:** ChainOfThought (analytical)
- **Strengths:** Deep analysis, fact-finding
- **Usage:**
```python
researcher = ResearcherAgent(
    name="InfoGatherer",
    role="Research Specialist"
)

result = researcher.process_task({
    "description": "Research AI trends",
    "input": "What are latest developments in LLMs?"
})
```

#### PlannerAgent
- **Role:** Strategy, planning, design
- **Reasoning:** TreeOfThoughts (exploratory)
- **Strengths:** Alternative exploration, plan generation
- **Usage:**
```python
planner = PlannerAgent(
    name="Strategist",
    role="Technical Architect"
)

result = planner.process_task({
    "description": "Plan system design",
    "input": "Design scalable recommendation system"
})
```

#### ExecutorAgent
- **Role:** Implementation, execution
- **Reasoning:** ReAct (action-oriented)
- **Strengths:** Tool use, interactive problem-solving
- **Usage:**
```python
executor = ExecutorAgent(
    name="Engineer",
    role="Implementation Lead"
)

result = executor.process_task({
    "description": "Implement feature",
    "input": "Build API endpoint for recommendations"
})
```

#### CriticAgent
- **Role:** Quality assurance, feedback
- **Reasoning:** SelfReflection (analytical critique)
- **Strengths:** Error detection, improvement suggestions
- **Usage:**
```python
critic = CriticAgent(
    name="QABot",
    role="Quality Assurance"
)

result = critic.process_task({
    "description": "Review solution",
    "input": "Evaluate recommendation system for bugs and efficiency"
})
```

#### MonitorAgent
- **Role:** Oversight, health monitoring
- **Reasoning:** MetaReasoning (strategy analysis)
- **Strengths:** Performance tracking, anomaly detection
- **Usage:**
```python
monitor = MonitorAgent(
    name="Watchdog",
    role="System Monitor"
)

result = monitor.process_task({
    "description": "Monitor system health",
    "input": "Check performance metrics and alert if degradation"
})
```

### Agent Communication

```python
researcher = ResearcherAgent()
planner = PlannerAgent()

# Agent 1 sends message
researcher.send_message(
    recipient=planner,
    message="Research findings: LLMs improve with scale"
)

# Agent 2 receives message
while planner.has_messages():
    incoming = planner.receive_message()
    print(f"From {incoming['sender']}: {incoming['message']}")
```

### Agent Configuration

```python
from agents.base_agent import AgentConfig

config = AgentConfig(
    model="gpt-4",
    temperature=0.7,
    max_tokens=2048,
    reasoning_pattern="CoT",
    memory_size=100,
    reflection_enabled=True
)

agent = MySpecializedAgent(
    name="Expert",
    role="Domain Expert",
    config=config
)
```

---

## Multi-Agent Coordination

### 4 Crew Communication Patterns

#### Pattern 1: SEQUENTIAL (Pipeline)

**Visualization:**
```
Input → Agent1 → Agent2 → Agent3 → Output
        search   analyze  report
```

**Characteristics:**
- Output of agent i → input of agent i+1
- Chain of responsibility
- Deterministic execution order

**Use Cases:**
- ETL pipelines
- Processing pipelines
- Linear workflows

**Example:**
```python
from agents.crew import CrewBuilder, CommunicationPattern

builder = CrewBuilder("DataPipeline", CommunicationPattern.SEQUENTIAL)
builder.add_agent(ResearcherAgent(), "data_collection")
builder.add_agent(PlannerAgent(), "data_preparation")
builder.add_agent(ExecutorAgent(), "data_analysis")

crew = builder.build()

result = crew.execute_task({
    "input": "Raw data",
    "description": "Process data pipeline"
})
```

#### Pattern 2: HIERARCHICAL (Supervisor)

**Visualization:**
```
              Supervisor
            /    |    \
        Agent1  Agent2  Agent3
            \    |    /
          Synthesis & Report
```

**Characteristics:**
- Supervisor analyzes task
- Delegates to specialists
- Collects and synthesizes results
- Hierarchical decision-making

**Use Cases:**
- Team coordination
- Complex projects
- Specialized expertise

**Example:**
```python
builder = CrewBuilder("ResearchTeam", CommunicationPattern.HIERARCHICAL)

builder.add_agent(ResearcherAgent(), "research")
builder.add_agent(PlannerAgent(), "planning")
builder.add_agent(ExecutorAgent(), "execution")

supervisor = PlannerAgent(name="ProjectLead", role="Team Supervisor")
builder.set_supervisor(supervisor)

crew = builder.build()

result = crew.execute_task({
    "description": "Complex research project",
    "input": "Problem statement"
})
```

#### Pattern 3: PARALLEL (Team)

**Visualization:**
```
Agent1 ─┐
Agent2 ─┼─→ Results ─→ Aggregation
Agent3 ─┘
```

**Characteristics:**
- All agents work independently
- Can process different subtasks
- Results aggregated at end
- Maximum parallelism

**Use Cases:**
- Solution space exploration
- Independent analysis
- Vote-based decisions

**Example:**
```python
builder = CrewBuilder("SearchTeam", CommunicationPattern.PARALLEL)

builder.add_agent(ResearcherAgent(), "research")
builder.add_agent(PlannerAgent(), "planning")
builder.add_agent(ExecutorAgent(), "execution")

crew = builder.build()

result = crew.execute_task({
    "description": "Explore solution space",
    "input": "Complex optimization problem"
})
```

#### Pattern 4: DEBATE (Consensus)

**Visualization:**
```
Round 1: Proposals      Round 2: Critiques      Round 3: Consensus
Agent1 ──→ Proposal    Critic  ──→ Analysis    → Agreement
Agent2 ──→ Proposal    (debate)                → Final Position
Agent3 ──→ Proposal
```

**Characteristics:**
- Round 1: Each agent proposes
- Round 2: Critique/counter-propose
- Round 3: Reach consensus
- Evidence-based disagreement

**Use Cases:**
- Trade-off decisions
- Requirements specification
- Architecture decisions

**Example:**
```python
builder = CrewBuilder("DebateClub", CommunicationPattern.DEBATE)

builder.add_agent(ResearcherAgent(), "proponent_a")
builder.add_agent(PlannerAgent(), "proponent_b")
builder.add_agent(CriticAgent(), "critic")

crew = builder.build()

result = crew.execute_task({
    "description": "Debate trade-offs",
    "input": "Should we use SQL or NoSQL for this application?"
})
# Debate includes multiple rounds with critiques and consensus building
```

### CrewBuilder API

```python
from agents.crew import CrewBuilder, CommunicationPattern

# Create builder
builder = CrewBuilder(
    name="MyTeam",
    pattern=CommunicationPattern.HIERARCHICAL,
    max_iterations=5
)

# Add agents
builder.add_agent(
    agent=ResearcherAgent(),
    channel="research"  # Used in hierarchical/sequential
)

# Set supervisor (for hierarchical only)
builder.set_supervisor(PlannerAgent())

# Build crew
crew = builder.build()

# Execute
result = crew.execute_task(task_dict)
```

---

## Observability

### Tracing Overview

Every operation can be traced for debugging and analysis.

```python
from infrastructure.observability import Tracer

tracer = Tracer(
    name="MyAgent",
    export_json=True,
    export_path="./traces"
)

# Start trace
trace = tracer.start_trace("task_123")

# Log operations
tracer.log_reasoning(thought="Problem needs analysis", step=1)
tracer.log_action(action="call_analyzer", tool="analyzer")
tracer.log_tool_call("analyzer", {"input": "data.csv"})

# End trace
result = tracer.end_trace()

# Access traces
summary = tracer.get_summary()
# {
#   "traces": 1,
#   "total_duration_ms": 250.5,
#   "total_tool_calls": 1,
#   "avg_duration_ms": 250.5
# }
```

### Observable Events

```python
from infrastructure.observability import EventType

# Task events
EventType.TASK_START
EventType.TASK_END
EventType.TASK_ERROR

# Agent events
EventType.AGENT_REASONING
EventType.AGENT_ACTION
EventType.AGENT_REFLECTION

# Tool events
EventType.TOOL_CALL
EventType.TOOL_RESULT

# Memory events
EventType.MEMORY_STORE
EventType.MEMORY_RETRIEVE
EventType.MEMORY_CONSOLIDATE

# Decision events
EventType.DECISION_MADE
EventType.DECISION_ALTERNATIVE

# Error events
EventType.ERROR_OCCURRED
EventType.WARNING_ISSUED
```

### Trace Export

Traces are automatically exported to JSON files in `./traces/` directory:

```json
{
  "task_id": "task_001",
  "start_time": "2024-10-01T10:30:00.000000",
  "end_time": "2024-10-01T10:30:00.250000",
  "total_duration_ms": 250.0,
  "events": [
    {
      "event_type": "task_start",
      "timestamp": "...",
      "actor": "MyAgent",
      "level": "INFO",
      "message": "Starting task",
      "context": {}
    }
  ]
}
```

---

## Evaluation

### Benchmark Suite

```python
from evaluation.benchmarks import Evaluator, BenchmarkSuite

# Create evaluator
evaluator = Evaluator("AGIEvaluator")

# Setup default benchmarks
evaluator.setup_default_suite()

# Evaluate agent output
result = evaluator.evaluate_task(agent_output)

print(f"Score: {result.get_average_score():.2f}")
print(f"Metrics: {len(result.metrics)}")
```

### Custom Benchmarks

```python
from evaluation.benchmarks import Benchmark, BenchmarkSuite

def my_test(agent_output):
    """Returns True if test passes"""
    return agent_output.get("success") == True

benchmark = Benchmark(
    name="my_custom_test",
    task_fn=my_test,
    expected_output=True  # Expected return value
)

suite = BenchmarkSuite()
suite.add_benchmark(benchmark)

results = suite.run_all(agent_output)
average_score = suite.get_average_score(results)
```

### Evaluation Metrics

```python
from evaluation.benchmarks import MetricType

# Metric types available:
MetricType.ACCURACY           # Correctness
MetricType.LATENCY           # Speed
MetricType.EFFICIENCY        # Resource usage
MetricType.REASONING_QUALITY # Chain validity, depth
MetricType.SELF_AWARENESS    # Plan accuracy, uncertainty
MetricType.COLLABORATION     # Multi-agent metrics
MetricType.CORRECTNESS       # Pass/fail
```

---

## Examples & Patterns

### Pattern 1: Self-Improving Agent

```python
from agents.base_agent import ExecutorAgent
from memory.hybrid_memory import HybridMemorySystem

memory = HybridMemorySystem()
agent = ExecutorAgent(name="LearningBot")

for iteration in range(5):
    # Execute task
    result = agent.process_task(task)
    
    # Store experience
    memory.record_experience(
        episode_id=f"iter_{iteration}",
        steps=[{"action": result["action"]}],
        outcome="success" if result["status"] == "success" else "failure",
        reflection=f"Iteration {iteration} completed"
    )
    
    # Retrieve best practices
    successes = memory.retrieve_by_outcome("success")
    best_tools = memory.get_best_tools("execution")
    
    # Adapt (would apply learnings to next iteration)
    print(f"Progress: {iteration+1}/5, Best tools: {best_tools}")
```

### Pattern 2: Debate-Based Architecture Decision

```python
from agents.crew import CrewBuilder, CommunicationPattern

builder = CrewBuilder("ArchDebate", CommunicationPattern.DEBATE)

builder.add_agent(ResearcherAgent(name="ProponentA"), "advocate_monolithic")
builder.add_agent(PlannerAgent(name="ProponentB"), "advocate_microservices")
builder.add_agent(CriticAgent(name="Mediator"), "evaluate")

crew = builder.build()

result = crew.execute_task({
    "description": "Debate monolithic vs microservices",
    "input": "Should we use monolithic or microservices for our system?"
})

print(f"Debate rounds: {result['execution_steps']}")
print(f"Consensus: {result['status']}")
```

### Pattern 3: Pipeline Processing

```python
from agents.crew import CrewBuilder, CommunicationPattern

builder = CrewBuilder("MLPipeline", CommunicationPattern.SEQUENTIAL)

builder.add_agent(ResearcherAgent(), "data_exploration")
builder.add_agent(PlannerAgent(), "feature_engineering")
builder.add_agent(ExecutorAgent(), "model_training")
builder.add_agent(CriticAgent(), "evaluation")

crew = builder.build()

result = crew.execute_task({
    "input": "raw_dataset.csv",
    "description": "End-to-end ML pipeline"
})
```

---

## Best Practices

### ✅ DO

1. **Use specialized agents** - Compose multiple agents for different roles
2. **Log decisions** - Trace all non-trivial choices
3. **Store experiences** - Record successes and failures in memory
4. **Evaluate regularly** - Use benchmarks to measure improvement
5. **Use hierarchical crews** - For complex multi-agent coordination
6. **Limit reasoning depth** - 3-5 steps optimal, not 10+
7. **Cache memory queries** - Avoid repeated semantic searches

### ❌ DON'T

1. **Don't create mega-agents** - Split into specialized agents
2. **Don't ignore memory** - Consolidation is automatic every 100 ops
3. **Don't skip tracing** - Lost visibility when debugging
4. **Don't use only sequential** - Parallel is better for independent tasks
5. **Don't use same pattern everywhere** - Choose pattern for problem type
6. **Don't evaluate once and move on** - Continuous measurement
7. **Don't store everything in memory** - Set capacity limits

### Performance Tips

- **Parallel vs Sequential:** Use PARALLEL when agents are independent (20-40% speedup)
- **Reasoning depth:** 3-5 steps better than 10+ (similar quality, 2x faster)
- **Memory:** Consolidate every 100 ops (prevents bloat)
- **Batch operations:** Execute multiple tasks before evaluation (60% efficiency gain)
- **Caching:** Cache frequent memory searches (3-5x faster)

---

## Quick Reference

### Imports

```python
# Memory
from memory.hybrid_memory import HybridMemorySystem

# Reasoning
from reasoning.reasoning_patterns import ReasoningSelector

# Agents
from agents.base_agent import BaseAgent, ResearcherAgent, PlannerAgent

# Crew
from agents.crew import Crew, CrewBuilder, CommunicationPattern

# Observability
from infrastructure.observability import Tracer, get_tracer

# Evaluation
from evaluation.benchmarks import Evaluator, BenchmarkSuite
```

### Common Operations

```python
# Create agent
agent = ResearcherAgent(name="Bot")

# Process task
result = agent.process_task({"input": "question"})

# Create crew
crew = CrewBuilder("Team", CommunicationPattern.HIERARCHICAL).build()

# Execute crew task
result = crew.execute_task(task)

# Trace execution
tracer = Tracer("name")
tracer.start_trace("task_id")
tracer.log_reasoning(thought="...")
tracer.end_trace()

# Evaluate
evaluator = Evaluator()
evaluator.setup_default_suite()
result = evaluator.evaluate_task(output)
```

---

**End of Deep Dive Guide**
