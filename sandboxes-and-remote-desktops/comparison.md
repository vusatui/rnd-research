# Сравнение платформ (данные 2026, перепроверить перед докладом)

| Платформа | Изоляция | Модель цены | Старт (замеры/вендор) | Desktop/GUI | Self-host |
|---|---|---|---|---|---|
| E2B | Firecracker microVM | wall-clock/сек: $0.0504 vCPU-ч, $0.0162 GiB-ч; Hobby free, Pro $150/мес | ~150 мс vendor; 0.7–1.6 с замеры | Да (E2B Desktop, Xfce+VNC) | Да (OSS infra, сложно) / BYOC |
| Daytona | контейнер; Kata/Sysbox opt-in | wall-clock, те же ставки; $200 кредит | 27–90 мс vendor; 0.27–0.74 с замеры | Да (VNC/computer-use, Windows) | Да |
| Modal Sandboxes | gVisor (+ VM Sandboxes GA 10/2026) | ~$0.071 vCPU-ч, $0.024 GiB-ч; $30/мес кредитов | 0.9–2.4 с | Нет из коробки (свой образ) | Нет |
| Cloudflare Sandbox | контейнер (+V8 isolates) | active CPU $0.072 vCPU-ч; $5/мес | изоляты мс; контейнер до ~5 с в burst | Нет из коробки | Нет |
| Vercel Sandbox | Firecracker | active CPU $0.128 vCPU-ч + память | 0.67–1.9 с | Нет | Нет |
| Fly Machines/Sprites | Firecracker | только реально использованный CPU $0.0385 | ~сек | Свой образ | Нет (но любой образ) |
| Runloop | microVM devboxes | usage | 0.9 с медиана | Ограниченно | Нет |
| Morph Cloud | VM + Infinibranch снапшоты | usage | мс-ветвление | Да (VM) | Нет |
| Browserbase / Steel / Hyperbrowser | изолированный Chrome | за браузер-час / сессию; free tier | ~1 с | Браузер (CDP, live view) | Steel — да (OSS) |
| Anthropic computer-use demo | Docker | бесплатно | секунды | Да (Xvfb+noVNC) | Да |
| OpenAI Codex CLI / cloud | Seatbelt, Landlock+seccomp / контейнер | в подписке | — | Нет | CLI локально |
| Cursor bg agents / Devin | удалённые VM | в подписке | десятки сек | Devin — да | Нет |
| Docker+Xvfb+noVNC / Kasm | контейнер (можно runsc) | своё железо | 1–3 с | Да | Да |
| Firecracker / Kata / gVisor DIY | microVM / runtime | своё железо | 100–300 мс | своими силами | Да |
| OpenHands | Docker runtime на сессию (или E2B/Daytona/remote) | OSS | секунды | браузер (Playwright) | Да |

Как выбирать: GUI/computer-use → E2B Desktop или Daytona, self-host → Docker+noVNC; агент ждёт LLM большую часть времени → active-CPU (Vercel/Cloudflare/Fly); GPU → Modal; fork/ветвление → E2B/Morph/Daytona; браузерная автоматизация → Browserbase/Steel.
