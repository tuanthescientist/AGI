# Getting Started with AGI System

## Quick Start

### 1. Clone the Repository
```bash
git clone https://github.com/tuanthescientist/AGI.git
cd AGI
```

### 2. Setup Environment
```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Install package in development mode
pip install -e .
```

### 3. Initialize Directories
```bash
python scripts/init_directories.py
```

### 4. Run Training Example
```bash
python experiments/train_example.py
```

### 5. Run Evaluation Example
```bash
python experiments/eval_example.py
```

## Core Concepts

### Self-Awareness
The AGI system monitors its own performance and identifies areas for improvement:

```python
from core.agi_engine import AGISystem

agi = AGISystem()
introspection = agi.selfaware_introspection()
print(f"Health Status: {introspection['health_status']}")
print(f"Improvement Areas: {introspection['improvement_areas']}")
```

### Self-Improvement
The system can autonomously improve itself:

```python
# Generate improvement plan
improvement_plan = agi.self_improvement.generate_improvement_plan()

# Apply improvements
agi.self_improvement.apply_improvements(improvement_plan)
```

### Meta-Learning
Learn to learn using few-shot adaptation:

```python
from algorithms.core_algorithms import get_algorithm

maml = get_algorithm('maml', model_fn=your_model)
loss = maml.backward(x_support, y_support)
```

### Continual Learning
Learn new tasks without forgetting old ones:

```python
from training.training_systems import ContinualLearningPipeline

continual = ContinualLearningPipeline()
continual.add_task(new_task_data)
result = continual.rehearsal_training(new_task_data)
```

### Multi-Task Learning
Learn multiple objectives simultaneously:

```python
from training.training_systems import MultiTaskLearner

multi_task = MultiTaskLearner(['task1', 'task2', 'task3'])
loss = multi_task.compute_loss(predictions, targets)
```

### Distributed Training
Scale training across multiple GPUs:

```python
from infrastructure.distributed_training import DistributedTrainer

trainer = DistributedTrainer(num_workers=4)
result = trainer.synchronous_update(batch)
```

### Data Pipeline
Complete data processing pipeline:

```python
from data.data_pipeline import DataPipeline

pipeline = DataPipeline()
result = pipeline.run_pipeline({
    'source1_config': {'type': 'synthetic'},
    'augmentation_factor': 2
})
```

### Evaluation
Comprehensive evaluation framework:

```python
from evaluation.metrics import EvaluationManager

eval_manager = EvaluationManager()
report = eval_manager.generate_comprehensive_report(model, test_data)
```

## Project Structure

```
AGI/
├── core/                      # Core AGI engine
│   ├── agi_engine.py         # Main engine with self-awareness
│   └── __init__.py
├── algorithms/                # AI/ML algorithms
│   ├── core_algorithms.py     # Transformers, MAML, GNN, RL, etc.
│   └── __init__.py
├── training/                  # Training systems
│   ├── training_systems.py    # Curriculum, multi-task, federated, etc.
│   └── __init__.py
├── infrastructure/            # Distributed training infrastructure
│   ├── distributed_training.py
│   └── __init__.py
├── data/                      # Data management
│   ├── data_pipeline.py       # Data processing pipeline
│   └── __init__.py
├── evaluation/                # Evaluation framework
│   ├── metrics.py
│   └── __init__.py
├── utils/                     # Utilities
│   ├── helpers.py
│   └── __init__.py
├── configs/
│   └── config.yaml            # Configuration file
├── experiments/
│   ├── train_example.py       # Example training script
│   ├── eval_example.py        # Example evaluation script
│   └── __init__.py
├── docs/
│   ├── ARCHITECTURE.md        # System architecture
│   ├── CONTRIBUTING.md        # Contributing guidelines
│   └── GETTING_STARTED.md
├── scripts/
│   └── init_directories.py    # Setup helper
├── requirements.txt
├── setup.py
├── README.md
└── LICENSE

```

## Configuration

Edit `configs/config.yaml` to customize:

```yaml
MODEL:
  type: "meta-transformer"
  hidden_dim: 512
  num_heads: 8

TRAINING:
  epochs: 100
  batch_size: 32
  enable_self_improvement: true

DATA:
  train_split: 0.8
  val_split: 0.1
  data_augmentation: true

DISTRIBUTED:
  num_workers: 4
```

## Key Features

✅ **Self-Aware AGI Engine** - Monitors and improves itself  
✅ **Advanced Algorithms** - Transformers, MAML, GNN, RL, etc.  
✅ **Flexible Training** - Curriculum, multi-task, federated, continual  
✅ **Distributed Infrastructure** - Multi-GPU/TPU coordination  
✅ **Data Pipeline** - Collection, processing, validation, privacy  
✅ **Comprehensive Evaluation** - Benchmarks, reasoning, self-awareness metrics  
✅ **Production Ready** - Monitoring, checkpointing, deployment pipeline  

## Running Examples

### Basic Training
```bash
python experiments/train_example.py
```

### Full Evaluation
```bash
python experiments/eval_example.py
```

### Custom Training Script
```python
from core.agi_engine import AGISystem
from utils.helpers import ExperimentTracker, Timer

tracker = ExperimentTracker()
exp_id = tracker.start_experiment("my_experiment", config)

agi = AGISystem(model_type="meta-transformer")
agi.train(data_source="./data", epochs=50, enable_self_improvement=True)

response = agi.query("What are your capabilities?", reasoning_depth="deep")

tracker.log_metric('response_confidence', response['confidence'])
tracker.end_experiment()
```

## Troubleshooting

### Import Errors
```bash
# Make sure package is installed
pip install -e .

# Check Python path
python -c "import sys; print('\n'.join(sys.path))"
```

### Memory Issues
- Reduce batch size in `config.yaml`
- Enable gradient checkpointing
- Use mixed precision training

### GPU Not Detected
```bash
python -c "import torch; print(torch.cuda.is_available())"
```

## Performance Optimization

### Memory Optimization
- Enable gradient checkpointing
- Use mixed precision (fp16)
- Reduce model size

### Speed Optimization
- Distribute across multiple GPUs
- Use compiled operators
- Profile with `python -m cProfile`

### Accuracy Optimization
- Enable self-improvement
- Use curriculum learning
- Ensemble multiple models

## Next Steps

1. ✅ Read [ARCHITECTURE.md](docs/ARCHITECTURE.md)
2. ✅ Run training and evaluation examples
3. ✅ Explore [experiments/](experiments/) directory
4. ✅ Modify [configs/config.yaml](configs/config.yaml)
5. ✅ Extend with custom algorithms
6. ✅ Deploy in production environment

## Additional Resources

- **Paper**: [Attention Is All You Need](https://arxiv.org/abs/1706.03762)
- **Paper**: [Model-Agnostic Meta-Learning](https://arxiv.org/abs/1703.03400)
- **Paper**: [Continual Lifelong Learning](https://arxiv.org/abs/2003.05495)
- **GitHub**: [PyTorch](https://github.com/pytorch/pytorch)

## Support

- Open an issue on GitHub
- Check existing issues and discussions
- Review architecture documentation

---

**Happy Learning! 🚀**
