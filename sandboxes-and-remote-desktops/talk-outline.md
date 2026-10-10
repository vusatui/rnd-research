# Talk: "Sandboxes and Remote Desktops for AI Agents" (~35 min)

1. **Hook (3 min).** Replit's agent deleted a production DB; a README with a prompt injection steals keys via Cursor. "The prompt is not a security boundary."
2. **Agent threat model (5 min).** Untrusted input → LLM → tools → side effects. The lethal trifecta: private data + untrusted content + external exfiltration channel. What we protect: the host, secrets, prod, the network, money.
3. **Why else, beyond security (4 min).** Reproducibility, parallelism/fork, long-running background agents, evals/RL, a GUI for computer use.
4. **Isolation technologies (7 min).** Seccomp/Landlock → containers → gVisor → Firecracker/Kata → VMs; WASM/isolates. "Trust boundary" diagram. Why microVMs became the standard (snapshots, 125 ms boot).
5. **Remote desktops for agents (5 min).** Xvfb + WM + x11vnc + noVNC; the screenshot→action loop; human in the loop via live view; browser clouds (CDP).
6. **Landscape and choosing (6 min).** Table from comparison.md, billing models (wall-clock vs active CPU), self-host vs managed. How Codex/Cursor/Devin/OpenHands are built.
7. **Live demo (4 min).** E2B code execution in a tool loop + a noVNC desktop where the agent opens a browser.
8. **Production checklist and takeaways (3 min).** Egress allowlist, no secrets, TTL/limits, auditing, approval for destructive actions, snapshots. Q&A.

~20–25 slides.
