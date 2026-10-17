#!/usr/bin/env bash
# Fetches AWS CardDemo (Apache-2.0) at a pinned commit and checks the toolchain.
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
CARDDEMO_COMMIT="${CARDDEMO_COMMIT:-59cc6c2fd7ebd7ef7925cad552a01a4b8b6e4d5e}"
DEST="$HERE/vendor/carddemo"
if [ ! -d "$DEST/.git" ]; then
  git clone --quiet https://github.com/aws-samples/aws-mainframe-modernization-carddemo.git "$DEST"
fi
git -C "$DEST" -c advice.detachedHead=false checkout --quiet "$CARDDEMO_COMMIT"
echo "CardDemo at $(git -C "$DEST" rev-parse --short HEAD) -> $DEST"
command -v cobc >/dev/null || { echo "GnuCOBOL missing: sudo apt-get install gnucobol3 (or brew install gnucobol)"; exit 1; }
cobc --version | head -1
cobc --info | grep -i "indexed file handler" || true
python3 -c 'import sys; assert sys.version_info >= (3, 10), "need Python 3.10+"'
echo "OK. Next: python -m pip install -r requirements.txt"
