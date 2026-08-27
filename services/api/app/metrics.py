from __future__ import annotations

import threading
from collections import defaultdict


class Metrics:
    """Minimal Prometheus text exposition — no extra deps."""

    def __init__(self) -> None:
        self._lock = threading.Lock()
        self.counters: dict[str, float] = defaultdict(float)
        self.gauges: dict[str, float] = defaultdict(float)

    def inc(self, name: str, value: float = 1.0, **labels: str) -> None:
        key = _key(name, labels)
        with self._lock:
            self.counters[key] += value

    def set(self, name: str, value: float, **labels: str) -> None:
        key = _key(name, labels)
        with self._lock:
            self.gauges[key] = value

    def render(self) -> str:
        lines: list[str] = [
            "# HELP agentops_requests_total Total ask requests",
            "# TYPE agentops_requests_total counter",
        ]
        with self._lock:
            for k, v in sorted(self.counters.items()):
                lines.append(f"{k} {v}")
            lines.append("# TYPE agentops_index_chunks gauge")
            for k, v in sorted(self.gauges.items()):
                lines.append(f"{k} {v}")
        return "\n".join(lines) + "\n"


def _key(name: str, labels: dict[str, str]) -> str:
    if not labels:
        return name
    inner = ",".join(f'{k}="{v}"' for k, v in sorted(labels.items()))
    return f"{name}{{{inner}}}"


metrics = Metrics()
