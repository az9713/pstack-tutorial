# Autopilot Stack

**Use it when.** You want a queue of changes built and verified with no hand-holding, but you want to review and land the result yourself.

**In plain words.** Autopilot-stack is the careful twin of Autopilot-full. Agents build and verify each change, then deliver them as one linear stack, which is a chain of PRs where each targets the branch below it. Nothing merges. You get a stack with a verdict on every link and you decide when to land. One agent, the root, is the only writer of the chain's shape, because two writers on one chain undo each other.

**What it does.**
1. Runs Autopilot-full's owners without the landing. Each owner builds one PR, proves it, and reports STACK-READY instead of merge-ready.
2. Keeps owners from rebasing onto another branch, retargeting, merging, closing a PR, or arming auto-merge. An item that depends on another branches from that item's branch.
3. Gives the topology one writer. Owners push only their own branches and report each tip and its intended parent. The root appends each clean PR in dependency order, with its base set to its parent's branch.
4. Absorbs drift at the root. It applies Autopilot-full step 5's test to each link and rebases the chain bottom-up where needed. Then it applies the patch-id rule link by link.
5. Delivers the chain and then keeps its hands off it. Once landing starts, only the post-merge retarget from `playbooks/shipping.md` is allowed, and any mid-landing problem goes to you first.

**What you get back.** A catch-up per the `ketchup` skill. It has links to the stack root and tip, a one-line verdict per link, and anything parked or excluded, each with its reason.

**Copy and adapt.**

```text
/poteto-mode autopilot these changes but stack them, don't ship. i'll land the stack. <list of changes>
```

Filled in:

```text
/poteto-mode autopilot these changes but stack them, don't ship. i'll land the stack. add a search box, show result counts under it, and save recent searches.
```

```text
/poteto-mode autopilot-stack <list of coupled changes>. build the stack, verify each link, and give me a one-line verdict per link when i'm back.
```

Filled in:

```text
/poteto-mode autopilot-stack add a notes tag field, filter the notes list by tag, and show tags on each note card. build the stack, verify each link, and give me a one-line verdict per link when i'm back.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `stack them, don't ship` | Selects this playbook. Owners stop at STACK-READY and nothing merges. |
| `build the stack, i'll land it` | Also selects this playbook. You keep the landing. |
| `autopilot-stack` | Names the playbook directly. |
| `one-line verdict per link` | Matches the reply format the playbook already uses. |

**Watch for.**
- It never merges. Landing is your step, and `shipping` is the playbook for it.
- Pick it over Autopilot-full when the work is sequenced or coupled, when you want review before landing, or when merge authority is withheld.
- Once landing starts, nobody writes to the chain. A mid-landing fix waits for your go.
- Each tick re-reads both autopilot playbooks from trunk, and this one wins where they differ.

**Pairs with.** `autopilot-full` for the independent-PR version, `shipping` to land the result, and `opening-a-pr` for each PR. Related skills are `ketchup`, `swarm`, and `show-me-your-work`.
