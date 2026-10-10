# Сравнение платформ (проверено 10.10.2026)

Легенда: ✅ проверено по первоисточнику (дата 2026-10-10, если не указано иное); ⚠️ только вендор/вторичный источник; ❓ не удалось проверить. Цены — публичные list prices, без скидок.

| Платформа | Изоляция | Цена (CPU / RAM / план) | Cold start | Desktop/GUI | Self-host |
|---|---|---|---|---|---|
| **E2B** | Firecracker microVM ✅[f] | $0.000014/vCPU-с (=$0.0504/ч), $0.0000045/GiB-с (=$0.0162/ч), wall-clock; Hobby $0 + разовые $100 кредитов, 20 параллельных, сессия ≤1 ч; Pro $150/мес, 100 параллельных, ≤24 ч; без GPU ✅[e2b] | ~150 мс ⚠️ вендор; независимые замеры 0.7–1.6 с ⚠️[mtp] | Да — E2B Desktop (Xfce, VNC-стрим, SDK `e2b-desktop` 2.6.1) ✅[e2bd] | Да: `e2b-dev/runtime` (бывш. `infra`), Apache-2.0, Terraform GCP / AWS beta ✅[gh][fly] |
| **Daytona** | по умолчанию контейнер (Sysbox, namespaces); отдельный класс **VM-sandbox** (Linux VM/Windows) со своим ядром ✅[dti] | $0.0504/vCPU-ч, $0.0162/GiB-ч, диск $0.000108/GiB-ч после 5 GiB; Windows $0.0858/vCPU-ч; GPU от $0.57/ч; $200 кредитов ✅[dtp] | вендор «90 мс» ⚠️[dts]; burst-тест 0.27 с с низким % успеха ⚠️[mtp] | Да (VM/Windows, computer-use) ⚠️ | ⚠️ **OSS-репо архивирован** (июнь 2026: разработка ушла в приватный код), self-host только форк v0.190 или Enterprise/BYOC ✅[gh] |
| **Modal Sandboxes** | gVisor по умолчанию; **VM Sandboxes GA (окт. 2026)** на Cloud Hypervisor, `runtime="vm"`, только CPU ✅[mvm] | $0.00003942/физ.ядро-с (=$0.142/ядро-ч ≈ $0.071/vCPU-ч), $0.00000667/GiB-с (=$0.024/ч); Starter $0 + $30/мес, Team $250 + $100/мес ✅[mp] | 0.9–2.4 с ⚠️[mtp] | своим образом (VM-runtime позволяет X/Docker) ⚠️ | Нет |
| **Cloudflare Sandbox** | Containers: **каждый инстанс — microVM со своим ядром** ✅[cf]; + Dynamic Workers (V8-изоляты) для JS/Python/WASM | CPU $0.000020/vCPU-с (=$0.072/ч) только активный; RAM $0.0000025/GiB-с (=$0.009/ч) за provisioned; Workers Paid $5/мес вкл. 375 vCPU-мин, 25 GiB-ч ✅[cfp] | ❓ (изоляты — мс; контейнер — секунды ⚠️[mtp]) | Нет из коробки | Нет |
| **Vercel Sandbox** | Firecracker microVM ✅[vs] | Active CPU $0.128/ч, RAM $0.0212/GB-ч (provisioned, мин. 1 мин), $0.60/1M созданий; Hobby: 5 ч CPU, 45 мин сессия, 10 параллельных; Pro: 24 ч, 10 000 параллельных, до 8 vCPU ✅[vs] | 0.67–1.9 с ⚠️[mtp] | Нет | Нет |
| **Fly.io Sprites / Machines** | Firecracker ✅[f] | Sprites: $0.0385/CPU-ч реально потреблённого, $0.021875/GB-ч фактической RAM; idle ~30 с → только storage ✅[fly] | ❓ | своим образом | Нет |
| **Runloop** | microVM с отдельным ядром ⚠️[rl] | $0.108/CPU-ч, $0.0252/GB-ч; suspended — не тарифицируется ⚠️[rl] | ❓ (раньше заявляли ~0.9 с) | ограниченно ❓ | Нет |
| **Morph Cloud** | VM + Infinibranch (snapshot/branch) ⚠️ | $0.05/MCU-ч; Team $40/мес (1000 MCU) ⚠️[mo] | ❓ «мс-ветвление» — вендор | Да (VM) ⚠️ | Нет |
| **Browserbase** | изолированный Chrome в облаке | Free 1 браузер-ч; Developer $20 (100 ч, далее $0.12/ч); Startup $99 (500 ч) ⚠️[bb] | ❓ | браузер (CDP, live view) | Нет |
| **Steel** | Chrome-sandbox | Launch $0.10/браузер-ч (+$30 разово); Scale $250/мес + $0.08/ч ⚠️[st] | ❓ | браузер | Да: `steel-browser` Apache-2.0 ✅[gh] |
| **Hyperbrowser** | облачный Chrome | ~$0.10/браузер-ч (100 кредитов/ч), прокси $10/GB ⚠️[hb] (источник — блог самого Hyperbrowser) | ❓ | браузер | Нет |
| **Anthropic computer-use demo** | Docker | бесплатно | секунды | Да (Xvfb+Mutter+Tint2+noVNC) ✅[cu] | Да; репо переименован в `anthropics/claude-quickstarts` ✅[gh] |
| **OpenAI Codex** | CLI: macOS Seatbelt, **Linux bwrap+seccomp** (не Landlock), Windows MXC; Cloud: контейнер на задачу, setup с сетью → агент офлайн по умолчанию ✅[cx] | в подписке | — | Нет (Computer Use — отдельная фича) | CLI локально |
| **Kasm Workspaces** | контейнеры, desktop в браузере | Community Edition бесплатна, ≤5 сессий, только некоммерческое использование ⚠️[ks] | 1–3 с ❓ | Да | Да |
| **Docker + Xvfb + noVNC (DIY)** | контейнер (можно `runsc`) | своё железо | 1–3 с (замерим в воркшопе) | Да | Да |
| **Firecracker / Kata / gVisor DIY** | microVM / VM-runtime / user-space ядро | своё железо, Apache-2.0 ✅[gh] | Firecracker <125 мс boot, <5 MiB overhead, 150 VM/с/хост ✅[f] | своими силами | Да |
| **OpenHands** | агент-сервер локально; **опционально** Docker-sandbox на разговор, VM, облако ✅[oh] | OSS (MIT) ✅[gh] | секунды | браузер | Да |

