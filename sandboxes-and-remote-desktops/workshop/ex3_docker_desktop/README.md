# Exercise 3: your own desktop for an agent (Docker + Xvfb + fluxbox + x11vnc + noVNC + Chromium)

Verified 2026-10-10 on Debian 13, Docker 29.9 (image ubuntu:24.04, Playwright Chromium 153).

```bash
docker build -t agent-desktop .
docker run --rm -d --name desk -p 127.0.0.1:6080:6080 --shm-size=1g --memory=2g --cpus=2 agent-desktop
# optional: --runtime=runsc (gVisor), --cap-drop=ALL
# if port 6080 is taken, publish a different one: -p 127.0.0.1:16080:6080
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:6080/vnc.html   # 200
# open in a browser: http://localhost:6080/vnc.html -> Connect (no password)
docker exec desk ps -eo comm | sort -u          # Xvfb, fluxbox, x11vnc, websockify, chrome
docker exec desk python3 /home/agent/browse.py  # headed Playwright, visible in noVNC; prints 5 HN headlines
python3 -c "
from desktop_tools import DockerDesktop as D
import time
d=D(); d.left_click(600,60); d.press('ctrl+l'); d.write('https://example.com'); d.press('Return')
time.sleep(5); open('desk.png','wb').write(d.screenshot())"
docker rm -f desk
```

`desktop_tools.py` provides screenshot/left_click/right_click/double_click/move_mouse/write/press/scroll/wait primitives
via `docker exec` with the same interface as `e2b_desktop.Sandbox`, so the container can be plugged into ex4.
The user running the script needs Docker access (the `docker` group).

Example output: `../../assets/ex3-desktop.png`.

Notes:
- x11vnc has no password and listens only on localhost inside the container; publish the port only on 127.0.0.1.
- If Docker runs inside a container/VM without nested overlayfs support (error `mount source: "overlay" ... invalid argument`
  during build), use `{"storage-driver":"vfs"}` в `/etc/docker/daemon.json`.
