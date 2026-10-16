# Autonomous run

**Use it when.** You have one long task and you want the agent to keep working until a clear finish line is met, without checking in.

**In plain words.** The agent first writes down what "done" means as a check it can run, such as "all tests pass". This check is called the exit condition, or predicate. Then it loops. Each round it makes the smallest change that the evidence supports, tests it against the check, and keeps it only if it helped. The agent handles side problems itself and stops only when the check passes or it hits a real dead end.

**What it does.**
1. Write the exit condition as a checkable predicate before the first iteration.
2. Pick a wake mechanism with Cursor's `/loop` command. Use a watcher subagent if there is an event to watch (CI, a merge). Use a fixed-interval heartbeat if there is not.
3. Make the smallest change the evidence justifies, verify it against the predicate, and commit it if it advanced. Discard changes that did not help. The `sequence-verifiable-units` skill orders the work so each unit is checked before the next.
4. Fix mid-run discoveries yourself through poteto-mode, such as flaky verifiers or related bugs. Put out-of-band fixes in their own PR. Surface only irreversible actions, product calls no experiment can settle, or a real dead end.
5. Checkpoint every iteration with the `show-me-your-work` skill. Add a row for what changed and whether the predicate moved.
6. Stop when the predicate is met. A plateau is not a stop, so change approach. Never relax the predicate to declare victory.

**What you get back.** A reply with the exit condition, the number of iterations run, what landed, what was discarded, and the final state of the predicate.

**Copy and adapt.**

```text
/poteto-mode run until <the check that means done>, don't stop until it passes. prove it by <the command that shows it> and show me what you tried each round
```

Filled in:

```text
/poteto-mode run until the checkout tests all pass, don't stop until they pass. prove it by running npm test and show me what you tried each round
```

```text
/poteto-mode /loop until <the thing to watch> is <the state you want>. keep going and fix side problems yourself. give me a done check at the end
```

Filled in:

```text
/poteto-mode /loop until the csv export test is green on ci. keep going and fix side problems yourself. give me a done check at the end
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| "run until done" | Routes to this playbook. |
| "/loop until X" | Routes to this playbook and names the exit condition. |
| "going to bed, keep going" | The agent does not stop to ask. Long unattended work also gets a decision trail via `show-me-your-work`. |
| "watch CI" or "wait for the merge" | Fits the event-watching wake mechanism (a watcher subagent). |
| "check again every <time>" | Fits the fixed-interval heartbeat when there is no event to watch. |

**Watch for.**
- The agent does not stop at a plateau. It changes approach instead.
- It does not relax the predicate. A vague "done" in your prompt weakens the whole loop.
- It surfaces irreversible actions to you. The poteto-mode Always-pause list covers force-push to shared branches, deploys, data deletion, and customer messages.
- A side fix goes in its own PR, so expect more than one PR.

**Pairs with.** `orchestrate` for multi-day programs, `babysit` for driving a PR green, `hillclimb` for improving one metric, and the `show-me-your-work` skill.
