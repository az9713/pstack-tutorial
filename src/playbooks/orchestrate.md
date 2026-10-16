# Orchestrate

**Use it when.** You hand over a whole project that runs for days, with many stacked PRs and dozens of subagents, and you want to check in only a couple of times a day.

**In plain words.** One standing chat acts as the coordinator. The coordinator never writes code. It writes briefs, collects results, keeps the merge line green, and makes decisions. Workers are subagents, which are helper agents that each do one unit of work. A worker cannot ask the coordinator questions, so every brief must be complete. The playbook warns that a vague brief fails quietly. Use this only when the work outlives one agent. A task one agent can finish in the session is Autonomous run instead.

**What it does.**
1. Frame the project. State a countable done predicate, such as "all 126 units merged". Quantify units, effort, and time budget. If one agent could finish in that budget, stop and run Autonomous run.
2. Install the runtime. Run `orch init`, open the trail with the `show-me-your-work` skill, write the standing orders (`preferences.md`) before any spawn, and seed `frontier.json` with `orch frontier set --repo <repo-dir>`.
3. Pilot one unit through the full path (brief, worker, verification, stack entry, ledger row, merge). Fix the contract from that evidence before any fan-out.
4. Scale with a rolling window of workers. Refill as children finish. Spawn track sub-coordinators only if one coordinator cannot drain the program.
5. Drain the queue at set points. Completions are queue events. Run `orch inbox drain`, classify each pointer, write the rows, run `orch status`, and spawn the next wave.
6. Land continuously and keep the frontier green. One stacker per stack changes topology. Workers never rebase, retarget, or merge.
7. Verify with ledger rows keyed by PR and head SHA. Use a verifier on a different model family when verification is costly.
8. Close. Reconcile every spawned agent to a terminal row, confirm the predicate on the real artifact, and keep the store as the postmortem.

**What you get back.** A reply at checkpoints and at close with the predicate and the count against it, what each track landed, the frontier (PR list plus SHAs), a verdict summary, what was abandoned and why, the gates awaiting you, the store path, the trail path, and PR links. Numbers come from `units.tsv` and `ledger.tsv`.

**Copy and adapt.**

```text
/poteto-mode run this whole project, <the project and the end state>. own it until it lands. done means <countable predicate>. give me a status page when you need me and prove each unit is verified
```

Filled in:

```text
/poteto-mode run this whole project, move our web shop from the old cart api to the new one across all 40 pages. own it until it lands. done means all 40 page PRs are merged and each one is verified. give me a status page when you need me and prove each unit is verified
```

```text
/poteto-mode own this migration until it lands. <what to migrate>, stacked PRs are fine, minimal check-ins. only ask me about <the decisions that are yours>
```

Filled in:

```text
/poteto-mode own this migration until it lands. move the notes app from plain javascript files to a typed config, stacked PRs are fine, minimal check-ins. only ask me about deletions and anything that changes what users see
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| "run this whole project" | Routes to this playbook. |
| "own this migration until it lands" | Routes to this playbook. |
| "minimal human turns" | Matches the playbook's design of few check-ins. |
| "only ask me about X" | A good habit. The agent can add your rule to the standing orders (`preferences.md`) so it reaches every worker. |
| "use the arena skill before we start" | Fits the playbook's rule that a contested decomposition goes through arena before the pilot. |

**Watch for.**
- Work one agent could finish in the session's budget is not a program. The playbook sends it to Autonomous run.
- The coordinator never edits code. Merge conflicts and rebases become tasks for workers or the stacker.
- Irreversible actions reach you as parked gates (`gates.md`). Examples are force-push to shared branches, deploys, deletions, and closing someone else's PR.
- A new head SHA voids a verification row. Expect re-verification after a restack.

**Pairs with.** `autonomous-run`, `babysit`, `shipping`, `pause-safely`, `session-pickup`, and the `show-me-your-work` and `arena` skills.
