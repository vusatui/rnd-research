# Sandboxes и remote desktops для AI-агентов — исследование (окт. 2026)

## 1. Зачем агентам песочницы
- **Безопасность / недоверенный код.** LLM генерирует и исполняет код, который никто не ревьюил. Prompt injection через README, rule-файлы, веб-страницы превращает агента в «чужой shell»: HiddenLayer показала, как Cursor через скрытый комментарий в README грепает ключи и шлёт их curl-ом; статья «Your AI, My Shell» (arXiv 2509.22040) — rule-файлы заставляли Copilot/Cursor выполнять curl и модифицировать ~/.bashrc; CVE-2025-65099 (Claude Code), CVE-2025-62222 (Copilot).
- **Ошибки самого агента (не только атаки).** Replit, июль 2025: агент удалил прод-БД (1 206 руководителей, 1 196 компаний) во время code freeze. Вывод Replit — разделение dev/prod, rollback, plan-only режим. Мораль: blast radius ограничивается инфраструктурой, а не промптом.
- **Изоляция и least privilege:** отдельная ФС, сеть с egress-allowlist, отсутствие прод-секретов, лимиты CPU/RAM/времени.
- **Воспроизводимость:** шаблон/образ → одинаковое окружение для каждого запуска, eval-ов и RL-роллаутов.
- **Параллелизм:** сотни эфемерных окружений (eval, best-of-N, fork состояния — E2B `fork` до 20 копий за вызов, Daytona fork/pause).
- **Computer-use / browser-агенты:** агенту нужен экран (Xvfb/VNC), браузер, мышь/клавиатура; человек наблюдает и может перехватить управление (human-in-the-loop через noVNC/stream URL).
- **Долгоживущие фоновые агенты** (Codex cloud, Cursor background agents, Devin): каждая задача — своя удалённая VM с репо, тестами и PR на выходе.

## 2. Технологии изоляции (от слабой к сильной)
| Технология | Граница | Плюсы | Минусы |
|---|---|---|---|
| Процесс + seccomp/Landlock/Seatbelt | ядро хоста | мгновенно, локально (так делает Codex CLI: Seatbelt на macOS, Landlock+seccomp на Linux) | общий FS/ядро, только политики |
| Docker/OCI контейнеры (runc) | namespaces+cgroups, общее ядро | быстро, экосистема | побег через уязвимость ядра; не для враждебного кода в multi-tenant |
| gVisor (runsc) | user-space ядро перехватывает syscalls | сильнее контейнера, OCI-совместим | overhead на syscalls/IO; Modal, частично Daytona |
| Firecracker microVM | KVM, минимальный VMM (Rust) | ~125 мс boot, <5 MiB overhead, снапшоты памяти | нужен KVM (bare metal/nested virt); E2B, Vercel Sandbox, Fly, AWS Lambda |
| Kata Containers | лёгкая VM под OCI API (QEMU/CH/Firecracker) | k8s-native, VM-граница | сложнее в эксплуатации |
| WASM (Wasmtime, Pyodide) / V8 isolates | sandbox рантайма | мс-старт, дешево (Cloudflare Worker Loader) | ограниченные языки/syscalls, нет «полноценного Linux» |
| Полные VM (QEMU/KVM, облачные VM) | гипервизор | максимальная совместимость, Windows/GUI | медленный старт, дорого |

Правило: свой код/доверенные пользователи → контейнер; чужой/LLM-код в multi-tenant → gVisor или microVM; GUI/Windows → VM.

