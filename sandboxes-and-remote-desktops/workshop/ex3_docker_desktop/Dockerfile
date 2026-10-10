FROM ubuntu:24.04
ENV DEBIAN_FRONTEND=noninteractive DISPLAY=:1 RES=1280x800x24
RUN apt-get update && apt-get install -y --no-install-recommends \
    xvfb fluxbox x11vnc novnc websockify xdotool scrot python3 python3-pip python3-venv \
    ca-certificates fonts-dejavu && rm -rf /var/lib/apt/lists/*
RUN python3 -m venv /opt/venv && /opt/venv/bin/pip install playwright && /opt/venv/bin/playwright install --with-deps chromium
ENV PATH=/opt/venv/bin:$PATH
RUN useradd -m agent
COPY start.sh /start.sh
COPY browse.py /home/agent/browse.py
RUN chmod +x /start.sh
USER agent
EXPOSE 6080
CMD ["/start.sh"]
