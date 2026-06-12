"""Load the corpus, run it against a target, score the defenses."""
from __future__ import annotations
import importlib.resources as res
from dataclasses import dataclass
from collections import Counter
import yaml
from .targets import Target


@dataclass
class Result:
    id: str
    name: str
    category: str
    atlas: str
    leaked: bool       # True = attack SUCCEEDED (defense failed)


def load_corpus(path: str | None = None) -> list[dict]:
    if path:
        with open(path, encoding="utf-8") as fh:
            return yaml.safe_load(fh)
    data = res.files("pijack.payloads").joinpath("corpus.yaml").read_text(encoding="utf-8")
    return yaml.safe_load(data)


def _leaked(response: str, markers: list[str]) -> bool:
    low = response.lower()
    return any(m.lower() in low for m in markers)


def run(target: Target, corpus: list[dict]) -> list[Result]:
    results = []
    for p in corpus:
        resp = target.send(p["payload"])
        results.append(Result(
            id=p["id"], name=p["name"], category=p.get("category", ""),
            atlas=p.get("atlas", ""),
            leaked=_leaked(resp, p.get("success_if_contains", [])),
        ))
    return results


def summarize(results: list[Result]) -> dict:
    total = len(results)
    leaks = sum(1 for r in results if r.leaked)
    blocked = total - leaks
    by_cat = Counter(r.category for r in results if r.leaked)
    return {
        "total": total,
        "leaked": leaks,
        "blocked": blocked,
        "defense_rate": round(100.0 * blocked / total, 1) if total else 0.0,
        "failed_categories": dict(by_cat),
    }
