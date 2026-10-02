# Layout eval scores
Hold-out = the fixed 1-in-5 split of golden.jsonl. Keep a prompt or library change only if it does not lower top-1 or top-3 on the same set.

| Date | Selector | Set | n (accepted) | Top-1 | Top-3 | Reasoning | Note |
|---|---|---|---|---|---|---|---|
| 2026-10-02 | layout_match.py | provisional (incl. pending) | 36 (0) | 47% | 69% | n/a | baseline before review; SG DC rows were tuned on in Phase 2 |
| 2026-10-02 | blind subagent | provisional (incl. pending) | 36 (0) | 50% | 75% | 94% | baseline before review (Opus subagent, 141 provisional examples) |
