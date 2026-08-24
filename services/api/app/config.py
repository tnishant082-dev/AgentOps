from __future__ import annotations

import os
from pathlib import Path


def _repo_root() -> Path:
    # services/api/app/config.py -> repo root
    return Path(__file__).resolve().parents[3]


class Settings:
    env: str = os.getenv("AGENTOPS_ENV", "dev")
    kb_path: Path = Path(
        os.getenv("AGENTOPS_KB_PATH", str(_repo_root() / "data" / "sample_kb"))
    )
    rate_limit_per_min: int = int(os.getenv("AGENTOPS_RATE_LIMIT_PER_MIN", "60"))
    llm_backend: str = os.getenv("AGENTOPS_LLM_BACKEND", "local_stub")
    tools_enabled: str = os.getenv("AGENTOPS_TOOLS_ENABLED", "search_kb,get_service_status")
    host: str = os.getenv("AGENTOPS_HOST", "0.0.0.0")
    port: int = int(os.getenv("AGENTOPS_PORT", "8080"))

    @property
    def enabled_tools(self) -> set[str]:
        return {t.strip() for t in self.tools_enabled.split(",") if t.strip()}


settings = Settings()
