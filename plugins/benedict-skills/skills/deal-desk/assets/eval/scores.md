# Layout eval scores
Hold-out = the fixed 1-in-5 split of golden.jsonl. Keep a prompt or library change only if it does not lower top-1 or top-3 on the same set.

| Date | Selector | Set | n (accepted) | Top-1 | Top-3 | Reasoning | Note |
|---|---|---|---|---|---|---|---|
| 2026-10-02 | layout_match.py | provisional (incl. pending) | 36 (0) | 47% | 69% | n/a | baseline before review; SG DC rows were tuned on in Phase 2 |
| 2026-10-02 | blind subagent | provisional (incl. pending) | 36 (0) | 50% | 75% | 94% | baseline before review (Opus subagent, 141 provisional examples) |
| 2026-10-02 | layout_match.py | provisional (incl. pending) | 47 (0) | 53% | 79% | n/a | re-labelled vs full menu (bk + ig), 40 infographic test rows added; still pending review |
| 2026-10-02 | layout_match.py | accepted + silver · dev | 41 (0) | 59% | 71% | n/a | round 0 (judge answers, before wording fixes) |
| 2026-10-02 | layout_match.py | accepted + silver | 47 (0) | 45% | 66% | n/a | round 0 (judge answers, before wording fixes) |
| 2026-10-02 | blind subagent | accepted + silver · dev | 41 (0) | 85% | 100% | 90% | round 0 baseline |
| 2026-10-02 | blind subagent | accepted + silver | 47 (0) | 83% | 96% | 91% | round 0 baseline |
| 2026-10-02 | blind subagent | accepted + silver · train-a | 61 (0) | 89% | 100% | 94% | round 0 baseline |
| 2026-10-02 | blind subagent | accepted + silver · train-b | 60 (0) | 80% | 90% | 88% | round 0 baseline |
| 2026-10-02 | layout_match.py | accepted + silver · dev | 41 (0) | 59% | 71% | n/a | round 1 |
| 2026-10-02 | blind subagent | accepted + silver · dev | 41 (0) | 90% | 100% | 94% | round 1 |
| 2026-10-02 | blind subagent | accepted + silver · train-a | 61 (0) | 97% | 100% | 89% | round 1 |
| 2026-10-02 | blind subagent | accepted + silver · train-b | 60 (0) | 85% | 95% | 85% | round 1 |
| 2026-10-02 | layout_match.py | accepted + silver · dev | 41 (0) | 59% | 71% | n/a | round 2 |
| 2026-10-02 | blind subagent | accepted + silver · dev | 41 (0) | 88% | 100% | 91% | round 2 |
| 2026-10-02 | layout_match.py | accepted + silver | 47 (0) | 43% | 66% | n/a | after round 1 (final) |
| 2026-10-02 | blind subagent | accepted + silver | 47 (0) | 87% | 98% | 88% | after round 1 (final) |
