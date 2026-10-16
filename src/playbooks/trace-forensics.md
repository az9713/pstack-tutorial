# Trace Forensics

**Use it when.** You already have a captured profiling file, such as a cpuprofile, a trace, a spindump or a heap snapshot, and you want to know what it says about the cause.

**In plain words.** A trace is a recorded timeline of a program run. In this playbook the capture is fixed data, so the agent reads it and does not run the program again. It loads the file into a sqlite database, which is a small file-based database you can query with SQL. Then it asks questions of the data until the cause shows up. The deliverable is a diagnosis, not a fix.

**What it does.**
1. Identifies the format and loads it with the right tool. A parser for cpuprofile and `.json.gz`, a text editor for a spindump, heap tooling for a heapsnapshot.
2. Parses large artifacts in a subagent, following the `principle-guard-the-context-window` skill. The main thread keeps only the reduced finding.
3. Dumps the trace or heap snapshot into sqlite, with one row per sample, frame or node. It gets to a queryable shape before it reads.
4. Narrows to the cause. It queries for the frames that hold the most time and walks the call tree to the hot path. For a leak, it follows the retainer chain to a GC root. For a spindump, it finds the thread stuck on-CPU or blocked, and its wait reason.
5. Attributes the hot frame to a file, symbol and line through the artifact's own symbols. A frame with no source mapping is not a diagnosis yet. The agent resolves the symbols or says the artifact does not carry them.
6. Diffs a paired before and after capture if one exists. Without a pair, it marks the finding as the strongest hypothesis the artifact supports, not a confirmed cause.
7. Hands back a cited diagnosis with the throughput checkpoint line `throughput checkpoint: n/a, read-only forensics`.

**What you get back.** The artifact and its format, the reduced finding, the source location, the artifact paths, and whether a paired capture confirmed it.

**Copy and adapt.**

```text
/poteto-mode here's a cpuprofile from <slow thing>. tell me where the time goes and which source lines own it. no fix yet.
```
Filled in:
```text
/poteto-mode here's a cpuprofile from the slow csv export. tell me where the time goes and which source lines own it. no fix yet.
```

```text
/poteto-mode here's a heap snapshot taken after <action>. find what is leaking, show the retainer chain, and map it to source. diagnosis only.
```
Filled in:
```text
/poteto-mode here's a heap snapshot taken after opening 50 product pages in the web shop. find what is leaking, show the retainer chain, and map it to source. diagnosis only.
```

```text
/poteto-mode here are two traces of <operation>, one before the change and one after. diff them and tell me what got slower. no fix yet.
```
Filled in:
```text
/poteto-mode here are two traces of the checkout page load, one before the change and one after. diff them and tell me what got slower. no fix yet.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `no fix yet` | Keeps the deliverable a diagnosis, which is the default for this playbook. |
| `which source lines own it` | Asks for the file, symbol and line attribution from step 5. |
| `show the retainer chain` | Asks for the path from a leaked object to a GC root. |
| `here are two traces` | Gives the agent a paired capture to diff, so the finding can be confirmed. |

**Watch for.**
- The agent does not re-run the program. If the capture does not exist yet, use Runtime forensics.
- Without a paired capture, the finding is labeled a hypothesis. Read the end of the reply for that label.
- If the artifact has no symbols, the agent says so. It does not guess a source line.

**Pairs with.** `runtime-forensics` when no capture exists, `bug-fix` and `perf-issue` for the fix that follows, and the `principle-guard-the-context-window` skill.
