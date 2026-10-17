#!/usr/bin/env bash
# Compiles the untouched CardDemo program CBACT04C plus our harness shims with GnuCOBOL.
# -std=ibm      : IBM Enterprise COBOL dialect (ASSIGN names are DD names, binary truncation)
# -fsign=EBCDIC : zoned-decimal sign overpunch as on z/OS ('{' = +0, '}' = -0, 'J'..'R' = -1..-9)
set -euo pipefail
HERE="$(cd "$(dirname "$0")" && pwd)"
SRC="$HERE/../vendor/carddemo/app"
OUT="$HERE/build"; mkdir -p "$OUT"
FLAGS=(-std=ibm -fsign=EBCDIC -I "$SRC/cpy" -Wno-others)
cobc "${FLAGS[@]}" -m -o "$OUT/CBACT04C.so" "$SRC/cbl/CBACT04C.cbl"
cobc "${FLAGS[@]}" -m -o "$OUT/CEE3ABD.so"  "$HERE/shims/CEE3ABD.cbl"
cobc "${FLAGS[@]}" -x -o "$OUT/runparm"     "$HERE/shims/RUNPARM.cbl"
cobc "${FLAGS[@]}" -x -o "$OUT/loadksds"    "$HERE/tools/LOADKSDS.cbl"
cobc "${FLAGS[@]}" -x -o "$OUT/dumpacct"    "$HERE/tools/DUMPACCT.cbl"
echo "built: $(ls "$OUT" | tr '\n' ' ')"
