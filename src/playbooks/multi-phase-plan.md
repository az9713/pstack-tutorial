# Multi-phase or multi-PR plan

**Use it when.** The work spans several phases or stacked pull requests, and you want a written plan before anyone builds.

**In plain words.** This playbook produces a plan file and does not write the code. The plan is a checklist. An "owner" agent runs it box by box, and you audit from the evidence each box names. Each pull request (PR) gets its own section with its own proof. The playbook applies one verification rule. Tests alone are not enough, and each PR needs its unit, live, and perf boxes all checked.

**What it does.**
1. Skips the plan if the change is one or two files with an obvious approach. It says so and stops.
2. Settles open questions by running the `prototype` playbook for each. It keeps the branch, SHA, and screenshots for Appendix A. It asks you only about product or preference calls no run can settle.
3. Explores in subagents. Each returns file pointers, conventions, test commands, and entry points, not inlined dumps.
4. Copies the plan skeleton into the plan file and fills every placeholder. One section per PR. It names the execution playbook, `autopilot-full` or `autopilot-stack`, in "How to read this".
5. Writes under `/technical-writing`, then `/unslop`.
6. Runs `node pstack/skills/poteto-mode/scripts/check-plan.mjs <plan.md>` and fixes every line it prints.
7. Hands back the plan path and the script's output, then stops. Execution starts only on your explicit go.

**What you get back.** The plan path, the PR ids with dependencies and the review-gated set, what the prototypes proved and what stays unproven, and the check script's output.

**Copy and adapt.**

```text
/poteto-mode turn this design into a plan. small verifiable PRs, each with its own verification steps.
```

Filled in:

```text
/poteto-mode turn the saved-carts design into a plan. small verifiable PRs, each with its own verification steps.
```

```text
/poteto-mode plan the migration of <library> to <target>. small verifiable PRs, each with visual regression checks. the result must match the original exactly, bugs included.
```

Filled in:

```text
/poteto-mode plan the migration of our button library to the new styling system. small verifiable PRs, each with visual regression checks. the result must match the original exactly, bugs included.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `small verifiable PRs` | Matches one section per PR with its own evidence. |
| `each with its own verification steps` | Matches the unit, live, and perf verification blocks. |
| `answer open questions with prototypes` | Matches step 2 (the guide uses this wording). |
| `bugs included` | Keeps a migration from fixing things on the way (from the guide). |
| `show me the dependency graph first` | A README example prompt for multi-phase work. |

**Watch for.**
- The plan is the deliverable. The playbook does not implement it.
- A PR that changes an interaction is review-gated. You review it in chat with screenshots and a video before merge.
- A surface with no control skill is recorded as a risk in Appendix C.
- The guide says a plan can live in the repo while the work runs. A good habit is to delete it when the work lands.

**Pairs with.** `prototype`, `autopilot-full`, `autopilot-stack`, `orchestrate`, and `visual-parity` for migrations.
