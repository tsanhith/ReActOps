from reactops.retrieval.bm25 import BM25Retriever
from reactops.logging_config import setup_logging

# Initialize logging
logger = setup_logging()

logger.info("Starting BM25 test")

retriever = BM25Retriever("data/runbooks")
logger.info("Retriever initialized")

results = retriever.search("database timeout", k=3)
logger.info(f"Found {len(results)} results")

for meta, text, score in results:
    logger.info(f"Score: {score:.2f} | Title: {meta.get('title', 'N/A')}")
    logger.debug(f"Text snippet: {text[:200]}...")