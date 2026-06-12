from pijack.runner import load_corpus, run, summarize
from pijack.targets import EchoTarget, GuardedTarget


def test_corpus_loads():
    c = load_corpus()
    assert len(c) >= 8
    assert all("payload" in p and "atlas" in p for p in c)


def test_undefended_leaks_everything():
    r = run(EchoTarget(), load_corpus())
    s = summarize(r)
    assert s["defense_rate"] == 0.0          # echo target has no guardrails


def test_guarded_blocks_more_than_undefended():
    g = summarize(run(GuardedTarget(), load_corpus()))
    e = summarize(run(EchoTarget(), load_corpus()))
    assert g["defense_rate"] > e["defense_rate"]


def test_atlas_present():
    r = run(GuardedTarget(), load_corpus())
    assert all(x.atlas.startswith("AML.") for x in r)
