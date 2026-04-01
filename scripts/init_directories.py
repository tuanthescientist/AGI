"""
Initialize data directories for AGI system
"""

import os
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def initialize_directories():
    """Create necessary directories"""
    dirs = [
        "./data/raw",
        "./data/processed",
        "./data/training_set",
        "./checkpoints",
        "./logs",
        "./results",
        "./models/pretrained",
        "./experiments/results"
    ]
    
    for dir_path in dirs:
        os.makedirs(dir_path, exist_ok=True)
        logger.info(f"✓ Created directory: {dir_path}")

if __name__ == "__main__":
    initialize_directories()
    logger.info("Directory initialization completed")
