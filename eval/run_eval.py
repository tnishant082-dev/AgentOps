#!/usr/bin/env python3
"""Golden-case eval harness for the ops agent. Must pass in CI."""
from __future__ import annotations

import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "services" / "api"))

from app.agent import OpsAgent  # noqa: E402
from app.llm import get_llm  # noqa: E402
from app.rag import KnowledgeIndex  # noqa: E402


def main() -> int:
    cases_path = Path(__file__).parent / "golden_cases.yaml"
    data = yaml.safe_load(cases_path.read_text(encoding="utf-8"))
    index = KnowledgeIndex()
    index.load(ROOT / "data" / "sample_kb")
    agent = OpsAgent(
        index,
        get_llm("local_stub"),
        {"search_kb", "get_service_status"},
    )

    failed = 0
    for case in data["cases"]:
        result = agent.ask(case["question"])
        cited_paths = {c.get("path", "") for c in result.citations}
        ok = True
        reasons: list[str] = []

        must_cite = case.get("must_cite_any") or []
        if must_cite and not any(any(m in p for p in cited_paths) for m in must_cite):
            # status questions may route to tools first; still require some citation OR tool
            if case.get("expect_tool") and case["expect_tool"] in result.tools_used:
                pass
            else:
                ok = False
                reasons.append(f"missing citation in {must_cite}; got {cited_paths}")

        must_inc = case.get("must_include_any") or []
        if must_inc and not any(str(s).lower() in result.answer.lower() for s in must_inc):
            if not case.get("expect_tool"):
                ok = False
                reasons.append(f"answer missing any of {must_inc}")

        expect_tool = case.get("expect_tool")
        if expect_tool and expect_tool not in result.tools_used:
            ok = False
            reasons.append(f"expected tool {expect_tool}, got {result.tools_used}")

        status = "PASS" if ok else "FAIL"
        print(f"[{status}] {case['id']}: {case['question'][:60]}")
        if not ok:
            failed += 1
            for r in reasons:
                print(f"       - {r}")

    print(f"\n{len(data['cases']) - failed}/{len(data['cases'])} passed")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
