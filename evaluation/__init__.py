"""Evaluation and benchmarking modules"""

# New comprehensive evaluation framework
from benchmarks import (
    Evaluator,
    BenchmarkSuite,
    Benchmark,
    EvaluationResult,
    EvaluationMetric,
    ReasoningQualityEvaluator,
    SelfAwarenessEvaluator,
    CollaborationEvaluator,
    MetricType
)

# Legacy metrics modules (if available)
try:
    from metrics import (
        MetricsCalculator,
        ReasoningBenchmark,
        SelfAwarenessMetrics,
        ContinualLearningBench,
        EvaluationManager
    )
except ImportError:
    pass

__all__ = [
    "MetricsCalculator",
    "BenchmarkSuite",
    "ReasoningBenchmark",
    "SelfAwarenessMetrics",
    "ContinualLearningBench",
    "EvaluationManager"
]
