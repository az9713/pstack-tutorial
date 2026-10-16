# Feature

**Use it when.** You want new or changed behavior in your code, such as a new flag, a new page, or a new export option.

**In plain words.** The agent acts as the lead designer. It studies the code, explores designs, and then hands the actual code-writing to a subagent (a helper agent that works on a narrow job). It names the data shape first, such as a table or a state machine, so the helper does not invent structure on the fly. A review and a check on the real running surface come before anything ships. The playbook works this way so the agent that designs also reviews, which catches mistakes the writer would miss.

**What it does.**
1. Runs `how` over the part of the code the feature touches.
2. Runs `architect` to explore design options in parallel.
3. Writes a four-item "throughput checkpoint" as todo items. The items are blocking first steps, independent workstreams, shared mutable state, and the smallest safe decomposition. An item that does not apply stays on the list with `n/a: <reason>`.
4. Delegates the code to a subagent with a specific scope. The scope names the file paths, the data shape, and the success criteria. When several valid shapes exist, it uses the `arena` skill instead.
5. Verifies on the matching surface. A result of "inconclusive" or a check on the wrong surface is not a pass, and the agent flags it.
6. Rebases the work into small, ordered commits, using the `sequence-verifiable-units` principle skill.
7. Runs `interrogate` before shipping if the design is contested.
8. Runs the Opening a PR playbook.

**What you get back.** A reply with what the agent built, what it chose and why, the throughput checkpoint, and the open decisions. Design alternatives appear in tables.

**Copy and adapt.**

```text
/poteto-mode add <new behavior> to <where>. <what must stay the same>. verify <how you will check it> and show me the evidence.
```

Filled in:

```text
/poteto-mode add a --json flag to the export command. text output stays byte-identical. verify both forms against the sample project and show me the evidence.
```

```text
/poteto-mode build <feature> behind a feature flag. /architect it first and let me review before you build.
```

Filled in:

```text
/poteto-mode build a wishlist button on the product page behind a feature flag. /architect it first and let me review before you build.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `/architect it first` | Runs `architect` for parallel design exploration before the build. |
| `let me review before proceeding` | Stops after design so you can review (a pattern from the guide). |
| `verify both forms` or `show me the evidence` | Asks for a check on the real surface and proof in the reply. |
| `text output stays byte-identical` | States what must not change, so the agent can check it. |
| `/interrogate it before shipping` | Asks for `interrogate` on a design you expect to be contested. |

**Watch for.**
- The playbook delegates the code-writing. It has no skip-with-reason escape, even for a small diff.
- "Inconclusive" is not a pass. If the agent could not check on the real surface, it must say so.
- Code-coupled work, such as one feature or one migration, goes to a single owner. Parent-level fan-out suits independent artifacts only.

**Pairs with.** `refactoring` for structure-only work, `prototype` to settle a design first, and the `architect`, `arena`, and `interrogate` skills.
