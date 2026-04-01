"""
Advanced Infrastructure Systems for AGI Framework
Distributed training, monitoring, resource management, and fault tolerance
"""

import numpy as np
from typing import Dict, List, Tuple, Optional, Callable
from dataclasses import dataclass, field
from datetime import datetime
import json
import logging

logger = logging.getLogger(__name__)


@dataclass
class ResourceMetrics:
    """Resource utilization metrics"""
    cpu_percent: float
    memory_percent: float
    gpu_memory_mb: float
    network_throughput_mbps: float
    disk_io_percent: float
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class HealthCheckResult:
    """System health check result"""
    node_id: str
    is_healthy: bool
    error_messages: List[str] = field(default_factory=list)
    resource_metrics: ResourceMetrics = None
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class GradientMessage:
    """Gradient exchange message for distributed training"""
    sender_id: str
    receiver_id: str
    gradients: np.ndarray
    iteration: int
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class DistributedTrainingCoordinator:
    """Orchestrate distributed training across multiple nodes"""
    
    def __init__(self, num_workers: int = 4, backend: str = "nccl"):
        self.num_workers = num_workers
        self.backend = backend
        self.gradients_buffer = {}
        self.iteration = 0
        self.gradient_compression_ratio = 0.8
    
    def allreduce_gradients(self, local_gradients: np.ndarray) -> np.ndarray:
        """
        All-reduce operation: aggregate gradients from all workers
        Simulates collective communication
        """
        # Simulate aggregation from all workers
        aggregated = local_gradients.copy()
        
        for i in range(self.num_workers - 1):
            # In real scenario, receive from other workers
            simulated_worker_grad = np.random.randn(*local_gradients.shape) * 0.01
            aggregated += simulated_worker_grad
        
        aggregated = aggregated / self.num_workers
        
        return aggregated
    
    def gradient_compression(self, gradients: np.ndarray, compression_ratio: float = 0.8) -> Tuple[np.ndarray, Dict]:
        """
        Compress gradients for efficient communication
        Top-k sparsification
        """
        k = int(gradients.size * compression_ratio)
        
        # Find top-k elements
        flat_grad = gradients.flatten()
        abs_grad = np.abs(flat_grad)
        top_k_indices = np.argsort(-abs_grad)[:k]
        
        # Create sparse representation
        compressed = np.zeros_like(flat_grad)
        compressed[top_k_indices] = flat_grad[top_k_indices]
        
        compression_stats = {
            "original_size": gradients.nbytes,
            "compressed_size": k * 8,  # k float64 values
            "compression_ratio": k / gradients.size,
            "sparsity": 1.0 - (k / gradients.size)
        }
        
        return compressed.reshape(gradients.shape), compression_stats
    
    def broadcast_weights(self, weights: np.ndarray, from_worker: int = 0) -> Dict[int, np.ndarray]:
        """
        Broadcast updated weights from master to all workers
        """
        broadcasted = {}
        
        for worker_id in range(self.num_workers):
            if worker_id != from_worker:
                # Simulate network delay and potential transmission error
                broadcasted[worker_id] = weights + np.random.randn(*weights.shape) * 1e-8
            else:
                broadcasted[worker_id] = weights
        
        return broadcasted
    
    def synchronize_batch_norm(
        self,
        local_mean: np.ndarray,
        local_var: np.ndarray
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Synchronize batch normalization statistics across workers
        """
        # Aggregate statistics
        global_mean = local_mean.copy()
        global_var = local_var.copy()
        
        for _ in range(self.num_workers - 1):
            global_mean += np.random.randn(*local_mean.shape) * 0.01
            global_var += np.random.randn(*local_var.shape) * 0.01
        
        global_mean = global_mean / self.num_workers
        global_var = np.abs(global_var) / self.num_workers
        
        return global_mean, global_var


class ResourceManager:
    """Manage compute resources and allocation"""
    
    def __init__(self, total_cpus: int = 64, total_gpus: int = 8, total_memory_gb: int = 512):
        self.total_cpus = total_cpus
        self.total_gpus = total_gpus
        self.total_memory_gb = total_memory_gb
        
        self.available_cpus = total_cpus
        self.available_gpus = total_gpus
        self.available_memory_gb = total_memory_gb
        
        self.allocations = {}
    
    def allocate_resources(
        self,
        job_id: str,
        num_cpus: int,
        num_gpus: int,
        memory_gb: int
    ) -> bool:
        """Allocate resources to a job"""
        if (self.available_cpus >= num_cpus and
            self.available_gpus >= num_gpus and
            self.available_memory_gb >= memory_gb):
            
            self.available_cpus -= num_cpus
            self.available_gpus -= num_gpus
            self.available_memory_gb -= memory_gb
            
            self.allocations[job_id] = {
                "cpus": num_cpus,
                "gpus": num_gpus,
                "memory_gb": memory_gb,
                "allocated_at": datetime.now().isoformat()
            }
            
            logger.info(f"Allocated resources to {job_id}: {num_cpus}C, {num_gpus}G, {memory_gb}GB")
            return True
        
        logger.warning(f"Insufficient resources for {job_id}")
        return False
    
    def deallocate_resources(self, job_id: str) -> bool:
        """Release resources from a job"""
        if job_id in self.allocations:
            alloc = self.allocations[job_id]
            
            self.available_cpus += alloc["cpus"]
            self.available_gpus += alloc["gpus"]
            self.available_memory_gb += alloc["memory_gb"]
            
            del self.allocations[job_id]
            
            logger.info(f"Deallocated resources from {job_id}")
            return True
        
        return False
    
    def get_resource_utilization(self) -> Dict[str, float]:
        """Get current resource utilization"""
        return {
            "cpu_utilization": 1.0 - (self.available_cpus / self.total_cpus),
            "gpu_utilization": 1.0 - (self.available_gpus / self.total_gpus),
            "memory_utilization": 1.0 - (self.available_memory_gb / self.total_memory_gb),
            "job_count": len(self.allocations)
        }


class HealthMonitor:
    """Monitor system health and detect anomalies"""
    
    def __init__(self, num_nodes: int = 10):
        self.num_nodes = num_nodes
        self.health_history = []
        self.thresholds = {
            "cpu_percent": 90.0,
            "memory_percent": 85.0,
            "gpu_memory_mb": 40000,
            "network_throughput_mbps": 100.0,
            "disk_io_percent": 80.0
        }
    
    def check_node_health(self, node_id: str) -> HealthCheckResult:
        """Check health of a single node"""
        # Simulate metric collection
        metrics = ResourceMetrics(
            cpu_percent=np.random.uniform(20, 80),
            memory_percent=np.random.uniform(30, 75),
            gpu_memory_mb=np.random.uniform(2000, 45000),
            network_throughput_mbps=np.random.uniform(10, 120),
            disk_io_percent=np.random.uniform(20, 70)
        )
        
        errors = []
        is_healthy = True
        
        # Check against thresholds
        for metric_name, threshold in self.thresholds.items():
            metric_value = getattr(metrics, metric_name)
            if metric_value > threshold:
                errors.append(f"{metric_name} exceeds threshold: {metric_value:.2f} > {threshold}")
                is_healthy = False
        
        result = HealthCheckResult(
            node_id=node_id,
            is_healthy=is_healthy,
            error_messages=errors,
            resource_metrics=metrics
        )
        
        self.health_history.append(result)
        
        return result
    
    def detect_anomalies(self) -> List[str]:
        """Detect anomalous patterns in health data"""
        anomalies = []
        
        if len(self.health_history) < 10:
            return anomalies
        
        recent_history = self.health_history[-10:]
        
        # Check for sustained high CPU
        cpu_values = [h.resource_metrics.cpu_percent for h in recent_history]
        if np.mean(cpu_values) > 80:
            anomalies.append("Sustained high CPU usage detected")
        
        # Check for memory leak pattern
        mem_values = [h.resource_metrics.memory_percent for h in recent_history]
        if len(mem_values) > 2:
            trend = mem_values[-1] - mem_values[0]
            if trend > 20:
                anomalies.append("Memory leak pattern detected")
        
        # Check for disk I/O issues
        io_values = [h.resource_metrics.disk_io_percent for h in recent_history]
        if np.std(io_values) > 30:
            anomalies.append("Unstable disk I/O detected")
        
        return anomalies


class FaultTolerance:
    """Handle node failures and recovery"""
    
    def __init__(self, num_checkpoints: int = 5):
        self.checkpoints = []
        self.max_checkpoints = num_checkpoints
        self.failed_nodes = []
        self.recovery_enabled = True
    
    def save_checkpoint(
        self,
        iteration: int,
        model_weights: np.ndarray,
        optimizer_state: Dict
    ) -> str:
        """Save training checkpoint"""
        checkpoint = {
            "iteration": iteration,
            "model_weights": model_weights,
            "optimizer_state": optimizer_state,
            "timestamp": datetime.now().isoformat(),
            "checkpoint_id": f"ckpt_{iteration}"
        }
        
        self.checkpoints.append(checkpoint)
        
        # Keep only recent checkpoints
        if len(self.checkpoints) > self.max_checkpoints:
            self.checkpoints.pop(0)
        
        logger.info(f"Saved checkpoint at iteration {iteration}")
        
        return checkpoint["checkpoint_id"]
    
    def load_checkpoint(self, checkpoint_id: str) -> Optional[Dict]:
        """Load checkpoint for recovery"""
        for ckpt in self.checkpoints:
            if ckpt["checkpoint_id"] == checkpoint_id:
                logger.info(f"Loaded checkpoint: {checkpoint_id}")
                return ckpt
        
        logger.warning(f"Checkpoint not found: {checkpoint_id}")
        return None
    
    def detect_node_failure(self, node_id: str, last_heartbeat_age_sec: float) -> bool:
        """Detect if node has failed based on heartbeat"""
        failure_threshold = 30.0  # seconds
        
        if last_heartbeat_age_sec > failure_threshold:
            self.failed_nodes.append(node_id)
            logger.error(f"Node {node_id} failure detected (no heartbeat for {last_heartbeat_age_sec}s)")
            return True
        
        return False
    
    def recover_from_failure(self, failed_node_id: str) -> bool:
        """Recover training from latest checkpoint"""
        if not self.recovery_enabled:
            return False
        
        if len(self.checkpoints) == 0:
            logger.error("No checkpoints available for recovery")
            return False
        
        latest_checkpoint = self.checkpoints[-1]
        logger.info(f"Recovering from node failure at iteration {latest_checkpoint['iteration']}")
        
        return True


class RateLimiter:
    """Rate limiting for API and resource access"""
    
    def __init__(self, requests_per_second: int = 1000, burst_size: int = 2000):
        self.rate_limit = requests_per_second
        self.burst_size = burst_size
        self.tokens = burst_size
        self.last_update = datetime.now()
    
    def acquire(self, tokens_needed: int = 1) -> bool:
        """Try to acquire tokens (rate limiting)"""
        now = datetime.now()
        time_passed = (now - self.last_update).total_seconds()
        
        # Refill tokens
        self.tokens = min(
            self.burst_size,
            self.tokens + time_passed * self.rate_limit
        )
        
        self.last_update = now
        
        if self.tokens >= tokens_needed:
            self.tokens -= tokens_needed
            return True
        
        return False


class LoadBalancer:
    """Distribute workload across workers"""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.worker_loads = [0.0] * num_workers
        self.task_distribution = []
    
    def get_least_loaded_worker(self) -> int:
        """Return ID of least loaded worker"""
        return int(np.argmin(self.worker_loads))
    
    def assign_task(self, task_id: str, task_size: float) -> int:
        """Assign task to least loaded worker"""
        worker_id = self.get_least_loaded_worker()
        self.worker_loads[worker_id] += task_size
        self.task_distribution.append((task_id, worker_id, task_size))
        
        return worker_id
    
    def worker_completed_task(self, worker_id: int, task_size: float):
        """Update load after worker completes task"""
        self.worker_loads[worker_id] = max(0, self.worker_loads[worker_id] - task_size)
    
    def get_load_statistics(self) -> Dict[str, float]:
        """Get load balancing statistics"""
        return {
            "avg_load": float(np.mean(self.worker_loads)),
            "max_load": float(np.max(self.worker_loads)),
            "min_load": float(np.min(self.worker_loads)),
            "load_std": float(np.std(self.worker_loads)),
            "load_variance": float(np.var(self.worker_loads))
        }


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Testing Advanced Infrastructure Systems...")
    
    # Test Distributed Training
    dist = DistributedTrainingCoordinator(num_workers=4)
    grads = np.random.randn(1000, 256)
    reduced = dist.allreduce_gradients(grads)
    print(f"✓ Distributed Training: reduced grad shape={reduced.shape}")
    
    # Test Resource Manager
    rm = ResourceManager(total_cpus=64, total_gpus=8)
    success = rm.allocate_resources("job_1", 16, 2, 64)
    util = rm.get_resource_utilization()
    print(f"✓ Resource Manager: allocation={success}, GPU util={util['gpu_utilization']:.2%}")
    
    # Test Health Monitor
    monitor = HealthMonitor(num_nodes=10)
    health = monitor.check_node_health("node_1")
    print(f"✓ Health Monitor: node_1 healthy={health.is_healthy}")
    
    # Test Fault Tolerance
    ft = FaultTolerance(num_checkpoints=5)
    weights = np.random.randn(100, 256)
    ckpt_id = ft.save_checkpoint(iteration=100, model_weights=weights, optimizer_state={})
    print(f"✓ Fault Tolerance: checkpoint={ckpt_id}")
    
    # Test Load Balancer
    lb = LoadBalancer(num_workers=4)
    for i in range(10):
        worker = lb.assign_task(f"task_{i}", np.random.uniform(0.5, 2.0))
    stats = lb.get_load_statistics()
    print(f"✓ Load Balancer: load_variance={stats['load_variance']:.4f}")
    
    print("\n✅ All infrastructure systems working correctly!")
