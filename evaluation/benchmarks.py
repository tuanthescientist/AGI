"""
Evaluation & Benchmarking Framework
====================================

Comprehensive evaluation system for AGI agents including:
- Task-based metrics (accuracy, latency, efficiency)
- Self-awareness metrics (meta-reasoning quality, plan correctness)
- Reasoning quality metrics (chain validity, alternative exploration)
- Multi-agent collaboration metrics
- Benchmark suite (AGI-specific + standard ML benchmarks)
"""

from dataclasses import dataclass, field
from typing import Any, Callable, Dict, List, Optional, Tuple
from enum import Enum
import json
import logging
from datetime import datetime


logger = logging.getLogger(__name__)


class MetricType(Enum):
    """Types of metrics"""
    ACCURACY = "accuracy"
    LATENCY = "latency"
    EFFICIENCY = "efficiency"
    REASONING_QUALITY = "reasoning_quality"
    SELF_AWARENESS = "self_awareness"
    COLLABORATION = "collaboration"
    CORRECTNESS = "correctness"


@dataclass
class EvaluationMetric:
    """Single computed metric"""
    name: str
    metric_type: MetricType
    value: float  # 0-1 scale typically
    timestamp: str = field(default_factory=lambda: datetime.utcnow().isoformat())
    context: Dict[str, Any] = field(default_factory=dict)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "name": self.name,
            "type": self.metric_type.value,
            "value": self.value,
            "timestamp": self.timestamp,
            "context": self.context
        }


@dataclass
class EvaluationResult:
    """Result of evaluating an agent/task"""
    task_id: str
    agent_name: str
    metrics: List[EvaluationMetric] = field(default_factory=list)
    success: bool = True
    error: Optional[str] = None
    duration_ms: float = 0.0
    
    def add_metric(self, metric: EvaluationMetric) -> None:
        """Add metric to result"""
        self.metrics.append(metric)
    
    def get_average_score(self) -> float:
        """Get average score across all metrics"""
        if not self.metrics:
            return 0.0
        return sum(m.value for m in self.metrics) / len(self.metrics)
    
    def to_dict(self) -> Dict[str, Any]:
        return {
            "task_id": self.task_id,
            "agent_name": self.agent_name,
            "success": self.success,
            "error": self.error,
            "duration_ms": self.duration_ms,
            "average_score": self.get_average_score(),
            "metrics": [m.to_dict() for m in self.metrics]
        }


class ReasoningQualityEvaluator:
    """Evaluate quality of reasoning chains"""
    
    @staticmethod
    def evaluate_chain_validity(reasoning_steps: List[str]) -> float:
        """Score: 0-1 (how logically consistent is the chain?)"""
        if not reasoning_steps:
            return 0.0
        
        # Simple heuristic: check for logical connectors
        logical_connectors = [
            "therefore", "thus", "so", "because", "hence", "since",
            "consequently", "implies", "leads to", "results in"
        ]
        
        connector_count = sum(
            1 for step in reasoning_steps 
            if any(connector in step.lower() for connector in logical_connectors)
        )
        
        return min(1.0, connector_count / max(len(reasoning_steps), 1))
    
    @staticmethod
    def evaluate_alternative_exploration(num_alternatives: int, max_alt: int = 5) -> float:
        """Score: 0-1 (did agent explore alternatives?)"""
        return min(1.0, num_alternatives / max_alt)
    
    @staticmethod
    def evaluate_reasoning_depth(reasoning_chain: List[str], min_depth: int = 3) -> float:
        """Score: 0-1 (is reasoning sufficiently deep?)"""
        return min(1.0, len(reasoning_chain) / min_depth)


class SelfAwarenessEvaluator:
    """Evaluate agent's self-awareness and meta-reasoning"""
    
    @staticmethod
    def evaluate_plan_correctness(plan: Dict[str, Any], actual_steps: int) -> float:
        """Score: 0-1 (did agent's plan match reality?)"""
        planned_steps = plan.get("steps", 0)
        if planned_steps == 0:
            return 0.0
        
        deviation = abs(actual_steps - planned_steps)
        return max(0.0, 1.0 - (deviation / planned_steps))
    
    @staticmethod
    def evaluate_uncertainty_quantification(confidence_scores: List[float]) -> float:
        """Score: 0-1 (did agent estimate confidence appropriately?)"""
        if not confidence_scores:
            return 0.0
        
        # Good if avg confidence is moderate (not overconfident, not underconfident)
        avg_confidence = sum(confidence_scores) / len(confidence_scores)
        
        # Best at 0.7 confidence (not too high, not too low)
        return 1.0 - abs(avg_confidence - 0.7)
    
    @staticmethod
    def evaluate_error_detection(errors_detected: int, total_errors: int) -> float:
        """Score: 0-1 (how many errors did agent catch?)"""
        if total_errors == 0:
            return 1.0
        
        return min(1.0, errors_detected / total_errors)


