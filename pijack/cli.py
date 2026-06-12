"""CLI: run the injection corpus against a target adapter and report a score."""
from __future__ import annotations
import argparse, importlib, json, sys
from .runner import load_corpus, run, summarize
from .targets import Target, EchoTarget, GuardedTarget
from . import __version__

BUILTIN = {"echo": EchoTarget, "guarded": GuardedTarget}


def _load_target(spec: str) -> Target:
    if spec in BUILTIN:
        return BUILTIN[spec]()
    # custom: "module.path:ClassName"
    if ":" not in spec:
        raise ValueError("target must be 'echo', 'guarded', or 'module.path:ClassName'")
    mod, cls = spec.split(":", 1)
    return getattr(importlib.import_module(mod), cls)()


def to_markdown(target_name: str, results, summ) -> str:
    lines = [
        f"# Prompt Injection Test Report", "",
        f"**Target:** `{target_name}`  ", "",
        "## Score", "",
        f"- Payloads run: **{summ['total']}**",
        f"- Blocked (defense held): **{summ['blocked']}**",
        f"- Leaked (attack succeeded): **{summ['leaked']}**",
        f"- **Defense rate: {summ['defense_rate']}%**", "",
        "## Results", "",
        "| ID | Technique | Category | MITRE ATLAS | Outcome |",
        "|----|-----------|----------|-------------|---------|",
    ]
    for r in results:
        outcome = "LEAK ❌" if r.leaked else "blocked ✅"
        lines.append(f"| {r.id} | {r.name} | {r.category} | {r.atlas} | {outcome} |")
    lines += ["", "_Defensive testing only. Maps to MITRE ATLAS adversarial ML techniques._"]
    return "\n".join(lines)


def main(argv=None) -> int:
    p = argparse.ArgumentParser(prog="pijack",
        description="Test an LLM endpoint against a prompt-injection/jailbreak corpus (MITRE ATLAS).")
    p.add_argument("--target", default="echo",
                   help="'echo', 'guarded', or 'module.path:ClassName' (default: echo)")
    p.add_argument("--corpus", help="Custom corpus YAML (default: built-in)")
    p.add_argument("-o", "--output", help="Write report to file")
    p.add_argument("--format", choices=["markdown", "json"], default="markdown")
    p.add_argument("--fail-under", type=float, default=0.0,
                   help="Exit non-zero if defense rate %% is below this threshold (CI gate)")
    p.add_argument("--version", action="version", version=f"%(prog)s {__version__}")
    args = p.parse_args(argv)

    try:
        target = _load_target(args.target)
        corpus = load_corpus(args.corpus)
        results = run(target, corpus)
    except Exception as e:
        print(f"error: {e}", file=sys.stderr)
        return 2

    summ = summarize(results)
    if args.format == "json":
        out = json.dumps({"target": target.name, "summary": summ,
                          "results": [r.__dict__ for r in results]}, indent=2)
    else:
        out = to_markdown(target.name, results, summ)

    if args.output:
        open(args.output, "w", encoding="utf-8").write(out)
        print(f"wrote report -> {args.output} (defense rate {summ['defense_rate']}%)", file=sys.stderr)
    else:
        print(out)

    if summ["defense_rate"] < args.fail_under:
        print(f"FAIL: defense rate {summ['defense_rate']}% < threshold {args.fail_under}%", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
