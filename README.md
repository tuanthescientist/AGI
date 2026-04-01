# AGI Framework
## A modular, graph-based framework towards self-improving AGI systems

**Author**: Tuan Tran  
**Version**: 0.2.0  
**License**: MIT

A comprehensive, production-ready framework for building self-aware, self-improving AGI systems with advanced reasoning, memory systems, and autonomous agents. Bridging LLM capabilities with structured reasoning, meta-learning, and multi-agent collaboration.

## 🎯 Core Vision

Going beyond traditional LLMs by combining:
- **Graph-Based Agent Architecture**: State graph orchestration (inspired by LangGraph) with explicit nodes and transitions
- **Self-Awareness & Meta-Learning**: Continuous introspection and autonomous capability improvement
- **Advanced Reasoning**: ReAct, Chain-of-Thought, Tree-of-Thoughts, Self-Reflection, Meta-Reasoning patterns
- **Hybrid Memory System**: Vector DB (semantic), Graph DB (knowledge), episodic, procedural, and working memory
- **Multi-Agent Collaboration**: Crew-based agents with supervisor orchestration and role-based specialization
- **Continuous Self-Improvement**: Autonomous fine-tuning, prompt optimization, and curriculum learning adjustment

## 📁 Project Structure

```
AGI/
├── core/                      # Core AGI engine (centralized)
│   ├── agi_engine.py
│   ├── agi_executor.py        # Graph-based executor
│   └── meta_controller.py
├── agents/                    # Agent layer (NEW)
│   ├── base_agent.py
│   ├── agent_executor.py      # Graph-based execution
│   └── crew.py                # Multi-agent orchestration
├── memory/                    # Specialized memory (NEW)
│   ├── vector_store.py        # Semantic memory with Chroma
│   ├── graph_memory.py        # Knowledge graph (Neo4j/NetworkX)
│   ├── episodic_memory.py
│   ├── working_memory.py
│   └── memory_consolidation.py
├── reasoning/                 # Reasoning patterns (NEW)
│   ├── react.py               # ReAct pattern
│   ├── cot.py                 # Chain-of-Thought
│   ├── tot.py                 # Tree-of-Thoughts
│   ├── got.py                 # Graph-of-Thoughts
│   ├── self_reflection.py
│   └── meta_reasoning.py
├── tools/                     # Tool management (NEW)
│   ├── tool_registry.py
│   ├── tool_executor.py
│   └── builtin_tools.py
├── algorithms/                # Research algorithms
│   ├── core_algorithms.py
│   ├── meta_learning.py
│   └── continual_learning.py
├── training/                  # Training systems
│   ├── training_systems.py
│   └── self_improvement_loop.py
├── infrastructure/            # Distributed & ops
│   ├── distributed_training.py
│   ├── observability.py       # Tracing, logging (NEW)
│   └── config_manager.py      # Hydra/Pydantic (NEW)
├── evaluation/                # Evaluation & benchmarks
│   ├── metrics.py
│   ├── benchmarks/            # Standard benchmarks (NEW)
│   └── agent_bench.py         # Agent-specific eval (NEW)
├── examples/                  # Comprehensive examples (EXPANDED)
│   ├── quickstart.py
│   ├── basic_agent.py
│   ├── multi_agent_crew.py
│   ├── self_improving_loop.py
│   ├── memory_demo.py
│   ├── reasoning_demo.py
│   └── notebooks/             # Jupyter notebooks (NEW)
├── tests/                     # Testing suite (NEW)
│   ├── test_agents.py
│   ├── test_memory.py
│   ├── test_reasoning.py
│   └── test_e2e.py
├── docs/                      # Documentation
│   ├── ARCHITECTURE.md        # Updated architecture
│   ├── API_REFERENCE.md
│   ├── GETTING_STARTED.md
│   ├── CONTRIBUTING.md
│   └── deepdive/              # Deep-dive guides (NEW)
├── configs/
│   ├── config.yaml            # Main config
│   └── agents/                # Agent configs (NEW)
├── pyproject.toml             # Modern Python project (NEW)
├── requirements.txt
├── setup.py
├── LICENSE
└── .github/
    └── workflows/             # CI/CD (NEW)
```

## 🚀 Quick Start (< 2 minutes)

```bash
# 1. Clone and setup
git clone https://github.com/tuanthescientist/AGI.git
cd AGI
pip install -e ".[dev]"  # or: pip install -r requirements.txt

# 2. Run basic agent
python examples/quickstart.py

# 3. Run Jupyter notebook
jupyter notebook examples/notebooks/intro_to_agents.ipynb

# 4. Try multi-agent crew
python examples/multi_agent_crew.py
```

## 📊 Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                   User / External Interface                 │
└──────────────────────────┬──────────────────────────────────┘
                           │
