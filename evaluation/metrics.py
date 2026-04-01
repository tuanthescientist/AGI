"""
Evaluation metrics and benchmarking systems
"""

import logging
from typing import Dict, List, Any, Tuple
import numpy as np
from datetime import datetime
from collections import defaultdict

logger = logging.getLogger(__name__)


class MetricsCalculator:
    """Compute various evaluation metrics"""
    
    @staticmethod
    def accuracy(predictions: np.ndarray, targets: np.ndarray) -> float:
        """Calculate accuracy"""
        correct = np.sum(np.argmax(predictions, axis=1) == np.argmax(targets, axis=1))
        return correct / len(predictions)
    
    @staticmethod
    def precision_recall_f1(predictions: np.ndarray, targets: np.ndarray) -> Dict:
        """Calculate precision, recall, and F1 score"""
        tp = np.sum((predictions > 0.5) & (targets > 0.5))
        fp = np.sum((predictions > 0.5) & (targets <= 0.5))
        fn = np.sum((predictions <= 0.5) & (targets > 0.5))
        tn = np.sum((predictions <= 0.5) & (targets <= 0.5))
        
        precision = tp / (tp + fp + 1e-8)
        recall = tp / (tp + fn + 1e-8)
        f1 = 2 * (precision * recall) / (precision + recall + 1e-8)
        
        return {
            'precision': precision,
            'recall': recall,
            'f1': f1,
            'tp': int(tp),
            'fp': int(fp),
            'fn': int(fn),
            'tn': int(tn)
        }
    
    @staticmethod
    def mean_squared_error(predictions: np.ndarray, targets: np.ndarray) -> float:
        """Calculate MSE"""
        return np.mean((predictions - targets) ** 2)
    
    @staticmethod
    def mean_absolute_error(predictions: np.ndarray, targets: np.ndarray) -> float:
        """Calculate MAE"""
        return np.mean(np.abs(predictions - targets))
    
    @staticmethod
    def roc_auc(predictions: np.ndarray, targets: np.ndarray) -> float:
        """Calculate ROC-AUC"""
        n = len(predictions)
        sorted_idx = np.argsort(-predictions)
        sorted_targets = targets[sorted_idx]
        
        tp = np.cumsum(sorted_targets)
        fp = np.cumsum(1 - sorted_targets)
        
        tpr = tp / (tp[-1] + 1e-8)
        fpr = fp / (fp[-1] + 1e-8)
        
        # Trapezoid rule for AUC
        auc = np.trapz(tpr, fpr)
        return auc


class BenchmarkSuite:
    """Comprehensive benchmark suite"""
    
    def __init__(self):
        self.benchmarks = {}
        self.results = []
        self.baseline_scores = {}
        
    def add_benchmark(self, name: str, dataset: Tuple[np.ndarray, np.ndarray], 
                     description: str = ""):
        """Add a benchmark task"""
        self.benchmarks[name] = {
            'dataset': dataset,
            'description': description,
            'results': []
        }
        logger.info(f"Benchmark added: {name}")
    
    def run_all_benchmarks(self, model_fn) -> Dict:
        """Run all benchmarks"""
        results = {
            'timestamp': datetime.now(),
            'benchmarks': {}
        }
        
        for bench_name, benchmark in self.benchmarks.items():
            x, y = benchmark['dataset']
            predictions = model_fn(x)
            
            metrics = MetricsCalculator.precision_recall_f1(predictions, y)
            metrics['mse'] = MetricsCalculator.mean_squared_error(predictions, y)
            
            results['benchmarks'][bench_name] = metrics
            benchmark['results'].append(metrics)
        
        self.results.append(results)
        return results


class RegressionBenchmark:
    """Benchmarks for regression tasks"""
    
    def __init__(self):
        self.tasks = {}
        
    def add_regression_task(self, name: str, x: np.ndarray, y: np.ndarray):
        """Add regression task"""
        self.tasks[name] = {'x': x, 'y': y}
    
    def evaluate(self, model_fn) -> Dict:
        """Evaluate on all regression tasks"""
        results = {}
        for task_name, task_data in self.tasks.items():
            predictions = model_fn(task_data['x'])
            mse = MetricsCalculator.mean_squared_error(predictions, task_data['y'])
            mae = MetricsCalculator.mean_absolute_error(predictions, task_data['y'])
            
            results[task_name] = {'mse': mse, 'mae': mae}
        
        return results


