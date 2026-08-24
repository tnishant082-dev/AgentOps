from __future__ import annotations

import re
from dataclasses import dataclass
from pathlib import Path

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity


@dataclass
class Chunk:
    doc_id: str
    title: str
    text: str
    path: str


@dataclass
class Hit:
    chunk: Chunk
    score: float


class KnowledgeIndex:
    """Local TF-IDF index over markdown runbooks. No remote vector DB required."""

    def __init__(self) -> None:
        self.chunks: list[Chunk] = []
        self._vectorizer: TfidfVectorizer | None = None
        self._matrix = None
        self.ready = False

    def load(self, kb_path: Path) -> int:
        kb_path = Path(kb_path)
        if not kb_path.exists():
            raise FileNotFoundError(f"KB path not found: {kb_path}")

        chunks: list[Chunk] = []
        for path in sorted(kb_path.rglob("*.md")):
            raw = path.read_text(encoding="utf-8")
            title = _first_heading(raw) or path.stem.replace("_", " ").title()
            for i, part in enumerate(_split_sections(raw)):
                text = part.strip()
                if len(text) < 40:
                    continue
                chunks.append(
                    Chunk(
                        doc_id=f"{path.stem}#{i}",
                        title=title,
                        text=text,
                        path=str(path.relative_to(kb_path)),
                    )
                )

        if not chunks:
            raise RuntimeError(f"No markdown chunks under {kb_path}")

        vectorizer = TfidfVectorizer(
            stop_words="english",
            ngram_range=(1, 2),
            max_features=8000,
        )
        matrix = vectorizer.fit_transform(c.text for c in chunks)
        self.chunks = chunks
        self._vectorizer = vectorizer
        self._matrix = matrix
        self.ready = True
        return len(chunks)

    def search(self, query: str, top_k: int = 3) -> list[Hit]:
        if not self.ready or self._vectorizer is None or self._matrix is None:
            raise RuntimeError("index not loaded")
        q = self._vectorizer.transform([query])
        scores = cosine_similarity(q, self._matrix)[0]
        ranked = sorted(enumerate(scores), key=lambda x: x[1], reverse=True)
        hits: list[Hit] = []
        for idx, score in ranked[:top_k]:
            if score <= 0:
                continue
            hits.append(Hit(chunk=self.chunks[idx], score=float(score)))
        return hits


def _first_heading(md: str) -> str | None:
    for line in md.splitlines():
        if line.startswith("# "):
            return line[2:].strip()
    return None


def _split_sections(md: str) -> list[str]:
    parts = re.split(r"(?=^## )", md, flags=re.MULTILINE)
    return [p for p in parts if p.strip()]
