# Platform comparison (verified 2026-10-10)

Legend: ✅ verified against a primary source (dated 2026-10-10 unless stated otherwise); ⚠️ vendor/secondary source only; ❓ could not verify. Prices are public list prices, no discounts.

| Platform | Isolation | Price (CPU / RAM / plan) | Cold start | Desktop/GUI | Self-host |
|---|---|---|---|---|---|
| **E2B** | Firecracker microVM ✅[f] | $0.000014/vCPU-s (=$0.0504/h), $0.0000045/GiB-s (=$0.0162/h), wall-clock; Hobby $0 + one-time $100 in credits, 20 concurrent, session ≤1 h; Pro $150/mo, 100 concurrent, ≤24 h; no GPU ✅[e2b] | ~150 ms ⚠️ vendor; independent measurements 0.7–1.6 s ⚠️[mtp] | Yes — E2B Desktop (Xfce, VNC stream, SDK `e2b-desktop` 2.6.1) ✅[e2bd] | Yes: `e2b-dev/runtime` (formerly `infra`), Apache-2.0, Terraform GCP / AWS beta ✅[gh][fly] |
| **Daytona** | container by default (Sysbox, namespaces); separate **VM-sandbox** class (Linux VM/Windows) with its own kernel ✅[dti] | $0.0504/vCPU-h, $0.0162/GiB-h, disk $0.000108/GiB-h beyond 5 GiB; Windows $0.0858/vCPU-h; GPU from $0.57/h; $200 in credits ✅[dtp] | vendor "90 ms" ⚠️[dts]; burst test 0.27 s with a low success rate ⚠️[mtp] | Yes (VM/Windows, computer use) ⚠️ | ⚠️ **OSS repo archived** (June 2026: development moved to private code), self-host only via a v0.190 fork or Enterprise/BYOC ✅[gh] |
| **Modal Sandboxes** | gVisor by default; **VM Sandboxes GA (Oct 2026)** on Cloud Hypervisor, `runtime="vm"`, CPU only ✅[mvm] | $0.00003942/physical core-s (=$0.142/core-h ≈ $0.071/vCPU-h), $0.00000667/GiB-s (=$0.024/h); Starter $0 + $30/mo, Team $250 + $100/mo ✅[mp] | 0.9–2.4 s ⚠️[mtp] | via your own image (VM runtime allows X/Docker) ⚠️ | No |
| **Cloudflare Sandbox** | Containers: **each instance is a microVM with its own kernel** ✅[cf]; + Dynamic Workers (V8 isolates) for JS/Python/WASM | CPU $0.000020/vCPU-s (=$0.072/h) active only; RAM $0.0000025/GiB-s (=$0.009/h) provisioned; Workers Paid $5/mo incl. 375 vCPU-min, 25 GiB-h ✅[cfp] | ❓ (isolates — ms; container — seconds ⚠️[mtp]) | Not out of the box | No |
| **Vercel Sandbox** | Firecracker microVM ✅[vs] | Active CPU $0.128/h, RAM $0.0212/GB-h (provisioned, 1 min minimum), $0.60/1M creations; Hobby: 5 CPU-h, 45 min session, 10 concurrent; Pro: 24 h, 10,000 concurrent, up to 8 vCPU ✅[vs] | 0.67–1.9 s ⚠️[mtp] | No | No |
| **Fly.io Sprites / Machines** | Firecracker ✅[f] | Sprites: $0.0385/CPU-h actually consumed, $0.021875/GB-h actual RAM; idle ~30 s → storage only ✅[fly] | ❓ | via your own image | No |
| **Runloop** | microVM with a separate kernel ⚠️[rl] | $0.108/CPU-h, $0.0252/GB-h; suspended — not billed ⚠️[rl] | ❓ (previously claimed ~0.9 s) | limited ❓ | No |
| **Morph Cloud** | VM + Infinibranch (snapshot/branch) ⚠️ | $0.05/MCU-h; Team $40/mo (1000 MCU) ⚠️[mo] | ❓ "ms branching" — vendor claim | Yes (VM) ⚠️ | No |
| **Browserbase** | isolated cloud Chrome | Free 1 browser-h; Developer $20 (100 h, then $0.12/h); Startup $99 (500 h) ⚠️[bb] | ❓ | browser (CDP, live view) | No |
| **Steel** | Chrome sandbox | Launch $0.10/browser-h (+$30 one-time); Scale $250/mo + $0.08/h ⚠️[st] | ❓ | browser | Yes: `steel-browser` Apache-2.0 ✅[gh] |
| **Hyperbrowser** | cloud Chrome | ~$0.10/browser-h (100 credits/h), proxy $10/GB ⚠️[hb] (source: Hyperbrowser's own blog) | ❓ | browser | No |
| **Anthropic computer-use demo** | Docker | free | seconds | Yes (Xvfb+Mutter+Tint2+noVNC) ✅[cu] | Yes; repo renamed to `anthropics/claude-quickstarts` ✅[gh] |
| **OpenAI Codex** | CLI: macOS Seatbelt, **Linux bwrap+seccomp** (not Landlock), Windows MXC; Cloud: one container per task, setup with network → agent offline by default ✅[cx] | included in subscription | — | No (Computer Use is a separate feature) | CLI runs locally |
| **Kasm Workspaces** | containers, desktop in the browser | Community Edition free, ≤5 sessions, non-commercial use only ⚠️[ks] | 1–3 s ❓ | Yes | Yes |
| **Docker + Xvfb + noVNC (DIY)** | container (`runsc` possible) | your own hardware | 1–3 s (to be measured in the workshop) | Yes | Yes |
| **Firecracker / Kata / gVisor DIY** | microVM / VM runtime / user-space kernel | your own hardware, Apache-2.0 ✅[gh] | Firecracker <125 ms boot, <5 MiB overhead, 150 VMs/s/host ✅[f] | DIY | Yes |
| **OpenHands** | agent server locally; **optional** per-conversation Docker sandbox, VM, cloud ✅[oh] | OSS (MIT) ✅[gh] | seconds | browser | Yes |

How to choose (essentially unchanged): GUI/computer use → E2B Desktop, Daytona VM, Modal VM or your own Docker+noVNC; agent mostly waits on the LLM → active-CPU/usage billing (Vercel, Cloudflare, Fly Sprites); GPU → Modal or Daytona GPU; fork/branching → E2B, Morph, Daytona (VM class only); browser → Browserbase/Steel; self-host → E2B runtime or DIY (Daytona OSS is no longer developed).

## Sources (all opened 2026-10-10)
- [e2b] https://e2b.dev/pricing
- [e2bd] https://github.com/e2b-dev/desktop (README) + `e2b_desktop` 2.6.1 source from PyPI
- [dtp] https://www.daytona.io/pricing ; [dti] https://www.daytona.io/docs/en/isolation/ ; [dts] https://www.daytona.io/docs/en/sandboxes/
- [mp] https://modal.com/pricing ; [mvm] https://modal.com/blog/vm-sandboxes-agent-computers , https://modal.com/docs/guide/vm-sandboxes , https://modal.com/blog/runtime-product-update-sandbox-endpoints (2026-10-01)
- [cf] https://developers.cloudflare.com/sandbox/ ; [cfp] https://developers.cloudflare.com/containers/pricing/
- [vs] https://vercel.com/docs/vercel-sandbox/pricing
- [fly] https://fly.io/learn/ai-sandbox-pricing/ (Fly.io, 2026-09-09 — a competitor, but links to pricing pages)
- [f] https://firecracker-microvm.github.io/
- [rl] https://runloop.ai/pricing , https://docs.runloop.ai/docs/devboxes/overview (via search)
- [mo] https://cloud.morph.so/web/subscribe (via search)
- [bb] https://docs.browserbase.com/account/billing/plans ; [st] https://docs.steel.dev/overview/pricinglimits ; [hb] https://tech.hyperbrowser.ai/hyperbrowser-vs-browserbase-2026-cloud-browser-platform (via search)
- [cu] https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool
- [cx] https://developers.openai.com/codex/agent-approvals-security
- [ks] https://www.kasmweb.com/docs/latest/license.html (via search)
- [oh] https://github.com/OpenHands/OpenHands (README)
- [mtp] MarkTechPost 2026-08-27 (benchmark, not re-checked)
- [gh] GitHub API, repository state as of 2026-10-10
