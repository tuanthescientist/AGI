"""
Infrastructure for distributed training and resource management
"""

import logging
from typing import Dict, List, Any, Optional
from dataclasses import dataclass
from datetime import datetime
import numpy as np

logger = logging.getLogger(__name__)


@dataclass
class ComputeResource:
    """Compute resource specification"""
    node_id: str
    gpu_memory: float
    cpu_cores: int
    network_bandwidth: float
    available: bool = True


class DistributedTrainer:
    """Distributed training coordinator for multi-GPU/TPU training"""
    
    def __init__(self, num_workers: int = 4):
        self.num_workers = num_workers
        self.workers = [self._create_worker(i) for i in range(num_workers)]
        self.global_step = 0
        self.communication_time = 0
        
    def _create_worker(self, worker_id: int) -> Dict:
        """Create a worker node"""
        return {
            'id': worker_id,
            'model_weights': np.random.randn(100, 50),
            'local_step': 0,
            'loss_history': []
        }
    
    def distribute_batch(self, batch: np.ndarray) -> List[np.ndarray]:
        """Distribute batch across workers"""
        batch_size = batch.shape[0]
        batch_per_worker = batch_size // self.num_workers
        
        distributed_batches = []
        for i in range(self.num_workers):
            start = i * batch_per_worker
            end = start + batch_per_worker if i < self.num_workers - 1 else batch_size
            distributed_batches.append(batch[start:end])
        
        return distributed_batches
    
    def all_reduce(self) -> np.ndarray:
        """All-reduce gradient aggregation"""
        aggregated = np.mean([w['model_weights'] for w in self.workers], axis=0)
        
        # Simulate communication
        self.communication_time += len(self.workers) * 0.001
        
        # Update all workers
        for worker in self.workers:
            worker['model_weights'] = aggregated.copy()
        
        logger.info(f"All-reduce completed. Global step: {self.global_step}")
        return aggregated
    
    def train_step(self, local_batch: np.ndarray, worker_id: int) -> float:
        """Execute training step on worker"""
        worker = self.workers[worker_id]
        
        # Simulate local training
        loss = np.random.randn() * 0.1 + 0.5
        worker['loss_history'].append(loss)
        worker['local_step'] += 1
        
        return loss
    
    def synchronous_update(self, batch: np.ndarray) -> Dict:
        """Synchronous distributed training step"""
        distributed_batches = self.distribute_batch(batch)
        losses = []
        
        # Local updates
        for worker_id, local_batch in enumerate(distributed_batches):
            loss = self.train_step(local_batch, worker_id)
            losses.append(loss)
        
        # Synchronize
        self.all_reduce()
        self.global_step += 1
        
        return {
            'global_step': self.global_step,
            'average_loss': np.mean(losses),
            'worker_losses': losses
        }


class ResourceManager:
    """Dynamic resource management for training"""
    
    def __init__(self):
        self.resources = []
        self.allocation_history = []
        self.utilization_targets = {
            'gpu_memory': 0.8,
            'cpu': 0.7,
            'network': 0.6
        }
        
    def add_resource(self, resource: ComputeResource):
        """Register a compute resource"""
        self.resources.append(resource)
        logger.info(f"Resource registered: {resource.node_id}")
    
    def allocate_resources(self, job_requirements: Dict) -> List[ComputeResource]:
        """Allocate resources based on job requirements"""
        required_gpu = job_requirements.get('gpu_memory', 0)
        required_cpu = job_requirements.get('cpu_cores', 0)
        
        allocated = []
        for resource in self.resources:
            if (resource.available and 
                resource.gpu_memory >= required_gpu and 
                resource.cpu_cores >= required_cpu):
                resource.available = False
                allocated.append(resource)
                
                if len(allocated) >= job_requirements.get('num_nodes', 1):
                    break
        
        self.allocation_history.append({
            'timestamp': datetime.now(),
            'allocated_nodes': len(allocated),
            'requested': job_requirements
        })
        
        logger.info(f"Allocated {len(allocated)} nodes")
        return allocated
    
    def release_resources(self, resources: List[ComputeResource]):
        """Release allocated resources"""
        for resource in resources:
            resource.available = True
        logger.info(f"Released {len(resources)} resources")
    
    def optimize_allocation(self) -> Dict:
        """Optimize resource allocation"""
        utilized = []
        underutilized = []
        
        for resource in self.resources:
            utilization = (1 - resource.gpu_memory / 100) if not resource.available else 0
            if utilization > 0.7:
                utilized.append(resource.node_id)
            elif utilization < 0.3 and not resource.available:
                underutilized.append(resource.node_id)
        
        return {
            'heavily_utilized': utilized,
            'underutilized': underutilized,
            'recommendation': "Scale up training parallelism" if len(utilized) > len(underutilized) else "Consider consolidation"
        }


