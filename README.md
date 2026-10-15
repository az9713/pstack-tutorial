# pstack tutorial

A single-page, tabbed tutorial for the **pstack** plugin for Cursor. It starts from zero. You learn the words of coding agents and plugins first, then the words of pstack, then run a first task. Two extra tabs summarize an article by pstack's author and a video review by Eric Tech.

**Read it live: https://az9713.github.io/pstack-tutorial/**

## What is in the page

Fourteen tabs.

| Tab | Content |
|---|---|
| Overview | The pstack README. |
| Start here | A 20-minute onboarding for people who have never used Cursor or a coding agent. |
| 1 to 10 | The ten pstack guide pages. Setup, `/poteto-mode`, understand, design, build and clean, verify and ship, overnight runs, principles, make it yours, recipes and pitfalls. |
| Article: Verification | A summary of "The Complete Guide to pstack Pt. 1". Verification skill, agent-friendly CLI, cloud agents against worktrees, the Feature Map. |
| Video: Six stages | A summary of Eric's video. pstack mapped onto six stages of the software life cycle, with chapter timestamps. |

Links between tabs work. Links to skills open the file on GitHub. The page is one file, `index.html`, with the images embedded.

## Sources

| Source | What it is | Used for |
|---|---|---|
| [The Complete Guide to pstack Pt. 1](https://x.com/poteto/status/2094457600259842065) | An X article by lauren ([@poteto](https://x.com/poteto)), posted 31 Aug 2026. | The "Article: Verification" tab. |
| ["Pstack: How a Cursor Engineer Ships Code With AI"](https://www.youtube.com/watch?v=4wBVuj2an8E) | A YouTube review of pstack across six stages by Eric Tech, about 15 minutes. | The "Video: Six stages" tab. |
| [cursor/plugins, pstack folder](https://github.com/cursor/plugins/tree/main/pstack) | The plugin, its skills, and its guide. | The Overview, Start here, and 1 to 10 tabs. |

The two summaries are written in our own words from the saved X page and the video's auto-generated transcript. Figures in the article, such as PR counts and productivity multiples, are the author's claims. We did not measure them. Where Eric's description differs from the pstack repo, the video tab says so.

## Credit and license

pstack and its guide come from the cursor/plugins repo and are MIT licensed, copyright Lauren Tan. This repo repackages that text into one page, adds the "Start here" tab, and adds the two summary tabs. It keeps the same MIT license. See `LICENSE`.
