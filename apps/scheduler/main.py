"""
Automated runner for periodic airfare collection and index recomputation.

Usage:
  python -m apps.scheduler.main
"""
import logging
import os
import sys
import time
from pathlib import Path

# Ensure project root is in sys.path
project_root = Path(__file__).resolve().parent.parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from packages.pipeline.runner import run_collection_cycle

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(name)s: %(message)s",
)
logger = logging.getLogger("apix-scheduler")

INTERVAL_SECONDS = int(os.getenv("COLLECTION_INTERVAL_SECONDS", "3600"))  # Default: 1 hour


def main():
    logger.info("Starting APIx Scheduler service (Interval: %d seconds)...", INTERVAL_SECONDS)
    while True:
        try:
            logger.info("Triggering scheduled collection cycle...")
            run_collection_cycle(max_routes=4)
        except Exception as e:
            logger.error("Error during scheduled cycle: %s", e)

        logger.info("Cycle completed. Next update in %d seconds (1 hour)...", INTERVAL_SECONDS)
        time.sleep(INTERVAL_SECONDS)


if __name__ == "__main__":
    main()
