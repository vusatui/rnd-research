FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive DISPLAY=:1 RES=1280x800x24 \
    PLAYWRIGHT_BROWSERS_PATH=/opt/pw-browsers
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb fluxbox x11vnc novnc websockify xdotool scrot python3 python3-pip python3-venv \
    ca-certificates fonts-dejavu curl && rm -rf /var/lib/apt/lists/*
# Браузеры Playwright ставим в общий путь, иначе они окажутся в /root/.cache и будут недоступны пользователю agent
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install --no-cache-dir playwright \
    && /opt/venv/bin/playwright install --with-deps chromium \
    && chmod -R a+rX /opt/pw-browsers && rm -rf /var/lib/apt/lists/*
ENV PATH=/opt/venv/bin:$PATH
RUN useradd -m agent
COPY start.sh /start.sh
COPY browse.py /home/agent/browse.py
RUN chmod +x /start.sh
USER agent
WORKDIR /home/agent
EXPOSE 6080
CMD ["/start.sh"]
