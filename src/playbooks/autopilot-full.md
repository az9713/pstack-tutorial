# Autopilot Full

**Use it when.** You have a queue of independent changes, you grant full autonomy, and you want each one built, verified, and merged.

**In plain words.** Autopilot-full gives each PR its own owner agent. The owner builds the change, opens the PR, proves it, babysits it to green, and merges it. The twist is that no owner merges on its own say-so. A separate swarm, which is a group of verifier agents that did not write the code, must prove the code that lands. Green CI alone never authorizes a merge, because CI covers one head and a verdict covers one patch.

**What it does.**
1. Honors the operator's gates first. Items you name as yours and PRs outside the queue stop at merge-ready. A request to state the plan is not a go.
2. Spawns one owner per PR. Each is a Cursor cloud agent that builds, opens its PR per `playbooks/opening-a-pr.md`, proves the change on the real artifact, and babysits per `playbooks/babysit.md`. The code counts as ready only after the `/deslop` and `/no-comments` passes. Each owner then rebases onto trunk and reports a code-ready head. They keep a decision trail per the `show-me-your-work` skill.
3. Runs owners in parallel off trunk, never stacked, so each PR lands on its own.
4. Swarm-verifies once at the code-ready head per the `swarm` skill. Verifiers re-run the gates, prove the behavior live through a control skill such as `control-ui` or `control-cli`, and audit the diff. Proven findings go to the owner in one fix-forward.
5. Lets the owner merge only what was verified, tested on the trunk it lands on. Right before merging, it checks whether trunk changed anything that can affect the patch and rebases only when needed.
6. Runs the root layer. Loosened gates need a verifier's proof and a fresh countersign. On your go, it arms `/loop 1h` to audit every agent until no delegated work is left, and replaces stuck agents.
7. Stands down at once on your stop. Every owner reports where it stands and writes nothing until you release it.

**What you get back.** A catch-up per the `ketchup` skill. It covers each PR's state and verdict, what merged, countersigns and why, and open operator gates, with links to each PR and the trails.

**Copy and adapt.**

```text
/poteto-mode full autopilot on this queue. each item is independent. <list of items>
```

Filled in:

```text
/poteto-mode full autopilot on this queue. each item is independent. fix the typo in the order email, add a dark mode toggle to the shop header, and make the product page load its images lazily.
```

```text
/poteto-mode autopilot this queue with one owner per pr. <list of items>. swarm-verify each pr before merge and give me the verdict for each pr when i'm back.
```

Filled in:

```text
/poteto-mode autopilot this queue with one owner per pr. add a csv export button, fix the date format on receipts, and hide sold-out items from search. swarm-verify each pr before merge and give me the verdict for each pr when i'm back.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `full autopilot` | Selects this playbook. Owners can merge once the root's verdict clears them. |
| `each item is independent` | Matches the playbook's rule that owners run in parallel off trunk. |
| `i want them merged by morning` | Taken from the guide's overnight example. It states the goal. |
| `<item> is mine, stop it at merge-ready` | The playbook stops items you name as yours at merge-ready. |
| `stop` | Stands every owner down with zero writes until you release it. |

**Watch for.**
- This playbook merges. Use it only when you grant landing authority. For review before landing, use `autopilot-stack`.
- It is for independent PRs. Coupled or sequenced work belongs in `autopilot-stack`.
- Never give or bypass an approval the forge enforces. No countersign covers it.
- A disabled or soft-failed check always comes out, because it stops guarding every case.

**Pairs with.** `autopilot-stack`, `opening-a-pr`, `babysit`, and `shipping`. Related skills are `swarm`, `ketchup`, `show-me-your-work`, and `/deslop`.
