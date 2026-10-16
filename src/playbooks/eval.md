# Eval

**Use it when.** You changed a skill, a prompt, or a structure and want to know whether agents behave better with the change.

**In plain words.** An agent that knows it is being tested behaves differently. So this playbook hides the test. Candidate agents get an organic-looking task in plainly named directories. They never see words like "eval" or "candidate", and they never learn other candidates exist. One judge scores all outputs under neutral labels. The agent then checks which files each candidate really read, instead of trusting what the candidate says.

**What it does.**
1. Frames the test. It states the variant under test and what success looks like, and writes a rubric of 3 to 6 concrete criteria for the judge only.
2. Sets up sanitized environments. Each candidate gets its own working directory with the variant in place.
3. Authors one organic prompt, what a user would type, with no hint of what is measured.
4. Spawns N parallel candidates on different models, per Phase B of the `arena` skill, each in its own directory with the same prompt.
5. Spawns one blinded judge on a different model family, per Phase C of the `arena` skill. The judge sees outputs by label and the rubric, never a model name.
6. Verifies the chain from transcripts, not self-report. It reads each candidate's transcript under the workspace's `agent-transcripts/` directory.
7. Reads every candidate output end to end, compares it to the judge's verdict, and synthesizes.

**What you get back.** The variant under test, the rubric, per-candidate notes, the judge's verdict, the agent's synthesis, and a recommendation on whether to promote the variant.

**Copy and adapt.**

```text
/poteto-mode run the eval playbook on <skill or prompt change>. same task for both variants, candidates stay blind.
```

Filled in:

```text
/poteto-mode run the eval playbook on this change to the commit-message skill. same task for both variants, candidates stay blind.
```

```text
/poteto-mode update <skill> so it <new behavior>, and eval the change. tell me whether to promote it.
```

Filled in:

```text
/poteto-mode update the review skill so it flags missing migrations, and eval the change. tell me whether to promote it.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `run the eval playbook` | Routes to this playbook. |
| `same task for both variants` | Matches the single-prompt, single-judge comparison. |
| `candidates stay blind` | Matches the blinding rules. |
| `and eval the change` | Tests a skill edit in the same task (from the guide). |
| `tell me whether to promote it` | Matches the recommendation the reply ends with. |

**Watch for.**
- Blinding rules are non-negotiable. The words `eval`, `test`, `judge`, `experiment`, `rubric`, `score`, `compare`, `benchmark`, `candidate`, and `arena` stay out of anything the candidate sees.
- Do not ask candidates to list which skills or files they used.
- If you disagree with the judge, the guide advises suspecting the rubric before your own judgment.
- The agent must not glob across `~/.cursor/projects/*/`. That reads private chats from other projects.

**Pairs with.** `authoring-a-skill`, the `arena` skill, and `hillclimb` for sustained metric work.
