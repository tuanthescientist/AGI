"""
Utility functions and helpers for AGI system
"""

import logging
from typing import Dict, Any, Optional, List
import json
import numpy as np
from datetime import datetime
import os

logger = logging.getLogger(__name__)


def setup_logging(log_level: int = logging.INFO, log_file: Optional[str] = None):
    """Setup logging configuration"""
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    
    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    
    # Get root logger
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    root_logger.addHandler(console_handler)
    
    # File handler
    if log_file:
        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        root_logger.addHandler(file_handler)


def save_json(data: Any, filepath: str, indent: int = 2):
    """Save data to JSON file"""
    with open(filepath, 'w') as f:
        json.dump(data, f, indent=indent, default=str)
    logger.info(f"Saved to {filepath}")


def load_json(filepath: str) -> Any:
    """Load data from JSON file"""
    with open(filepath, 'r') as f:
        data = json.load(f)
    logger.info(f"Loaded from {filepath}")
    return data


def save_numpy(data: np.ndarray, filepath: str):
    """Save numpy array"""
    np.save(filepath, data)
    logger.info(f"Saved numpy array to {filepath}")


def load_numpy(filepath: str) -> np.ndarray:
    """Load numpy array"""
    data = np.load(filepath)
    logger.info(f"Loaded numpy array from {filepath}")
    return data


class Config:
    """Configuration management"""
    
    def __init__(self, config_dict: Optional[Dict] = None):
        self.config = config_dict or {}
        
    def get(self, key: str, default: Any = None) -> Any:
        """Get config value"""
        return self.config.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set config value"""
        self.config[key] = value
    
    def update(self, config_dict: Dict):
        """Update config from dict"""
        self.config.update(config_dict)
    
    def save(self, filepath: str):
        """Save config to file"""
        save_json(self.config, filepath)
    
    @classmethod
    def load(cls, filepath: str):
        """Load config from file"""
        config_dict = load_json(filepath)
        return cls(config_dict)


class Timer:
    """Simple timer utility"""
    
    def __init__(self, name: str = ""):
        self.name = name
        self.start_time = None
        self.end_time = None
        
    def __enter__(self):
        self.start_time = datetime.now()
        return self
    
    def __exit__(self, *args):
        self.end_time = datetime.now()
        duration = (self.end_time - self.start_time).total_seconds()
        logger.info(f"Timer '{self.name}' took {duration:.4f} seconds")
    
    def elapsed(self) -> float:
        """Get elapsed time in seconds"""
        if self.end_time and self.start_time:
            return (self.end_time - self.start_time).total_seconds()
        return None


class ExperimentTracker:
    """Track experiments and results"""
    
    def __init__(self, experiment_dir: str = "./experiments"):
        self.experiment_dir = experiment_dir
        self.experiments = []
        self.current_experiment = None
        
        os.makedirs(experiment_dir, exist_ok=True)
    
    def start_experiment(self, name: str, config: Dict) -> str:
        """Start new experiment"""
        exp_id = f"{name}_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        self.current_experiment = {
            'id': exp_id,
            'name': name,
            'config': config,
            'start_time': datetime.now(),
            'metrics': {},
            'artifacts': []
        }
        
        self.experiments.append(self.current_experiment)
        logger.info(f"Experiment started: {exp_id}")
        
        return exp_id
    
    def log_metric(self, metric_name: str, value: Any, step: Optional[int] = None):
        """Log metric for current experiment"""
        if self.current_experiment is None:
            logger.warning("No active experiment")
            return
        
        if metric_name not in self.current_experiment['metrics']:
            self.current_experiment['metrics'][metric_name] = []
        
        self.current_experiment['metrics'][metric_name].append({
            'value': value,
            'step': step,
            'timestamp': datetime.now()
        })
    
    def save_artifact(self, artifact_path: str):
        """Save artifact for current experiment"""
        if self.current_experiment is None:
            logger.warning("No active experiment")
            return
        
        self.current_experiment['artifacts'].append(artifact_path)
        logger.info(f"Artifact saved: {artifact_path}")
    
    def end_experiment(self):
        """End current experiment"""
        if self.current_experiment is None:
            logger.warning("No active experiment")
            return
        
        self.current_experiment['end_time'] = datetime.now()
        duration = (self.current_experiment['end_time'] - 
                   self.current_experiment['start_time']).total_seconds()
        
        # Save experiment summary
        exp_dir = os.path.join(self.experiment_dir, self.current_experiment['id'])
        os.makedirs(exp_dir, exist_ok=True)
        
        save_json(self.current_experiment, 
                 os.path.join(exp_dir, 'summary.json'))
        
        logger.info(f"Experiment ended: {self.current_experiment['id']} (Duration: {duration:.2f}s)")
        
        self.current_experiment = None


def print_banner(text: str, width: int = 60):
    """Print formatted banner"""
    print("\n" + "=" * width)
    print(f" {text.center(width-2)} ")
    print("=" * width + "\n")


def print_metrics(metrics: Dict, title: str = "Metrics"):
    """Pretty print metrics"""
    print(f"\n{title}:")
    print("-" * 40)
    for key, value in metrics.items():
        if isinstance(value, float):
            print(f"  {key:.<30} {value:.6f}")
        else:
            print(f"  {key:.<30} {value}")
    print()


def get_system_info() -> Dict:
    """Get system information"""
    import platform
    
    info = {
        'os': platform.system(),
        'os_version': platform.release(),
        'python_version': platform.python_version(),
        'processor': platform.processor(),
        'timestamp': datetime.now()
    }
    
    # Try to get GPU info
    try:
        import torch
        info['pytorch_version'] = torch.__version__
        info['cuda_available'] = torch.cuda.is_available()
        if torch.cuda.is_available():
            info['gpu_count'] = torch.cuda.device_count()
    except ImportError:
        pass
    
    return info
