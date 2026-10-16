# Pause safely

**Use it when.** You must stop work now and want the agent to leave a clean checkpoint that a fresh agent can resume from.

**In plain words.** A pause is a stop that loses nothing. The agent finishes or backs out of its current step, saves its edits in one commit, and writes a resume note. The note says what the work is for, how far it got, and what to do first. Compaction is when a long chat is trimmed to fit its memory. A resume note on disk survives compaction. This playbook runs only when you ask for it.

**What it does.**
1. Stop at a safe boundary. Finish the current atomic step or back out of it. Start nothing new and cancel any nested subagents.
2. Take no irreversible action to pause. Make no PR and no push unless one was already out.
3. Make the work durable. Commit uncommitted edits as one clear `wip:` commit on the current branch. If the tree is broken, say so in the commit body in one line.
4. Write the resume note off-context. Include intent, what you were doing, progress and what is verified, current state, next steps, key files, and gotchas. For the compaction trigger, write it to a file such as `/tmp/<slug>-resume.md`. If a `show-me-your-work` trail exists, point at it instead of copying it.

**What you get back.** A reply with where you are in the loop, what is on disk versus still in the agent's head (paths, no diff dumps), the commits made and whether the tree is clean, and the first action on resume. It is a pause, not a final report.

**Copy and adapt.**

```text
/poteto-mode pause safely. stop at a safe point, commit the work as a wip commit, and write a resume note so a fresh agent can continue <the task>
```

Filled in:

```text
/poteto-mode pause safely. stop at a safe point, commit the work as a wip commit, and write a resume note so a fresh agent can continue the notes app search feature
```

```text
/poteto-mode i'm going offline, so suspend <the task> cleanly. don't push or open a pr. tell me what's on disk and the first thing to do when we resume
```

Filled in:

```text
/poteto-mode i'm going offline, so suspend the shop discount code work cleanly. don't push or open a pr. tell me what's on disk and the first thing to do when we resume
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| "pause safely" | Routes to this playbook. |
| "going offline" | The playbook lists going offline as a reason to pause. |
| "before we compact" | The playbook lists imminent context compaction as a trigger. The resume note goes to a file. |
| "restarting cursor" | The playbook lists a Cursor restart as a trigger. |
| "suspend this so it can be resumed" | Matches the playbook's purpose, a clean stop that a fresh agent can resume. |

**Watch for.**
- Do not combine a pause request with "keep going", "going to bed, keep going", or "don't stop". The playbook then does not pause.
- The agent makes no PR and no push to pause, unless one was already out.
- Edits go in one `wip:` commit on the current branch. The tree may be broken, and the commit body says so in one line.
- A good habit is to read the resume note before you close the chat.

**Pairs with.** `session-pickup` (its complement), `autonomous-run`, `orchestrate`, and the `show-me-your-work` skill.