class CollaborationEvaluator:
    """Evaluate multi-agent collaboration quality"""
    
    @staticmethod
    def evaluate_communication_clarity(messages: List[str]) -> float:
        """Score: 0-1 (are agent messages clear and structured?)"""
        if not messages:
            return 0.0
        
        # Heuristic: check for structured format
        structured_count = sum(
            1 for msg in messages
            if any(marker in msg.lower() for marker in ["step:", "decision:", "action:", "result:"])
        )
        
        return structured_count / len(messages)
    
    @staticmethod
    def evaluate_consensus_quality(proposal_agreement: float) -> float:
        """Score: 0-1 (did agents reach good consensus?)"""
        # 0-0.3: very low agreement (no consensus)
        # 0.3-0.7: moderate agreement (weak consensus)
        # 0.7-1.0: high agreement (strong consensus)
        return proposal_agreement
    
    @staticmethod
    def evaluate_knowledge_transfer(knowledge_shared: int, total_agents: int) -> float:
        """Score: 0-1 (how much knowledge was transferred?)"""
        if total_agents <= 1:
            return 0.0
        
        # Maximum possible transfers: C(n,2) = n*(n-1)/2
        max_transfers = total_agents * (total_agents - 1) // 2
        return min(1.0, knowledge_shared / max(max_transfers, 1))


class Benchmark:
    """Single benchmark task"""
    
    def __init__(self, name: str, task_fn: Callable, expected_output: Optional[Any] = None):
        self.name = name
        self.task_fn = task_fn
        self.expected_output = expected_output
    
    def evaluate(self, agent_output: Any, timeout_ms: float = 5000) -> Tuple[bool, float, Dict[str, Any]]:
        """
        Evaluate agent's performance on this benchmark
        Returns: (success, score 0-1, metadata)
        """
        import time
        
        start = time.time()
        
        try:
            result = self.task_fn(agent_output)
            duration_ms = (time.time() - start) * 1000
            
            # Check correctness
            correct = (result == self.expected_output) if self.expected_output else result
            
            # Score based on correctness and latency
            latency_score = max(0.0, 1.0 - (duration_ms / timeout_ms))
            correctness_score = 1.0 if correct else 0.0
            
            final_score = 0.7 * correctness_score + 0.3 * latency_score
            
            return correct, final_score, {
                "duration_ms": duration_ms,
                "correct": correct
            }
        
        except Exception as e:
            return False, 0.0, {"error": str(e)}


class BenchmarkSuite:
    """Collection of benchmarks for comprehensive evaluation"""
    
    def __init__(self, name: str = "AGI Benchmark Suite"):
        self.name = name
        self.benchmarks: Dict[str, Benchmark] = {}
        self.results: Dict[str, List[EvaluationResult]] = {}
    
    def add_benchmark(self, benchmark: Benchmark) -> None:
        """Add benchmark to suite"""
        self.benchmarks[benchmark.name] = benchmark
    
    def add_reasoning_benchmark(self) -> None:
        """Add standard reasoning benchmarks"""
        
        # Logic puzzle
        def logic_puzzle(agent_output: Dict[str, Any]) -> bool:
            """Simple logic puzzle evaluation"""
            required_keys = ["conclusion", "reasoning_steps"]
            return all(k in agent_output for k in required_keys)
        
        self.add_benchmark(Benchmark(
            name="logic_puzzle",
            task_fn=logic_puzzle,
            expected_output=True
        ))
        
        # Mathematical reasoning
        def math_reasoning(agent_output: Dict[str, Any]) -> bool:
            """Mathematical problem solving"""
            if "answer" not in agent_output:
                return False
            try:
                # Verify answer is reasonable (e.g., numeric)
                float(agent_output["answer"])
                return True
            except:
                return False
        
        self.add_benchmark(Benchmark(
            name="math_reasoning",
            task_fn=math_reasoning,
            expected_output=True
        ))
    
    def add_planning_benchmark(self) -> None:
        """Add planning benchmarks"""
        
        def plan_generation(agent_output: Dict[str, Any]) -> bool:
            """Evaluate plan structure"""
            required = ["steps", "estimate_duration", "dependencies"]
            return all(k in agent_output for k in required)
        
        self.add_benchmark(Benchmark(
            name="plan_generation",
            task_fn=plan_generation,
            expected_output=True
        ))
    
    def add_self_awareness_benchmark(self) -> None:
        """Add self-awareness benchmarks"""
        
        def plan_accuracy(agent_output: Dict[str, Any]) -> bool:
            """Evaluate plan vs reality"""
            required = ["planned_steps", "actual_steps", "accuracy"]
            if not all(k in agent_output for k in required):
                return False
            
            accuracy = agent_output.get("accuracy", 0)
            return accuracy > 0.5  # At least 50% accuracy
        
        self.add_benchmark(Benchmark(
            name="plan_accuracy",
            task_fn=plan_accuracy,
            expected_output=True
        ))
    
    def run_benchmark(self, benchmark_name: str, agent_output: Any) -> EvaluationResult:
        """Run single benchmark"""
        if benchmark_name not in self.benchmarks:
            raise ValueError(f"Benchmark '{benchmark_name}' not found")
        
        benchmark = self.benchmarks[benchmark_name]
        success, score, metadata = benchmark.evaluate(agent_output)
        
        result = EvaluationResult(
            task_id=benchmark_name,
            agent_name="agent",
            success=success,
            duration_ms=metadata.get("duration_ms", 0.0)
        )
        
        result.add_metric(EvaluationMetric(
            name=benchmark_name,
            metric_type=MetricType.CORRECTNESS,
            value=score,
            context=metadata
        ))
        
        return result
    
    def run_all(self, agent_output: Any) -> Dict[str, EvaluationResult]:
        """Run all benchmarks, return results by name"""
        results = {}
        for benchmark_name in self.benchmarks:
            try:
                results[benchmark_name] = self.run_benchmark(benchmark_name, agent_output)
            except Exception as e:
                logger.error(f"Error running benchmark {benchmark_name}: {e}")
                results[benchmark_name] = EvaluationResult(
                    task_id=benchmark_name,
                    agent_name="agent",
                    success=False,
                    error=str(e)
                )
        
        return results
    
    def get_average_score(self, results: Dict[str, EvaluationResult]) -> float:
        """Get average score across all results"""
        if not results:
            return 0.0
        
        valid_results = [r for r in results.values() if r.success]
        if not valid_results:
            return 0.0
        
        return sum(r.get_average_score() for r in valid_results) / len(valid_results)


