# Opening a PR

**Use it when.** Your work is done on a branch and you want it turned into a clean pull request that a reviewer can read in about a minute.

**In plain words.** A PR (pull request) is a request to merge your branch into the main line of code, called trunk. This playbook is the last step of every other playbook, and you can also ask for it alone. It works from a git worktree, which is a separate checkout of the repo, so unrelated work cannot leak in. It splits the work into small ordered commits and writes a short description, because a reviewer who has the diff mostly needs to know why the change exists, what it leaves out, and how you proved it.

**What it does.**
1. Works from a git worktree off main. Subagents inherit that worktree.
2. Rebases the work into small, ordered commits. Each commit should be landable and tell part of the story.
3. Runs `/deslop` from `cursor-team-kit` over the diff before commit, and `/no-comments` before review.
4. Writes the PR title, description, and commit bodies with `/technical-writing`, then applies `/unslop`.
5. Titles the PR in Conventional Commits form, `type(scope): subject`, with no trailing period.
6. Writes the body with `##` headings in this order, dropping any section with nothing to say. The headings are `## Why`, `## What changed`, `## Scope`, `## Tradeoffs`, `## Blast Radius`, and `## Verification`.
7. Opens the PR ready for review, never as a draft. It uses `gh` by default, or `origin pr` when the Origin CLI can resolve the repo, or the built-in PR tool when the run has one.
8. Posts the PR URL and keeps building. It does not start a babysit.

**What you get back.** The PR link in the form `https://github.com/<owner>/<repo>/pull/<number>`. The PR body carries the why, the scope, the blast radius, and verification bullets with real run paths and outcomes. Videos or screenshots are attached when they prove a claim. Long evidence such as full SHAs goes in a linked artifact, not the body.

**Copy and adapt.**

```text
/poteto-mode open the pr for <what changed>. small ordered commits, evidence in the description.
```

Filled in:

```text
/poteto-mode open the pr for the new coupon code field at checkout. small ordered commits, evidence in the description.
```

```text
/poteto-mode open the pr. split <the change> into small ordered commits, strip slop from the diff, and put the proof you ran in the verification section. open it ready, not draft.
```

Filled in:

```text
/poteto-mode open the pr. split the csv export fix into small ordered commits, strip slop from the diff, and put the proof you ran in the verification section. open it ready, not draft.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `small ordered commits` | Asks for the rebase into small commits that tell the story. |
| `evidence in the description` | Puts run paths and outcomes in the `## Verification` section. |
| `open it ready, not draft` | Matches the playbook's default of opening every PR ready. |
| `five narrow PRs` | Asks for several small PRs instead of one large one. The playbook prefers this. |
| `stack them` | Asks for a base-branch chain. Each child PR targets its parent's branch. |

**Watch for.**
- Opening a PR does not start a babysit. Ask for Babysit separately, after the whole stack exists.
- The playbook does not merge. It stops at the PR link.
- Perf changes get one primary number in the body, in the form `before → after`, with a link for the rest.
- If a PR still opens as a draft, the playbook marks it ready through the PR tool, `origin pr ready <number>`, or `gh pr ready <number>`.

**Pairs with.** Every other playbook ends here. Next steps are `babysit` and `shipping`. Related skills are `/deslop`, `/no-comments`, `/technical-writing`, and `/unslop`.
