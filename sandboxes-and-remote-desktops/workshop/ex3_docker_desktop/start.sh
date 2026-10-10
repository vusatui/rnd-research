#!/bin/bash
set -e
Xvfb :1 -screen 0 "$RES" -nolisten tcp &
for i in $(seq 1 50); do [ -e /tmp/.X11-unix/X1 ] && break; sleep 0.1; done
fluxbox >/dev/null 2>&1 &
x11vnc -display :1 -forever -shared -nopw -rfbport 5900 -localhost -quiet &
websockify --web /usr/share/novnc 6080 localhost:5900 >/dev/null 2>&1 &
# Chromium (из Playwright) на рабочем столе, чтобы агенту было что кликать
CHROME=$(ls -d /opt/pw-browsers/chromium-*/chrome-linux*/chrome | head -1)
"$CHROME" --no-sandbox --no-first-run --disable-dev-shm-usage --window-size=1200,750 \
  --user-data-dir=/tmp/chrome-profile about:blank >/dev/null 2>&1 &
echo "noVNC: http://localhost:6080/vnc.html"
wait
