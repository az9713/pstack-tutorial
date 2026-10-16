# Playbooks: copy, adapt, paste

A **playbook** is a written list of steps for one kind of job. pstack has 23 of them. You do not call a playbook by name. You type `/poteto-mode` and describe the job. `/poteto-mode` reads your words, picks the playbook that fits, copies its steps into a todo list, and works through them.

This page is a reference for all 23. Each page has the same parts, so you can find what you need fast.

| Part | What it gives you |
|---|---|
| **Use it when** | One sentence to match the playbook to your situation. |
| **In plain words** | An explanation of the idea, with jargon defined. |
| **What it does** | The steps the playbook follows, in order. |
| **What you get back** | What the final reply contains. |
| **Copy and adapt** | Prompts with `<placeholders>`, each followed by a filled-in example. |
| **Make it yours** | Short phrases you can add to change what the agent does. |
| **Watch for** | Limits, stop points, and common mistakes. |
| **Pairs with** | The playbooks and skills that work well next to it. |

Every code block has a **Copy** button.

## How to use a prompt from this page

1. Pick the playbook that matches your job. Use the table below.
2. Copy a prompt from its **Copy and adapt** section.
3. Replace each `<placeholder>` with your own words.
4. Keep the phrases that name the job, such as "repro first" or "don't change any code yet". The router uses them to pick the playbook.
5. Paste it into a Cursor chat.

The filled-in examples show the level of detail that works. A prompt does not need to be long.

Some playbooks have no published trigger phrase. For those, the prompts use wording we chose from the playbook text. If `/poteto-mode` picks the wrong playbook, name the one you want in the prompt, for example "use the babysit playbook".

## What a good prompt carries

A good prompt has up to five parts. Each part fits in one sentence.

| Part | Example |
|---|---|
| The goal | "the export drops its last row" |
| The done check | "done means the 60k-row fixture exports every row" |
| The proof | "show me the row counts before and after" |
| What you know | "failing job id is 4812" |
| The real constraints | "repro first", "don't change any code yet", "let me review before you proceed" |

Do not list steps or skills in your prompt. The playbook already holds them in the right order.

## Which playbook do I need?

| You want to | Playbook |
|---|---|
| Ask how something works, or why it was built that way | [Investigation](tab:investigation) |
| Find the cause of a live symptom such as a leak or a CPU spin | [Runtime forensics](tab:runtime-forensics) |
| Read a profile or trace file you already captured | [Trace forensics](tab:trace-forensics) |
| Fix a defect | [Bug fix](tab:bug-fix) |
| Make something faster | [Perf issue](tab:perf-issue) |
| Push one number toward a target over many tries | [Hillclimb](tab:hillclimb) |
| Add or change behavior | [Feature](tab:feature) |
| Restructure code and keep behavior the same | [Refactoring](tab:refactoring) |
| Compare design options by building throwaway versions | [Prototype](tab:prototype) |
| Make a UI match a reference exactly | [Visual parity](tab:visual-parity) |
| Plan work that spans several PRs | [Multi-phase plan](tab:multi-phase-plan) |
| Write or edit a skill | [Authoring a skill](tab:authoring-a-skill) |
| Test whether a skill or prompt change helps | [Eval](tab:eval) |
| Open a PR | [Opening a PR](tab:opening-a-pr) |
| Get a PR through conflicts, review, and CI | [Babysit](tab:babysit) |
| Land a green stack of PRs | [Shipping](tab:shipping) |
| Build and verify a stack for you to review and land | [Autopilot: stack](tab:autopilot-stack) |
| Run independent PRs all the way to merged | [Autopilot: full](tab:autopilot-full) |
| Drive one long task to a finish line without stopping | [Autonomous run](tab:autonomous-run) |
| Run a standing project across days and many PRs | [Orchestrate](tab:orchestrate) |
| Take over work another agent left in flight | [Session pickup](tab:session-pickup) |
| Stop work safely so you can resume later | [Pause safely](tab:pause-safely) |
| Free disk space from old worktrees | [Worktree cleanup](tab:worktree-cleanup) |

No row fits? Type `/poteto-mode` with your task anyway. When no playbook matches, it uses `/figure-it-out` to design one for the job.

## Three habits that make every playbook work better

- **Say "new task" when you change subject.** This tells `/poteto-mode` to choose a fresh playbook instead of continuing the last one.
- **Keep the mode on.** Pick `/poteto-mode` from the `/` menu and press Option+Enter (Mac) or Alt+Enter (Windows). It becomes a Custom Mode that stays in context on every turn. Then short follow-ups such as "continue" are enough.
- **Ask for evidence you can inspect.** A video, a screenshot, a command output, or a before-and-after number. A reply that says "done" without evidence is a warning sign.

New to all of this? Start with the [tutorial](index.html).
