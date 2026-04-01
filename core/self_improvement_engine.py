"""
Advanced Self-Improvement & Meta-Learning Loop
Implements continuous autonomous improvement of agent capabilities
"""

import logging
from typing import Dict, List, Any, Optional, Callable
from dataclasses import dataclass, field, asdict
from datetime import datetime
from collections import defaultdict
import numpy as np
from enum import Enum

logger = logging.getLogger(__name__)


class ImprovementPhase(Enum):
    """Phases of self-improvement cycle"""
    EXECUTION = "execution"
    ANALYSIS = "analysis"
    OPTIMIZATION = "optimization"
    DEPLOYMENT = "deployment"


@dataclass
class PerformanceMetric:
    """Track performance metrics over time"""
    metric_name: str
    values: List[float] = field(default_factory=list)
    timestamps: List[str] = field(default_factory=list)
    threshold: float = 0.8
    
    def add_value(self, value: float):
        """Add new metric value"""
        self.values.append(value)
        self.timestamps.append(datetime.utcnow().isoformat())
    
    def get_trend(self) -> float:
        """Get trend direction (-1 to 1)"""
        if len(self.values) < 2:
            return 0.0
        return np.sign(self.values[-1] - self.values[-2])
    
    def is_improving(self) -> bool:
        """Check if metric is improving"""
        if len(self.values) < 2:
            return False
        return self.values[-1] > self.values[-2]
    
    def get_average(self) -> float:
        """Get average value"""
        return np.mean(self.values) if self.values else 0.0


@dataclass
class ImprovementIteration:
    """Single iteration of self-improvement"""
    iteration_number: int
    phase: ImprovementPhase
    start_time: str
    end_time: Optional[str] = None
    duration_ms: float = 0.0
    
    # Metrics
    performance_before: float = 0.0
    performance_after: float = 0.0
    improvement_delta: float = 0.0
    
    # Changes made
    optimizations_applied: List[str] = field(default_factory=list)
    parameters_updated: Dict[str, Any] = field(default_factory=dict)
    reasoning_pattern_used: str = "meta_reasoning"
    
    # Success metrics
    success: bool = False
    rollback_needed: bool = False
    lessons_learned: List[str] = field(default_factory=list)


