# Refactoring

**Use it when.** You want to change how code is organized, such as a rename, an extract, a move, or a dedupe, without changing what it does.

**In plain words.** A refactor changes structure and keeps behavior. To prove that, the agent first records what the code does today. This record is a "pin", such as a characterization test (a test that captures current output, right or wrong) or a snapshot. Every later step must keep the pin green. The playbook also removes dead code before it adds anything, and it reverts a change that does not make the code easier to read.

**What it does.**
1. Pins the behavior first. It runs `how` over the subsystem, then writes a characterization test, snapshot, or equivalence harness. Type check and lint are not a pin.
2. Names the structure the code is missing, per `principle-model-the-domain`. The reshape must delete branches or invalid states, not add indirection.
3. Names the target shape. If the target crosses a function boundary, it runs `architect`.
4. Subtracts before adding. It deletes dead code, one-caller wrappers, and redundant validators first.
5. Moves in small steps that each keep the pin green. For API changes it migrates every caller and deletes the old API in the same wave. It spot-checks every rename against the real files and delegates mechanical edits to a subagent.
6. Proves behavior is unchanged on the real artifact. For larger reshapes it runs an equivalence check, such as a script that diffs old and new output.
7. Confirms the change lowers reader load. If it does not, the agent reverts it.
8. Rebases into small ordered commits (subtraction, then reshape, then cleanup) and runs the Opening a PR playbook.

**What you get back.** The structure that changed, the pin it held against, the equivalence proof, the reader-load change, and what shipped or got reverted. The change adds no new behavior.

**Copy and adapt.**

```text
/poteto-mode move <code> into <new place>, zero behavior change. record the current output first and prove it's unchanged after.
```

Filled in:

```text
/poteto-mode move the csv parsing in the import script into one module, zero behavior change. record the current output first and prove it's unchanged after.
```

```text
/poteto-mode refactor <area> so <goal>. behavior must stay identical. delete dead code first and show me the before and after diff of outputs.
```

Filled in:

```text
/poteto-mode refactor the cart code so the price rules live in one table. behavior must stay identical. delete dead code first and show me the before and after diff of outputs.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `zero behavior change` | States the contract the pin must hold. |
| `record the current output first` | Asks for the pin before structure moves. |
| `prove it's unchanged after` | Asks for the equivalence proof on the real artifact. |
| `delete dead code first` | Matches the subtract-before-add step. |

**Watch for.**
- If cleanup reveals a missing feature or a real bug, the playbook splits it out. The structural change ships first against the pinned contract.
- A redesign is allowed, but the agent names it and routes it to `feature`.
- Large or cross-cutting structural work belongs to the `figure-it-out` skill, not this playbook.
- A cleanup that does not lower reader load gets reverted.

**Pairs with.** `feature` for new behavior, the bug fix playbook for defects, `figure-it-out` for large moves, and the `how` and `architect` skills.
