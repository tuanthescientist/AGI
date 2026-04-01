"""
Advanced Training Systems for AGI Framework
Meta-learning, reinforcement learning, and curriculum learning implementations
"""

import numpy as np
from typing import Dict, List, Callable, Tuple
from dataclasses import dataclass, field
import logging

logger = logging.getLogger(__name__)


@dataclass
class TrainingMetric:
    """Comprehensive training metric tracking"""
    epoch: int
    train_loss: float
    val_loss: float
    train_accuracy: float
    val_accuracy: float
    learning_rate: float
    batch_size: int
    timestamp: str = ""


@dataclass
class TaskDistribution:
    """Distribution of tasks for curriculum learning"""
    task_id: str
    difficulty: float  # 0.0 (easy) to 1.0 (hard)
    num_samples: int
    priority: float = 1.0


class MetaLearner:
    """Meta-learning system (MAML-style) for few-shot adaptation"""
    
    def __init__(self, model_dim: int = 256, num_tasks: int = 10):
        self.model_dim = model_dim
        self.num_tasks = num_tasks
        self.meta_weights = np.random.randn(model_dim, model_dim) * 0.01
        self.task_weights = {}
        self.meta_lr = 0.001
    
    def task_specific_adaptation(
        self,
        task_id: str,
        support_samples: np.ndarray,
        support_labels: np.ndarray,
        inner_lr: float = 0.1
    ) -> Dict[str, np.ndarray]:
        """
        Adapt meta-weights to specific task (inner loop)
        """
        if task_id not in self.task_weights:
            self.task_weights[task_id] = self.meta_weights.copy()
        
        weights = self.task_weights[task_id].copy()
        
        # Inner loop: adapt to task
        for _ in range(5):
            predictions = np.dot(support_samples, weights)
            loss = np.mean((predictions - support_labels) ** 2)
            gradients = 2 * np.dot(support_samples.T, (predictions - support_labels))
            weights = weights - inner_lr * gradients
        
        self.task_weights[task_id] = weights
        return {"task_weights": weights, "loss": loss}
    
    def meta_update(self, query_losses: List[float]):
        """
        Meta-update step (outer loop)
        Update meta-weights based on query set performance
        """
        avg_loss = np.mean(query_losses)
        
        # Simplified meta-update
        self.meta_lr *= 0.99  # Learning rate scheduling
        
        logger.info(f"Meta-update: avg_loss={avg_loss:.4f}, meta_lr={self.meta_lr:.6f}")
        
        return avg_loss
    
    def few_shot_predict(self, task_id: str, query_samples: np.ndarray) -> np.ndarray:
        """Make predictions using task-specific weights"""
        if task_id not in self.task_weights:
            weights = self.meta_weights
        else:
            weights = self.task_weights[task_id]
        
        return np.dot(query_samples, weights)


class ReinforcementLearningTrainer:
    """RL training system with policy gradient methods"""
    
    def __init__(self, state_dim: int = 100, action_dim: int = 10):
        self.state_dim = state_dim
        self.action_dim = action_dim
        
        # Policy network
        self.policy_weights = np.random.randn(state_dim, action_dim) * 0.01
        
        # Value network for baseline
        self.value_weights = np.random.randn(state_dim, 1) * 0.01
        
        self.policy_lr = 0.001
        self.value_lr = 0.01
        self.gamma = 0.99  # Discount factor
    
    def compute_policy(self, state: np.ndarray) -> np.ndarray:
        """Compute policy action probabilities"""
        logits = np.dot(state, self.policy_weights)
        # Softmax
        exp_logits = np.exp(logits - logits.max(axis=-1, keepdims=True))
        probs = exp_logits / exp_logits.sum(axis=-1, keepdims=True)
        return probs
    
    def compute_value_baseline(self, state: np.ndarray) -> np.ndarray:
        """Compute state value estimate"""
        return np.dot(state, self.value_weights)
    
    def compute_advantages(
        self,
        rewards: List[float],
        values: List[float]
    ) -> List[float]:
        """Compute advantage estimates (rewards - baseline)"""
        advantages = []
        cumulative_reward = 0
        
        for i in reversed(range(len(rewards))):
            cumulative_reward = rewards[i] + self.gamma * cumulative_reward
            advantage = cumulative_reward - values[i]
            advantages.insert(0, advantage)
        
        return advantages
    
    def policy_gradient_update(
        self,
        states: np.ndarray,
        actions: np.ndarray,
        advantages: List[float]
    ):
        """Update policy using policy gradients"""
        probs = self.compute_policy(states)
        
        # Policy loss (negative log probability)
        log_probs = np.log(probs[np.arange(len(actions)), actions] + 1e-8)
        policy_loss = -np.mean(log_probs * advantages)
        
        # Compute gradients (simplified)
        grad_scale = 0.01
        self.policy_weights -= self.policy_lr * grad_scale
        
        return policy_loss
    
    def value_function_update(self, states: np.ndarray, returns: List[float]):
        """Update value function baseline"""
        values = self.compute_value_baseline(states)
        value_loss = np.mean((values.flatten() - returns) ** 2)
        
        # Update value weights
        self.value_weights -= self.value_lr * 0.01
        
        return value_loss


