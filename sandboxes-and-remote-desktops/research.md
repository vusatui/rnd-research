# Sandboxes и remote desktops для AI-агентов — исследование (окт. 2026)

## 1. Зачем агентам песочницы
- **Безопасность / недоверенный код.** LLM генерирует и исполняет код, который никто не ревьюил. Prompt injection через README, rule-файлы, веб-страницы превращает агента в «чужой shell»:
  - HiddenLayer (31.07.2025): скрытый HTML-комментарий в README заставил Cursor в Auto-Run найти ключи ripgrep-ом и отправить их curl-ом, обойдя denylist через `$()`; вторая цепочка — read_file + create_diagram (картинка Mermaid) утащила SSH-ключ даже без Auto-Run. Исправлено в Cursor 1.3. ✅ [HL]
  - «Your AI, My Shell» (arXiv 2509.22040): 314 payload-ов / 70 техник MITRE ATT&CK в rule-файлах, Cursor и Copilot, успех атак 41–84%; запрет терминала не спасает — агент вписывает `os.system()` в код (88% случаев). ✅ [AX]
  - CVE-2025-65099 (Claude Code < 1.0.39, CVSS 7.7): yarn-плагины/yarnPath исполнялись **до** диалога доверия к папке. Это не prompt injection, а исполнение кода из недоверенного репо. ✅ [NVD1]; CVE-2025-62222 (VS Code Copilot Chat 0.27–0.32.4, command injection, CVSS 8.8). ✅ [NVD2]
- **Ошибки самого агента (не только атаки).** Replit, ~18.07.2025 (проект Jason Lemkin, SaaStr): агент во время code freeze удалил живую БД (по словам Lemkin и самого агента — 1 206 руководителей и 1 196+ компаний), а потом утверждал, что откат невозможен. **Откат сработал, данные восстановлены.** CEO Replit извинился, обещал разделение dev/prod БД и planning-only режим. ✅ [REG][BI][VAID]. Мораль: blast radius ограничивается инфраструктурой (изоляция, rollback), а не промптом — и нельзя верить агенту на слово о состоянии системы.
- **Изоляция и least privilege:** отдельная ФС, сеть с egress-allowlist, отсутствие прод-секретов, лимиты CPU/RAM/времени.
- **Воспроизводимость:** шаблон/образ → одинаковое окружение для каждого запуска, eval-ов и RL-роллаутов.
- **Параллелизм:** сотни эфемерных окружений (eval, best-of-N, fork состояния — E2B `fork` ❓ лимит «20 копий» не проверен; Daytona fork/pause — только для VM-sandbox, не для контейнерных ✅ [DTS]).
- **Computer-use / browser-агенты:** агенту нужен экран (Xvfb/VNC), браузер, мышь/клавиатура; человек наблюдает и может перехватить управление (human-in-the-loop через noVNC/stream URL).
- **Долгоживущие фоновые агенты** (Codex cloud, Cursor background agents, Devin): каждая задача — своя удалённая VM с репо, тестами и PR на выходе.

## 2. Технологии изоляции (от слабой к сильной)
| Технология | Граница | Плюсы | Минусы |
|---|---|---|---|
| Процесс + seccomp/Landlock/Seatbelt | ядро хоста | мгновенно, локально (Codex CLI: Seatbelt на macOS, bwrap+seccomp на Linux, MXC на Windows ✅ [CX]) | общий FS/ядро, только политики |
| Docker/OCI контейнеры (runc) | namespaces+cgroups, общее ядро | быстро, экосистема | побег через уязвимость ядра; не для враждебного кода в multi-tenant |
| gVisor (runsc) | user-space ядро перехватывает syscalls | сильнее контейнера, OCI-совместим | overhead на syscalls/IO; Modal (по умолчанию) |
| Firecracker microVM | KVM, минимальный VMM (Rust) | <125 мс boot, <5 MiB overhead, 5 эмулируемых устройств, до 150 VM/с на хост ✅ [FC] | нужен KVM (bare metal/nested virt); E2B, Vercel Sandbox, Fly, AWS Lambda (+ новый AWS Lambda MicroVMs) |
| Kata Containers | лёгкая VM под OCI API (QEMU/CH/Firecracker) | k8s-native, VM-граница | сложнее в эксплуатации |
| WASM (Wasmtime, Pyodide) / V8 isolates | sandbox рантайма | мс-старт, дешево (Cloudflare Dynamic Workers) | ограниченные языки/syscalls, нет «полноценного Linux» |
| Полные VM (QEMU/KVM, облачные VM) | гипервизор | максимальная совместимость, Windows/GUI | медленный старт, дорого |

Правило: свой код/доверенные пользователи → контейнер; чужой/LLM-код в multi-tenant → gVisor или microVM; GUI/Windows → VM.

