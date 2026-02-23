"""
Tests for the retrieval module.
"""

import pytest
from reactops.retrieval.bm25 import BM25Retriever

@pytest.fixture
def retriever_with_temp_data(tmp_path):
    """
    Create a temporary runbook directory with a single test runbook.
    This fixture is automatically used by pytest.
    """
    runbook_dir = tmp_path / "runbooks"
    runbook_dir.mkdir()
    test_file = runbook_dir / "test.md"
    test_file.write_text("""---
title: Test Runbook
last_reviewed: 2024-01-01
---
This is a test document about database failures.
""")
    return BM25Retriever(str(runbook_dir))

def test_search_returns_expected(retriever_with_temp_data):
    retriever = retriever_with_temp_data
    results = retriever.search("database", k=1)
    assert len(results) == 1
    meta, text, score = results[0]
    assert meta.get("title") == "Test Runbook"
    assert "database" in text
    assert isinstance(score, float)

def test_search_empty_query(retriever_with_temp_data):
    """Test that an empty query returns results (BM25 will return all documents with zero scores)."""
    retriever = retriever_with_temp_data
    results = retriever.search("", k=1)
    # We just check that it doesn't crash and returns a list
    assert isinstance(results, list)
    # With empty query, BM25 returns all documents with score 0, so we should get at least one
    assert len(results) > 0