class Evaluator:
    """Main evaluation orchestrator"""
    
    def __init__(self, name: str = "AGIEvaluator"):
        self.name = name
        self.suite = BenchmarkSuite()
        self.reasoning_evaluator = ReasoningQualityEvaluator()
        self.self_awareness_evaluator = SelfAwarenessEvaluator()
        self.collaboration_evaluator = CollaborationEvaluator()
        self.history: List[EvaluationResult] = []
    
    def setup_default_suite(self) -> None:
        """Setup default benchmark suite"""
        self.suite.add_reasoning_benchmark()
        self.suite.add_planning_benchmark()
        self.suite.add_self_awareness_benchmark()
    
    def evaluate_reasoning_chain(self, reasoning_steps: List[str]) -> float:
        """Evaluate quality of reasoning"""
        validity = self.reasoning_evaluator.evaluate_chain_validity(reasoning_steps)
        depth = self.reasoning_evaluator.evaluate_reasoning_depth(reasoning_steps)
        
        return 0.6 * validity + 0.4 * depth
    
    def evaluate_agent_plan(self, plan: Dict[str, Any], actual_steps: int) -> float:
        """Evaluate self-awareness of agent's plan"""
        return self.self_awareness_evaluator.evaluate_plan_correctness(plan, actual_steps)
    
    def evaluate_multi_agent(self, messages: List[str], agreement: float) -> float:
        """Evaluate multi-agent collaboration"""
        clarity = self.collaboration_evaluator.evaluate_communication_clarity(messages)
        consensus = self.collaboration_evaluator.evaluate_consensus_quality(agreement)
        
        return 0.5 * clarity + 0.5 * consensus
    
    def evaluate_task(self, task_output: Any) -> EvaluationResult:
        """Full evaluation of task output"""
        result = EvaluationResult(
            task_id="eval_001",
            agent_name=self.name
        )
        
        # Run benchmark suite
        benchmark_results = self.suite.run_all(task_output)
        
        for name, bench_result in benchmark_results.items():
            for metric in bench_result.metrics:
                result.add_metric(metric)
        
        self.history.append(result)
        return result
    
    def get_summary(self) -> Dict[str, Any]:
        """Get evaluation summary"""
        if not self.history:
            return {"evaluations": 0}
        
        avg_score = sum(r.get_average_score() for r in self.history) / len(self.history)
        success_rate = sum(1 for r in self.history if r.success) / len(self.history)
        
        return {
            "total_evaluations": len(self.history),
            "average_score": avg_score,
            "success_rate": success_rate,
            "failed_evaluations": sum(1 for r in self.history if not r.success)
        }


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    
    print("Initializing Evaluation Framework...")
    
    # Create evaluator with default suite
    evaluator = Evaluator("AGITester")
    evaluator.setup_default_suite()
    
    # Example agent output
    agent_output = {
        "reasoning_steps": ["First, understand the problem", "Therefore, decompose into parts", "Hence, solve each part"],
        "conclusion": "Solution found",
        "steps": 3,
        "estimate_duration": 5.0,
        "dependencies": [],
        "planned_steps": 3,
        "actual_steps": 3,
        "accuracy": 0.95
    }
    
    # Evaluate
    result = evaluator.evaluate_task(agent_output)
    
    print(f"\nEvaluation Result:")
    print(f"  Success: {result.success}")
    print(f"  Average Score: {result.get_average_score():.2f}")
    print(f"  Metrics: {len(result.metrics)}")
    
    print(f"\nSummary:")
    print(f"  {evaluator.get_summary()}")
    
    print("\n✅ Evaluation framework ready!")
    print("   Use for: benchmarking agents, tracking improvement, quality assurance")
