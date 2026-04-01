"""
Quick reference and API documentation
"""

# AGI System - API Reference

## Core Engine

### AGISystem

```python
from core.agi_engine import AGISystem

# Initialize
agi = AGISystem(
    model_type="meta-transformer",
    memory_capacity=1.0e9
)

# Training
agi.train(
    data_source="./data/training_set",
    epochs=100,
    enable_self_improvement=True
)

# Query
response = agi.query(
    question="How can I improve?",
    reasoning_depth="deep"  # shallow, medium, deep
)

# Self-Awareness
introspection = agi.selfaware_introspection()

# Save/Load
agi.save_checkpoint("./checkpoints/model.json")
agi.load_checkpoint("./checkpoints/model.json")
```

### AGIMonitor

```python
from core.agi_engine import AGIMonitor

monitor = AGIMonitor()
monitor.log_metric("accuracy", 0.95)
bottlenecks = monitor.identify_bottlenecks()
health = monitor.get_health_status()
```

### MemorySystem

```python
from core.agi_engine import MemorySystem

memory = MemorySystem(capacity=1e9)
memory.store_experience("key1", data, memory_type="semantic")
retrieved = memory.retrieve("key1", memory_type="semantic")
memory.consolidate()
```

## Algorithms

### Getting Algorithms

```python
from algorithms.core_algorithms import get_algorithm, ALGORITHM_REGISTRY

# List available algorithms
print(ALGORITHM_REGISTRY.keys())

# Get algorithm
attention = get_algorithm('attention', dim=512, num_heads=8)
maml = get_algorithm('maml', model_fn=model)
gnn = get_algorithm('gnn', input_dim=10, hidden_dim=64, output_dim=5)
rl = get_algorithm('rl', state_dim=10, action_dim=5)
```

## Training Systems

### TrainingManager

```python
from training.training_systems import TrainingManager

trainer = TrainingManager()
results = trainer.run_training_pipeline({
    'federated_rounds': 5,
    'epochs': 100
})
```

### CurriculumLearning

```python
from training.training_systems import CurriculumLearning

curriculum = CurriculumLearning()
curriculum.add_curriculum(tasks, difficulties)
batch = curriculum.get_current_batch(batch_size=32)
curriculum.advance_curriculum()
```

### MultiTaskLearner

```python
from training.training_systems import MultiTaskLearner

multi_task = MultiTaskLearner(['task1', 'task2', 'task3'])
loss = multi_task.compute_loss(predictions, targets)
weights = multi_task.reweight_tasks()
```

### FederatedLearner

```python
from training.training_systems import FederatedLearner

fed_learner = FederatedLearner(num_clients=10)
for round_num in range(num_rounds):
    avg_loss = fed_learner.federated_round(data_shards)
```

### AdaptiveTrainer

```python
from training.training_systems import AdaptiveTrainer

trainer = AdaptiveTrainer()
epoch_stats = trainer.train_epoch(batch_data)
adaptation = trainer.evaluate_and_adapt(validation_data)
```

## Infrastructure

### DistributedTrainer

```python
from infrastructure.distributed_training import DistributedTrainer

dist_trainer = DistributedTrainer(num_workers=4)
result = dist_trainer.synchronous_update(batch)
```

### ResourceManager

```python
from infrastructure.distributed_training import ResourceManager

resource_mgr = ResourceManager()
resource_mgr.add_resource(resource)
allocated = resource_mgr.allocate_resources(requirements)
optimization = resource_mgr.optimize_allocation()
```

### MonitoringSystem

```python
from infrastructure.distributed_training import MonitoringSystem

monitor = MonitoringSystem()
monitor.record_metric('loss', 0.5)
checkpoint = monitor.save_checkpoint(model_state, 'ckpt_1')
health_report = monitor.get_health_report()
```

### ModelRegistry

```python
from infrastructure.distributed_training import ModelRegistry

registry = ModelRegistry()
version = registry.register_model('my_model', model_state)
model = registry.get_model(version)
latest = registry.get_latest_model('my_model')
```

## Data Pipeline

### DataPipeline

```python
from data.data_pipeline import DataPipeline

pipeline = DataPipeline()
result = pipeline.run_pipeline(config)
```

### DataCollector

```python
from data.data_pipeline import DataCollector

collector = DataCollector()
collector.register_source('source1', config)
data = collector.collect_from_source('source1', batch_size=1000)
```

### DataProcessor

```python
from data.data_pipeline import DataProcessor

processor = DataProcessor()
normalized = processor.normalize(data)
cleaned = processor.remove_outliers(data)
augmented = processor.augment_data(data, num_augmentations=2)
```

### DataLoader

