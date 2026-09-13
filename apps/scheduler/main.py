"""
APScheduler-based runner for fixed-window airfare collection (09:00 & 18:00 IST)
and periodic index recomputation.
"""
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("apix-scheduler")


def run_collection_job():
    logger.info("Executing scheduled airfare collection job...")


def run_index_computation():
    logger.info("Executing index recomputation job...")


if __name__ == "__main__":
    logger.info("Starting APIx Scheduler service...")

