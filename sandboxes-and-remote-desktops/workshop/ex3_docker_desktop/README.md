```bash
docker build -t agent-desktop .
docker run --rm -d --name desk -p 6080:6080 --shm-size=1g --memory=2g --cpus=2 agent-desktop
# опционально: --runtime=runsc (gVisor), --cap-drop=ALL
open http://localhost:6080/vnc.html
docker exec desk python3 /home/agent/browse.py           # смотрим в noVNC
docker exec desk bash -c 'xdotool mousemove 400 300 click 1; scrot /tmp/s.png'
docker cp desk:/tmp/s.png .
```
`desktop_tools.py` — те же примитивы (screenshot/click/type) через `docker exec`, чтобы подключить контейнер к ex4.
