"""
BM25-based retriever for runbook documents.
"""

import glob
from pathlib import Path
from typing import List, Tuple, Dict, Any

from rank_bm25 import BM25Okapi

class BM25Retriever:
    """
    A BM25-based retriever for runbook documents.
    
    Each document's text is tokenized (split by whitespace) for BM25 indexing.
    The class also parses YAML frontmatter from Markdown files to extract metadata.
    """

    def __init__(self, runbook_path: str):
        """
        Initialize the retriever by loading and indexing all runbooks in the given directory.
        
        Args:
            runbook_path: Path to directory containing .md runbook files.
        """
        self.runbook_path = Path(runbook_path)
        self.documents: List[str] = []          # full text of each runbook
        self.metadata: List[Dict[str, Any]] = [] # associated metadata (title, last_reviewed, etc.)
        self.bm25: BM25Okapi = None              # will be built in _load_and_index
        self._load_and_index()

    def _load_and_index(self):
        """Load all markdown files, extract metadata and text, and build BM25 index."""
        # Find all .md files in the runbook directory
        files = glob.glob(str(self.runbook_path / "*.md"))
        if not files:
            raise ValueError(f"No markdown files found in {self.runbook_path}")

        texts = []  # list of document texts for indexing

        for file in files:
            with open(file, 'r', encoding='utf-8') as f:
                content = f.read()

            # Parse frontmatter (metadata between --- lines)
            metadata = self._parse_frontmatter(content)
            # Remove frontmatter to get the clean text content
            clean_text = self._strip_frontmatter(content)

            texts.append(clean_text)
            self.metadata.append(metadata)
            self.documents.append(clean_text)

        # Tokenize each document by splitting on whitespace
        tokenized_corpus = [doc.split() for doc in texts]
        # Build BM25 index
        self.bm25 = BM25Okapi(tokenized_corpus)
        print(f"Indexed {len(files)} runbooks.")

    def _parse_frontmatter(self, content: str) -> Dict[str, Any]:
        """
        Extract YAML frontmatter between --- markers.
        This is a simple parser; for production, you might use a YAML library.
        """
        metadata = {}
        if content.startswith('---'):
            # Split on the first and second '---'
            parts = content.split('---', 2)
            if len(parts) >= 3:
                frontmatter = parts[1]
                for line in frontmatter.strip().split('\n'):
                    if ':' in line:
                        key, val = line.split(':', 1)
                        metadata[key.strip()] = val.strip()
        return metadata

    def _strip_frontmatter(self, content: str) -> str:
        """Remove YAML frontmatter, return only the content."""
        if content.startswith('---'):
            parts = content.split('---', 2)
            if len(parts) >= 3:
                return parts[2].strip()
        return content

    def search(self, query: str, k: int = 5) -> List[Tuple[Dict[str, Any], str, float]]:
        """
        Search for top-k runbooks matching the query.
        
        Args:
            query: The search query string.
            k: Number of results to return.
        
        Returns:
            List of tuples (metadata, text, BM25 score).
        """
        if not self.bm25:
            raise RuntimeError("BM25 index not built. Call _load_and_index first.")

        # Tokenize query
        tokenized_query = query.split()
        # Get BM25 scores for all documents
        scores = self.bm25.get_scores(tokenized_query)

        # Get indices of top k scores
        top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]

        results = []
        for idx in top_indices:
            results.append((self.metadata[idx], self.documents[idx], scores[idx]))
        return results