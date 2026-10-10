#!/bin/bash
set -e
Xvfb :1 -screen 0 $RES &
sleep 1
fluxbox &
x11vnc -display :1 -forever -shared -nopw -rfbport 5900 -quiet &
websockify --web /usr/share/novnc 6080 localhost:5900 &
echo "noVNC: http://localhost:6080/vnc.html"
wait
