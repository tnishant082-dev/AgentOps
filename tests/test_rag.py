from pathlib import Path

from app.rag import KnowledgeIndex

ROOT = Path(__file__).resolve().parents[1]


def test_index_loads_sample_kb():
    idx = KnowledgeIndex()
    n = idx.load(ROOT / "data" / "sample_kb")
    assert n >= 5
    assert idx.ready


def test_search_rollback():
    idx = KnowledgeIndex()
    idx.load(ROOT / "data" / "sample_kb")
    hits = idx.search("roll back a bad deploy")
    assert hits
    assert any("deploy" in h.chunk.path or "faq" in h.chunk.path for h in hits)
