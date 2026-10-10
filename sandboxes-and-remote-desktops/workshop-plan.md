# Воркшоп (2–2.5 ч)

**Пререквизиты:** Python 3.10+, Docker, ключ E2B (Hobby, бесплатно), ключ LLM (OpenAI или Anthropic; можно любой OpenAI-совместимый). `pip install -r workshop/requirements.txt`.

| # | Упражнение | Время | Результат |
|---|---|---|---|
| 1 | `ex1_e2b_code` — создать песочницу, выполнить код, файлы, лимиты, убить | 20 мин | понимание жизненного цикла sandbox |
| 2 | `ex2_llm_loop` — tool `run_python` → E2B, агент решает задачу анализа данных | 35 мин | агентный цикл с изоляцией |
| 3 | `ex3_docker_desktop` — свой desktop: Docker+Xvfb+noVNC+Chromium, Playwright внутри, смотрим в браузере на :6080 | 35 мин | self-host remote desktop |
| 4 | `ex4_computer_use` — screenshot→LLM→action loop на E2B Desktop (или на контейнере из ex3) | 40 мин | computer-use агент с live view |

Бонусы: запустить ex3 с `--runtime=runsc` (gVisor); ограничить egress (`--network none` / allowlist-прокси); prompt-injection демо: файл с «инструкцией» внутри песочницы — показать, что ущерб локализован.