```python
from data.data_pipeline import DataLoader

loader = DataLoader(batch_size=32, shuffle=True)
loader.load_data(x_data, y_data)
batches = loader.get_batches()
batch = loader.get_batch(batch_idx=0)
```

## Evaluation

### EvaluationManager

```python
from evaluation.metrics import EvaluationManager

eval_mgr = EvaluationManager()
report = eval_mgr.generate_comprehensive_report(model, test_data)
```

### MetricsCalculator

```python
from evaluation.metrics import MetricsCalculator

acc = MetricsCalculator.accuracy(predictions, targets)
metrics = MetricsCalculator.precision_recall_f1(predictions, targets)
mse = MetricsCalculator.mean_squared_error(predictions, targets)
auc = MetricsCalculator.roc_auc(predictions, targets)
```

### SelfAwarenessMetrics

```python
from evaluation.metrics import SelfAwarenessMetrics

self_aware = SelfAwarenessMetrics()
introspection = self_aware.measure_introspection(agi, queries)
uncertainty = self_aware.measure_uncertainty(predictions)
```

## Utilities

### Config

```python
from utils.helpers import Config

config = Config({'param1': value1})
value = config.get('param1')
config.set('param2', value2)
config.save('config.json')
config = Config.load('config.json')
```

### ExperimentTracker

```python
from utils.helpers import ExperimentTracker

tracker = ExperimentTracker()
exp_id = tracker.start_experiment('exp1', config)
tracker.log_metric('accuracy', 0.95, step=1)
tracker.save_artifact('artifact.pkl')
tracker.end_experiment()
```

### Timer

```python
from utils.helpers import Timer

with Timer("operation") as timer:
    # do something
    pass

elapsed = timer.elapsed()
```

### Logging

```python
from utils.helpers import setup_logging
import logging

setup_logging(log_level=logging.INFO, log_file='app.log')
logger = logging.getLogger(__name__)
logger.info("Message")
```

### Helper Functions

```python
from utils.helpers import (
    save_json, load_json,
    save_numpy, load_numpy,
    get_system_info,
    print_banner, print_metrics
)

save_json(data, 'file.json')
data = load_json('file.json')

save_numpy(array, 'array.npy')
array = load_numpy('array.npy')

info = get_system_info()

print_banner("Title")
print_metrics({'metric1': 0.95})
```

## Common Workflows

### 1. Self-Improving AGI Training

```python
from core.agi_engine import AGISystem
from utils.helpers import ExperimentTracker, Timer

tracker = ExperimentTracker()
tracker.start_experiment("self_improving_agi", config)

agi = AGISystem(model_type="meta-transformer")

with Timer("Training"):
    agi.train(
        data_source="./data",
        epochs=100,
        enable_self_improvement=True
    )

introspection = agi.selfaware_introspection()
improvement_plan = agi.self_improvement.generate_improvement_plan()

tracker.log_metric('improvements', len(improvement_plan['strategies']))
tracker.end_experiment()
```

### 2. Distributed Multi-GPU Training

```python
from infrastructure.distributed_training import DistributedTrainer, InfrastructureManager

infra = InfrastructureManager()
infra.setup_training_environment({'num_nodes': 4})

trainer = infra.distributed_trainer

for epoch in range(num_epochs):
    result = trainer.synchronous_update(batch)
    print(f"Loss: {result['average_loss']}")
```

### 3. Complete Data Pipeline

```python
from data.data_pipeline import DataPipeline

pipeline = DataPipeline()
result = pipeline.run_pipeline({
    'source1_config': {...},
    'augmentation_factor': 2,
    'normalize': True
})

dataset = pipeline.storage.retrieve('pipeline_output')
```

### 4. Comprehensive Evaluation

```python
from evaluation.metrics import EvaluationManager
from utils.helpers import Timer

eval_mgr = EvaluationManager()

with Timer("Full Evaluation"):
    report = eval_mgr.generate_comprehensive_report(model, test_data)

print(f"Accuracy: {report['evaluations']['basic_metrics']['accuracy']}")
```

## Tips & Best Practices

✅ Always use `ExperimentTracker` for reproducibility  
✅ Enable self-improvement for continuous optimization  
✅ Monitor system health regularly  
✅ Save checkpoints frequently  
✅ Use distributed training for large datasets  
✅ Evaluate on multiple benchmarks  
✅ Profile code for bottlenecks  
✅ Log metrics systematically  

## Performance Tips

- Use batch normalization
- Enable gradient checkpointing
- Use mixed precision (fp16)
- Profile with cProfile
- Monitor GPU memory
- Use data parallelism for large batches
- Enable model compilation

---

For more details, see [ARCHITECTURE.md](ARCHITECTURE.md) and [GETTING_STARTED.md](GETTING_STARTED.md)
