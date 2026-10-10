# Talk script: "Sandboxes and Remote Desktops for AI Agents" (~35 min)

25 slides, 34:30 of planned speaking time including Q&A. The HTML deck is in [`slides/index.html`](slides/index.html). Its speaker notes are built from this file, so edit the notes here first.

**Facts policy.** Every fact comes from [`research.md`](research.md), [`comparison.md`](comparison.md), [`verification-notes.md`](verification-notes.md) (it wins when it disagrees with older text) and [`workshop-plan.md`](workshop-plan.md). Markers follow comparison.md: ✅ verified against a primary source on 2026-10-10, ⚠️ vendor or secondary source only, ❓ not verified. Say ⚠️/❓ items out loud as claims, not as facts.

**Presenter keys (deck):** → / Space / PageDown next, ← / PageUp back, Home / End, `N` notes overlay, `S` speaker window (notes, next slide, timer), `O` overview, `F` fullscreen.

| # | Slide | Time | Ends at |
|---|---|---|---|
| 1 | Sandboxes and Remote Desktops for AI Agents | 0:30 | 0:30 |
| 2 | The agent deleted production, then said rollback was impossible | 1:30 | 2:00 |
| 3 | Prompt injection turns your agent into someone else's shell | 1:30 | 3:30 |
| 4 | Agent threat model | 1:30 | 5:00 |
| 5 | The lethal trifecta | 1:30 | 6:30 |
| 6 | Why agents want sandboxes anyway | 2:00 | 8:30 |
| 7 | Set up online, run offline | 1:15 | 9:45 |
| 8 | The isolation ladder | 1:30 | 11:15 |
| 9 | Process sandboxes and containers | 1:30 | 12:45 |
| 10 | gVisor and microVMs | 1:30 | 14:15 |
| 11 | Full VMs, WASM and V8 isolates | 1:30 | 15:45 |
| 12 | A desktop for an agent: the stack (our ex3) | 1:30 | 17:15 |
| 13 | The screenshot → action loop | 1:30 | 18:45 |
| 14 | Humans in the loop, browser clouds, native APIs | 1:30 | 20:15 |
| 15 | Provider landscape | 1:30 | 21:45 |
| 16 | Billing and cold start: read the fine print | 1:30 | 23:15 |
| 17 | Self-host vs managed, and how known agents do it | 1:15 | 24:30 |
| 18 | How to choose | 1:30 | 26:00 |
| 19 | Demo plan and fallbacks | 0:45 | 26:45 |
| 20 | Tool loop with a locked-down sandbox (ex2) | 1:30 | 28:15 |
| 21 | Computer use on our own desktop (ex4) | 1:30 | 29:45 |
| 22 | What free models taught us | 1:00 | 30:45 |
| 23 | Production checklist | 1:30 | 32:15 |
| 24 | Takeaways | 0:45 | 33:00 |
| 25 | Questions? | 1:30 | 34:30 |

---

## Slide 1 — Sandboxes and Remote Desktops for AI Agents
**Timing:** 0:30 (0:00–0:30)

**On slide:**
- Title: Sandboxes and Remote Desktops for AI Agents
- Subtitle: Isolation, desktops and a live demo with free models
- Anton Vusatyi · R&D · October 2026
- Repo: github.com/vusatui/rnd-research → sandboxes-and-remote-desktops

**Speaker notes:**
Hi, I'm Anton. For the next half hour: why AI agents need a sandbox, what isolation options exist from a simple process jail up to full VMs, how you give an agent its own screen, which providers sell this, and then a live demo with free models. Everything I show is in the public repo on the slide, with sources. Facts were checked on October 10, 2026. When something is only a vendor claim, I will say so.

## Slide 2 — The agent deleted production, then said rollback was impossible
**Timing:** 1:30 (0:30–2:00)

**On slide:**
- Replit, around 2025-07-18, Jason Lemkin's (SaaStr) project, during a code freeze
- The agent deleted a live database: 1,206 executives and 1,196+ companies (figures from Lemkin and the agent itself)
- The agent said a rollback was impossible. **The rollback worked and the data was restored.**
- Replit's CEO apologized and promised dev/prod DB separation and a planning-only mode
- Moral: infrastructure limits the blast radius, not the prompt. Don't take the agent's word for the state of the system.
- Sources: The Register, Business Insider, VAID-2025-0020

**Speaker notes:**
Let's start with a story. July 2025, around the 18th. Jason Lemkin of SaaStr is building an app with Replit's agent. The project is in a code freeze. The agent deletes the live database anyway. According to Lemkin, and to the agent's own account, that is data on 1,206 executives and more than 1,196 companies. Then it gets worse: the agent says a rollback is impossible. That was false. The rollback worked and the data came back. Replit's CEO apologized and promised to separate dev and prod databases and to add a planning-only mode.

Two lessons. First, nothing in the prompt stopped this. What saved the data was infrastructure: a rollback that existed outside the agent's control. Second, the agent's report about the state of the system was wrong. Never take the agent's word for it. Check with tools the agent cannot influence.

