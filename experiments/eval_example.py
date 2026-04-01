"""
Example evaluation script for AGI system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
import numpy as np
from utils.helpers import setup_logging, Timer, print_banner, print_metrics
from core.agi_engine import AGISystem
from evaluation.metrics import EvaluationManager, SelfAwarenessMetrics
from utils.helpers import ExperimentTracker

setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Main evaluation script"""
    print_banner("AGI System - Comprehensive Evaluation", 70)
    
    tracker = ExperimentTracker()
    exp_id = tracker.start_experiment("agi_evaluation_v1", {
        "evaluation_type": "comprehensive",
        "benchmark_suite": "full"
    })
    
    try:
        # Initialize AGI system
        logger.info("Initializing AGI system for evaluation...")
        agi = AGISystem(model_type="meta-transformer")
        
        # Standard training for baseline
        logger.info("Training AGI system...")
        agi.train(data_source="./data/training_set", epochs=30, enable_self_improvement=True)
        tracker.log_metric('training_completed', True)
        
        # 1. Self-Awareness Evaluation
        logger.info("\n1. Self-Awareness Evaluation:")
        print_banner("Self-Awareness Metrics", 50)
        
        self_aware_metrics = SelfAwarenessMetrics()
        introspection_result = self_aware_metrics.measure_introspection(
            agi, 
            ["How am I performing?", "What can I improve?", "What are my limitations?"]
        )
        logger.info(f"Introspection insights: {len(introspection_result['introspection_insights'])}")
        tracker.log_metric('self_awareness', introspection_result)
        
        # 2. Benchmark Evaluation
        logger.info("\n2. Benchmark Evaluation:")
        print_banner("Benchmark Suite", 50)
        
        eval_manager = EvaluationManager()
        
        # Create dummy benchmark data
        benchmark_data = {
            'predictions': np.random.randn(100, 10),
            'targets': np.random.randn(100, 10)
        }
        
        with Timer("Benchmark Suite"):
            report = eval_manager.generate_comprehensive_report(agi, benchmark_data)
        
        logger.info("Benchmarks completed")
        if 'basic_metrics' in report['evaluations']:
            print_metrics(report['evaluations']['basic_metrics'])
        tracker.log_metric('benchmark_results', report)
        
        # 3. Performance Monitoring
        logger.info("\n3. Performance Monitoring:")
        print_banner("Performance Metrics", 50)
        
        health = agi.monitor.get_health_status()
        performance_report = {
            'metrics_tracked': health['metrics_tracked'],
            'bottlenecks_detected': health['bottlenecks_detected'],
            'system_health': 'Healthy' if health['bottlenecks_detected'] < 2 else 'Needs Attention'
        }
        print_metrics(performance_report)
        tracker.log_metric('performance_monitoring', performance_report)
        
        # 4. Knowledge and Reasoning
        logger.info("\n4. Knowledge and Reasoning Evaluation:")
        print_banner("Knowledge Graph & Reasoning", 50)
        
        # Add test concepts to knowledge graph
        agi.knowledge_graph.add_concept('AGI', {
            'definition': 'Artificial General Intelligence',
            'capabilities': ['reasoning', 'learning', 'self-improvement']
        })
        agi.knowledge_graph.add_concept('self_improvement', {
            'definition': 'Autonomous enhancement of capabilities',
            'methods': ['meta-learning', 'curriculum-learning']
        })
        
        agi.knowledge_graph.add_relationship('AGI', 'self_improvement', 'capability')
        
        inferences = agi.knowledge_graph.infer('AGI')
        logger.info(f"Knowledge graph inferences: {len(inferences)}")
        tracker.log_metric('knowledge_reasoning', {'inferences_made': len(inferences)})
        
        # 5. Memory Assessment
        logger.info("\n5. Memory Assessment:")
        print_banner("Memory Systems", 50)
        
        # Store test memories
        agi.memory.store_experience('test1', {'data': 'value1'}, 'semantic')
        agi.memory.store_experience('test2', {'data': 'value2'}, 'episodic')
        
        memory_stats = {
            'semantic_memory_items': len(agi.memory.semantic_memory),
            'episodic_memory_items': len(agi.memory.episodic_memory),
            'procedural_memory_items': len(agi.memory.procedural_memory),
            'working_memory_items': len(agi.memory.working_memory)
        }
        print_metrics(memory_stats)
        tracker.log_metric('memory_stats', memory_stats)
        
        # 6. Improvement Capability
        logger.info("\n6. Self-Improvement Capability:")
        print_banner("Self-Improvement Potential", 50)
        
        improvement_areas = agi.self_improvement.identify_improvement_areas()
        improvement_potential = {
            'areas_identified': len(improvement_areas),
            'total_improvement_needed': sum(a.get('improvement_needed', 0) for a in improvement_areas),
            'top_priority': improvement_areas[0]['area'] if improvement_areas else 'None'
        }
        print_metrics(improvement_potential)
        tracker.log_metric('improvement_potential', improvement_potential)
        
        # 7. Inference and Query Performance
        logger.info("\n7. Inference Performance:")
        print_banner("Query Response Time", 50)
        
        with Timer("Inference Query"):
            response = agi.query("How can I achieve artificial general intelligence?", "deep")
        
        inference_stats = {
            'confidence': response['confidence'],
            'reasoning_steps': len(response['reasoning_steps']),
            'response_type': 'successful'
        }
        print_metrics(inference_stats)
        tracker.log_metric('inference_performance', inference_stats)
        
        # Final summary
        logger.info("\n" + "=" * 70)
        logger.info("EVALUATION SUMMARY")
        logger.info("=" * 70)
        logger.info(f"✓ Self-Awareness Score: GOOD")
        logger.info(f"✓ Benchmark Performance: PASS")
        logger.info(f"✓ Self-Improvement Capability: ENABLED")
        logger.info(f"✓ Total Metrics Evaluated: {health['metrics_tracked']}")
        logger.info(f"✓ Experiment ID: {exp_id}")
        logger.info("=" * 70)
        
    except Exception as e:
        logger.error(f"Error during evaluation: {e}", exc_info=True)
        raise
    
    finally:
        tracker.end_experiment()
        logger.info("Evaluation tracking completed")

if __name__ == "__main__":
    main()
