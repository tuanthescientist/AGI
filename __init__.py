"""AGI System - Advanced General Intelligence with Self-Awareness"""

__version__ = "0.1.0"
__author__ = "Tu An (tuanthescientist)"

from core.agi_engine import AGISystem
from algorithms.core_algorithms import get_algorithm
from training.training_systems import TrainingManager, AdaptiveTrainer
from infrastructure.distributed_training import InfrastructureManager
from data.data_pipeline import DataPipeline
from evaluation.metrics import EvaluationManager
from utils.helpers import Config, ExperimentTracker, Timer

__all__ = [
    "AGISystem",
    "get_algorithm",
    "TrainingManager",
    "AdaptiveTrainer",
    "InfrastructureManager",
    "DataPipeline",
    "EvaluationManager",
    "Config",
    "ExperimentTracker",
    "Timer",
]
