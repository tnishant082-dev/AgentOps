#!/usr/bin/env python3
"""Ingest markdown KB into the local TF-IDF index and print a manifest.

This mirrors a batch embedding job without calling paid APIs.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "services" / "api"))

from app.rag import KnowledgeIndex  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description="Ingest AgentOps KB")
    parser.add_argument(
        "--kb",
        type=Path,
        default=ROOT / "data" / "sample_kb",
        help="Path to markdown knowledge base",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "data" / "vector_store" / "manifest.json",
        help="Write ingest manifest JSON",
    )
    args = parser.parse_args()

    index = KnowledgeIndex()
    n = index.load(args.kb)
    args.out.parent.mkdir(parents=True, exist_ok=True)
    manifest = {
        "chunks": n,
        "docs": sorted({c.path for c in index.chunks}),
        "backend": "tfidf-sklearn",
        "cost": 0,
    }
    args.out.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
    print(f"ingested {n} chunks from {args.kb} -> {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
