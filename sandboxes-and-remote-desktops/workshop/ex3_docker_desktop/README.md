# Упр. 3: свой рабочий стол для агента (Docker + Xvfb + fluxbox + x11vnc + noVNC + Chromium)

Проверено 10.10.2026 на Debian 13, Docker 29.9 (образ ubuntu:24.04, Playwright Chromium 153).

```bash
docker build -t agent-desktop .
docker run --rm -d --name desk -p 127.0.0.1:6080:6080 --shm-size=1g --memory=2g --cpus=2 agent-desktop
# опционально: --runtime=runsc (gVisor), --cap-drop=ALL
# если порт 6080 занят, публикуйте другой: -p 127.0.0.1:16080:6080
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:6080/vnc.html   # 200
# открыть в браузере: http://localhost:6080/vnc.html -> Connect (без пароля)
docker exec desk ps -eo comm | sort -u          # Xvfb, fluxbox, x11vnc, websockify, chrome
docker exec desk python3 /home/agent/browse.py  # headed Playwright, видно в noVNC; печатает 5 заголовков HN
python3 -c "
from desktop_tools import DockerDesktop as D
import time
d=D(); d.left_click(600,60); d.press('ctrl+l'); d.write('https://example.com'); d.press('Return')
time.sleep(5); open('desk.png','wb').write(d.screenshot())"
docker rm -f desk
```

`desktop_tools.py` — примитивы screenshot/left_click/right_click/double_click/move_mouse/write/press/scroll/wait
через `docker exec` с тем же интерфейсом, что у `e2b_desktop.Sandbox`, чтобы подключить контейнер к ex4.
Пользователь, запускающий скрипт, должен иметь доступ к docker (группа `docker`).

Пример результата: `../../assets/ex3-desktop.png`.

Заметки:
- x11vnc без пароля и слушает только localhost внутри контейнера; наружу публикуйте порт только на 127.0.0.1.
- Если Docker запущен внутри контейнера/VM без поддержки вложенного overlayfs (ошибка `mount source: "overlay" ... invalid argument`
  при сборке), используйте `{"storage-driver":"vfs"}` в `/etc/docker/daemon.json`.
