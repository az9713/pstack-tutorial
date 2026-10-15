# Video: pstack across six stages

**Source.** "Pstack: How a Cursor Engineer Ships Code With AI", a YouTube video by Eric Tech. Eric describes himself as a former senior software engineer at Amazon and Microsoft and the founder of bookzero.ai. [Watch on YouTube](https://www.youtube.com/watch?v=4wBVuj2an8E). The video is about 15 minutes long.

Eric reviews pstack against two other skill sets, Matt Pocock's skills and Superpowers. He walks through pstack in the six stages of the software development life cycle: planning, design, build, testing, deploy, and maintain.

This tab is a summary of the auto-generated transcript, in our own words. The transcript has some mis-heard words. Where Eric's description differs from the pstack repo, this tab says so.

## Chapters

| Time | Chapter | What he covers |
|---|---|---|
| [0:00](https://www.youtube.com/watch?v=4wBVuj2an8E&t=0s) | What is pstack | Who made it, and what the video will cover. |
| [0:55](https://www.youtube.com/watch?v=4wBVuj2an8E&t=55s) | Planning skills | Learn the code first. Plan a big job. |
| [2:10](https://www.youtube.com/watch?v=4wBVuj2an8E&t=130s) | Design skills | Settle the code shape with several models. |
| [3:16](https://www.youtube.com/watch?v=4wBVuj2an8E&t=196s) | Build skills | TDD, TypeScript rules, cleaning the diff, no comments. |
| [5:33](https://www.youtube.com/watch?v=4wBVuj2an8E&t=333s) | Testing skills | Prove the app works, swarm, attack the diff. |
| [8:18](https://www.youtube.com/watch?v=4wBVuj2an8E&t=498s) | Deploy skills | An easy-to-review PR, then babysit it to merge. |
| [11:52](https://www.youtube.com/watch?v=4wBVuj2an8E&t=712s) | Extra skills | The router, catch-up and plain-talk skills. |
| [12:36](https://www.youtube.com/watch?v=4wBVuj2an8E&t=756s) | Principles and learnings | Why principles are skills, and which ones he will adopt. |

A sponsor segment runs from about 9:54 to 11:49. It is not about pstack.

## The six stages, mapped to this tutorial

| Stage | Eric's workflows | pstack skills he names | Where to read more |
|---|---|---|---|
| Planning | Learn the code first. Plan a big job. | `/how`, `/why`, `/teach`, `/figure-it-out`, `/show-me-your-work` | [Understand the code](./03-understand.md) |
| Design | Settle the code shape. | `/architect`, `/arena`, `/interrogate` | [Design the change](./04-design.md) |
| Build | Test first. Clean the diff. | `/tdd`, `/typescript-best-practices`, `/deslop`, `/no-comments` | [Build and clean](./05-build-and-clean.md) |
| Testing | Prove it works. Swarm. Attack the diff. | `/create-verification-skill`, `/maintain-verification-skill`, `/swarm`, `/interrogate` | [Verify and ship](./06-verify-and-ship.md) |
| Deploy | Easy-to-review PR. Babysit to merge. | Opening a PR and Babysit playbooks | [Verify and ship](./06-verify-and-ship.md#open-the-pr) |
| Maintain | Collect issues and cycle back to planning. | None, in Eric's view | [Run work while you sleep](./07-overnight.md) |

## What he says, stage by stage

### Planning

Eric says pstack's planning skills are aimed at **brownfield** work, meaning a project that already has code. He sees two workflows. The first is learning the code. `/how` tells you how it works, `/why` tells you why it works that way, and `/teach` joins the two. The second is planning a big job with `/figure-it-out`, and keeping a log of decisions with `/show-me-your-work`.

His own view is that pstack is not strong on planning, which matches the author's stance in the [README](../../README.md). For a new build from scratch, he prefers Matt Pocock's skills or Superpowers. For migrations and large changes to existing code, he finds pstack up to the job.

### Design

The workflow is "settle the code shape". `/architect` calls `/arena`, which sends the same brief to several models and agents. Eric stresses the contrast with other skill sets he reviewed, which rely on one model. pstack asks models such as Opus, GPT, and Grok to design separately, compares them, and combines the best parts into one report.

Eric says `/interrogate` judges and combines the designs. In the repo, a judge inside `/arena` scores the candidates, and `/interrogate` is for reviewing a diff. See [Design the change](./04-design.md).

### Build

- **`/tdd`.** Write the test first. Eric has compared the TDD skills from pstack, Matt Pocock, and Superpowers on his own skill map.
- **`/typescript-best-practices`.** Loads TypeScript rules. He ties it to the author's React background.
- **Cleaning the diff.** `/deslop` compares your branch to main and removes extra comments, needless `try`/`catch`, untyped variables, and deep nesting. Tests keep the behavior the same, and you get a one-to-three-sentence summary. `/deslop` ships in the `cursor-team-kit` plugin, not in pstack.
- **`/no-comments`.** Eric's explanation of why it exists is that an AI may trust a comment over the code. If a comment says a function returns A and the code returns B, the AI can follow the comment. Removing comments removes that noise.

### Testing

Eric calls these skills "really really interesting". This stage has three workflows.

1. **Prove the application works.** `/create-verification-skill` builds end-to-end checks. He separates it from `/tdd`. TDD writes unit or functional tests. This skill writes the whole flow. It sets up the environment, launches the app, diagnoses problems, drives real user behavior, collects evidence, and cleans up. It keeps one feature per folder, and it points you to the maintain skill.
2. **Swarm.** `/swarm` runs many agents, on models you choose, each on a small part. One report comes back.
3. **Attack the diff.** `/interrogate` has several models try to break your change, compared to main. A code-quality review layer pushes for simpler code. Eric compares this to the `ponytail` skill he reviewed earlier.

### Deploy

The skills make a PR easy to review, then **babysit** it. Babysit fixes merge conflicts, lists and handles review comments, and fixes CI failures. Eric notes that everyone has a PR style of their own, so read the pstack skill and adapt it. See [Open the PR](./06-verify-and-ship.md#open-the-pr) and the Babysit playbook.

### Maintain

Eric says pstack has no skill that collects issues from production and sends them back to planning. The repo does ship a dormant [benny automation pack](https://github.com/cursor/plugins/tree/main/pstack/automations/benny). It triages Slack issue reports, then reproduces and fixes confirmed bugs. It is not active until you set it up.

### Extra skills

- `/poteto-mode` as a **router**. When you do not know which skill to use, describe the problem and it picks. [`/poteto-help`](../../skills/poteto-help/SKILL.md) also answers this.
- Setup skills, such as `/setup-pstack`.
- **Catch-up and plain-talk skills.** Eric likes these. After you switch projects, they bring you back up to date. They are [`/recall`](../../skills/recall/SKILL.md), [`/ketchup`](../../skills/ketchup/SKILL.md), and [`/bro`](../../skills/bro/SKILL.md).
- Writing skills, and skills that improve pstack over time, such as `/reflect` and `/correct`.

### Principles and what he took from them

Eric asks why the principles are skills and not a system prompt. His answer is that a system prompt with every rule is a large file, and the model reads it on every message even when the rules do not apply. Separate skills with an index load a rule only when it is needed. This matches how `/poteto-mode` works. See [Steer with principle names](./08-principles.md).

He picked three principles to add to his own workflow.

- **Keep it small.** Close to the `ponytail` skill he already uses. This is the [Laziness Protocol](../../skills/principle-laziness-protocol/SKILL.md).
- **Attack the premise.** When an AI fixes a bug, the bug returns, and it fixes it again, the loop can run for a long time. This principle makes the AI stop and question its assumption first. See [Attack the Premise](../../skills/principle-attack-the-premise/SKILL.md).
- **Type-system discipline.** Reject impossible states. His example is a payment that is both paid and pending. See [Type System Discipline](../../skills/principle-type-system-discipline/SKILL.md).

## What a beginner can take from it

1. pstack covers the whole life of a change, not only coding. The stage table above is a good map.
2. The two most distinctive ideas are multi-model design and end-to-end verification.
3. You can adopt one skill or one principle at a time. Eric took three principles and left the rest.

Also read: [Article: verification is the first skill to build](tab:article) is the companion tab for the testing stage.