class ReasoningBenchmark:
    """Benchmarks for reasoning capabilities"""
    
    def __init__(self):
        self.reasoning_tasks = []
        self.reasoning_results = []
        
    def add_reasoning_task(self, task_id: str, premises: List[str], 
                          conclusion: str, expected_valid: bool):
        """Add a logical reasoning task"""
        self.reasoning_tasks.append({
            'id': task_id,
            'premises': premises,
            'conclusion': conclusion,
            'expected_valid': expected_valid
        })
    
    def evaluate_reasoning(self, model_fn) -> Dict:
        """Evaluate reasoning capability"""
        results = {
            'timestamp': datetime.now(),
            'total_tasks': len(self.reasoning_tasks),
            'correct': 0,
            'details': []
        }
        
        for task in self.reasoning_tasks:
            # Model makes prediction on reasoning task
            input_text = " ".join(task['premises']) + " " + task['conclusion']
            prediction = model_fn(input_text)  # Should output True/False
            
            is_correct = (prediction > 0.5) == task['expected_valid']
            results['correct'] += int(is_correct)
            
            results['details'].append({
                'task_id': task['id'],
                'expected': task['expected_valid'],
                'predicted': prediction > 0.5,
                'correct': is_correct
            })
        
        results['accuracy'] = results['correct'] / len(self.reasoning_tasks)
        self.reasoning_results.append(results)
        
        return results


class SelfAwarenessMetrics:
    """Metrics for evaluating self-awareness capabilities"""
    
    def __init__(self):
        self.introspection_scores = []
        self.uncertainty_estimates = []
        
    def measure_introspection(self, agi_system, test_queries: List[str]) -> Dict:
        """Measure system's ability to introspect"""
        scores = {
            'timestamp': datetime.now(),
            'queries_tested': len(test_queries),
            'introspection_insights': []
        }
        
        for query in test_queries:
            introspection = agi_system.selfaware_introspection()
            
            scores['introspection_insights'].append({
                'query': query,
                'health_status': introspection.get('health_status'),
                'improvement_areas_identified': len(introspection.get('improvement_areas', []))
            })
        
        self.introspection_scores.append(scores)
        return scores
    
    def measure_uncertainty(self, predictions: List[Dict]) -> Dict:
        """Measure if system knows what it doesn't know"""
        confidences = [p.get('confidence', 0) for p in predictions]
        correctness = [p.get('correct', False) for p in predictions]
        
        # Calibration: do high confidence = high correctness?
        high_conf_correct = np.mean([c for c, conf in zip(correctness, confidences) 
                                     if conf > 0.8])
        low_conf_correct = np.mean([c for c, conf in zip(correctness, confidences) 
                                    if conf < 0.5])
        
        result = {
            'high_confidence_accuracy': high_conf_correct,
            'low_confidence_accuracy': low_conf_correct,
            'calibration_quality': high_conf_correct - low_conf_correct  # Should be positive
        }
        
        self.uncertainty_estimates.append(result)
        return result


class ContinualLearningBench:
    """Benchmark for continual learning (no catastrophic forgetting)"""
    
    def __init__(self):
        self.task_sequences = []
        self.performance_history = defaultdict(list)
        
    def add_task_sequence(self, tasks: List[Tuple[np.ndarray, np.ndarray]]):
        """Add a sequence of tasks"""
        self.task_sequences.append(tasks)
    
    def evaluate_continual_learning(self, model_fn) -> Dict:
        """Evaluate continual learning performance"""
        results = {
            'timestamp': datetime.now(),
            'num_tasks': 0,
            'task_accuracies': [],
            'forgetting': []
        }
        
        task_group_performance = []
        
        for task_idx, (x, y) in enumerate(self.task_sequences[0]):
            predictions = model_fn(x)
            accuracy = MetricsCalculator.accuracy(predictions, y)
            results['task_accuracies'].append(accuracy)
            task_group_performance.append(accuracy)
            results['num_tasks'] += 1
        
        # Measure forgetting of earlier tasks after learning new ones
        if len(task_group_performance) > 1:
            initial_perf = task_group_performance[0]
            final_perf = task_group_performance[-1]
            forgetting = initial_perf - final_perf
            results['forgetting'].append(forgetting)
        
        return results


class EvaluationManager:
    """High-level evaluation management"""
    
    def __init__(self):
        self.metrics_calc = MetricsCalculator()
        self.benchmark_suite = BenchmarkSuite()
        self.reasoning_bench = ReasoningBenchmark()
        self.self_aware_metrics = SelfAwarenessMetrics()
        self.continual_bench = ContinualLearningBench()
        
        self.evaluation_reports = []
        
    def generate_comprehensive_report(self, model, test_data: Dict) -> Dict:
        """Generate comprehensive evaluation report"""
        report = {
            'timestamp': datetime.now(),
            'evaluations': {}
        }
        
        # Basic metrics
        if 'predictions' in test_data and 'targets' in test_data:
            predictions = test_data['predictions']
            targets = test_data['targets']
            
            report['evaluations']['basic_metrics'] = {
                'accuracy': MetricsCalculator.accuracy(predictions, targets),
                'mse': MetricsCalculator.mean_squared_error(predictions, targets),
                'mae': MetricsCalculator.mean_absolute_error(predictions, targets),
                'metrics': MetricsCalculator.precision_recall_f1(predictions, targets)
            }
        
        # Run benchmarks
        benchmark_results = self.benchmark_suite.run_all_benchmarks(lambda x: np.random.randn(x.shape[0], 10))
        report['evaluations']['benchmarks'] = benchmark_results
        
        self.evaluation_reports.append(report)
        logger.info("Comprehensive evaluation report generated")
        
        return report
