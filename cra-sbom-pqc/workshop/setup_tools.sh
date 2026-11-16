#!/usr/bin/env bash
# Installs the three scanners used by the labs into ./.tools/bin (no root, nothing global). Linux/macOS, amd64/arm64.
# Tested versions (2026-11-16): syft 1.57.1, grype 0.121.3, osv-scanner 2.7.1. Needs curl; osv-scanner via `go install` or release binary.
set -euo pipefail
cd "$(dirname "$0")"
BIN="$PWD/.tools/bin"; mkdir -p "$BIN"
[ -x "$BIN/syft" ]  || curl -sSfL https://raw.githubusercontent.com/anchore/syft/main/install.sh  | sh -s -- -b "$BIN" v1.57.1
[ -x "$BIN/grype" ] || curl -sSfL https://raw.githubusercontent.com/anchore/grype/main/install.sh | sh -s -- -b "$BIN" v0.121.3
if [ ! -x "$BIN/osv-scanner" ]; then
  os=$(uname -s | tr A-Z a-z); arch=$(uname -m); case "$arch" in x86_64) arch=amd64;; aarch64) arch=arm64;; esac
  curl -sSfL -o "$BIN/osv-scanner" "https://github.com/google/osv-scanner/releases/download/v2.7.1/osv-scanner_${os}_${arch}"
  chmod +x "$BIN/osv-scanner"
fi
"$BIN/grype" db update
for t in syft grype osv-scanner; do printf '%s: ' "$t"; "$BIN/$t" --version | head -1; done
command -v openssl >/dev/null && openssl version
