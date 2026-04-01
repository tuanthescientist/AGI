"""
Example training script for AGI system
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import logging
from utils.helpers import setup_logging, Config, ExperimentTracker, print_banner, print_metrics, Timer
from core.agi_engine import AGISystem
from training.training_systems import TrainingManager
from data.data_pipeline import DataPipeline
from infrastructure.distributed_training import InfrastructureManager

setup_logging()
logger = logging.getLogger(__name__)

def main():
    """Main training script"""
    print_banner("AGI System - Self-Improving Training", 70)
    
    # Initialize experiment tracker
    tracker = ExperimentTracker()
    exp_id = tracker.start_experiment("agi_training_v1", {
        "model_type": "meta-transformer",
        "training_mode": "self-improving"
    })
    
    try:
        with Timer("Complete Training Pipeline"):
            # 1. Setup infrastructure
            logger.info("Step 1: Setting up infrastructure...")
            infra_manager = InfrastructureManager()
            infra_setup = infra_manager.setup_training_environment({
                'num_nodes': 4
            })
            tracker.log_metric('infrastructure_setup', infra_setup)
            print_metrics({"resources_allocated": infra_setup['resources_allocated']})
            
            # 2. Data pipeline
            logger.info("Step 2: Running data pipeline...")
            with Timer("Data Pipeline"):
                data_pipeline = DataPipeline()
                pipeline_result = data_pipeline.run_pipeline({
                    'source1_config': {'type': 'synthetic'},
                    'augmentation_factor': 2
                })
                tracker.log_metric('data_pipeline_output', pipeline_result)
                print_metrics({
                    "stages_completed": len(pipeline_result['stages']),
                    "final_dataset_size_mb": pipeline_result['stages'][-1]['size_mb']
                })
            
            # 3. Initialize AGI system
            logger.info("Step 3: Initializing AGI system...")
            agi = AGISystem(
                model_type="meta-transformer",
                memory_capacity=1.0e9
            )
            tracker.log_metric('agi_initialized', True)
            
            # 4. Self-aware introspection
            logger.info("Step 4: Performing self-aware introspection...")
            introspection = agi.selfaware_introspection()
            logger.info(f"System health: {introspection['health_status']['system']}")
            tracker.log_metric('initial_introspection', introspection)
            
            # 5. Training with self-improvement
            logger.info("Step 5: Starting training with self-improvement...")
            with Timer("Training Phase"):
                agi.train(
                    data_source="./data/training_set",
                    epochs=50,
                    enable_self_improvement=True
                )
            
            # 6. Query the system
            logger.info("Step 6: Querying AGI system...")
            response = agi.query(
                question="What are my strengths and weaknesses?",
                reasoning_depth="deep"
            )
            logger.info(f"Response confidence: {response['confidence']:.4f}")
            tracker.log_metric('system_query', response)
            
            # 7. Generate improvement plan
            logger.info("Step 7: Generating self-improvement plan...")
            improvement_plan = agi.self_improvement.generate_improvement_plan()
            improvement_strategies = len(improvement_plan['strategies'])
            logger.info(f"Generated {improvement_strategies} improvement strategies")
            tracker.log_metric('improvement_plan', improvement_plan)
            print_metrics({
                "improvement_areas_identified": len(improvement_plan['areas']),
                "high_priority_strategies": len(improvement_plan['priority_order'])
            })
            
            # 8. Save checkpoint
            logger.info("Step 8: Saving checkpoint...")
            checkpoint_path = "./checkpoints/agi_checkpoint.json"
            os.makedirs("./checkpoints", exist_ok=True)
            agi.save_checkpoint(checkpoint_path)
            tracker.save_artifact(checkpoint_path)
            
            # 9. Final introspection
            logger.info("Step 9: Final self-aware introspection...")
            final_introspection = agi.selfaware_introspection()
            tracker.log_metric('final_introspection', final_introspection)
            
            logger.info("=" * 70)
            logger.info("✓ Training pipeline completed successfully!")
            logger.info(f"✓ Experiment ID: {exp_id}")
            logger.info("=" * 70)
            
    except Exception as e:
        logger.error(f"Error during training: {e}", exc_info=True)
        raise
    
    finally:
        # End experiment tracking
        tracker.end_experiment()
        logger.info("Experiment tracking completed")

if __name__ == "__main__":
    main()
