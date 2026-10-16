# Visual parity

**Use it when.** A screen must match a reference exactly, such as two versions of a component or a styling-system migration.

**In plain words.** Pixel-exact means every pixel matches. The agent proves this with an image diff, which compares two screenshots and reports differing pixels. It does not judge by eye. The baseline (the screenshots of the current version) is the spec. The agent must not edit it or the harness to make a diff pass. If the baseline looks wrong, the agent stops and asks you.

**What it does.**
1. Establishes the baseline before any migration. This is a visual regression harness that screenshots the component across its states, plus the target when matching two implementations. No baseline means no parity claim.
2. States the anti-shortcut clauses. There are no harness changes, no baseline tampering, and no component restructuring to make a diff pass. A baseline that looks wrong means stop and ask.
3. Migrates one component at a time, with one owner per component in parallel worktrees. Shared primitives migrate first.
4. Verifies each component against its baseline with an image diff on the matching surface through the control skill. A nonzero diff is a fail. It investigates the pixel difference and runs `/loop` per component until the diff is zero.
5. Runs the Opening a PR playbook per component or per safe batch.

**What you get back.** The components migrated, the diff result for each, the baseline harness location, and what is left.

**Copy and adapt.**

```text
/poteto-mode <what looks wrong> in <place>. the <reference> is correct. repro and fix until it matches pixel for pixel.
```

Filled in:

```text
/poteto-mode the row spacing is too tall in the orders table when the compact flag is on. the second image is correct. repro and fix until it matches pixel for pixel.
```

```text
/poteto-mode migrate <components> to <new styling>. the result must match the original exactly, bugs included. image diff each component against a frozen baseline.
```

Filled in:

```text
/poteto-mode migrate the button and card components to the new styling system. the result must match the original exactly, bugs included. image diff each component against a frozen baseline.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `must match the original exactly, bugs included` | Keeps the migration from fixing things on the way (from the guide). |
| `the second image is correct` | Names the reference to match. |
| `repro and fix until it matches` | Asks for the loop until the diff is zero. |
| `image diff against a frozen baseline` | Names the verification the playbook expects. |

**Watch for.**
- A nonzero diff is a fail.
- The agent must not edit the baseline or harness. It stops and asks if the baseline looks wrong.
- Without a baseline there is no parity claim, and building it is the first step.

**Pairs with.** `multi-phase-plan` for a migration plan with visual checks, `feature` for new UI, and the control skill for screenshots.
