# Prototype

**Use it when.** You are unsure which design, layout, or behavior to pick and want a cheap throwaway sketch to decide.

**In plain words.** A prototype is a quick model built only to answer one question. Speed matters more than polish, and the code is thrown away. The playbook asks the agent to scope the decision first, because no decision means no prototype. For a visual choice it builds the options behind one switcher and takes screenshots. For a behavior or timing choice it builds the smallest script and watches the result.

**What it does.**
1. Scopes the decision the prototype exists to make. With no decision, it routes to `feature`.
2. Gathers references when the design space is open. It searches prior art and summarizes a moodboard, and you pick directions before it builds. It skips this when the direction is set.
3. Builds throwaway code in an isolated scratch directory. Visual work uses vanilla HTML, CSS, and JS or the lightest stack that renders it. Behavior work uses the smallest script. It adds no production framework, no tests, and no abstractions.
4. Puts alternatives behind one switcher, with each variant labeled.
5. Verifies on the matching surface. For visual work it screenshots each variant. For behavior or timing it logs, prints, or watches the output.
6. Presents alternatives, tradeoffs, and a recommendation, then hands the chosen direction to `feature` (or `architect` for the shape).

**What you get back.** The variants explored, the evidence (screenshots, or the observed output or timing), tradeoffs, a recommendation, and the scratch path. The reply says plainly that the prototype is throwaway.

**Copy and adapt.**

```text
/poteto-mode prototype a few options for <ui piece>. put them behind a switcher and send me screenshots of each.
```

Filled in:

```text
/poteto-mode prototype a few options for the settings page layout. put them behind a switcher and send me screenshots of each.
```

```text
/poteto-mode build two prototypes of <thing> so we can compare. spawn an agent for each. recommend one.
```

Filled in:

```text
/poteto-mode build two prototypes of the search results list so we can compare. spawn an agent for each. recommend one.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `prototype`, `mock it up`, `try this layout`, `sketch it to decide` | Routing phrases for this playbook. |
| `put them behind a switcher` | Matches the one-switcher step. |
| `take screenshots or videos for me to compare` | Asks for visual evidence per variant. |
| `spawn an agent for each` | Builds each option in its own agent (an example from the README). |

**Watch for.**
- The prototype is throwaway. Do not ship it.
- This playbook inverts the usual "smallest change" and verification bar. Code quality does not matter here.
- The real build follows the `feature` playbook.

**Pairs with.** `feature` for the real build, `multi-phase-plan` (which runs this playbook for open questions), and the `architect` skill.
