# Bug Fix

**Use it when.** You have a reported defect and you want it reproduced, traced to its root cause, and fixed with proof that it is gone.

**In plain words.** The agent runs the program itself and makes the bug happen before it touches any code. Then it narrows down the cause by ruling out candidate explanations one at a time, using runtime evidence. It ships only the smallest change that the evidence justifies. A guess that "might help" does not ship. The fix is checked on the same surface where the bug was first seen, so a passing unit test alone does not count.

**What it does.**
1. Reproduces the bug itself on the matching surface through the control skill. It asks you only when it can state a specific reason the control surface cannot reach the target.
2. Binary-searches the cause. A binary search splits the possible causes in half each time. It forms candidate hypotheses, seeds them with `how` and `why` (for regression history), and rules them out with runtime evidence until one survives. It can use Cursor's `/loop` command for a long hunt.
3. Plans the fix. If the fix crosses a function boundary, it runs `architect` first. It delegates the implementation to a subagent with a specific scope.
4. Verifies on the same surface. The original repro must now pass. A result of "inconclusive" or a check on the wrong surface is not a pass, and the agent flags it.
5. Stages the commits so the failing repro lands before the fix in git history. When the bug has a cheap local test, it follows the `tdd` skill for the failing-test-first order.
6. Runs the Opening a PR playbook.

**What you get back.** What was broken, the root cause, the fix, and how it was verified. The reply pastes the failing and then passing repro output verbatim.

**Copy and adapt.**

```text
/poteto-mode <bug in plain words>. repro it first. if there's a cheap test path, /tdd it. then fix and rerun the repro to show it passes.
```
Filled in:
```text
/poteto-mode the web shop cart total is wrong when i apply a discount code twice. repro it first. if there's a cheap test path, /tdd it. then fix and rerun the repro to show it passes.
```

```text
/poteto-mode this pr has a subtle bug where <symptom> even when <condition>. repro it, find the root cause with runtime evidence, and show me the failing then passing output.
```
Filled in:
```text
/poteto-mode this pr has a subtle bug where the notes list jumps back to the top even when i am not typing. repro it, find the root cause with runtime evidence, and show me the failing then passing output.
```

```text
/poteto-mode <thing> breaks when <trigger>. repro first, then fix the root cause with the smallest change the evidence supports. done when the original repro passes.
```
Filled in:
```text
/poteto-mode the csv export breaks when a product name has a comma. repro first, then fix the root cause with the smallest change the evidence supports. done when the original repro passes.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `repro first` | Gives the routing signal for Bug fix and makes the reproduction the first step. |
| `/tdd it` | Uses the failing-test-first order when a cheap local test path exists. |
| `done when the original repro passes` | Gives a checkable outcome that matches step 4. |
| `show me the failing then passing output` | Matches the reply, which pastes both outputs verbatim. |
| `with runtime evidence` | Matches the rule that every shipped line traces to runtime evidence. |

**Watch for.**
- A fix without runtime evidence is a hypothesis, and the playbook does not ship it. If evidence refutes a hypothesis, the agent reverts what it motivated.
- Unit tests show branch behavior, not bug absence. The repro on the original surface is the proof.
- The agent can ask you to reproduce the bug only with a stated, specific reason. If it asks without one, remind it of that rule.
- A good habit is to name the surface in your prompt, for example the browser page or the command, so the agent drives the right one.

**Pairs with.** `runtime-forensics` and `trace-forensics` when you want the cause before the fix, `perf-issue` for slowness, and the `tdd`, `how`, `why` and `architect` skills.