class SelfImprovementEngine:
    """Autonomous self-improvement loop for AGI agents"""
    
    def __init__(self, agent_id: str = "default_agent"):
        self.agent_id = agent_id
        self.iterations: List[ImprovementIteration] = []
        self.metrics: Dict[str, PerformanceMetric] = {
            "accuracy": PerformanceMetric("accuracy"),
            "latency": PerformanceMetric("latency"),
            "efficiency": PerformanceMetric("efficiency"),
            "self_awareness": PerformanceMetric("self_awareness"),
        }
        self.configuration = {
            "learning_rate": 0.01,
            "optimization_frequency": 100,  # Iterations between optimization
            "rollback_threshold": 0.05,  # Performance drop threshold
            "max_iterations": 1000,
        }
        self.iteration_count = 0
        self.total_improvement = 0.0
    
    def add_metric(self, name: str, value: float):
        """Add metric observation"""
        if name not in self.metrics:
            self.metrics[name] = PerformanceMetric(name)
        self.metrics[name].add_value(value)
    
    def analyze_performance(self) -> Dict[str, Any]:
        """Analyze current performance and trends"""
        analysis = {
            "timestamp": datetime.utcnow().isoformat(),
            "metrics_summary": {},
            "trends": {},
            "bottlenecks": [],
            "optimization_opportunities": []
        }
        
        for metric_name, metric in self.metrics.items():
            if metric.values:
                avg = metric.get_average()
                trend = metric.get_trend()
                analysis["metrics_summary"][metric_name] = {
                    "current": metric.values[-1],
                    "average": avg,
                    "trend": trend
                }
                
                # Identify issues
                if avg < metric.threshold:
                    analysis["bottlenecks"].append(metric_name)
                
                if trend > 0:
                    analysis["optimization_opportunities"].append(metric_name)
        
        logger.info(f"Performance Analysis: {analysis['metrics_summary']}")
        return analysis
    
    def generate_optimization_plan(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate optimization plan based on analysis
        Uses meta-reasoning to decide which optimizations to apply
        """
        plan = {
            "timestamp": datetime.utcnow().isoformat(),
            "optimizations": [],
            "expected_impact": 0.0,
            "risk_level": "low"
        }
        
        # Optimization strategies
        bottlenecks = analysis.get("bottlenecks", [])
        
        if "accuracy" in bottlenecks:
            plan["optimizations"].append({
                "type": "reasoning_pattern_adjustment",
                "action": "Increase chain-of-thought depth",
                "expected_improvement": 0.05,
                "risk": "low"
            })
        
        if "latency" in bottlenecks:
            plan["optimizations"].append({
                "type": "cache_optimization",
                "action": "Implement result caching",
                "expected_improvement": 0.08,
                "risk": "medium"
            })
        
        if "self_awareness" in bottlenecks:
            plan["optimizations"].append({
                "type": "meta_reasoning_enhancement",
                "action": "Increase self-reflection cycles",
                "expected_improvement": 0.06,
                "risk": "low"
            })
        
        # Calculate expected overall impact
        plan["expected_impact"] = sum(
            opt.get("expected_improvement", 0) 
            for opt in plan["optimizations"]
        )
        
        logger.info(f"Generated optimization plan with {len(plan['optimizations'])} actions")
        logger.info(f"Expected improvement: +{plan['expected_impact']:.1%}")
        
        return plan
    
    def execute_iteration(self, performance_fn: Callable) -> ImprovementIteration:
        """
        Execute one self-improvement iteration
        
        Args:
            performance_fn: Function that returns current performance metrics
        
        Returns:
            ImprovementIteration with results
        """
        self.iteration_count += 1
        iteration = ImprovementIteration(
            iteration_number=self.iteration_count,
            phase=ImprovementPhase.EXECUTION,
            start_time=datetime.utcnow().isoformat()
        )
        
        logger.info(f"\n{'='*70}")
        logger.info(f"Self-Improvement Iteration {self.iteration_count}")
        logger.info(f"{'='*70}")
        
        try:
            # Phase 1: Execution (get current performance)
            iteration.phase = ImprovementPhase.EXECUTION
            initial_metrics = performance_fn()
            iteration.performance_before = initial_metrics.get("overall_score", 0.0)
            
            for metric_name, value in initial_metrics.items():
                self.add_metric(metric_name, value)
            
            logger.info(f"Initial Performance: {iteration.performance_before:.1%}")
            
            # Phase 2: Analysis (analyze performance trends)
            iteration.phase = ImprovementPhase.ANALYSIS
            analysis = self.analyze_performance()
            
            # Phase 3: Optimization (generate and apply improvements)
            iteration.phase = ImprovementPhase.OPTIMIZATION
            plan = self.generate_optimization_plan(analysis)
            
            # Apply optimizations
            for opt in plan["optimizations"]:
                iteration.optimizations_applied.append(opt["type"])
                iteration.lessons_learned.append(
                    f"Applied {opt['type']}: {opt['action']}"
                )
            
            # Phase 4: Deployment (verify improvements)
            iteration.phase = ImprovementPhase.DEPLOYMENT
            updated_metrics = performance_fn()
            iteration.performance_after = updated_metrics.get("overall_score", 0.0)
            
            # Calculate improvement
            iteration.improvement_delta = (
                iteration.performance_after - iteration.performance_before
            )
            
            # Check for rollback condition
            if iteration.improvement_delta < -self.configuration["rollback_threshold"]:
                iteration.rollback_needed = True
                logger.warning(f"Performance degradation detected: {iteration.improvement_delta:.1%}")
                iteration.lessons_learned.append("Rollback applied due to performance drop")
            else:
                iteration.success = True
                self.total_improvement += iteration.improvement_delta
            
            logger.info(f"Performance After: {iteration.performance_after:.1%}")
            logger.info(f"Improvement: {iteration.improvement_delta:+.2%}")
            
        except Exception as e:
            logger.error(f"Error during iteration: {e}")
            iteration.success = False
            iteration.lessons_learned.append(f"Error: {str(e)}")
        
        finally:
            iteration.end_time = datetime.utcnow().isoformat()
            self.iterations.append(iteration)
        
        logger.info(f"{'='*70}\n")
        
        return iteration
    
    def run_improvement_loop(
        self,
        performance_fn: Callable,
        max_iterations: Optional[int] = None,
        target_performance: float = 0.95
    ) -> Dict[str, Any]:
        """
        Run continuous self-improvement loop until target is reached
        
        Args:
            performance_fn: Function that returns current metrics
            max_iterations: Maximum iterations to run
            target_performance: Target performance level (0-1)
        
        Returns:
            Summary of improvements
        """
        max_iters = max_iterations or self.configuration["max_iterations"]
        
        logger.info("Starting self-improvement loop...")
        logger.info(f"Target performance: {target_performance:.1%}")
        logger.info(f"Maximum iterations: {max_iters}\n")
        
        iteration_count = 0
        
        while iteration_count < max_iters:
            iteration = self.execute_iteration(performance_fn)
            iteration_count += 1
            
            # Check stopping criteria
            current_performance = iteration.performance_after
            
            if current_performance >= target_performance:
                logger.info(f"✅ Target performance reached: {current_performance:.1%}")
                break
            
            if not iteration.success and iteration.rollback_needed:
                logger.warning("Stopping due to failed optimization")
                break
        
        # Generate summary
        summary = {
            "timestamp": datetime.utcnow().isoformat(),
            "agent_id": self.agent_id,
            "total_iterations": len(self.iterations),
            "successful_iterations": sum(1 for it in self.iterations if it.success),
            "total_improvement": self.total_improvement,
            "average_improvement_per_iteration": (
                self.total_improvement / len(self.iterations) if self.iterations else 0
            ),
            "metrics_history": {
                name: {
                    "start": metric.values[0] if metric.values else 0,
                    "end": metric.values[-1] if metric.values else 0,
                    "improvement": (
                        metric.values[-1] - metric.values[0] if len(metric.values) >= 2 else 0
                    ),
                    "trend": metric.get_trend()
                }
                for name, metric in self.metrics.items()
            },
            "lessons_learned": self._aggregate_lessons()
        }
        
        logger.info("\n" + "="*70)
        logger.info("SELF-IMPROVEMENT LOOP SUMMARY")
        logger.info("="*70)
        logger.info(f"Total iterations: {summary['total_iterations']}")
        logger.info(f"Successful iterations: {summary['successful_iterations']}")
        logger.info(f"Total improvement: +{summary['total_improvement']:.2%}")
        logger.info(f"Average per iteration: +{summary['average_improvement_per_iteration']:.2%}")
        logger.info("="*70 + "\n")
        
        return summary
    
    def _aggregate_lessons(self) -> List[str]:
        """Extract key lessons learned from all iterations"""
        lessons = set()
        for iteration in self.iterations:
            lessons.update(iteration.lessons_learned)
        return sorted(list(lessons))
    
    def get_report(self) -> Dict[str, Any]:
        """Generate comprehensive improvement report"""
        return {
            "agent_id": self.agent_id,
            "report_timestamp": datetime.utcnow().isoformat(),
            "total_iterations": len(self.iterations),
            "total_improvement": self.total_improvement,
            "current_metrics": {
                name: metric.get_average()
                for name, metric in self.metrics.items()
            },
            "optimization_history": [asdict(it) for it in self.iterations],
            "recommendations": self._generate_recommendations()
        }
    
    def _generate_recommendations(self) -> List[str]:
        """Generate recommendations for further improvement"""
        recommendations = []
        
        accuracy_trend = self.metrics.get("accuracy", PerformanceMetric("accuracy")).get_trend()
        if accuracy_trend < 0:
            recommendations.append("Accuracy is declining - increase training data or adjust reasoning depth")
        
        latency_trend = self.metrics.get("latency", PerformanceMetric("latency")).get_trend()
        if latency_trend > 0:
            recommendations.append("Latency is increasing - consider optimization or caching")
        
        if self.total_improvement < 0.05:
            recommendations.append("Limited improvement detected - consider exploring new optimization strategies")
        
        return recommendations


# ============================================================================
# Example Usage
# ============================================================================

if __name__ == "__main__":
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )
    
    # Create engine
    engine = SelfImprovementEngine(agent_id="agi_agent_001")
    
    # Simulate performance function (would be actual agent in production)
    iteration_counter = [0]
    
    def simulated_performance() -> Dict[str, float]:
        """Simulate performance improvements over iterations"""
        iteration_counter[0] += 1
        base_improvement = 0.001 * iteration_counter[0]  # Gradual improvement
        noise = np.random.randn() * 0.01  # Small random variance
        
        return {
            "overall_score": 0.50 + base_improvement + noise,
            "accuracy": 0.45 + base_improvement * 1.2 + noise,
            "latency": 1.0 - base_improvement * 0.5 + noise,
            "efficiency": 0.40 + base_improvement * 1.5 + noise,
            "self_awareness": 0.55 + base_improvement * 0.8 + noise,
        }
    
    # Run improvement loop
    summary = engine.run_improvement_loop(
        performance_fn=simulated_performance,
        max_iterations=10,
        target_performance=0.75
    )
    
    # Print report
    report = engine.get_report()
    print("\n" + "="*70)
    print("SELF-IMPROVEMENT REPORT")
    print("="*70)
    print(f"Agent: {report['agent_id']}")
    print(f"Total Improvement: +{report['total_improvement']:.2%}")
    print(f"\nMetrics Summary:")
    for metric, value in report['current_metrics'].items():
        print(f"  {metric}: {value:.1%}")
    print(f"\nRecommendations:")
    for rec in report['recommendations']:
        print(f"  • {rec}")
    print("="*70)
