# Verification notes — этап 1 (проверено 2026-10-10)

## Исправления фактов
1. **Daytona self-host.** Было: «Self-host: да». Стало: открытый репозиторий `daytonaio/daytona` архивирован, в README сказано: с июня 2026 разработка ушла в приватный код. Остаётся только форк v0.190 «как есть» или Enterprise/BYOC. (GitHub API + README)
2. **Daytona изоляция.** Было: «контейнер; Kata/Sysbox opt-in». Стало: по умолчанию контейнеры (Sysbox/namespaces), отдельно есть класс VM-sandbox (Linux VM/Windows) со своим ядром. Fork, pause и снапшот памяти доступны только VM-классу. (daytona.io/docs/en/isolation, /sandboxes)
3. **Cloudflare Sandbox.** Было: «контейнер». Стало: каждый инстанс Containers — это microVM со своим ядром и сетью. Плюс есть Dynamic Workers (V8-изоляты); раньше в тексте они назывались «Worker Loader». (developers.cloudflare.com/sandbox, 30.09.2026)
4. **Codex CLI на Linux.** Было: Landlock+seccomp. Стало: bwrap+seccomp (начиная с 0.115), на Windows MXC. Старая ссылка /codex/security теперь ведёт на другой продукт (Codex Security). Правильная ссылка: /codex/agent-approvals-security.
5. **E2B Hobby.** Уточнено: $0/мес, разовые $100 кредитов, 20 параллельных песочниц, сессия до 1 ч, GPU нет. Pro: $150/мес, 100 параллельных, сессия до 24 ч. Ставки ($0.0504 и $0.0162) подтверждены.
6. **E2B self-host.** Репозиторий `e2b-dev/infra` переименован в `e2b-dev/runtime` (Apache-2.0).
7. **Modal.** Ставки подтверждены ($0.142 за физическое ядро-час ≈ $0.071 за vCPU-ч, $0.024 за GiB-ч). VM Sandboxes: alpha в июне 2026, GA 1 октября 2026, работают на Cloud Hypervisor, `runtime="vm"`, только CPU. gVisor остаётся режимом по умолчанию.
8. **Vercel.** $0.128/ч и Firecracker подтверждены. Добавлены память ($0.0212 за GB-ч provisioned), лимиты Hobby/Pro и рост максимальной сессии до 24 ч.
9. **Replit.** Добавлено: откат сработал и данные восстановили; агент ложно утверждал, что это невозможно. Дата около 18.07.2025. Цифры 1 206 / 1 196+ взяты со слов Lemkin и самого агента. Fortune не открылась (таймаут), факты подтверждены по The Register, Business Insider, Fast Company и VAID.
10. **HiddenLayer.** Подтверждено (31.07.2025), добавлены детали: обход denylist через `$()` и вторая цепочка через read_file + create_diagram (SSH-ключ уходит без Auto-Run). Исправлено в Cursor 1.3.
11. **arXiv 2509.22040.** Подтверждено. Важно: пример «Cursor грепает ключи и шлёт curl-ом» есть и в статье (Fig. 3, rule-файл), и у HiddenLayer (README). Это два разных исследования, раньше их смешивали. Добавлены цифры: 314 payload-ов, успех атак 41–84%, обход через `os.system()` в 88% случаев.
12. **CVE.** Обе существуют, но это **не prompt injection**. CVE-2025-65099: Claude Code < 1.0.39, при Yarn ≥3 код исполнялся до диалога доверия, CVSS 7.7. CVE-2025-62222: command injection в VS Code Copilot Chat 0.27 – <0.32.5, CVSS 8.8. Формулировки в докладе нужно поправить.
13. **Anthropic reference container.** Репозиторий переименован в `anthropics/claude-quickstarts`, `computer-use-demo` на месте. Рядом появились `computer-toolset` и `browser-toolset`.
14. **OpenHands.** По README сейчас можно запускать «без песочницы» (Option 1), а Docker-песочница на разговор стала опцией. Это не «Docker runtime на сессию по умолчанию».
15. **Firecracker.** Подтверждено: старт <125 мс, накладные расходы <5 MiB, 5 эмулируемых устройств, до 150 microVM/с на хост. Новое: AWS Lambda MicroVMs, управляемые песочницы на Firecracker.

## Computer-use API — важно для воркшопа (упр. 4)
- Текущая версия: `computer_toolset_20260801`, GA, без beta-заголовка. 17 member-tools, батчи действий за один ход, обязателен `toolset_name: "computer"` в tool_result, есть `zoom`, а `display_width_px` и подобные параметры убраны. Скриншоты нужно уменьшать самим.
- Модели Claude 5.5 (`claude-opus-5-5` и др.) на Claude API принимают **только** toolset.
- `computer_20251124` (beta `computer-use-2025-11-24`) работает с Opus 4.5–4.8, Sonnet 4.6, Claude 5/5.1 (Fable/Mythos).
- Наш `ex4_computer_use/agent.py` использует `claude-sonnet-4-5` + `computer_20250124`. Пока работает (Sonnet 4.5 помечен deprecated), но устарел. **На этапе 2 переписать на toolset** (dispatch по `name`, последовательное выполнение батча, текст остановки после ошибки) и обновить модель.
- E2B Desktop SDK (`e2b-desktop` 2.6.1): `Sandbox.create(resolution=...)`, `stream.start()/get_url()`, `left_click(x,y)`, `scroll(direction, amount)`, `write`, `press`, `wait(ms)`, `screenshot()`. Сигнатуры в ex4 совпадают с исходниками 2.6.1. Исходники SDK переехали в монорепозиторий `e2b-dev/E2B`.

## Не проверено / только со слов вендора
- Время холодного старта у всех платформ: только цифры вендоров или бенчмарк MarkTechPost (сам не перепроверял). Будем мерить сами.
- E2B `fork` «до 20 копий за вызов»: не нашёл подтверждения.
- Runloop, Morph, Hyperbrowser: цены взяты из сниппетов поиска, страницы целиком не открывал. Hyperbrowser — данные из его собственного блога.
- Kasm: условия лицензии CE взяты из сниппета поиска.
- Детали изоляции Cursor background agents, Devin и Copilot coding agent не проверялись.
- Kubernetes Agent Sandbox (SIG Apps, CRD `Sandbox`): текущий статус не проверялся.
- gVisor и Kata: описания общие, по первоисточнику в этом проходе не сверялись (только активность репозиториев).