class MonitoringSystem:
    """System monitoring and performance tracking"""
    
    def __init__(self):
        self.metrics = {}
        self.alerts = []
        self.checkpoints = []
        self.alert_thresholds = {
            'loss_explosion': 10.0,
            'memory_critical': 95.0,
            'gpu_temp': 85.0
        }
        
    def record_metric(self, metric_name: str, value: float):
        """Record a metric"""
        if metric_name not in self.metrics:
            self.metrics[metric_name] = []
        self.metrics[metric_name].append({
            'value': value,
            'timestamp': datetime.now()
        })
        
        # Check for alerts
        self._check_alerts(metric_name, value)
    
    def _check_alerts(self, metric_name: str, value: float):
        """Check if metric triggers any alerts"""
        if metric_name == 'loss' and value > self.alert_thresholds['loss_explosion']:
            self.alerts.append({
                'type': 'loss_explosion',
                'value': value,
                'timestamp': datetime.now(),
                'severity': 'critical'
            })
            logger.warning(f"ALERT: Loss explosion detected! Value: {value}")
        
        elif metric_name == 'memory_usage' and value > self.alert_thresholds['memory_critical']:
            self.alerts.append({
                'type': 'memory_critical',
                'value': value,
                'timestamp': datetime.now(),
                'severity': 'warning'
            })
            logger.warning(f"ALERT: Memory critical! Usage: {value}%")
    
    def save_checkpoint(self, model_state: Dict, checkpoint_name: str) -> Dict:
        """Save training checkpoint"""
        checkpoint = {
            'name': checkpoint_name,
            'timestamp': datetime.now(),
            'model_state': model_state,
            'metrics_snapshot': {k: v[-1] if v else None for k, v in self.metrics.items()}
        }
        self.checkpoints.append(checkpoint)
        logger.info(f"Checkpoint saved: {checkpoint_name}")
        return checkpoint
    
    def get_health_report(self) -> Dict:
        """Get system health report"""
        recent_alerts = self.alerts[-10:] if len(self.alerts) > 10 else self.alerts
        
        return {
            'timestamp': datetime.now(),
            'total_metrics_tracked': len(self.metrics),
            'total_checkpoints': len(self.checkpoints),
            'recent_alerts': recent_alerts,
            'system_status': 'healthy' if len(recent_alerts) == 0 else 'warning' if len(recent_alerts) < 3 else 'critical'
        }


class ModelRegistry:
    """Model versioning and management"""
    
    def __init__(self):
        self.models = {}
        self.version_history = []
        
    def register_model(self, model_name: str, model_state: Dict, 
                      metadata: Optional[Dict] = None) -> str:
        """Register a new model version"""
        version = f"{model_name}_v{len([v for v in self.version_history if v['model_name'] == model_name]) + 1}"
        
        self.models[version] = {
            'name': model_name,
            'state': model_state,
            'metadata': metadata or {},
            'registered_at': datetime.now()
        }
        
        self.version_history.append({
            'version': version,
            'model_name': model_name,
            'timestamp': datetime.now()
        })
        
        logger.info(f"Model registered: {version}")
        return version
    
    def get_model(self, version: str) -> Optional[Dict]:
        """Retrieve a model by version"""
        return self.models.get(version)
    
    def list_models(self, model_name: Optional[str] = None) -> List[str]:
        """List all registered models or specific versions"""
        if model_name:
            return [v for v in self.models if v.startswith(model_name)]
        return list(self.models.keys())
    
    def get_latest_model(self, model_name: str) -> Optional[Dict]:
        """Get latest version of a model"""
        versions = self.list_models(model_name)
        if versions:
            latest = max(versions, key=lambda v: self.models[v]['registered_at'])
            return self.models[latest]
        return None


class DeploymentPipeline:
    """Model deployment and A/B testing"""
    
    def __init__(self):
        self.deployments = []
        self.ab_tests = []
        
    def prepare_deployment(self, model_version: str, deployment_config: Dict) -> Dict:
        """Prepare model for deployment"""
        deployment = {
            'model_version': model_version,
            'config': deployment_config,
            'status': 'prepared',
            'prepared_at': datetime.now()
        }
        self.deployments.append(deployment)
        logger.info(f"Model prepared for deployment: {model_version}")
        return deployment
    
    def run_ab_test(self, model_a: str, model_b: str, test_data: List[Dict]) -> Dict:
        """Run A/B test between two models"""
        ab_test = {
            'model_a': model_a,
            'model_b': model_b,
            'sample_size': len(test_data),
            'model_a_score': np.random.uniform(0.7, 0.95),
            'model_b_score': np.random.uniform(0.7, 0.95),
            'timestamp': datetime.now()
        }
        
        ab_test['winner'] = model_a if ab_test['model_a_score'] > ab_test['model_b_score'] else model_b
        self.ab_tests.append(ab_test)
        
        logger.info(f"A/B test completed. Winner: {ab_test['winner']}")
        return ab_test


class InfrastructureManager:
    """High-level infrastructure manager"""
    
    def __init__(self):
        self.distributed_trainer = DistributedTrainer()
        self.resource_manager = ResourceManager()
        self.monitoring = MonitoringSystem()
        self.model_registry = ModelRegistry()
        self.deployment = DeploymentPipeline()
        
    def setup_training_environment(self, config: Dict) -> Dict:
        """Setup complete training environment"""
        logger.info("Setting up training environment...")
        
        # Add resources
        for i in range(config.get('num_nodes', 4)):
            resource = ComputeResource(
                node_id=f"node_{i}",
                gpu_memory=32,
                cpu_cores=32,
                network_bandwidth=100
            )
            self.resource_manager.add_resource(resource)
        
        # Allocate resources
        allocated = self.resource_manager.allocate_resources({
            'gpu_memory': 16,
            'cpu_cores': 16,
            'num_nodes': config.get('num_nodes', 4)
        })
        
        return {
            'resources_allocated': len(allocated),
            'distributed_trainer_ready': True,
            'monitoring_active': True
        }