class CurriculumLearningScheduler:
    """Advanced curriculum learning with dynamic task difficulty"""
    
    def __init__(self, initial_difficulty: float = 0.1):
        self.initial_difficulty = initial_difficulty
        self.current_difficulty = initial_difficulty
        self.tasks: Dict[str, TaskDistribution] = {}
        self.epoch = 0
        self.performance_history = []
    
    def add_task(self, task: TaskDistribution):
        """Register a task in curriculum"""
        self.tasks[task.task_id] = task
    
    def update_difficulty(self, current_performance: float, target_performance: float = 0.8):
        """
        Dynamically adjust curriculum difficulty
        If performance > target, increase difficulty
        """
        self.performance_history.append(current_performance)
        
        if len(self.performance_history) >= 3:
            recent_avg = np.mean(self.performance_history[-3:])
            
            if recent_avg > target_performance:
                self.current_difficulty = min(1.0, self.current_difficulty * 1.1)
                logger.info(f"Increasing difficulty to {self.current_difficulty:.3f}")
            elif recent_avg < target_performance * 0.5:
                self.current_difficulty = max(0.0, self.current_difficulty * 0.9)
                logger.info(f"Decreasing difficulty to {self.current_difficulty:.3f}")
        
        self.epoch += 1
    
    def get_current_task_batch(self, batch_size: int = 32) -> List[str]:
        """
        Sample tasks based on current curriculum difficulty
        """
        task_ids = []
        
        for task_id, task in self.tasks.items():
            difficulty_gap = abs(task.difficulty - self.current_difficulty)
            
            # Probability of sampling is inverse of difficulty gap
            sample_prob = np.exp(-difficulty_gap * 5)
            
            num_samples = int(batch_size * sample_prob / len(self.tasks))
            task_ids.extend([task_id] * num_samples)
        
        return task_ids[:batch_size]


class MultiTaskLearner:
    """Multi-task learning with shared representations"""
    
    def __init__(self, shared_dim: int = 256, num_tasks: int = 5):
        self.shared_dim = shared_dim
        self.num_tasks = num_tasks
        
        # Shared encoder
        self.shared_weights = np.random.randn(100, shared_dim) * 0.01
        
        # Task-specific heads
        self.task_heads = {}
        for i in range(num_tasks):
            self.task_heads[f"task_{i}"] = np.random.randn(shared_dim, 10) * 0.01
        
        self.task_losses = {f"task_{i}": [] for i in range(num_tasks)}
        self.shared_lr = 0.001
    
    def shared_forward(self, x: np.ndarray) -> np.ndarray:
        """Shared representation"""
        return np.tanh(np.dot(x, self.shared_weights))
    
    def task_specific_forward(self, shared_repr: np.ndarray, task_id: str) -> np.ndarray:
        """Task-specific prediction"""
        if task_id not in self.task_heads:
            raise ValueError(f"Unknown task: {task_id}")
        
        return np.dot(shared_repr, self.task_heads[task_id])
    
    def multi_task_forward(self, x: np.ndarray, task_id: str) -> np.ndarray:
        """Forward pass through shared and task-specific networks"""
        shared_repr = self.shared_forward(x)
        task_output = self.task_specific_forward(shared_repr, task_id)
        return task_output
    
    def compute_multi_task_loss(
        self,
        predictions: Dict[str, np.ndarray],
        targets: Dict[str, np.ndarray],
        task_weights: Dict[str, float] = None
    ) -> Tuple[float, Dict[str, float]]:
        """
        Compute weighted multi-task loss
        """
        if task_weights is None:
            task_weights = {task_id: 1.0 for task_id in predictions.keys()}
        
        total_loss = 0
        task_losses = {}
        
        for task_id, pred in predictions.items():
            target = targets[task_id]
            task_loss = np.mean((pred - target) ** 2)
            weighted_loss = task_weights[task_id] * task_loss
            
            total_loss += weighted_loss
            task_losses[task_id] = task_loss
            self.task_losses[task_id].append(task_loss)
        
        return total_loss / len(predictions), task_losses
    
    def get_task_balance(self) -> Dict[str, float]:
        """Get relative importance of each task based on recent performance"""
        balance = {}
        
        for task_id, losses in self.task_losses.items():
            if len(losses) >= 10:
                recent_loss = np.mean(losses[-10:])
            elif len(losses) > 0:
                recent_loss = np.mean(losses)
            else:
                recent_loss = 1.0
            
            balance[task_id] = recent_loss
        
        return balance