Как выбирать (не изменилось по сути): GUI/computer-use → E2B Desktop, Daytona VM, Modal VM или свой Docker+noVNC; агент ждёт LLM → active-CPU/usage биллинг (Vercel, Cloudflare, Fly Sprites); GPU → Modal или Daytona GPU; fork/ветвление → E2B, Morph, Daytona (только VM-класс); браузер → Browserbase/Steel; self-host → E2B runtime или DIY (Daytona OSS больше не развивается).

## Источники (все открыты 2026-10-10)
- [e2b] https://e2b.dev/pricing
- [e2bd] https://github.com/e2b-dev/desktop (README) + исходник `e2b_desktop` 2.6.1 с PyPI
- [dtp] https://www.daytona.io/pricing ; [dti] https://www.daytona.io/docs/en/isolation/ ; [dts] https://www.daytona.io/docs/en/sandboxes/
- [mp] https://modal.com/pricing ; [mvm] https://modal.com/blog/vm-sandboxes-agent-computers , https://modal.com/docs/guide/vm-sandboxes , https://modal.com/blog/runtime-product-update-sandbox-endpoints (01.10.2026)
- [cf] https://developers.cloudflare.com/sandbox/ ; [cfp] https://developers.cloudflare.com/containers/pricing/
- [vs] https://vercel.com/docs/vercel-sandbox/pricing
- [fly] https://fly.io/learn/ai-sandbox-pricing/ (Fly.io, 09.09.2026 — конкурент, но со ссылками на прайсы)
- [f] https://firecracker-microvm.github.io/
- [rl] https://runloop.ai/pricing , https://docs.runloop.ai/docs/devboxes/overview (через поиск)
- [mo] https://cloud.morph.so/web/subscribe (через поиск)
- [bb] https://docs.browserbase.com/account/billing/plans ; [st] https://docs.steel.dev/overview/pricinglimits ; [hb] https://tech.hyperbrowser.ai/hyperbrowser-vs-browserbase-2026-cloud-browser-platform (через поиск)
- [cu] https://docs.anthropic.com/en/docs/agents-and-tools/tool-use/computer-use-tool
- [cx] https://developers.openai.com/codex/agent-approvals-security
- [ks] https://www.kasmweb.com/docs/latest/license.html (через поиск)
- [oh] https://github.com/OpenHands/OpenHands (README)
- [mtp] MarkTechPost 27.08.2026 (бенчмарк, не перепроверялся)
- [gh] GitHub API, состояние репозиториев на 2026-10-10
