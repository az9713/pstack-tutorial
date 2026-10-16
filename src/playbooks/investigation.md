# Investigation

**Use it when.** You have a question about how something works, why it was built that way, or whether to pick option A or B, and you want an answer without any code change.

**In plain words.** An investigation is read-only. The agent reads the code and the history and writes a cited explanation. A cited explanation points at the files and facts that back each claim, so you can check them. The playbook uses the `how` skill to explain mechanics and the `why` skill to explain motivation. If your question is a choice between options, you get a recommendation with a trade-offs table instead.

**What it does.**
1. Routes the question through the `how` skill. For questions about motivation, it also routes through the `why` skill.
2. Writes one line for the throughput checkpoint, which reads `throughput checkpoint: n/a, read-only investigation`.
3. Writes the answer in the `how` shape. The sections are Overview, Key Concepts, How It Works, Where Things Live and Gotchas.
4. Writes a recommendation with a trade-offs table instead, if the question is a decision between alternatives.
5. Applies the `unslop` skill to the reply.
6. Opens no PR, runs no babysit, and skips `architect`. If the findings point to a code change, it hands back to you, and the change becomes a new Bug fix or Feature task.

**What you get back.** The investigation output itself. For an "are we sure?" question, the reply includes the agent's real judgment with reasons. The agent pushes back if your premise is wrong.

**Copy and adapt.**

```text
/poteto-mode investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.
```
Filled in:
```text
/poteto-mode investigate why the shop's order emails go out twice for some customers. give me what we know, what data you used, and your best hypotheses. don't change any code yet.
```

```text
/poteto-mode new task. figure out how <feature> works end to end and where it lives. don't change any code yet.
```
Filled in:
```text
/poteto-mode new task. figure out how the notes app saves a note from the editor to the database and where it lives. don't change any code yet.
```

```text
/poteto-mode should we use <option a> or <option b> for <decision>? don't change any code yet. are we sure? give me your real judgment.
```
Filled in:
```text
/poteto-mode should we use csv or json for the nightly export? don't change any code yet. are we sure? give me your real judgment.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `don't change any code yet` | Routes the task to Investigation and keeps it read-only. |
| `new task` | Tells `/poteto-mode` to match a playbook again instead of continuing the previous one. |
| `give me what we know, what data you used, and your best hypotheses` | Makes the agent separate its evidence from its guesses. |
| `are we sure?` | Asks for the agent's real judgment with reasons. |
| `why was it built this way` | Adds the `why` skill for questions about motivation. |

**Watch for.**
- The agent does not change code in this playbook. Start the fix as a new task.
- A mode that is already in the middle of a Feature can treat your question as the next feature step. Add `new task` and `don't change any code yet` to avoid this.
- The agent can push back if your question rests on a wrong premise. Read that part of the reply first.

**Pairs with.** `bug-fix` and `feature` for the change that follows, `prototype` when a question can be settled by trying it, and the `how` and `why` skills.