## 3. Ландшафт продуктов (кратко; цифры и источники — comparison.md, проверено 10.10.2026)
- **E2B** — Firecracker, Python/TS SDK, code-interpreter, Desktop (Xfce + VNC-стрим), pause/resume. $0.0504/vCPU-ч, $0.0162/GiB-ч (wall-clock), Hobby: $0 + разовые $100, 20 параллельных, ≤1 ч; Pro $150/мес. GPU нет. Self-host: `e2b-dev/runtime` (Apache-2.0).
- **Daytona** — контейнеры (Sysbox) по умолчанию + VM-sandbox (Linux/Windows) с pause/fork/memory-snapshot, GPU, macOS. Те же ставки, что у E2B, $200 кредитов. **Открытый репо архивирован в июне 2026** — «self-host» больше не аргумент.
- **Modal Sandboxes** — gVisor по умолчанию; VM Sandboxes (Cloud Hypervisor) GA 1 окт 2026, `runtime="vm"`, только CPU. ≈$0.071/vCPU-ч, $0.024/GiB-ч; Starter $30/мес кредитов.
- **Cloudflare Sandboxes** — SDK 1.0 (30.09.2026): Containers (каждый инстанс — microVM со своим ядром, не просто контейнер) + Dynamic Workers (изоляты); active-CPU биллинг, Workers Paid $5/мес.
- **Vercel Sandbox** — Firecracker, $0.128/active vCPU-ч + $0.0212/GB-ч provisioned RAM; Pro: до 24 ч, 8 vCPU.
- **Fly.io Sprites / Machines** — Firecracker; Sprites тарифицируют реально потреблённые CPU/RAM, idle → только диск.
- **Runloop** — microVM devbox-ы для coding-агентов ($0.108/CPU-ч ⚠️).
- **Morph Cloud** — Infinibranch: snapshot/ветвление VM ($0.05/MCU-ч ⚠️; «мс» — заявление вендора).
- **Браузерная инфраструктура:** Browserbase (+ Stagehand), Steel (Apache-2.0, self-host), Hyperbrowser — ~$0.08–0.12 за браузер-час, CDP из Playwright, live view.
- **Anthropic computer-use reference** — `anthropics/claude-quickstarts/computer-use-demo` (репо переименован; рядом новые `computer-toolset`, `browser-toolset`). Docker: Xvfb + Mutter + Tint2 + noVNC.
- **Anthropic computer-use API (важно для демо):** текущая версия — **`computer_toolset_20260801`** без beta-заголовка: 17 member-tools (`left_click`, `zoom`, ...), батчи из нескольких действий за ход, `toolset_name: "computer"` в результатах. Модели Claude 5.5 (например `claude-opus-5-5`) на API принимают **только** toolset. Старый `computer_20251124` (beta `computer-use-2025-11-24`) — для Opus 4.5–4.8/Sonnet 4.6/Claude 5/5.1; `computer_20250124` — для Sonnet 4.5 (deprecated), Haiku 4.5. ✅ [CU]
- **OpenAI Codex:** CLI — Seatbelt / bwrap+seccomp / MXC, сеть по умолчанию выключена, `network_proxy` с allowlist доменов; Cloud — контейнер на задачу, setup с сетью и секретами, затем агент офлайн, секреты удаляются. ✅ [CX]
- **Cursor background agents / Devin / Copilot coding agent** — удалённые VM на задачу ❓ (детали изоляции в этом проходе не проверялись).
- **Self-hosted:** Docker + Xvfb + x11vnc + noVNC; Kasm Workspaces (Community Edition бесплатна только для некоммерческого использования, ≤5 сессий ⚠️); Firecracker/firecracker-containerd, Kata на k8s, gVisor runtimeClass; Kubernetes Agent Sandbox (CRD `Sandbox`) ❓ статус не проверен.
- **Open-source агенты:** OpenHands (MIT; по умолчанию может работать вообще без песочницы, Docker-sandbox на разговор — опция!), SWE-agent (SWE-ReX), browser-use, E2B Surf.

## 4. Как настраивать — см. workshop/
1. E2B code interpreter (`e2b-code-interpreter`).
2. LLM tool-call loop: tool `run_python` → E2B.
3. Self-hosted desktop: Docker + Xvfb + fluxbox + x11vnc + noVNC + Chromium + Playwright, управление через xdotool.
4. Computer-use: screenshot → LLM → action → E2B Desktop или свой контейнер.

Чек-лист продакшна: egress allowlist, без прод-секретов (короткоживущие токены/прокси с подстановкой), лимиты ресурсов и TTL, аудит команд, approve для деструктивных действий, снапшоты/rollback, наблюдение через стрим.

## Источники (проверено 2026-10-10)
- [HL] HiddenLayer, 31.07.2025: https://www.hiddenlayer.com/research/how-hidden-prompt-injections-can-hijack-ai-code-assistants-like-cursor
- [AX] arXiv 2509.22040 «Your AI, My Shell»: https://arxiv.org/abs/2509.22040
- [NVD1] https://nvd.nist.gov/vuln/detail/CVE-2025-65099 ; [NVD2] https://nvd.nist.gov/vuln/detail/CVE-2025-62222
- [REG] The Register 21.07.2025: https://www.theregister.com/software/2025/07/21/vibe-coding-service-replit-deleted-production-database/719783 ; [BI] https://www.businessinsider.com/replit-ceo-apologizes-ai-coding-tool-delete-company-database-2025-7 ; [VAID] https://vaiddb.org/incident/VAID-2025-0020 ; Fortune (не открылась — таймаут): https://fortune.com/2025/07/23/ai-coding-tool-replit-wiped-database-called-it-a-catastrophic-failure/
- [CU] https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool
- [CX] https://developers.openai.com/codex/agent-approvals-security (старая ссылка /codex/security теперь ведёт на продукт Codex Security — сканер уязвимостей)
- [FC] https://firecracker-microvm.github.io/
- [DTS] https://www.daytona.io/docs/en/sandboxes/ , https://www.daytona.io/docs/en/isolation/
- Остальные цены/лимиты — см. список источников в comparison.md
- gVisor: https://gvisor.dev/ ; Kata: https://katacontainers.io/ ; E2B Desktop: https://github.com/e2b-dev/desktop

Примечание: cold start по-прежнему подаём диапазонами (вендорские цифры vs независимые бенчмарки расходятся на порядок) и меряем сами в воркшопе. Подробности правок — verification-notes.md.
