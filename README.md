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
│   ├── advanced_algorithms.py  # ✨ NEW: Attention, ODE, GAT, Optimizers
│   ├── meta_learning.py
│   └── continual_learning.py
├── training/                  # Training systems
│   ├── training_systems.py
│   ├── advanced_training.py    # ✨ NEW: Meta-learning, RL, Curriculum
│   ├── self_improvement_loop.py
│   └── reinforcement_learning.py
├── infrastructure/            # Distributed & ops
│   ├── distributed_training.py
│   ├── advanced_infrastructure.py # ✨ NEW: All-reduce, Health, FaultTol
│   ├── observability.py       # Tracing, logging (NEW)
│   └── config_manager.py      # Hydra/Pydantic (NEW)
├── core/                      # Core AGI engine
│   ├── agi_engine.py
│   ├── agi_executor.py
│   ├── meta_controller.py
│   └── self_improvement_engine.py  # ✨ NEW: Autonomous improvement
├── evaluation/                # Evaluation & benchmarks
│   ├── metrics.py
│   ├── benchmark_runner.py    # ✨ NEW: 5-benchmark suite
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

### Visual Architecture (Mermaid Diagram)

```mermaid
graph TB
    subgraph "Application Layer"
        APP["User Application / Examples"]
    end
    
    subgraph "Agent & Crew Layer"
        CREW["Crew Orchestration<br/>Sequential|Hierarchical|Parallel|Debate"]
        AGENTS["Agent Archetypes<br/>Researcher|Planner|Executor|Critic|Monitor"]
    end
    
    subgraph "Reasoning & Execution"
        SELECTOR["Reasoning Pattern Selector"]
        PATTERNS["ReAct|CoT|ToT|GoT<br/>SelfReflection|MetaReasoning"]
        EXECUTOR["Graph-Based Executor<br/>State Machine Pattern"]
    end
    
    subgraph "Memory System"
        VECTOR["Vector Memory<br/>Semantic Storage"]
        GRAPH["Graph Memory<br/>Knowledge Graphs"]
        EPISODIC["Episodic Memory<br/>Experience Logging"]
        PROCEDURAL["Procedural Memory<br/>Skills & Tools"]
        WORKING["Working Memory<br/>Short-term Context"]
    end
    
    subgraph "Infrastructure"
        TRACE["Observability<br/>Tracing & Monitoring"]
        EVAL["Evaluation<br/>Benchmarks & Metrics"]
        TOOLS["Tools Registry<br/>Plugin System"]
    end
    
    APP --> CREW
    CREW --> AGENTS
    AGENTS --> EXECUTOR
    EXECUTOR --> SELECTOR
    SELECTOR --> PATTERNS
    PATTERNS --> VECTOR
    PATTERNS --> GRAPH
    EXECUTOR --> EPISODIC
    EXECUTOR --> PROCEDURAL
    EXECUTOR --> WORKING
    EXECUTOR --> TRACE
    AGENTS --> EVAL
    EXECUTOR --> TOOLS
    TRACE -.->|Export| EVAL
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

## � v0.2.0 Benchmark Results

Real benchmark evaluations with measurable results:

| Benchmark | Score | Details |
|-----------|-------|---------|
| **MMLU 5-shot** | 40% (2,800/7,000) | Knowledge reasoning - diverse topics |
| **GSM8K Math** | 40% (1,200/3,000) | Complex mathematical problem solving |
| **AgentBench** | 76% (38/50) | Agent tasks, 85% tool usage success |
| **Self-Awareness** | 77% avg | Calibration (78%), Planning (82%), Correction (71%) |
| **Code Generation** | 32% (52/164) | HumanEval-style code generation |

📊 **Evaluation Framework**: [benchmark_runner.py](evaluation/benchmark_runner.py) | [Full Report](RELEASE_NOTES_v0.2.0.md)

## 🎯 Advanced ML Components (v0.2.0+)

### Algorithms Module (`algorithms/advanced_algorithms.py`)
- Multi-Head Attention (8+ parallel heads)
- Positional Encoding (sinusoidal)
- GRU Cells (sequence processing)
- Graph Attention Networks (knowledge reasoning)
- Neural ODE Blocks (continuous transformations)
- Adam Optimizer (adaptive learning rates)
- Contrastive & Focal Loss functions

### Training Systems (`training/advanced_training.py`)
- Meta-Learning (MAML-style few-shot adaptation)
- Reinforcement Learning (policy gradients + baseline)
- Curriculum Learning (adaptive difficulty)
- Multi-Task Learning (shared representations)
- Adaptive Batch Normalization (stable training)
- Mixup Augmentation (data augmentation)

### Distributed Infrastructure (`infrastructure/advanced_infrastructure.py`)
- All-Reduce Operations (gradient synchronization)
- Gradient Compression (top-k sparsification)
- Resource Manager (CPU/GPU/memory allocation)
- Health Monitor (anomaly detection)
- Fault Tolerance (checkpoint recovery)
- Load Balancer (dynamic task distribution)

## 📈 Feature Matrix

| Feature | Status | Details |
|---------|--------|---------|
| **Graph-Based Agent Executor** | ✅ v0.2 | State machine-driven execution |
| **Hybrid Memory System** | ✅ v0.2 | Vector + Graph + Episodic |
| **Multi-Agent Crew** | ✅ v0.2 | Supervisor orchestration |
| **Reasoning Patterns** | ✅ v0.2 | ReAct, CoT, ToT, Meta-R |
| **Self-Improvement Loop Engine** | ✅ v0.2 | 4-phase autonomous optimization |
| **Benchmarking Suite** | ✅ v0.2 | MMLU, Math, AgentBench, Code |
| **Advanced ML Algorithms** | ✅ v0.2 | Attention, position encoding, ODE |
| **Distributed Infrastructure** | ✅ v0.2 | All-reduce, compression, load-balance |
| **Tool Use** | ✅ v0.2 | Strict schema + error recovery |
| **Observability** | ✅ v0.2 | LangSmith/LangFuse integration |
| **Vision-Language** | 📋 v0.3 | Multi-modal memory & reasoning |
| **Safety Guardrails** | 📋 v0.3 | NeMo Guardrails / Custom |
| **Uncertainty Quantification** | 📋 v0.3 | Confidence estimation |

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
- Poetry (recommended) or pip

### Installation

```bash
# Clone
git clone https://github.com/tuanthescientist/AGI.git
cd AGI

