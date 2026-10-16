# Shipping

**Use it when.** Your stack of PRs is green and you want it landed safely, one verified PR at a time.

**In plain words.** Green checks do not prove a change works, because CI does not run the change the way a user would. So Shipping asks a separate verifier agent to run each PR for real before anything merges. A stack is a chain of PRs where each one builds on the one below. Shipping lands only the verified PRs that touch the bottom of the chain, in order, and stops at the first PR that has no passing verdict.

**What it does.**
1. Resolves the forge (`gh` by default, `origin pr` when available). Then runs one verifier per PR, each a Cursor cloud agent. The verifier uses the matching control skill, such as `control-ui` or `control-cli`, and posts `PASS`, `PASS+NOTES`, or `FAIL` on the PR.
2. Walks up from the lowest unmerged PR and stops at the first one without `PASS` or `PASS+NOTES`. The PRs below that point are the run. The top one is the ceiling.
3. Checks that each verdict still describes the code. It compares `git patch-id` at the verdict SHA with the current head, because a rebase moves a PR to a new SHA.
4. Lands bottom-up, one PR at a time, with `origin pr merge <pr>` or `gh pr merge <pr> --squash`. It reads the PR back to confirm the merge, then retargets the next PR to trunk and pushes with `--force-with-lease`.
5. Leaves the stack alone while it lands. On GitHub it watches with `scripts/watch-pr/watch-pr --queued-stack --stack-prs <bottom-to-top>` under `/loop` until `COMPLETE`.
6. Stops at the ceiling. Extending the run needs new verdicts.

**What you get back.** The verified run and its ceiling. For each PR, its verdict and who produced it. What landed and how the merge was confirmed. What the next gap needs.

**Copy and adapt.**

```text
/poteto-mode land the stack. <stack root pr or branch>
```

Filled in:

```text
/poteto-mode land the stack. the root is pr 482 and three more checkout prs sit above it.
```

```text
/poteto-mode land the stack. verify each pr with a fresh agent first, land only the verified run from the bottom, and tell me where it stopped and why.
```

Filled in:

```text
/poteto-mode land the stack for the new login form. verify each pr with a fresh agent first, land only the verified run from the bottom, and tell me where it stopped and why.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `land` or `ship` | Routes the request to Shipping. |
| `verify each pr first` | Matches step 1. One verifier per PR runs before anything is armed. |
| `land only the verified run` | Matches step 2. Landing stops at the first PR without a passing verdict. |
| `tell me where it stopped` | Asks for the ceiling and the next gap in the reply, which the playbook already reports. |

**Watch for.**
- Green CI and an approving bot review are not verdicts. Only a verifier that did not write the code counts.
- A verified PR above an unverified one waits. It cannot land without the code below it.
- A merge command can report success when a merge queue only queued the PR, so the playbook reads the PR back to confirm.
- Once landing starts, nobody changes branches or bases except the post-merge retarget in step 4. If a merge stalls, the playbook finds out why before it changes anything.

**Pairs with.** `babysit` comes first and ends at merge-ready. `autopilot-stack` hands its finished stack to you for this step. Related skills are `control-ui` and `control-cli` from `cursor-team-kit`.