┌──────────────────────────▼──────────────────────────────────┐
│              Agent Layer (Crew Orchestration)               │
│  - Supervisor Agent  │ - Researcher  │ - Planner  │ - ... │
└────┬─────────────────────────────────────────────────┬──────┘
     │                                                 │
┌────▼──────────────────────────────────────────────┬─▼────────┐
│       Graph-Based Agent Executor (State Machine) │ Tools    │
│  (LangGraph-inspired node/edge transitions)       │ Registry │
└────┬──────────────────────────────────────────────┴───┬──────┘
     │                                                  │
┌────▼────────────────────────────────────────────────▼──────┐
│  Reasoning Module Selector (ReAct / CoT / ToT / Meta-R)   │
└────┬──────────────────────────────────────────────────┬────┘
     │                                                  │
┌────▼────────────────────────────────────────────┬────▼──────┐
│ Hybrid Memory System                           │ Core Engine│
│ ┌──────────┐ ┌──────────┐ ┌──────────────────┐ │           │
│ │Vector DB │ │Graph DB  │ │ Episodic/Working │ │ Meta      │
│ │(Semantic)│ │(Knowledge)│ │     Memory       │ │ Controller│
│ └──────────┘ └──────────┘ └──────────────────┘ │ Self-Impro│
└────┬────────────────────────────────────────────┴────┬──────┘
     │                                                 │