## 3. Ландшафт продуктов (кратко; таблица — comparison.md)
- **E2B** — Firecracker, Python/TS SDK, code-interpreter, Desktop (Xfce + VNC stream), pause/resume, fork. $0.0504/vCPU-ч, $0.0162/GiB-ч, Hobby бесплатно (сессия до 1 ч), Pro $150/мес. Open-source инфраструктура (self-host возможен, сложный).
- **Daytona** — контейнеры по умолчанию (Kata/Sysbox opt-in), очень быстрый старт (vendor: <90 мс), GPU/Windows, self-host, $200 стартового кредита.
- **Modal Sandboxes** — gVisor; GPU; VM Sandboxes GA с 1 окт 2026; Starter $30 кредитов/мес.
- **Cloudflare Sandbox SDK** — контейнеры на Workers/Durable Objects, SDK 1.0 (30 сен 2026), active-CPU биллинг, $5/мес Workers Paid; плюс V8-изоляты (Worker Loader).
- **Vercel Sandbox** — Firecracker, active-CPU billing ($0.128/active vCPU-ч), TS-first.
- **Fly.io Machines / Sprites** — Firecracker, платишь за реально использованный CPU, idle бесплатно.
- **Runloop** — devbox-ы для coding-агентов, снапшоты, бенчмарки (SWE-bench).
- **Morph Cloud** — Infinibranch: снапшот/ветвление VM за мс, удобно для поиска по дереву состояний.
- **Браузерная инфраструктура:** Browserbase (+ Stagehand), Steel (open-source, self-host), Hyperbrowser — headless/headful Chrome в облаке, CDP-подключение из Playwright, captcha/прокси, запись сессий.
- **Anthropic computer-use reference container** (anthropic-quickstarts/computer-use-demo) — Docker: Ubuntu + Xvfb + mutter + tint2 + x11vnc + noVNC + Streamlit; эталон self-hosted desktop.
- **OpenAI:** Codex CLI — локальный sandbox (Seatbelt / Landlock+seccomp), сеть выключена по умолчанию; Codex cloud — контейнер на задачу, интернет на этапе setup, затем по политике; Responses API — Code Interpreter (контейнеры) и computer-use tool (окружение даёте вы).
- **Cursor background agents / Devin / Codex cloud / Copilot coding agent** — удалённые VM на задачу, snapshot окружения, PR на выходе.
- **Self-hosted:** Docker + Xvfb + x11vnc + noVNC (+ Kasm Workspaces для готовых браузерных desktop-ов), Firecracker/firecracker-containerd, Kata на k8s, gVisor runtimeClass в k8s; Kubernetes Agent Sandbox (SIG Apps, CRD `Sandbox`).
- **Open-source агенты:** OpenHands (Docker runtime на сессию, есть remote runtime/E2B/Daytona), SWE-agent (SWE-ReX), browser-use, E2B Surf (computer-use агент-пример).

## 4. Как настраивать — см. workshop/
1. E2B code interpreter (`e2b-code-interpreter`).
2. LLM tool-call loop: tool `run_python` → E2B.
3. Self-hosted desktop: Docker + Xvfb + fluxbox + x11vnc + noVNC + Chromium + Playwright, управление через xdotool.
4. Computer-use: screenshot → LLM → action → E2B Desktop или свой контейнер.

Чек-лист продакшна: egress allowlist, без прод-секретов (короткоживущие токены/прокси с подстановкой), лимиты ресурсов и TTL, аудит команд, approve для деструктивных действий, снапшоты/rollback, наблюдение через стрим.

## Источники
- MarkTechPost, Best Agent Sandboxes 2026 (27.08.2026): https://www.marktechpost.com/2026/08/27/best-agent-sandboxes-2026-cold-start-pricing-network-policy/
- Developers Digest, E2B vs Daytona vs Modal 2026: https://www.developersdigest.tech/blog/ai-agent-code-sandbox-comparison-2026
- Fly.io, AI Sandbox Pricing: https://fly.io/learn/ai-sandbox-pricing/
- Q, Sandbox Cold Start Bake-Off (Apr 2026): https://www.getqpro.com/blog/sandbox-startup-benchmark-2026
- LogRocket, Comparing AI agent sandbox platforms: https://blog.logrocket.com/comparing-ai-agent-sandbox-platforms-e2b-modal-daytona-and-more/
- E2B Desktop: https://github.com/e2b-dev/desktop , https://pypi.org/project/e2b-desktop/ , https://e2b.dev/docs/use-cases/computer-use
- Replit инцидент: https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/
- HiddenLayer, prompt injection в Cursor: https://www.hiddenlayer.com/research/how-hidden-prompt-injections-can-hijack-ai-code-assistants-like-cursor
- «Your AI, My Shell»: https://arxiv.org/html/2509.22040v2
- Anthropic computer-use demo: https://github.com/anthropics/anthropic-quickstarts/tree/main/computer-use-demo
- Firecracker: https://firecracker-microvm.github.io/ ; gVisor: https://gvisor.dev/ ; Kata: https://katacontainers.io/
- OpenHands: https://github.com/All-Hands-AI/OpenHands ; Steel: https://github.com/steel-dev/steel-browser ; Browserbase: https://www.browserbase.com/
- Codex sandboxing: https://developers.openai.com/codex/security

Примечание: цифры cold start сильно расходятся между бенчмарками (Daytona 27–90 мс vendor vs 0.27 с с 37% успеха в burst-тесте MarkTechPost); на докладе подавать как диапазоны и мерить самим. Цены/лимиты проверить перед выступлением.
