# Session pickup

**Use it when.** An earlier agent started work, and you want a fresh agent to take over from where it stopped.

**In plain words.** The playbook treats the earlier agent's trail as the source of truth. A trail is a transcript, a cloud-agent URL, or a pushed branch. The new agent reads it, works out what already landed and what is left, and continues from there. It does not redo finished work. It does check the final result on the real artifact, because a past "it passed" is a report and not proof.

**What it does.**
1. Locate the prior trail in the active workspace's `agent-transcripts/` directory, a cloud-agent URL, or a pushed branch. Read the overview and last messages first. Parse a long transcript in a subagent.
2. Reconstruct the operational state. Check the branch and worktree, what landed (`git log`, `git diff` against the base), the open todos, and the decisions made.
3. Diff done against pending. Name the resume point. Do not re-run the old repro or redo completed work.
4. Route the remaining work to the matching playbook. Pick a verdict among continue, ship a finished recommendation, ratify or override a prior conclusion, or postmortem a failed run.
5. Verify the inherited claims against the original goal on the real artifact, using the `principle-prove-it-works` skill.

**What you get back.** A reply with where the prior agent stopped, what you inherited and what you redid (ideally nothing redone), the resume point, and the outcome.

**Copy and adapt.**

```text
/poteto-mode pick up where the last agent left off on <branch, transcript, or cloud-agent URL>. don't redo finished work. finish <the remaining goal> and prove it works
```

Filled in:

```text
/poteto-mode pick up where the last agent left off on the branch login-form-fix. don't redo finished work. finish the password reset flow and prove it works
```

```text
/poteto-mode resume the work from <where the prior chat or branch lives>. tell me what you inherited and the resume point, then <what you want next>. check the result on the real <artifact>
```

Filled in:

```text
/poteto-mode resume the work from the csv export chat from yesterday. tell me what you inherited and the resume point, then finish the export. check the result on the real exported file
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| "pick up where X left off" | Routes to this playbook. |
| "take over from <URL or branch>" | Points step 1 at a cloud-agent URL or pushed branch. |
| "postmortem the failed run" | Selects the postmortem verdict in step 4. |
| "ratify or override its conclusion" | Selects the ratify or override verdict in step 4. |
| "ship the finished recommendation" | Selects the ship verdict in step 4. The routed playbook owns the rest. |

**Watch for.**
- The playbook warns against a "let me verify from scratch" pass. That treats an authoritative trail as untrustworthy.
- Do not glob across `~/.cursor/projects/*/`. That crosses workspace boundaries and reads private chats from unrelated projects.
- The pickup playbook ends at routing. The routed playbook owns the rest.
- A prior self-report of passing is not proof. Step 5 checks the real artifact.

**Pairs with.** `pause-safely` (its complement), `autonomous-run`, `bug-fix`, `feature`, and the `principle-guard-the-context-window` and `principle-prove-it-works` skills.