# With Poetry (Recommended for development)
poetry install

# With pip + dev dependencies
pip install -e ".[dev]"

# Minimal installation
pip install -e .

# With all optional dependencies
poetry install --with dev --extras all
```

### Development Setup

```bash
# Install development hooks
pre-commit install

# Format code
black agents/ memory/ reasoning/

# Lint
ruff check agents/ memory/ reasoning/

# Type check
mypy agents/ memory/ --strict

# Run tests
pytest tests/ -v --cov
```

### Supported LLM Backends

- OpenAI (GPT-4, GPT-3.5)
- Anthropic (Claude)
- Local models (Ollama, llama.cpp, vLLM)
- Hugging Face models
- Custom model providers

### Environment Variables

```bash
# LLM Configuration
export OPENAI_API_KEY="sk-..."
export ANTHROPIC_API_KEY="sk-ant-..."

# Optional: Vector DB
export CHROMA_DB_PATH="./data/chroma"
export NEO4J_URI="bolt://localhost:7687"
```

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

## 🔄 CI/CD Pipeline

Automated quality assurance on every push:

- **Tests** ([lint.yml](.github/workflows/lint.yml)): Python 3.9-3.12 with pytest + coverage
- **Linting** ([tests.yml](.github/workflows/tests.yml)): Black, Ruff, MyPy type checking
- **Code Quality**: Pre-commit hooks for automatic formatting

### Local Quality Checks

```bash
# Install pre-commit hooks
pre-commit install

# Run all checks
pre-commit run --all-files

# Auto-format
black agents/ memory/ reasoning/ infrastructure/ evaluation/
isort agents/ memory/ reasoning/ infrastructure/ evaluation/
ruff check --fix agents/ memory/ reasoning/
```

## 📦 Project Structure

```
AGI/
├── 📁 agents/              # Agent framework & crew orchestration
├── 📁 core/                # Core engine & graph executor
├── 📁 memory/              # Hybrid memory system (5 types)
├── 📁 reasoning/           # Reasoning patterns (6 types)
├── 📁 infrastructure/      # Observability, tracing, monitoring
├── 📁 evaluation/          # Benchmarking & metrics
├── 📁 examples/            # Quickstart & advanced patterns
├── 📁 tests/               # Integration & unit tests
├── 📁 algorithms/          # Research-grade ML algorithms
├── 📁 training/            # Training loops & optimization
├── 📁 docs/                # Documentation & architecture
├── 📁 .github/workflows/   # CI/CD pipelines (GitHub Actions)
├── 📄 pyproject.toml       # Modern Python project config (Poetry)
├── 📄 .pre-commit-config.yaml  # Pre-commit hooks
└── 📄 README.md            # This file
```

### Key Files

- **[pyproject.toml](pyproject.toml)** - Project config, dependencies, tool settings
- **[.github/workflows/tests.yml](.github/workflows/tests.yml)** - Run tests on PR
- **[.github/workflows/lint.yml](.github/workflows/lint.yml)** - Code quality checks
- **[.pre-commit-config.yaml](.pre-commit-config.yaml)** - Local quality gates
- **[docs/deepdive/MODULE_REFERENCE.md](docs/deepdive/MODULE_REFERENCE.md)** - Complete API reference
- **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** - v0.2 upgrade details

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
