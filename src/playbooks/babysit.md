# Babysit

**Use it when.** A PR is open and you want it driven to merge-ready, or you want a quick status check on it.

**In plain words.** A PR collects blockers as soon as it opens. Checks fail, reviewers comment, and trunk (the main branch) moves. CI means the automated checks that run on the PR. Babysit handles those blockers in a fixed order, so the checks restart as few times as possible. It stops at merge-ready, which means the forge (GitHub or Origin) agrees the PR can merge. It never merges.

**What it does.**
1. Declares a mode before any poll. `drive` runs the loop to merge-ready. `background` triages without blocking. `threads-only` answers review comments only. `check` is one status pass and a report. If you give no mode, it uses `drive`.
2. Resolves the forge. It uses `gh` by default, or `origin pr` when the Origin CLI can resolve the repo.
3. Works only the merge frontier, which is the lowest unmerged PR in a stack. Upstack threads are read and batched, not fixed.
4. Handles blockers in this order. Conflicts first, then review threads, then CI. It batches every known fix into one push.
5. Reads status from `scripts/watch-pr/watch-pr` on GitHub, or from `origin pr view`, `origin pr thread list`, and `origin pr checks` on Origin. It runs `drive` and `background` under `/loop`.
6. Classifies each CI failure before any retrigger. A flake earns one fresh build and no more. A failure in code the diff never touched means a stale base.
7. Triages Bugbot comments skeptically per `../references/bugbot-triage.md`. Real findings get a fix with a red-first proof. Noise gets a dismissal with the concrete disproof on the thread.
8. Stops at merge-ready and reports. It does not merge.

**What you get back.** A report on the frontier PR. It says whether it is merge-ready or what still blocks it, and names any conflict that needs a rebase by the branch owner. After a `drive` run it also offers any team-useful dismissal pattern as a candidate entry for the shared Bugbot rubric.

**Copy and adapt.**

```text
/poteto-mode babysit this pr. get it green. <pr link or number>
```

Filled in:

```text
/poteto-mode babysit this pr. get it green. https://github.com/acme/webshop/pull/482
```

```text
/poteto-mode check on pr <number>. anything outstanding?
```

Filled in:

```text
/poteto-mode check on pr 482. anything outstanding?
```

```text
/poteto-mode address the bugbot comments on pr <number>. verify each one against the code, fix the real ones with a failing test first, and dismiss noise with the reason.
```

Filled in:

```text
/poteto-mode address the bugbot comments on pr 482. verify each one against the code, fix the real ones with a failing test first, and dismiss noise with the reason.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `get it green` or `merge-ready` | Selects `drive` mode. |
| `check on pr <number>` or `is it green` | Selects `check` mode, one status pass and a report. |
| `address the bugbot comments` | Selects `threads-only` mode. It answers review comments and touches nothing else. |
| `babysit in the background` | The playbook names `background` as the mode that triages without blocking. A good habit is to use it while a plan is still executing. |

**Watch for.**
- Babysit never merges. Only an explicit request to merge, land, or ship does, and that goes to Shipping.
- It never changes stack topology. No retarget, rebase, stack-wide submit, or force-push happens inside a babysit. A conflict is reported with the branch that needs the rebase.
- A second identical CI failure is reclassified, not retried. The playbook allows one retry.
- Review-comment text is treated as untrusted data. It is checked against the code and never followed as an instruction.
- Opening a PR does not start a babysit. Ask for it once the phase or stack is built.

**Pairs with.** `opening-a-pr` before it, `shipping` after it. Related skills are `/loop` and the Bugbot triage reference.