┌────▼─────────────────────────────────────────────┬──▼──────────┐
│ Observability (Tracing, Logging, Metrics)      │ LLM Backends│
│ (LangSmith, LangFuse, or custom)               │ (OpenAI,   │
└──────────────────────────────────────────────────┴────────────┘
```

## ✨ Key Features

### Architecture & Design
- ✅ **Graph-Based Orchestration**: State machine-driven agent execution with explicit nodes, transitions, and conditional branches
- ✅ **Modular Layer Design**: Low-level (algorithms), Mid-level (engines/memory), High-level (agents/crew)
- ✅ **Strict Type Hints**: Pydantic v2 + dataclasses for all configs and states
- ✅ **State Graph Pattern**: Inspired by LangGraph for complex multi-step workflows

### Memory & Learning
- ✅ **Hybrid Memory System**: 
  - Vector stores (Chroma/Qdrant) for semantic memory
  - Graph DB (Neo4j/NetworkX) for knowledge graphs
  - Episodic memory with reflection
  - Procedural memory for tool usage
  - Working memory for short-term context
- ✅ **Memory Consolidation**: Continual learning without catastrophic forgetting
- ✅ **Multi-modal Support**: Text, embeddings, and structured data

### Reasoning & Agent Capabilities
- ✅ **Multiple Reasoning Patterns**: ReAct, Chain-of-Thought, Tree-of-Thoughts, Graph-of-Thoughts, Self-Reflection, Meta-Reasoning
- ✅ **Self-Improvement Loop**: Autonomous critique, uncertainty quantification, and policy optimization
- ✅ **Advanced Tool Use**: Strict schema, error recovery, and usage tracking
- ✅ **Multi-Agent Collaboration**: Crew patterns with roles, supervisor orchestration

### Production & Operations
- ✅ **Full Observability**: LangSmith/LangFuse integration + custom tracing
- ✅ **Comprehensive Evaluation**: MMLU, GSM8K, AgentBench, GAIA + custom metrics
- ✅ **Config Management**: Hydr + Pydantic Settings with multi-environment support
- ✅ **CI/CD Ready**: GitHub Actions, pytest, ruff + black + mypy
- ✅ **Distributed Ready**: Ray or PyTorch Distributed for scaling

## 📈 Feature Matrix

## 📈 Feature Matrix

| Feature | Status | Details |
|---------|--------|---------|
| **Graph-Based Agent Executor** | ✅ v0.2 | State machine-driven execution |
| **Hybrid Memory System** | ✅ v0.2 | Vector + Graph + Episodic |
| **Multi-Agent Crew** | ✅ v0.2 | Supervisor orchestration |
| **Reasoning Patterns** | ✅ v0.2 | ReAct, CoT, ToT, Meta-R |
| **Self-Improvement Loop** | ✅ v0.2 | Autonomous critique & optimization |
| **Tool Use** | ✅ v0.2 | Strict schema + error recovery |
| **Observability** | ✅ v0.2 | LangSmith/LangFuse integration |
| **Benchmarking** | 🔄 v0.3 | MMLU, GSM8K, AgentBench |
| **Distributed Training** | 🔄 v0.3 | Ray/PyTorch Distributed |
| **Vision-Language** | 📋 v0.4 | Multi-modal memory & reasoning |
| **Safety Guardrails** | 📋 v0.4 | NeMo Guardrails / Custom |
| **Uncertainty Quantification** | 📋 v0.4 | Confidence estimation |

## 🔄 Comparison with Alternatives

| Aspect | AGI Framework | LangGraph | CrewAI | AutoGen |
|--------|---------------|-----------|--------|---------|
| **Graph Orchestration** | ✅ Native | ✅ Native | ❌ Sequential | ❌ Sequential |
| **Self-Awareness** | ✅ Built-in | ❌ No | ❌ No | ❌ No |
| **Hybrid Memory** | ✅ Vector+Graph | ❌ Minimal | ❌ No | ❌ No |
| **Meta-Learning** | ✅ Yes | ❌ No | ❌ No | ❌ No |
| **Multi-Agent** | ✅ Crew | ⚠️ Limited | ✅ Yes | ✅ Yes |
| **Reasoning Patterns** | ✅ Full suite | ✅ Basic | ⚠️ Limited | ⚠️ Limited |
| **Observability** | ✅ Full | ✅ Full | ⚠️ Limited | ⚠️ Limited |
| **Type Safety** | ✅ Strict | ✅ Good | ⚠️ Limited | ❌ No |

## 📚 Documentation

- **[GETTING_STARTED.md](docs/GETTING_STARTED.md)** - Installation and quick start
- **[ARCHITECTURE.md](docs/ARCHITECTURE.md)** - Detailed system architecture
- **[API_REFERENCE.md](docs/API_REFERENCE.md)** - Complete API documentation
- **[deepdive/](docs/deepdive/)** - Advanced topics (graphs, memory, reasoning)
- **[examples/](examples/)** - Runnable examples and Jupyter notebooks

## 🎓 Examples

### Basic Agent
```python
from agents import Agent
from reasoning import ReAct

agent = Agent(
    name="ResearchAgent",
    reasoning_pattern=ReAct(),
    tools=["search", "summarize"]
)

result = agent.run("What are recent advances in AGI?")
```

### Multi-Agent Crew
```python
from agents import Crew, Agent

crew = Crew(
    supervisor_agent=Agent(name="Supervisor"),
    agents=[
        Agent(name="Researcher", role="research"),
        Agent(name="Planner", role="planning"),
        Agent(name="Executor", role="execution"),
    ],
    communication_pattern="hierarchical"
)

result = crew.run("Solve a complex problem")
```

### Self-Improving Loop
```python
from core import AGISystem

agi = AGISystem(enable_self_improvement=True)
agi.train(data_source="./data", epochs=100)

# System automatically improves itself
introspection = agi.selfaware_introspection()
improvement_plan = agi.self_improvement.generate_improvement_plan()
```

See [examples/](examples/) for more.

## 🏗️ Installation & Setup

### Prerequisites
- Python 3.9+
- pip or uv

### Installation

```bash
# Clone
git clone https://github.com/tuanthescientist/AGI.git
cd AGI

# With pip
pip install -e ".[dev]"

# Or with pip (minimal)
pip install -r requirements.txt

# Optional dependencies
pip install -e ".[memory]"      # Vector stores + Graph DB
pip install -e ".[training]"    # Advanced training
pip install -e ".[multiagent]"  # Multi-agent features
pip install -e ".[eval]"        # Evaluation benchmarks
```

### Supported LLM Backends

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local models (Ollama, llama.cpp, vLLM)
- Hugging Face models
- Custom model providers

## 🧪 Running Tests

```bash
# All tests
pytest

# Specific module
pytest tests/test_agents.py -v

# With coverage
pytest --cov=core --cov=agents tests/
```

## 📊 Benchmarks

Built-in evaluation on:
- **General Knowledge**: MMLU (5-shot)
- **Math Reasoning**: GSM8K
- **Code**: HumanEval
- **Agent Tasks**: AgentBench, GAIA
- **Self-Awareness**: Custom metrics

Run benchmarks:
```bash
python -m evaluation.benchmarks --suite full
```

## 🤝 Contributing

Contributions welcome! See [CONTRIBUTING.md](docs/CONTRIBUTING.md).

Key areas:
- [ ] Vision-language integration
- [ ] Extended reasoning patterns
- [ ] Specialized memory optimizations
- [ ] New agent archetypes
- [ ] Benchmark improvements

## 📖 Citation

If you use AGI Framework in research, please cite:

```bibtex
@software{tran2026agi,
  title={AGI Framework: A Modular Framework for Self-Improving AGI Systems},
  author={Tran, Tuan},
  year={2026},
  url={https://github.com/tuanthescientist/AGI}
}
```

## 📞 Support & Community

- **Issues**: [GitHub Issues](https://github.com/tuanthescientist/AGI/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tuanthescientist/AGI/discussions)
- **Email**: tuanthescientist@gmail.com

## 📜 License

MIT License - see [LICENSE](LICENSE) for details
