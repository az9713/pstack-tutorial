# Hillclimb

**Use it when.** You want to improve one measurable number step by step toward a target, and a single fix is not enough.

**In plain words.** Hillclimbing is a loop. The agent changes one thing, measures, and keeps the change only if the number improves past noise and the tests stay green. Otherwise it reverts the change fully. Before the loop starts, the agent builds one repeatable measurement command and freezes it, so every attempt is judged the same way. It writes every attempt to a decision log, so you can see what was tried and why it was kept or dropped.

**What it does.**
1. Grounds the workload with the `how` skill. It picks a case that reproduces your complaint, then fixes one metric, the direction that counts as better, and a stop predicate. The predicate pairs a target with a minimum number of attempts, for example "at least 50% better than baseline and at least 10 iterations".
2. Builds the measurement harness, proves it can tell cases apart, and freezes it. It vets the harness with `benchmark-checklist`. It uses a median of N runs, and it records the baseline and a green run of the regression gate, which is the set of tests that must keep passing.
3. Opens a decision log with the `show-me-your-work` skill. It is a `decision.tsv` with one row per attempt, kept out of the tree.
4. Grounds each hypothesis in a specific mechanism. For a performance metric, it orders hypotheses by the performance mantras from the Perf issue playbook.
5. Loops one hypothesis at a time. A subagent makes the change. The agent measures before and after, runs the regression gate, keeps a change only if the metric moves past noise and the gate stays green, and otherwise reverts it in full. It makes one commit per accepted fix and logs every row.
6. Pushes past the first plateau by pivoting category, combining near-misses, re-reading the source, or trying something more radical. Correctness and simplicity outrank the number.
7. Stops when the predicate is met, or when the remaining ideas are marginal.
8. Runs the Opening a PR playbook with the accepted commits stacked in the order they landed.

**What you get back.** The metric and target, the baseline and final values with the percent change, the iterations run (kept versus reverted), one line per accepted fix, the `decision.tsv` path, and the best idea to try next.

**Copy and adapt.**

```text
/poteto-mode hillclimb <metric> on <workload>. target is at least <percent>% better than baseline and at least <n> iterations. one change, one measurement, keep or revert.
```
Filled in:
```text
/poteto-mode hillclimb the page load time of the product search page on the demo shop data. target is at least 50% better than baseline and at least 10 iterations. one change, one measurement, keep or revert.
```

```text
/poteto-mode <operation> is too slow on <fixture>. hillclimb it. freeze a measurement harness first, keep the <test command> green, and log every attempt in decision.tsv.
```
Filled in:
```text
/poteto-mode the csv export is too slow on 50000 orders. hillclimb it. freeze a measurement harness first, keep the unit tests green, and log every attempt in decision.tsv.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `hillclimb` | Names the playbook for sustained improvement of one metric. |
| `at least <percent>% better than baseline and at least <n> iterations` | Sets the stop predicate in the target-plus-attempts shape from step 1. |
| `one change, one measurement, keep or revert` | States the core discipline of the loop. |
| `keep <tests> green` | Names the regression gate. |
| `log every attempt in decision.tsv` | Matches the decision log in step 3. |

**Watch for.**
- If no case reproduces your complaint, the agent fixes the repro first and does not hillclimb.
- The agent does not relax the stop predicate to meet it. If it is stuck, it says so instead of spinning.
- A change that "might help" is not kept. Only a change that moves the metric past noise with a green gate is kept.
- For a single fix, use Perf issue or Bug fix. This playbook is the loop.

**Pairs with.** `perf-issue` for a one-off fix, `autonomous-run` for unattended runs, and the `how`, `benchmark-checklist` and `show-me-your-work` skills.