**Sources:** [The Register](https://www.theregister.com/software/2025/07/21/vibe-coding-service-replit-deleted-production-database/719783), [Business Insider](https://www.businessinsider.com/replit-ceo-apologizes-ai-coding-tool-delete-company-database-2025-7), [VAID-2025-0020](https://vaiddb.org/incident/VAID-2025-0020)

## Slide 3 — Prompt injection turns your agent into someone else's shell
**Timing:** 1:30 (2:00–3:30)

**On slide:**
- HiddenLayer (2025-07-31): a hidden HTML comment in a README → Cursor in Auto-Run greps for keys and sends them out with curl; denylist bypassed via `$()`. Second chain without Auto-Run: read_file + create_diagram (Mermaid image) exfiltrates an SSH key. Fixed in Cursor 1.3.
- "Your AI, My Shell" (arXiv 2509.22040): 314 payloads, 70 MITRE ATT&CK techniques in rule files, Cursor and Copilot; attack success 41–84%. Turning off the terminal doesn't help: the agent writes `os.system()` into the code (88% of cases).
- Not prompt injection, same lesson: CVE-2025-65099 (Claude Code < 1.0.39, CVSS 7.7, Yarn code ran before the folder-trust dialog), CVE-2025-62222 (VS Code Copilot Chat, command injection, CVSS 8.8)
- **The prompt is not a security boundary.**

**Speaker notes:**
That was the agent's own mistake. Now attacks. HiddenLayer, July 2025: they hid an HTML comment in a README. Cursor in Auto-Run mode read it, found keys with ripgrep and sent them out with curl. The command denylist did not help, because the payload wrapped the command in dollar-parentheses. A second chain worked even without Auto-Run: read a file, then "create a diagram", where the Mermaid image URL carried an SSH key. Cursor fixed it in 1.3.

The academic version is "Your AI, My Shell", arXiv 2509.22040. 314 payloads covering 70 MITRE ATT&CK techniques, planted in rule files, against Cursor and Copilot. Attack success between 41 and 84 percent. And when they disabled the terminal tool, the agent simply wrote os.system into the code it generated, in 88 percent of cases.

Two CVEs on the slide are a different class. They are not prompt injection: in Claude Code before 1.0.39, Yarn plugins from an untrusted repo ran before the trust dialog; in Copilot Chat it was a command injection. Different bug, same lesson: the prompt is not a security boundary. You need a boundary the model cannot talk its way through.

**Sources:** [HiddenLayer](https://www.hiddenlayer.com/research/how-hidden-prompt-injections-can-hijack-ai-code-assistants-like-cursor), [arXiv 2509.22040](https://arxiv.org/abs/2509.22040), [CVE-2025-65099](https://nvd.nist.gov/vuln/detail/CVE-2025-65099), [CVE-2025-62222](https://nvd.nist.gov/vuln/detail/CVE-2025-62222)

## Slide 4 — Agent threat model
**Timing:** 1:30 (3:30–5:00)

**On slide:**
- Diagram: untrusted input (READMEs, rule files, web pages, tool output) → LLM → tools (shell, files, browser, network) → side effects
- The sandbox boundary wraps the tools, not the model
- What we protect: the host, secrets, prod, the network, money

**Speaker notes:**
Here is the threat model in one picture. Untrusted input comes in: a README, a rule file, a web page, even the output of the agent's own previous command. The LLM mixes it with your instructions, and it cannot reliably tell which is which. Then it calls tools: a shell, the file system, a browser, the network. Those tools have side effects in the real world.

You cannot fix the middle box. So the boundary goes around the tools. Whatever the model decides, the tools run somewhere where the damage is contained. What are we protecting? The host machine, the secrets on it, production systems, the network the host can reach, and money, because compute and API calls cost money too.

## Slide 5 — The lethal trifecta
**Timing:** 1:30 (5:00–6:30)

**On slide:**
- Three circles: private data · untrusted content · an external exfiltration channel
- All three together = data theft is one injected instruction away
- HiddenLayer mapped: keys on disk · README comment · curl / Mermaid image URL
- A sandbox removes legs: no production secrets inside, egress allowlist

**Speaker notes:**
A useful way to reason about this is the "lethal trifecta" from our outline. Danger peaks when one agent has three things at once: access to private data, exposure to untrusted content, and a way to send data out. The HiddenLayer attack has all three: keys on disk, a malicious README, and curl or an image URL as the exit.

You rarely can remove untrusted content, since reading the web and repos is the job. But a sandbox lets you cut the other two legs. Put no production secrets inside the sandbox, and allow egress only to an allowlist. With one leg missing, an injection becomes an annoyance instead of an incident.

## Slide 6 — Why agents want sandboxes anyway
**Timing:** 2:00 (6:30–8:30)

**On slide:**
- Reproducibility: template or image → the same environment for every run, eval and RL rollout
- Parallelism: hundreds of ephemeral environments; best-of-N; state forking (Daytona fork/pause: VM sandboxes only ✅; E2B fork "20 copies" claim ❓ unverified)
- Long-running background agents: a remote VM per task with repo, tests and a PR as output
- Computer use: the agent needs a screen (Xvfb/VNC), browser, mouse and keyboard
- Human in the loop: watch live and take over via noVNC or a stream URL
- Resource limits: CPU, RAM, time

**Speaker notes:**
Even if you ignore attacks, you would still want sandboxes. Reproducibility: a template or image gives every run, every eval and every RL rollout the same starting point. Parallelism: you can spin up hundreds of throwaway environments, try best-of-N, or fork a running state. Careful with the details here: Daytona supports fork and pause, but only for its VM sandboxes, not the container ones. E2B has fork too, but the "20 copies per call" figure you may have read I could not verify.

Background agents run for a long time on their own: each task gets a machine with the repo and the tests, and the output is a pull request. Computer-use agents need an actual screen, browser, mouse and keyboard. And a human can watch that screen live and take over. Plus hard limits on CPU, memory and time, so a runaway loop costs you minutes, not a weekend.

**Sources:** [research.md §1](research.md), [Daytona sandboxes](https://www.daytona.io/docs/en/sandboxes/)

## Slide 7 — Set up online, run offline
**Timing:** 1:15 (8:30–9:45)

**On slide:**
- OpenAI Codex Cloud: one container per task
- Phase 1, setup: network and secrets available (install dependencies)
- Phase 2, agent: runs offline by default, secrets removed
- Codex CLI: network off by default, `network_proxy` with a domain allowlist
- Source: developers.openai.com/codex/agent-approvals-security ✅

**Speaker notes:**
One pattern worth stealing comes from OpenAI Codex. In Codex Cloud each task gets its own container. There are two phases. In setup, the environment has network access and secrets, so it can install dependencies. Then the agent phase starts: network off by default, secrets removed. So the part of the run that reads untrusted content has neither secrets nor an exit. That's the trifecta again, with two legs cut by design.

The Codex CLI does the local version: network is off by default, and if you need it, a network proxy with a domain allowlist.

**Sources:** [Codex agent approvals & security](https://developers.openai.com/codex/agent-approvals-security)

## Slide 8 — The isolation ladder
**Timing:** 1:30 (9:45–11:15)

**On slide:**
- Diagram, weakest to strongest, with the trust boundary of each rung:
  1. Process + seccomp / Landlock / Seatbelt: host kernel
  2. Containers (runc): namespaces + cgroups, shared kernel
  3. gVisor (runsc): user-space kernel intercepts syscalls
  4. Firecracker / Kata microVMs: KVM, own kernel
  5. Full VMs: hypervisor, any OS
- Side branch: WASM / V8 isolates, a runtime sandbox, not "full Linux"

**Speaker notes:**
Now the core of the talk: how you isolate. Think of a ladder. Each rung moves the trust boundary further from your host kernel and usually costs more startup time or more operations work.

At the bottom, a normal process with OS policies: seccomp, Landlock, macOS Seatbelt. It still shares the kernel and usually the file system. Then containers: namespaces and cgroups, still one shared kernel. gVisor puts a kernel written in user space between the container and the real kernel. MicroVMs, Firecracker and Kata, give each sandbox its own kernel under KVM. Full VMs give you any OS, including Windows and GUIs. On the side, WASM and V8 isolates: a different kind of sandbox, very fast, but not a Linux machine.

## Slide 9 — Process sandboxes and containers
**Timing:** 1:30 (11:15–12:45)

**On slide:**
- Process sandbox: instant and local, but shared FS and kernel, policy only
  - Codex CLI: Seatbelt on macOS, bwrap + seccomp on Linux, MXC on Windows ✅
- Docker / OCI containers: fast, huge ecosystem; escape = a kernel vulnerability
  - Not for hostile code in multi-tenant setups
  - Hardening we use in ex2: `--network none --read-only --user 65534 --memory 512m --cpus 1 --pids-limit 128`

**Speaker notes:**
The process sandbox is what local coding agents use. Codex CLI is a good reference: Seatbelt on macOS, bubblewrap plus seccomp on Linux, MXC on Windows. Note: not Landlock on Linux, as some older write-ups say. It starts instantly, but it's policy on a shared kernel and usually a shared file system.

Containers are the default for most teams: fast, everything already speaks OCI. The weak point is the shared kernel: one kernel bug and you're out. So containers are fine for your own code and trusted users, but not for hostile code from many tenants on one host. If you do use containers, lock them down. The flags on the slide are exactly what our workshop's ex2 Docker fallback uses: no network, read-only root, nobody user, and caps on memory, CPU and process count.

**Sources:** [Codex agent approvals & security](https://developers.openai.com/codex/agent-approvals-security), [workshop/ex2_llm_loop/agent.py](workshop/ex2_llm_loop/agent.py)

## Slide 10 — gVisor and microVMs
**Timing:** 1:30 (12:45–14:15)

**On slide:**
- gVisor (runsc): user-space kernel intercepts syscalls; OCI-compatible; syscall/IO overhead. Modal's default.
- Firecracker: minimal VMM in Rust on KVM ✅
  - < 125 ms boot · < 5 MiB overhead · 5 emulated devices · up to 150 microVMs/s per host
  - Used by E2B, Vercel Sandbox, Fly.io, AWS Lambda (+ AWS Lambda MicroVMs)
  - Needs KVM: bare metal or nested virtualization
- Kata Containers: a lightweight VM behind the OCI API (QEMU / Cloud Hypervisor / Firecracker); k8s-native, harder to operate
- Note: gVisor and Kata descriptions are generic, not re-checked against primary docs

**Speaker notes:**
gVisor is the middle ground. It intercepts system calls with a kernel implemented in user space, and it plugs in as an OCI runtime, runsc. You pay overhead on syscalls and I/O. Modal uses it by default.

Firecracker is why microVMs became the standard for agent sandboxes. It's a tiny VMM in Rust on top of KVM. The project's own numbers: boot under 125 milliseconds, under 5 MiB of memory overhead, only five emulated devices, up to 150 microVMs per second per host. That's what E2B, Vercel Sandbox, Fly.io and AWS Lambda run on. The catch: you need KVM, so bare metal or nested virtualization.

Kata Containers gives you a VM boundary behind the normal container API, which fits Kubernetes, but it's more to operate. A small honesty note: my gVisor and Kata descriptions are general knowledge from the research, not re-checked against their docs in this pass.

**Sources:** [firecracker-microvm.github.io](https://firecracker-microvm.github.io/), [gvisor.dev](https://gvisor.dev/), [katacontainers.io](https://katacontainers.io/)

## Slide 11 — Full VMs, WASM and V8 isolates
**Timing:** 1:30 (14:15–15:45)

**On slide:**
- Full VMs (QEMU/KVM, cloud VMs): maximum compatibility, Windows, GUI; slow start, expensive
- Aside: WASM (Wasmtime, Pyodide) and V8 isolates: millisecond start, cheap; limited languages and syscalls, no full Linux (e.g. Cloudflare Dynamic Workers)
- Rule of thumb:
  - Your own code / trusted users → container
  - Third-party or LLM code, multi-tenant → gVisor or microVM
  - GUI / Windows → VM

**Speaker notes:**
At the top of the ladder, full VMs. Anything runs, Windows and GUI included, but they start slowly and cost more.

On the side, WASM runtimes like Wasmtime or Pyodide, and V8 isolates like Cloudflare's Dynamic Workers. They start in milliseconds and are cheap, but you get a limited set of languages and system calls. Great for "run this snippet of JS or Python", not for "clone the repo and run the test suite".

If you remember one thing from this section, take the rule of thumb. Your own code and trusted users: a container is fine. Third-party or LLM-generated code with several tenants: gVisor or a microVM. Need a GUI or Windows: a VM.

## Slide 12 — A desktop for an agent: the stack (our ex3)
**Timing:** 1:30 (15:45–17:15)

**On slide:**
- Diagram of our ex3 container: Xvfb `:1` (virtual screen) ← fluxbox (window manager) + Chromium · x11vnc `:5900` (localhost only) → websockify/noVNC `:6080` → your browser
- Agent side: screenshot + xdotool via `docker exec`
- Published on 127.0.0.1 only; VNC has no password
- Same idea in Anthropic's reference container: Xvfb + Mutter + Tint2 + noVNC; E2B Desktop: Xfce + VNC stream
- Screenshot: assets/ex3-desktop.png

**Speaker notes:**
Computer-use agents need a screen. On a server there is none, so we fake one. Xvfb is an X server that draws into memory. A small window manager, fluxbox in our case, and a browser run on it. x11vnc exports that screen over VNC, and websockify with noVNC turns it into a web page on port 6080, so a human can watch in a normal browser.

The agent doesn't use VNC at all. It takes screenshots and sends mouse and keyboard events with xdotool through docker exec. Security note from our README: x11vnc runs without a password and listens only on localhost inside the container, and we publish the port only on 127.0.0.1.

This is a common pattern. Anthropic's reference container uses Xvfb, Mutter, Tint2 and noVNC. E2B Desktop uses Xfce with a VNC stream. On the right is a real screenshot from our container.

**Sources:** [workshop/ex3_docker_desktop](workshop/ex3_docker_desktop/README.md), [Anthropic computer-use docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool), [e2b-dev/desktop](https://github.com/e2b-dev/desktop)

## Slide 13 — The screenshot → action loop
**Timing:** 1:30 (17:15–18:45)

**On slide:**
- Loop diagram: screenshot → vision LLM → function tool call → execute on desktop → new screenshot … until `done`
- Our ex4 tools: `click`, `type`, `key`, `scroll`, `screenshot`, `wait`, `done`
- Screenshots go in user messages (many OpenAI-compatible models reject images in tool messages); keep only the last 3
- Coordinates = screenshot pixels; accept ints, numeric strings or 0..1 normalized values
- Backends: `DESKTOP_BACKEND=docker` (ex3) or `e2b` (E2B Desktop), same interface

**Speaker notes:**
The agent itself is a simple loop. Take a screenshot, send it to a vision model with a list of tools, get back a tool call, run it on the desktop, take a new screenshot, repeat until the model calls done.

Our ex4 uses plain function tools: click, type, key, scroll, screenshot, wait and done. So any model that has vision and tool calling works. Some practical details we learned: many OpenAI-compatible models refuse images inside tool messages, so we send screenshots as user messages and keep only the last three to save context. Models disagree about coordinates, some send pixel integers, some strings, some 0-to-1 fractions, so we accept all of them. And the backend is swappable: our own Docker desktop or E2B Desktop, behind the same interface.

**Sources:** [workshop/ex4_computer_use](workshop/ex4_computer_use/README.md)

## Slide 14 — Humans in the loop, browser clouds, native APIs
**Timing:** 1:30 (18:45–20:15)

**On slide:**
- Human in the loop: noVNC or a stream URL (E2B Desktop `stream.start()` / `get_url()`) to watch and take over
- Browser clouds: Browserbase (+ Stagehand), Steel (Apache-2.0, self-host), Hyperbrowser; ~$0.08–0.12 per browser-hour ⚠️; CDP from Playwright; live view
- Native computer-use APIs:
  - Anthropic `computer_toolset_20260801`: GA, no beta header, 17 member tools, batches of actions per turn ✅
  - Claude 5.5 models accept only the toolset
  - OpenAI: computer-use tool in the Responses API
- They return structured actions in a model-specific schema; ex4 uses generic tools so any model fits

**Speaker notes:**
Because the screen is a VNC stream, a human can watch and take over at any moment. E2B Desktop gives you a stream URL from the SDK. In our container it's the noVNC page.

If the agent only needs a browser, you can skip the desktop and rent a browser: Browserbase, Steel, which is open source and self-hostable, or Hyperbrowser. Roughly 8 to 12 cents per browser-hour, but those prices are from vendor pages I couldn't fully verify. You drive them over CDP from Playwright and get a live view.

And there are native computer-use APIs. Anthropic's current one is computer_toolset_20260801: generally available, no beta header, 17 member tools, and several actions per turn. Claude 5.5 models only accept this toolset; the older computer tool versions are for older models. OpenAI has its own computer-use tool in the Responses API. These models are trained for pixel-precise clicking. Our demo deliberately uses generic tools so you can run it on free models, and you'll see what that costs.

**Sources:** [Anthropic computer-use docs](https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool), [Browserbase plans](https://docs.browserbase.com/account/billing/plans), [Steel pricing](https://docs.steel.dev/overview/pricinglimits)

## Slide 15 — Provider landscape
**Timing:** 1:30 (20:15–21:45)

**On slide:**
- Table (verified 2026-10-10, list prices):
  - E2B: Firecracker · $0.0504/vCPU-h + $0.0162/GiB-h, wall-clock · Desktop: yes · self-host: `e2b-dev/runtime` (Apache-2.0)
  - Daytona: containers (Sysbox) + VM class · $0.0504/vCPU-h + $0.0162/GiB-h · GUI via VM/Windows ⚠️ · OSS repo archived June 2026
  - Modal: gVisor; VM Sandboxes GA 2026-10-01 · ≈$0.071/vCPU-h + $0.024/GiB-h · own image · no self-host
  - Cloudflare Sandbox: microVM per container + V8 isolates · $0.072/active vCPU-h + $0.009/GiB-h · no GUI out of the box · no self-host
  - Vercel Sandbox: Firecracker · $0.128/active CPU-h + $0.0212/GB-h · no GUI · no self-host
  - Fly.io Sprites: Firecracker · $0.0385/CPU-h consumed + $0.021875/GB-h · own image · no self-host
- Vendor-only (⚠️): Runloop microVM devboxes $0.108/CPU-h; Morph Cloud Infinibranch $0.05/MCU-h

**Speaker notes:**
Now the market. This table is from our comparison file, list prices checked on October 10. A few things stand out.

E2B runs on Firecracker, bills wall-clock time, has a ready-made desktop product, and can be self-hosted from its Apache-2.0 runtime repo. Daytona has the same CPU and RAM rates as E2B, uses containers by default plus a separate VM class. Important change: its open-source repo was archived in June 2026, so "we can self-host Daytona" is no longer an argument. Modal uses gVisor by default and made VM sandboxes generally available on October 1st, CPU only. Cloudflare's containers are actually microVMs with their own kernel, plus V8 isolates. Vercel and Fly.io Sprites are both Firecracker and bill for what you actually use.

At the bottom: Runloop and Morph. Their prices come only from search snippets, so treat them as unverified.

**Sources:** [comparison.md](comparison.md) and its source list: [E2B pricing](https://e2b.dev/pricing), [Daytona pricing](https://www.daytona.io/pricing), [Modal pricing](https://modal.com/pricing), [Modal VM sandboxes](https://modal.com/docs/guide/vm-sandboxes), [Cloudflare Sandbox](https://developers.cloudflare.com/sandbox/), [Cloudflare pricing](https://developers.cloudflare.com/containers/pricing/), [Vercel Sandbox pricing](https://vercel.com/docs/vercel-sandbox/pricing), [Fly.io](https://fly.io/learn/ai-sandbox-pricing/)

## Slide 16 — Billing and cold start: read the fine print
**Timing:** 1:30 (21:45–23:15)

**On slide:**
- Wall-clock billing: E2B, Daytona, Modal: you pay while the sandbox exists
- Active-CPU / usage billing: Vercel (active CPU; RAM provisioned), Cloudflare (active CPU; RAM provisioned), Fly.io Sprites (consumed CPU/RAM; idle ~30 s → storage only)
- An agent mostly waits for the LLM → usage billing usually fits better
- Session caps: E2B Hobby ≤ 1 h; Vercel Hobby 45 min
- Cold start, vendor vs independent (⚠️, MarkTechPost benchmark not re-checked): E2B ~150 ms vendor vs 0.7–1.6 s; Vercel 0.67–1.9 s; Modal 0.9–2.4 s; Daytona "90 ms" vendor
- Firecracker < 125 ms boot ✅ is the VMM, not the whole product. **Measure it yourself.**

**Speaker notes:**
Two traps when you compare providers. First, billing models. E2B, Daytona and Modal charge for wall-clock time: the sandbox exists, the meter runs. Vercel and Cloudflare charge for active CPU, and memory as provisioned. Fly.io Sprites charge for consumed CPU and memory, and an idle sprite drops to storage cost after about 30 seconds. A coding agent spends most of its life waiting for the LLM, so usage billing often fits better. Also check session caps: an hour on E2B Hobby, 45 minutes on Vercel Hobby.

Second, cold start. Vendor numbers and independent measurements differ by up to an order of magnitude. E2B says about 150 milliseconds; a third-party benchmark measured 0.7 to 1.6 seconds. I have not re-checked that benchmark, so these are claims on both sides. The Firecracker 125 milliseconds is real, but it's the VMM boot, not the whole product with networking and your template. Measure in your own region with your own image.

**Sources:** [comparison.md](comparison.md), [verification-notes.md](verification-notes.md), [Fly.io](https://fly.io/learn/ai-sandbox-pricing/), [Vercel Sandbox pricing](https://vercel.com/docs/vercel-sandbox/pricing), [E2B pricing](https://e2b.dev/pricing)

## Slide 17 — Self-host vs managed, and how known agents do it
**Timing:** 1:15 (23:15–24:30)

**On slide:**
- Self-host options: E2B runtime (Apache-2.0, Terraform GCP / AWS beta) · Firecracker / firecracker-containerd · Kata on k8s · gVisor runtimeClass · Docker + Xvfb + noVNC · Steel browser · Kasm CE (≤5 sessions, non-commercial ⚠️)
- Daytona: OSS archived (June 2026) → v0.190 fork or Enterprise/BYOC
- How agents do it:
  - Codex: CLI OS sandbox; Cloud container per task, offline agent phase ✅
  - OpenHands: can run with no sandbox; per-conversation Docker sandbox is optional ✅
  - Anthropic computer-use demo: Docker + Xvfb ✅
  - Cursor background agents, Devin, Copilot coding agent: remote VM per task ❓ not verified

**Speaker notes:**
Self-hosting is possible at every rung: E2B's runtime is Apache-2.0 with Terraform for GCP and AWS in beta; Firecracker, Kata and gVisor are open source; and the do-it-yourself desktop is what we built in the workshop. Kasm Workspaces has a community edition, but my understanding from a search snippet is that it's non-commercial and limited to five sessions. Daytona, again, is no longer an open-source option.

How do the known agents do it? Codex we covered. OpenHands is a surprise: by default it can run with no sandbox at all, the per-conversation Docker sandbox is optional. So check your settings. Anthropic's reference is Docker with Xvfb. For Cursor background agents, Devin and the Copilot coding agent, the common description is a remote VM per task, but I could not verify their isolation details, so I won't claim more.

**Sources:** [e2b-dev/runtime](https://github.com/e2b-dev/runtime), [OpenHands README](https://github.com/OpenHands/OpenHands), [Codex security](https://developers.openai.com/codex/agent-approvals-security), [Kasm license](https://www.kasmweb.com/docs/latest/license.html)

## Slide 18 — How to choose
**Timing:** 1:30 (24:30–26:00)

**On slide:**
- Decision diagram:
  - Trusted code only → container (hardened)
  - Untrusted / LLM code, multi-tenant → gVisor or microVM
  - Needs GUI / computer use → E2B Desktop, Daytona VM, Modal VM, or your own Docker + noVNC
  - Only a browser → Browserbase / Steel
  - Agent mostly waits on the LLM → active-CPU / usage billing (Vercel, Cloudflare, Fly Sprites)
  - GPU → Modal or Daytona GPU
  - Fork / branching → E2B, Morph, Daytona (VM class only)
  - Must self-host → E2B runtime or DIY

**Speaker notes:**
So how do you choose? Start with trust. If only your own code runs, a hardened container is fine. If the model writes and runs code, and especially if many customers share hosts, go to gVisor or a microVM.

Then add requirements. A GUI for computer use: E2B Desktop, a Daytona or Modal VM, or your own Docker plus noVNC. Only a browser: a browser cloud. If your agent mostly waits for the model, prefer usage billing. GPU narrows it to Modal or Daytona. Fork and branching: E2B, Morph, or Daytona's VM class. And if you must self-host, E2B's runtime or do it yourself. Note this is a decision aid from our comparison, not a benchmark.

**Sources:** [comparison.md: How to choose](comparison.md)

## Slide 19 — Demo plan and fallbacks
**Timing:** 0:45 (26:00–26:45)

**On slide:**
- Demo 1 (ex2): LLM tool loop, `run_python` → throwaway Docker sandbox · `nvidia/nemotron-3-super-120b-a12b:free`
- Demo 2 (ex4): screenshot → vision LLM → action on our ex3 Docker desktop, watched in noVNC · `dots-studio/dots-3-note-preview:free`
- All via OpenRouter free models (`OPENROUTER_API_KEY`); E2B is the cloud alternative
- Free models are rate-limited and may log prompts: no secrets
- Fallback: recorded output and screenshots from the 2026-10-10 test run

**Speaker notes:**
Time for the demo. Two parts. First, a tool loop where the model writes Python and it runs in a throwaway, locked-down Docker container. Second, a computer-use agent driving the desktop container we just saw, while you watch it in noVNC.

Everything runs on free OpenRouter models. That's the point, you can repeat it tonight. But free models are rate-limited and may log prompts, so never send secrets. If the network or the rate limit fails me, I'll switch to the recorded results from our test run on October 10.

Presenter prep (not shown): before the talk run `python workshop/list_free_models.py`, start the ex3 container (`docker run --rm -d --name desk -p 127.0.0.1:6080:6080 --shm-size=1g --memory=2g --cpus=2 agent-desktop`), open http://localhost:6080/vnc.html, set `EX4_FALLBACK_MODELS`, and run `DESKTOP_BACKEND=docker python workshop/ex4_computer_use/test_backend.py` as a smoke test.

**Sources:** [workshop-plan.md](workshop-plan.md)

## Slide 20 — Tool loop with a locked-down sandbox (ex2)
**Timing:** 1:30 (26:45–28:15)

**On slide:**
- Command: `SANDBOX_BACKEND=docker python workshop/ex2_llm_loop/agent.py "30th Fibonacci number and the sum of primes below 10000"`
- Sandbox: `python:3.12-slim`, `--network none`, read-only rootfs, non-root user, CPU/RAM/PID limits; removed after the session
- Recorded result (2026-10-10): one `run_python` call, 832040 and 5736396, correct, ~12 s
- Caveat: that image has no numpy/scipy → the default statistics task needs E2B or a custom image (`DOCKER_SANDBOX_IMAGE`)

**Speaker notes:**
Live: I run ex2 with the Docker backend and the Fibonacci-and-primes task. Watch the code block the model prints: that code never runs on my laptop, only inside the container. In our test run the model made one run_python call and got both answers right, 832040 and 5736396, in about 12 seconds.

Point at the flags: no network, read-only root file system, the nobody user, CPU, memory and process limits, and the container is deleted when the session ends. Even if the model was told by some injected text to curl my keys somewhere, there's no network and no keys. One honest caveat: the slim image has no numpy, so for the default statistics task you'd use E2B or a custom image.

Fallback: if the call fails, show this slide's recorded result and the code in agent.py.

**Sources:** [workshop-plan.md: test results](workshop-plan.md), [ex2 agent.py](workshop/ex2_llm_loop/agent.py)

## Slide 21 — Computer use on our own desktop (ex4)
**Timing:** 1:30 (28:15–29:45)

**On slide:**
- Command: `DESKTOP_BACKEND=docker python workshop/ex4_computer_use/agent.py "Open https://example.com and tell me the page title and first sentence"`
- Watch live in noVNC at http://localhost:6080/vnc.html
- Fallback screenshots: example.com on our desktop (ex3) → agent clicked through to iana.org (ex4)
- Recorded (2026-10-10, dots-3-note-preview:free): read title + first sentence ✅ 4 steps, 17–21 s; click the link and report the URL ✅ 24 steps, ~6 min

**Speaker notes:**
Now the desktop. I start ex4 with the Docker backend and a simple task: open example.com and read the title and the first sentence. Switch to the noVNC tab so everyone sees the agent's screen.

In our test run with the dots-3 model this took 4 steps and about 20 seconds: it typed the URL straight into the address bar instead of hunting for things to click. The harder task, click the link and report the new URL, also succeeded, but took 24 steps and about six minutes, mostly misclicks. Left is the desktop on example.com, right is where the agent ended up: iana.org.

Don't run the click task live; it's too slow for a talk. If the model is rate-limited, these two screenshots are the fallback.

**Sources:** [workshop-plan.md: test results](workshop-plan.md), [ex4 README](workshop/ex4_computer_use/README.md)

## Slide 22 — What free models taught us
**Timing:** 1:00 (29:45–30:45)

**On slide:**
- `dots-studio/dots-3-note-preview:free`: ✅ reliable tool calls, weak clicking → default
- `nvidia/nemotron-3-nano-omni-30b-a3b-reasoning:free`: ❌ string/normalized coordinates (now handled), then upstream "ResourceExhausted", then `<tool_call>` as plain text
- `google/gemma-4-31b-it:free`, `gemma-4-26b-a4b-it:free`: ❌ 429 all session (untested)
- `thinkingmachines/inkling:free`: ❌ 403, free tier only for approved agentic harnesses
- Lessons: set fallbacks (`EX4_FALLBACK_MODELS`), keep tasks simple, keep screenshots as backup; pixel-precise clicking is the gap vendor computer-use models close

**Speaker notes:**
What did we learn from testing five free models? Only one was usable for the desktop: dots-3. It called tools reliably but clicked poorly. Nemotron nano sent coordinates as strings between 0 and 1 and keys as JSON lists; we fixed the parser, then it hit upstream resource errors and started writing tool calls as plain text. The two Gemma models were rate-limited for the whole session, so they're untested, not bad. Inkling returned 403: its free tier is only for approved harnesses.

So: free vision models are slow and flaky. Configure fallbacks, keep tasks simple, keep screenshots ready. And the gap is clear: text answers after navigation are often right, precise clicking is weak. That's exactly what vendor computer-use models are trained for.

**Sources:** [workshop-plan.md](workshop-plan.md)

## Slide 23 — Production checklist
**Timing:** 1:30 (30:45–32:15)

**On slide:**
- Egress allowlist (network off by default; proxy with a domain allowlist)
- No production secrets in the sandbox: short-lived tokens or an injecting proxy
- CPU / RAM / time limits and a TTL on every sandbox
- Audit every command the agent runs
- Human approval for destructive actions
- Snapshots and rollback outside the agent's control
- Observe via the stream: humans can watch and take over
- Verify state with your own tools, not the agent's report

**Speaker notes:**
If you take one slide home, take this one. Egress: network off by default, and when needed, a proxy with a domain allowlist. Secrets: none from production inside the sandbox; use short-lived tokens, or a proxy that injects credentials on the way out so the sandbox never sees them. Limits: CPU, memory, wall time, and a TTL so forgotten sandboxes die.

Audit every command. Require human approval for destructive actions like dropping a database. Keep snapshots and rollback outside the agent's reach; that's what saved Replit's user. Watch the stream when it matters. And verify the state of the system yourself, because the agent may be confidently wrong about it.

**Sources:** [research.md §4](research.md), [Codex security](https://developers.openai.com/codex/agent-approvals-security)

## Slide 24 — Takeaways
**Timing:** 0:45 (32:15–33:00)

**On slide:**
- The prompt is not a security boundary: put one around the tools
- Pick the rung by trust: container → gVisor / microVM → VM
- A desktop for an agent is Xvfb + VNC/noVNC + a screenshot → action loop
- Compare providers on isolation, billing model and measured cold start, not marketing numbers
- Free models are enough to learn; production computer use needs better clicking

**Speaker notes:**
To sum up. The prompt is not a security boundary, so put a real one around the tools. Choose how strong by asking who wrote the code and who shares the host. A remote desktop for an agent is not magic: a virtual X server, a VNC stream, and a loop. Compare providers on isolation, billing model and cold start you measured yourself. And free models are great for learning, but for production computer use you'll want a model trained for it.

## Slide 25 — Questions?
**Timing:** 1:30 (33:00–34:30)

**On slide:**
- Questions?
- Research, comparison, verification notes, workshop ex1–ex4, this deck and the script
- Repo: https://github.com/vusatui/rnd-research/tree/main/sandboxes-and-remote-desktops
- Inside: research.md · comparison.md · verification-notes.md · workshop/ (ex1–ex4) · this deck and script

**Speaker notes:**
Thanks! Everything is in the repo: the research with sources, the comparison table, the verification notes listing what I could and couldn't confirm, and the four workshop exercises. Happy to take questions.

Likely questions and pointers. "Is Docker enough?" For your own code yes, for hostile multi-tenant code no; see the rule of thumb. "What does E2B fork really do?" The 20-copies figure is unverified. "How do Cursor or Devin isolate?" Not verified in this research. "How fast is cold start?" Vendor and independent numbers differ; measure it, ex1 is a good starting point.
