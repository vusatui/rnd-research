#!/usr/bin/env bash
docker rm -f finops-litellm finops-pg >/dev/null 2>&1 || true
echo "stopped (spend data in Postgres is discarded)"
