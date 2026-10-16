# Perf Issue

**Use it when.** Something is measurably slow and you want it traced, fixed, and shown faster with before and after numbers.

**In plain words.** The agent measures first and fixes second. It captures a baseline, which is the starting measurement, and it checks that the measurement is trustworthy. Then it tries ideas in a fixed order from cheapest to most expensive, called the performance mantras. The cheapest idea is to not do the work at all. It stops at the first idea that meets the target and proves the result with a second measurement.

**What it does.**
1. Captures a baseline trace through the matching control skill. It checks the baseline, and each later number, with the `benchmark-checklist` skill.
2. Grounds hypotheses with `how`. It does not claim a performance ceiling without running it first.
3. Tries the performance mantras in order, cheapest first. They are don't do it, do it but don't do it again, do it less, do it later, do it when they're not looking, do it concurrently, and do it cheaper. When an earlier mantra meets the target, it stops.
4. Plans the fix from the trace. If the fix crosses a function boundary, it runs `architect` first. It delegates the implementation to a subagent, reviews the diff, and captures a post-fix trace. It verifies each attempt before the next, following `sequence-verifiable-units`.
5. Parses and compares the artifacts, for example JSON into sqlite and a diff. A result of "inconclusive" or a check on the wrong surface is not a pass, and the agent flags it.
6. Cites the measurement in the PR, then runs the Opening a PR playbook.

**What you get back.** The baseline number, the post-fix number, the delta and the artifact path.

**Copy and adapt.**

```text
/poteto-mode <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.
```
Filled in:
```text
/poteto-mode the product search page takes 1.8s to load on the demo shop data. trace it, fix the measured cause, show me before and after.
```

```text
/poteto-mode <operation> is slow when <condition>. capture a baseline trace, try the cheapest fix first, and cite the before and after numbers in the pr.
```
Filled in:
```text
/poteto-mode the csv export is slow when there are 50000 orders. capture a baseline trace, try the cheapest fix first, and cite the before and after numbers in the pr.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `trace it` | Starts with a baseline trace, as in step 1. |
| `show me before and after` | Matches the reply, which gives the baseline, post-fix number, delta and artifact path. |
| `try the cheapest fix first` | Matches the order of the performance mantras. |
| `cite the numbers in the pr` | Matches step 6, which cites the measurement in the PR. |

**Watch for.**
- The playbook ties every fix to a measurement. It does not read the source instead of measuring.
- A baseline the `benchmark-checklist` skill rejects is not a baseline. Expect the agent to fix the measurement first.
- This is a one-off fix. For sustained improvement against a metric, use the Hillclimb playbook.
- If you want the cause only and no fix, use Runtime forensics or Trace forensics.

**Pairs with.** `hillclimb` for sustained work, `trace-forensics` for an existing capture, `bug-fix` for incorrect behavior, and the `benchmark-checklist` skill.
