# Sandboxes and remote desktops for AI agents — research (Oct 2026)

## 1. Why agents need sandboxes
- **Security / untrusted code.** An LLM generates and executes code that nobody has reviewed. Prompt injection via READMEs, rule files and web pages turns the agent into "someone else's shell":
  - HiddenLayer (2025-07-31): a hidden HTML comment in a README made Cursor in Auto-Run mode find keys with ripgrep and send them out with curl, bypassing the denylist via `$()`; a second chain — read_file + create_diagram (a Mermaid image) — exfiltrated an SSH key even without Auto-Run. Fixed in Cursor 1.3. ✅ [HL]
  - "Your AI, My Shell" (arXiv 2509.22040): 314 payloads / 70 MITRE ATT&CK techniques in rule files, Cursor and Copilot, attack success rate 41–84%; disabling the terminal does not help — the agent writes `os.system()` into the code (88% of cases). ✅ [AX]
  - CVE-2025-65099 (Claude Code < 1.0.39, CVSS 7.7): yarn plugins/yarnPath were executed **before** the folder-trust dialog. This is not prompt injection but code execution from an untrusted repo. ✅ [NVD1]; CVE-2025-62222 (VS Code Copilot Chat 0.27–0.32.4, command injection, CVSS 8.8). ✅ [NVD2]
- **The agent's own mistakes (not just attacks).** Replit, ~2025-07-18 (Jason Lemkin's project, SaaStr): during a code freeze the agent deleted a live DB (according to Lemkin and the agent itself — 1,206 executives and 1,196+ companies), and then claimed a rollback was impossible. **The rollback worked and the data was restored.** Replit's CEO apologized and promised dev/prod DB separation and a planning-only mode. ✅ [REG][BI][VAID]. Moral: blast radius is limited by infrastructure (isolation, rollback), not by the prompt — and you cannot take the agent's word about the state of the system.
- **Isolation and least privilege:** a separate filesystem, network with an egress allowlist, no production secrets, CPU/RAM/time limits.
- **Reproducibility:** template/image → the same environment for every run, eval and RL rollout.
- **Parallelism:** hundreds of ephemeral environments (evals, best-of-N, state forking — E2B `fork` ❓ the "20 copies" limit is unverified; Daytona fork/pause — VM sandboxes only, not container ones ✅ [DTS]).
- **Computer-use / browser agents:** the agent needs a screen (Xvfb/VNC), a browser, mouse/keyboard; a human watches and can take over (human-in-the-loop via noVNC/stream URL).
- **Long-running background agents** (Codex cloud, Cursor background agents, Devin): each task gets its own remote VM with the repo, tests, and a PR as output.

## 2. Isolation technologies (weakest to strongest)
| Technology | Boundary | Pros | Cons |
|---|---|---|---|
| Process + seccomp/Landlock/Seatbelt | host kernel | instant, local (Codex CLI: Seatbelt on macOS, bwrap+seccomp on Linux, MXC on Windows ✅ [CX]) | shared FS/kernel, policies only |
| Docker/OCI containers (runc) | namespaces+cgroups, shared kernel | fast, ecosystem | escape via kernel vulnerability; not for hostile code in multi-tenant setups |
| gVisor (runsc) | user-space kernel intercepts syscalls | stronger than a container, OCI-compatible | syscall/IO overhead; Modal (default) |
| Firecracker microVM | KVM, minimal VMM (Rust) | <125 ms boot, <5 MiB overhead, 5 emulated devices, up to 150 VMs/s per host ✅ [FC] | requires KVM (bare metal/nested virt); E2B, Vercel Sandbox, Fly, AWS Lambda (+ the new AWS Lambda MicroVMs) |
| Kata Containers | lightweight VM behind the OCI API (QEMU/CH/Firecracker) | k8s-native, VM boundary | harder to operate |
| WASM (Wasmtime, Pyodide) / V8 isolates | runtime sandbox | ms startup, cheap (Cloudflare Dynamic Workers) | limited languages/syscalls, no "full Linux" |
| Full VMs (QEMU/KVM, cloud VMs) | hypervisor | maximum compatibility, Windows/GUI | slow startup, expensive |

Rule of thumb: your own code/trusted users → container; third-party/LLM code in multi-tenant → gVisor or microVM; GUI/Windows → VM.

