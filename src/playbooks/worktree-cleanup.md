# Worktree and simulator cleanup

**Use it when.** Your disk is filling up and you want to remove old git worktrees and stale iOS simulators safely.

**In plain words.** A git worktree is an extra checked-out copy of a repository, often made for a branch or a task. They pile up and take disk space. This playbook runs an audit script that lists each worktree with its size, age, and state, and suggests a bucket for it. The bucket is advice only. The agent then confirms which chats still use each worktree before it deletes anything. This playbook deletes user state with no code review to catch a slip, so its gates act as the review.

**What it does.**
1. Record `df -h /`. Run `scripts/worktree-audit.sh [-b <pr-base-ref>] [repo-path]`. Pass `-b origin/<branch>` when PRs target another branch. Run the slow transcript scan in the background.
2. Treat the bucket as advice. Get the pinned and active chats from you or the sidebar, and cross-check every candidate. The pinned set wins.
3. Verify usage before deleting. For each `verify-recent-chat` row, or anything doubtful, fan out subagents to read the transcripts.
4. Pause on irreversible loss. `wip:N` is N tracked uncommitted edits, so show the diff and get a decision first. `scratch:N` is untracked throwaway, safe to drop, but name the files.
5. Prune the confirmed set with `git worktree remove --force <path>`. If the directory survives, `rm -rf` it, then run `git worktree prune`. Branch refs survive. Confirm with `df -h /` and re-list.
6. Reclaim simulators and other caches. The playbook lists `xcrun simctl --set testing delete all`, `xcrun simctl delete unavailable`, `xcrun simctl runtime list` then `runtime delete <id>`, Xcode `DerivedData` and `iOS DeviceSupport`, Cursor application support files, and package caches. Clear only caches you have not said to keep.

**What you get back.** A reply with `df -h /` before and after and the space reclaimed, the worktrees pruned, and a one-line reason for each one held back (in use by which chat, or uncommitted work).

**Copy and adapt.**

```text
/poteto-mode clean up worktrees. my disk is low. prune the safe-to-prune ones, keep anything used by <my pinned chats>, and show me the disk space before and after
```

Filled in:

```text
/poteto-mode clean up worktrees. my disk is low. prune the safe-to-prune ones, keep anything used by my pinned web shop chats, and show me the disk space before and after
```

```text
/poteto-mode what's using my disk? free up space by deleting old simulators and pruning merged worktrees in <repo path>. ask me before deleting any uncommitted work
```

Filled in:

```text
/poteto-mode what's using my disk? free up space by deleting old simulators and pruning merged worktrees in ~/code/notes-app. ask me before deleting any uncommitted work
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| "clean up worktrees" | Routes to this playbook. |
| "prune safe-to-prune worktrees" | Routes to this playbook. |
| "delete old simulators" | Routes to this playbook and points at step 6. |
| "my prs target <branch>" | Fits the `-b origin/<branch>` option of the audit script. |
| "keep my pinned chats" | Gives the agent the pinned set, which wins over the script's bucket. |

**Watch for.**
- The script has marked a worktree `safe` that the user had pinned. The pinned set always wins.
- A pinned chat spawns arena and repro trees into sibling worktrees through background subagents. Those are in use even when their names are not in the sidebar.
- `wip` rows and in-use worktrees pause for your decision. Only clean, merged, not-in-use worktrees proceed on their own.
- Uncommitted work removed with `git worktree remove --force` is gone. Branch refs survive, so committed work is safe.

**Pairs with.** The `principle-build-the-lever`, `principle-prove-it-works`, and `principle-guard-the-context-window` skills.
