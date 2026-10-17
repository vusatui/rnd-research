#!/usr/bin/env bash
# Self-hosted Arize Phoenix (Elastic License 2.0, free to self-host) as the OTLP trace backend + UI.
# UI: http://127.0.0.1:6006   OTLP/HTTP: http://127.0.0.1:6006/v1/traces   OTLP/gRPC: 127.0.0.1:4317
# Ports are bound to localhost only: traces contain prompts, tool arguments and customer data.
set -euo pipefail
IMAGE=${PHOENIX_IMAGE:-arizephoenix/phoenix:latest}   # pin a version for real use, e.g. :version-20.23.0
docker rm -f phoenix >/dev/null 2>&1 || true
docker run -d --name phoenix -p 127.0.0.1:6006:6006 -p 127.0.0.1:4317:4317 "$IMAGE"
for i in $(seq 1 30); do curl -sf -o /dev/null http://127.0.0.1:6006/ && break; sleep 1; done
echo "Phoenix up: http://127.0.0.1:6006  (export OTEL_EXPORTER_OTLP_TRACES_ENDPOINT=http://127.0.0.1:6006/v1/traces)"