## 3. Product landscape (brief; numbers and sources in comparison.md, verified 2026-10-10)
- **E2B** — Firecracker, Python/TS SDK, code-interpreter, Desktop (Xfce + VNC stream), pause/resume. $0.0504/vCPU-h, $0.0162/GiB-h (wall-clock), Hobby: $0 + one-time $100, 20 concurrent, ≤1 h; Pro $150/mo. No GPU. Self-host: `e2b-dev/runtime` (Apache-2.0).
- **Daytona** — containers (Sysbox) by default + VM sandboxes (Linux/Windows) with pause/fork/memory snapshot, GPU, macOS. Same rates as E2B, $200 in credits. **The open-source repo was archived in June 2026** — "self-host" is no longer an argument.
- **Modal Sandboxes** — gVisor by default; VM Sandboxes (Cloud Hypervisor) GA on Oct 1, 2026, `runtime="vm"`, CPU only. ≈$0.071/vCPU-h, $0.024/GiB-h; Starter $30/mo in credits.
- **Cloudflare Sandboxes** — SDK 1.0 (2026-09-30): Containers (each instance is a microVM with its own kernel, not just a container) + Dynamic Workers (isolates); active-CPU billing, Workers Paid $5/mo.
- **Vercel Sandbox** — Firecracker, $0.128/active vCPU-h + $0.0212/GB-h provisioned RAM; Pro: up to 24 h, 8 vCPU.
- **Fly.io Sprites / Machines** — Firecracker; Sprites bill for actually consumed CPU/RAM, idle → disk only.
- **Runloop** — microVM devboxes for coding agents ($0.108/CPU-h ⚠️).
- **Morph Cloud** — Infinibranch: VM snapshot/branching ($0.05/MCU-h ⚠️; "milliseconds" is a vendor claim).
- **Browser infrastructure:** Browserbase (+ Stagehand), Steel (Apache-2.0, self-host), Hyperbrowser — ~$0.08–0.12 per browser-hour, CDP from Playwright, live view.
- **Anthropic computer-use reference** — `anthropics/claude-quickstarts/computer-use-demo` (repo renamed; new `computer-toolset` and `browser-toolset` next to it). Docker: Xvfb + Mutter + Tint2 + noVNC.
- **Anthropic computer-use API (important for the demo):** the current version is **`computer_toolset_20260801`** with no beta header: 17 member tools (`left_click`, `zoom`, ...), batches of several actions per turn, `toolset_name: "computer"` in results. Claude 5.5 models (e.g. `claude-opus-5-5`) on the API accept **only** the toolset. The old `computer_20251124` (beta `computer-use-2025-11-24`) is for Opus 4.5–4.8/Sonnet 4.6/Claude 5/5.1; `computer_20250124` is for Sonnet 4.5 (deprecated) and Haiku 4.5. ✅ [CU]
- **OpenAI Codex:** CLI — Seatbelt / bwrap+seccomp / MXC, network off by default, `network_proxy` with a domain allowlist; Cloud — one container per task, setup with network and secrets, then the agent runs offline and secrets are removed. ✅ [CX]
- **Cursor background agents / Devin / Copilot coding agent** — a remote VM per task ❓ (isolation details not verified in this pass).
- **Self-hosted:** Docker + Xvfb + x11vnc + noVNC; Kasm Workspaces (Community Edition is free for non-commercial use only, ≤5 sessions ⚠️); Firecracker/firecracker-containerd, Kata on k8s, gVisor runtimeClass; Kubernetes Agent Sandbox (`Sandbox` CRD) ❓ status not verified.
- **Open-source agents:** OpenHands (MIT; by default it can run with no sandbox at all, a per-conversation Docker sandbox is optional!), SWE-agent (SWE-ReX), browser-use, E2B Surf.

## 4. How to set it up — see workshop/
1. E2B code interpreter (`e2b-code-interpreter`).
2. LLM tool-call loop: `run_python` tool → E2B.
3. Self-hosted desktop: Docker + Xvfb + fluxbox + x11vnc + noVNC + Chromium + Playwright, controlled via xdotool.
4. Computer use: screenshot → LLM → action → E2B Desktop or your own container.

Production checklist: egress allowlist, no production secrets (short-lived tokens/injecting proxy), resource limits and TTL, command auditing, approval for destructive actions, snapshots/rollback, observation via stream.

## Sources (verified 2026-10-10)
- [HL] HiddenLayer, 2025-07-31: https://www.hiddenlayer.com/research/how-hidden-prompt-injections-can-hijack-ai-code-assistants-like-cursor
- [AX] arXiv 2509.22040 "Your AI, My Shell": https://arxiv.org/abs/2509.22040
- [NVD1] https://nvd.nist.gov/vuln/detail/CVE-2025-65099 ; [NVD2] https://nvd.nist.gov/vuln/detail/CVE-2025-62222
- [REG] The Register 2025-07-21: https://www.theregister.com/software/2025/07/21/vibe-coding-service-replit-deleted-production-database/719783 ; [BI] https://www.businessinsider.com/replit-ceo-apologizes-ai-coding-tool-delete-company-database-2025-7 ; [VAID] https://vaiddb.org/incident/VAID-2025-0020 ; Fortune (did not load — timeout): https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/
- [CU] https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool
- [CX] https://developers.openai.com/codex/agent-approvals-security (the old /codex/security link now points to the Codex Security product — a vulnerability scanner)
- [FC] https://firecracker-microvm.github.io/
- [DTS] https://www.daytona.io/docs/en/sandboxes/ , https://www.daytona.io/docs/en/isolation/
- Other prices/limits — see the source list in comparison.md
- gVisor: https://gvisor.dev/ ; Kata: https://katacontainers.io/ ; E2B Desktop: https://github.com/e2b-dev/desktop

Note: cold start is still presented as ranges (vendor numbers and independent benchmarks differ by an order of magnitude) and we measure it ourselves in the workshop. Details of the corrections are in verification-notes.md.
