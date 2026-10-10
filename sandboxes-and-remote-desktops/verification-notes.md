# Verification notes — stage 1 (verified 2026-10-10)

## Factual corrections
1. **Daytona self-host.** Was: "Self-host: yes". Now: the open-source repo `daytonaio/daytona` is archived; the README says development moved to private code in June 2026. Only an as-is fork of v0.190 or Enterprise/BYOC remain. (GitHub API + README)
2. **Daytona isolation.** Was: "container; Kata/Sysbox opt-in". Now: containers by default (Sysbox/namespaces), plus a separate VM-sandbox class (Linux VM/Windows) with its own kernel. Fork, pause and memory snapshots are available only for the VM class. (daytona.io/docs/en/isolation, /sandboxes)
3. **Cloudflare Sandbox.** Was: "container". Now: each Containers instance is a microVM with its own kernel and network. There are also Dynamic Workers (V8 isolates); the text previously called them "Worker Loader". (developers.cloudflare.com/sandbox, 2026-09-30)
4. **Codex CLI on Linux.** Was: Landlock+seccomp. Now: bwrap+seccomp (since 0.115), MXC on Windows. The old /codex/security link now points to a different product (Codex Security). Correct link: /codex/agent-approvals-security.
5. **E2B Hobby.** Clarified: $0/mo, one-time $100 in credits, 20 concurrent sandboxes, sessions up to 1 h, no GPU. Pro: $150/mo, 100 concurrent, sessions up to 24 h. Rates ($0.0504 and $0.0162) confirmed.
6. **E2B self-host.** The `e2b-dev/infra` repo was renamed to `e2b-dev/runtime` (Apache-2.0).
7. **Modal.** Rates confirmed ($0.142 per physical core-hour ≈ $0.071 per vCPU-h, $0.024 per GiB-h). VM Sandboxes: alpha in June 2026, GA on October 1, 2026, run on Cloud Hypervisor, `runtime="vm"`, CPU only. gVisor remains the default.
8. **Vercel.** $0.128/h and Firecracker confirmed. Added memory ($0.0212 per GB-h provisioned), Hobby/Pro limits, and the max session increase to 24 h.
9. **Replit.** Added: the rollback worked and the data was restored; the agent falsely claimed it was impossible. Date around 2025-07-18. The 1,206 / 1,196+ figures come from Lemkin and the agent itself. Fortune did not load (timeout); facts confirmed via The Register, Business Insider, Fast Company and VAID.
10. **HiddenLayer.** Confirmed (2025-07-31), details added: denylist bypass via `$()` and a second chain via read_file + create_diagram (SSH key exfiltrated without Auto-Run). Fixed in Cursor 1.3.
11. **arXiv 2509.22040.** Confirmed. Important: the "Cursor greps for keys and sends them with curl" example appears both in the paper (Fig. 3, rule file) and at HiddenLayer (README). These are two different studies that were previously conflated. Added numbers: 314 payloads, attack success 41–84%, bypass via `os.system()` in 88% of cases.
12. **CVEs.** Both exist, but they are **not prompt injection**. CVE-2025-65099: Claude Code < 1.0.39, with Yarn ≥3 code ran before the trust dialog, CVSS 7.7. CVE-2025-62222: command injection in VS Code Copilot Chat 0.27 – <0.32.5, CVSS 8.8. The wording in the talk needs fixing.
13. **Anthropic reference container.** The repo was renamed to `anthropics/claude-quickstarts`; `computer-use-demo` is still there. `computer-toolset` and `browser-toolset` appeared next to it.
14. **OpenHands.** Per the README it can now run "without a sandbox" (Option 1), and the per-conversation Docker sandbox became optional. It is not "a Docker runtime per session by default".
15. **Firecracker.** Confirmed: <125 ms boot, <5 MiB overhead, 5 emulated devices, up to 150 microVMs/s per host. New: AWS Lambda MicroVMs, managed Firecracker-based sandboxes.

## Computer-use API — important for the workshop (ex. 4)
- Current version: `computer_toolset_20260801`, GA, no beta header. 17 member tools, batches of actions per turn, `toolset_name: "computer"` is required in tool_result, `zoom` is available, and `display_width_px` and similar parameters were removed. Screenshots must be downscaled by the caller.
- Claude 5.5 models (`claude-opus-5-5` etc.) on the Claude API accept **only** the toolset.
- `computer_20251124` (beta `computer-use-2025-11-24`) works with Opus 4.5–4.8, Sonnet 4.6, Claude 5/5.1 (Fable/Mythos).
- Our `ex4_computer_use/agent.py` uses `claude-sonnet-4-5` + `computer_20250124`. It still works (Sonnet 4.5 is marked deprecated) but is outdated. **In stage 2, rewrite it for the toolset** (dispatch by `name`, sequential batch execution, stop text after an error) and update the model.
- E2B Desktop SDK (`e2b-desktop` 2.6.1): `Sandbox.create(resolution=...)`, `stream.start()/get_url()`, `left_click(x,y)`, `scroll(direction, amount)`, `write`, `press`, `wait(ms)`, `screenshot()`. The signatures in ex4 match the 2.6.1 sources. The SDK sources moved to the `e2b-dev/E2B` monorepo.

## Unverified / vendor claims only
- Cold start for all platforms: only vendor numbers or the MarkTechPost benchmark (not re-checked by me). We will measure ourselves.
- E2B `fork` "up to 20 copies per call": no confirmation found.
- Runloop, Morph, Hyperbrowser: prices taken from search snippets; full pages not opened. Hyperbrowser data comes from its own blog.
- Kasm: CE license terms taken from a search snippet.
- Isolation details of Cursor background agents, Devin and Copilot coding agent were not verified.
- Kubernetes Agent Sandbox (SIG Apps, `Sandbox` CRD): current status not verified.
- gVisor and Kata: descriptions are generic and were not checked against primary sources in this pass (only repo activity).
