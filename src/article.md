# Article: verification is the first skill to build

**Source.** "The Complete Guide to pstack Pt. 1", an X article by lauren ([@poteto](https://x.com/poteto)), the author of pstack. Posted 31 Aug 2026. [Read the original](https://x.com/poteto/status/2094457600259842065).

This tab is a summary in our own words. Numbers and results below are the author's own claims. We did not measure them.

## The claim

The author says the most important skill to own is a high-quality **verification skill**. They treat it as critical infrastructure, not as one skill among many. In their words, a good one multiplies a team's output by 100 to 1000 times, and it helps people who are not engineers too.

**Verification** means the agent can check its own work. It keeps going until the check passes. You are no longer the bottleneck.

This is the same idea as the [Prove It Works principle](../../skills/principle-prove-it-works/SKILL.md) and as Step 6 of [Start here](./00-start-here.md).

## Why volume matters

The author says they used to ignore how many PRs or lines of code a person landed. Since building pstack, they changed their mind. When quality holds or improves, volume matters.

The example is Grok Bot. The author says the team lands hundreds of PRs a day, and that pstack let them keep the code quality high while they refactored the foundations, added lints and checks, and built features. They call this role the **gardener**. A gardener watches the stream of PRs, notices repeated smells, and removes them.

## How to build a verification skill

1. Install pstack.
2. Run [`/create-verification-skill`](../../skills/create-verification-skill/SKILL.md).
3. Let the agent work. It reads your app, builds a small CLI, and writes a feature map.

The article adds a second route. It names a bot called Dr Eggbot that ships with pstack. The author says it teaches coding bots how to use the skill, and that you can ask it to create an engineer bot that runs `/create-verification-skill` and a daily `/maintain-verification-skill`.

### Your tech stack decides how easy this is

The author wants the agent to do what you would do by hand. Interact with the app, debug it, take performance traces, and read logs. A web or Electron app can use the Chrome DevTools Protocol (CDP). An iOS app can use the simulator. If your stack has no rich runtime, the author suggests that you ask the agent to build the tools. They go further. They say it can be worth choosing a different stack to make agent verification easier, because the harder an app is to debug and control, the harder it is to use agents on it.

## Make it reproducible with a small CLI

pstack has a principle named [Build the Lever](../../skills/principle-build-the-lever/SKILL.md). For a skill, it means that you give agents a tool and not only markdown. For verification, the tool is a small CLI that scripts how to drive and debug your app. Agents use fewer tokens, because they run one command and do not write a throwaway script to click a button. The skill also becomes repeatable and testable.

The article shows a made-up Electron app called Atlas with a CLI named `control-atlas.mjs`. These are the command groups it lists.

| Group | Example commands |
|---|---|
| Inspection | `info`, `snapshot`, `screenshot`, `components` |
| Navigation | `home`, `new-session`, `select-project`, `select-runtime`, `scroll` |
| Interaction | `send`, `click`, `click-xy`, `aria-click`, `type`, `press`, `eval`, `upload-image`, `add-context`, `feature-flag` |
| Performance | `trace`, `profile`, `record`, `perf-metrics`, `wait-settle` |
| Streaming | `console`, `network-log`, `network-summary` |
| Health and cleanup | `doctor`, `cleanup`, `watch --restart` |

The author asks you to spend time here first. Make the CLI good and free of errors before you do anything more advanced. Also prepare the development setup, since agents need it as much as you do. That means a seeded dev database, test users and auth, API calls against a test or staging environment, and one consistent way to bring the environment up.

### What makes a CLI good for agents

- The commands are easy to combine. The author points to John Ousterhout's idea of deep modules.
- Any command with destructive side effects has a `--dry-run` option.
- Subcommands reveal features gradually.
- Error messages say what the agent should do instead.
- `--help` text is rich.
- Output is machine-readable, such as JSON.

## Use cloud agents, not worktrees, to go parallel

Once the skill lands a few PRs, you will want more agents at once. The first idea is a git worktree for each agent. The author recommends against it. Worktrees use disk space and machine resources. Depending on repo size and machine power, they say you may reach about 10 agents in parallel.

The better route in the article is Cursor **cloud agents**. A cloud agent runs on Cursor's infrastructure on a real computer. It can install dependencies, run your app, record video and screenshots, and use the app like a person. Cursor helps an agent set up the cloud environment the first time, and then saves a snapshot, so later runs start fast. The author says a later post will cover running hundreds of subagents in the cloud.

This agrees with [Route work through `/poteto-mode`](./02-poteto-mode.md#give-parallel-work-its-own-machine), which says a cloud subagent is the cleanest isolation and a worktree is the local option.

## The Feature Map

As an app grows, an agent needs help to find features. The **Feature Map** is a searchable map of every feature. For each feature it records what the feature does and how a user reaches it.

- `/create-verification-skill` creates a `references/features` folder next to a `README.md`. The README is the map. It gives an overview and links to a page for each feature.
- A feature page has these sections. Sub-features. How to get to it, from the user's point of view. How to drive it with the CLI. Gotchas.
- The agent writes these pages for you by walking through your app.

The author calls the map "materialized memory". Their argument has three parts. Your code is the best record of the decisions your team made. A Feature Map is a smaller form of that record, made to save tokens. It is markdown inside a skill, so everyone who works in the repo shares it.

The worked example is in the repo [`create-verification-skill/references/feature-map-example`](../../skills/create-verification-skill/references/feature-map-example/README.md).

### Keep it true

Run [`/maintain-verification-skill`](../../skills/maintain-verification-skill/SKILL.md) at least once a day. Agents will often update the skill as they work, and the command catches what they miss. The author suggests treating the skill like production infrastructure. They even suggest an on-call rotation for it.

## How the author uses it

Start the prompt with `/poteto-mode`. In Cursor, press Option+Enter when you pick it, to pin it as a Custom Mode. This is the same step as in [Part 2 of Start here](./00-start-here.md#two-ways-to-start-a-skill).

**A new feature**

```text
/poteto-mode build <description of feature, any useful context>. use /control-app to verify your changes and show me a video and screenshots as proof
```

Here `/control-app` stands for the skill that `/create-verification-skill` made for your app. The generated name differs by app. This tutorial writes it as `/verify-<app>`.

**In Grok Bot.** The author tells the bot to spawn a cloud agent to do the work. The bot stays free and its context window stays clean. They think of their bots as coordinators that supervise cloud agents.

**Performance work.** First take a trace of the current state with the verification skill. Make one targeted fix. Then use the verification skill with [`/swarm`](../../skills/swarm/SKILL.md) to confirm the win over a large enough sample. A swarm of verifiers can also fuzz the app to catch regressions.

**Reproducing user reports.** Put the verification skill into a Grok Bot routine or a Cursor Automation. These run on a schedule or on an event. If user feedback flows into Slack, a bot can try to reproduce every report with a cloud agent. If the skill and the Feature Map are good enough, the author says you may let it auto-fix too. The repo's [benny automation pack](https://github.com/cursor/plugins/tree/main/pstack/automations/benny) is a ready example of this pattern.

## Links from the article

- A made-up example app with a verification skill: [poteto/verification-skill-example](https://github.com/poteto/verification-skill-example).
- The earlier post the author recommends, "Loops You Can Trust".
- The article says pstack also runs as a plugin in Grok Bot. This tutorial covers Cursor only.

## What to take from it

1. Build the verification skill first. Every later skill depends on it.
2. Put your effort into a small, reliable CLI and a true Feature Map.
3. Maintain the skill daily.
4. Parallelize on cloud agents when you can.

Next: [Verify and ship](./06-verify-and-ship.md) in this tutorial covers the same ground step by step.
