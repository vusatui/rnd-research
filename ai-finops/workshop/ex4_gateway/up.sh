#!/usr/bin/env bash
# Start a self-hosted LiteLLM proxy + Postgres (plain `docker run`, no compose needed).
# Proxy: http://127.0.0.1:4000 (UI at /ui). Needs OPENROUTER_API_KEY in the environment or ../.env.
set -euo pipefail
cd "$(dirname "$0")"
[ -f ../.env ] && set -a && . ../.env && set +a
: "${OPENROUTER_API_KEY:?set OPENROUTER_API_KEY}"
MASTER="${LITELLM_MASTER_KEY:-sk-workshop-master-change-me}"
IMAGE="${LITELLM_IMAGE:-ghcr.io/berriai/litellm:v1.106.0}"
docker rm -f finops-pg finops-litellm >/dev/null 2>&1 || true
# Host networking: on some Docker setups user-defined networks have no DNS. Postgres listens on 127.0.0.1:${PG_PORT}.
PG_PORT="${PG_PORT:-55432}"
docker run -d --name finops-pg --network host -e POSTGRES_USER=llm -e POSTGRES_PASSWORD=llm -e PGPORT="$PG_PORT" \
  -e POSTGRES_DB=litellm postgres:16-alpine -c listen_addresses=127.0.0.1 >/dev/null
for i in $(seq 1 60); do
  docker exec finops-pg pg_isready -U llm -h 127.0.0.1 -p "$PG_PORT" >/dev/null 2>&1 && break
  if [ "$(docker inspect -f '{{.State.Running}}' finops-pg 2>/dev/null)" != "true" ] || [ "$i" = 60 ]; then
    echo "Postgres did not start (port $PG_PORT busy? try PG_PORT=55433 ./up.sh):"; docker logs --tail 5 finops-pg; exit 1
  fi
  sleep 1
done
docker run -d --name finops-litellm --network host \
  -e OPENROUTER_API_KEY -e LITELLM_MASTER_KEY="$MASTER" \
  -e DATABASE_URL="postgresql://llm:llm@127.0.0.1:${PG_PORT}/litellm" \
  -e STORE_MODEL_IN_DB=False \
  -v "$PWD/litellm_config.yaml:/app/config.yaml:ro" "$IMAGE" --config /app/config.yaml --host 127.0.0.1 --port 4000 >/dev/null
echo -n "waiting for LiteLLM (first start runs DB migrations, can take a few minutes)"
for i in $(seq 1 180); do
  if curl -sf http://127.0.0.1:4000/health/liveliness >/dev/null; then echo " up: http://127.0.0.1:4000"; exit 0; fi
  echo -n "."; sleep 2
done
echo; docker logs --tail 50 finops-litellm; exit 1
