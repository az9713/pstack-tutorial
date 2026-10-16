# Runtime Forensics

**Use it when.** Something is going wrong in a running program, such as a memory leak, a CPU spin while idle, or a visual glitch, and you want the cause before any fix.

**In plain words.** Forensics means finding the cause from evidence. Here the agent attaches to the live process and measures it, instead of guessing from the source. It captures a real artifact, such as a CPU profile or a heap snapshot, and reduces it to the one finding that explains the symptom. Then it tests that finding on the running process before it believes it. The deliverable is a diagnosis, not a fix.

**What it does.**
1. Captures the live signal on the matching surface through the control skill. A spinning process gets a CPU profile, a leak gets a heap snapshot, and a visual glitch gets a CDP trace. CDP is the Chrome DevTools Protocol.
2. Reduces the artifact to the smoking gun. Examples are the function on the hot path, the retainer chain from the leaked object to a GC root, or the loop that fires without input.
3. Parses large artifacts in a subagent, following the `guard-the-context-window` principle skill. The main thread keeps only the reduced finding.
4. Proves the mechanism. It injects instrumentation through CDP eval on the running process, or hotfixes the live code without reloading, to confirm the hypothesis cheaply.
5. Maps the finding back to source, meaning the file, the symbol and the line that allocates or schedules.
6. Writes one line for the throughput checkpoint, which reads `throughput checkpoint: n/a, read-only forensics`.

**What you get back.** The signal captured, the reduced finding, how the agent proved the mechanism, the source location and the artifact paths. There is no fix unless you ask for one.

**Copy and adapt.**

```text
/poteto-mode <app> uses <symptom> when <situation>. capture a live profile or snapshot, find the cause, prove the mechanism, and tell me the source line. no fix yet.
```
Filled in:
```text
/poteto-mode the web shop admin page uses 100% cpu when it is open and nobody touches it. capture a live profile, find the cause, prove the mechanism, and tell me the source line. no fix yet.
```

```text
/poteto-mode memory in <app> keeps growing after <action>. take heap snapshots, find what holds the leaked objects, and show me the file and line that allocates them. diagnosis only.
```
Filled in:
```text
/poteto-mode memory in the notes app keeps growing after i open and close a note 50 times. take heap snapshots, find what holds the leaked objects, and show me the file and line that allocates them. diagnosis only.
```

```text
/poteto-mode <element> flickers when <action>. trace it live and tell me what causes it. don't fix it yet.
```
Filled in:
```text
/poteto-mode the login form button flickers when i type in the password field. trace it live and tell me what causes it. don't fix it yet.
```

**Make it yours.**

| Add this phrase | Effect |
|---|---|
| `no fix yet` | Keeps the deliverable a diagnosis, which is the default for this playbook. |
| `capture a live profile` | Names the signal to capture for a spinning process. |
| `take heap snapshots` | Names the signal to capture for a leak. |
| `prove the mechanism` | Asks for the live test of the hypothesis from step 4. |
| `tell me the source line` | Asks for the file, symbol and line mapping from step 5. |

**Watch for.**
- This playbook instruments a live process. If you already have a saved capture, use Trace forensics.
- It gives no fix unless you ask. Once the cause is known, hand back to Bug fix or Perf issue.
- A finding the agent has not proved on the running process is a hypothesis. Check that the reply says how the mechanism was proved.

**Pairs with.** `trace-forensics` for a saved capture, `bug-fix` and `perf-issue` for the fix that follows, and the `guard-the-context-window` principle skill.
