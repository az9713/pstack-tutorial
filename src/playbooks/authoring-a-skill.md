# Authoring or modifying a skill

**Use it when.** You want to write a new `SKILL.md` or edit an existing one.

**In plain words.** A skill is a folder with a `SKILL.md` file that an agent loads for a kind of task. Agent-facing prose has a high bar, because an unhelpful sentence becomes an instruction a future agent follows. So the playbook routes the work through Cursor's built-in `create-skill` skill and then validates the result. It also tells the agent to delete first and keep only prose that changes a decision.

**What it does.**
1. Uses the `create-skill` skill.
2. Validates the skill. The frontmatter has `name` and `description`, referenced files exist, and cross-skill links resolve.
3. Adds test cases if the skill is structural. It skips them if the skill is subjective.
4. Runs the Opening a PR playbook.

The playbook also sets writing rules. When in doubt, delete. Tell the agent to do the thing and skip the reason, unless the rule is confusing without one. Point at structural sources and delegate to other skills by path instead of restating. If you keep repeating a workflow that no skill captures, the playbook says to propose a new skill.

**What you get back.** A summary of the skill, key design decisions, and validation notes.

**Copy and adapt.**

```text
/poteto-mode write a skill for <workflow>
```

Filled in:

```text
/poteto-mode write a skill for checking that every new database migration has a rollback step
```

```text
/poteto-mode update the <name> skill so it <new behavior>, and eval the change.
```

Filled in:

```text
/poteto-mode update the review skill so it flags missing migrations, and eval the change.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `and eval the change` | Adds the `eval` playbook to test the edit blind (from the guide). |
| `write a skill for ...` | Routes to this playbook (the guide's example wording). |
| `update the <name> skill` | Routes an edit of an existing skill here. |

**Watch for.**
- Do not write `SKILL.md` freehand. Route it here so validation and review happen.
- A skill that must drive your app and prove behavior is a verification skill. The guide points to `/create-verification-skill` and `/maintain-verification-skill` for that case.
- Do not edit a skill mid-task because it misbehaves. The guide advises fixing it in its own PR.

**Pairs with.** `eval` to test a skill change blind, the `create-skill` skill, and the Opening a PR playbook.