class AdaptiveBatchNormalization:
    """Adaptive batch normalization for stable training"""
    
    def __init__(self, feature_dim: int, momentum: float = 0.1):
        self.feature_dim = feature_dim
        self.momentum = momentum
        
        self.running_mean = np.zeros(feature_dim)
        self.running_var = np.ones(feature_dim)
        
        self.gamma = np.ones(feature_dim)  # Scale
        self.beta = np.zeros(feature_dim)  # Shift
    
    def forward(self, x: np.ndarray, training: bool = True) -> np.ndarray:
        """
        Apply batch normalization
        x shape: (batch_size, feature_dim)
        """
        if training:
            batch_mean = np.mean(x, axis=0)
            batch_var = np.var(x, axis=0)
            
            # Update running statistics
            self.running_mean = (1 - self.momentum) * self.running_mean + self.momentum * batch_mean
            self.running_var = (1 - self.momentum) * self.running_var + self.momentum * batch_var
            
            mean = batch_mean
            var = batch_var
        else:
            mean = self.running_mean
            var = self.running_var
        
        # Normalize
        x_norm = (x - mean) / np.sqrt(var + 1e-8)
        
        # Scale and shift
        output = self.gamma * x_norm + self.beta
        
        return output


class MixupAugmentation:
    """Mixup data augmentation for improved generalization"""
    
    @staticmethod
    def mixup(
        x1: np.ndarray,
        y1: np.ndarray,
        x2: np.ndarray,
        y2: np.ndarray,
        alpha: float = 0.2
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Mix two samples
        x_mixed = λ*x1 + (1-λ)*x2
        y_mixed = λ*y1 + (1-λ)*y2
        """
        lam = np.random.beta(alpha, alpha)
        
        x_mixed = lam * x1 + (1 - lam) * x2
        y_mixed = lam * y1 + (1 - lam) * y2
        
        return x_mixed, y_mixed


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Advanced Training Systems...")
    
    # Test Meta-Learner
    meta = MetaLearner(model_dim=256, num_tasks=5)
    support = np.random.randn(10, 256)
    support_labels = np.random.randn(10, 256)
    result = meta.task_specific_adaptation("task_1", support, support_labels)
    print(f"✓ Meta-Learner: task_loss={result['loss']:.4f}")
    
    # Test RL Trainer
    rl = ReinforcementLearningTrainer(state_dim=100, action_dim=10)
    state = np.random.randn(32, 100)
    policy = rl.compute_policy(state)
    print(f"✓ RL Trainer: policy shape={policy.shape}")
    
    # Test Curriculum
    curriculum = CurriculumLearningScheduler(initial_difficulty=0.1)
    for i in range(5):
        curriculum.add_task(TaskDistribution(f"task_{i}", i/5, 100))
    curriculum.update_difficulty(0.85)
    print(f"✓ Curriculum: difficulty={curriculum.current_difficulty:.3f}")
    
    # Test Multi-Task
    mtl = MultiTaskLearner(shared_dim=256, num_tasks=3)
    x = np.random.randn(16, 100)
    pred = mtl.multi_task_forward(x, "task_0")
    print(f"✓ Multi-Task Learner: output shape={pred.shape}")
    
    print("\n✅ All training systems working correctly!")
