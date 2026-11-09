# One small image for both System One workshops (deep-dive workshop/ and presentation/workshop-lite/).
# Multi-arch base (linux/amd64 + linux/arm64), all Python deps pinned. Build from system-one-models/:
#   docker build -f docker/Dockerfile -t system-one-workshops .
FROM python:3.12.16-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    EMULATOR_HOST=0.0.0.0 \
    EMULATOR_PORT=8787

# No apt packages on purpose: fewer things that can break when building on conference Wi-Fi.
# The curl example runs in a separate pinned curl container (`make curl`).

COPY docker/requirements.lock /tmp/requirements.lock
RUN pip install --no-deps -r /tmp/requirements.lock && rm /tmp/requirements.lock

RUN useradd --create-home --uid 1000 app
WORKDIR /app
COPY --chown=app:app workshop/ /app/workshop/
COPY --chown=app:app presentation/workshop-lite/ /app/workshop-lite/
COPY --chown=app:app docker/*.sh /app/bin/
# never bake keys into the image
RUN rm -f /app/workshop/.env /app/workshop-lite/.env && chmod +x /app/bin/*.sh
USER app

EXPOSE 8787
CMD ["/app/bin/lite.sh"]
