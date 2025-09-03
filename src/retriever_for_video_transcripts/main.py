import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
formatter = logging.Formatter(
    "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)


def run():
    """Run _summary_."""
    logger.info("Welcome to this retrieval-augmented generation (RAG) example!")
    logger.info("Please see the notebooks for more details.")