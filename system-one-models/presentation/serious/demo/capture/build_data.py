#!/usr/bin/env python3
"""Pack the REAL source files and the recorded runs into ../remotion/src/data.json for the replay.

Files are read from the repo as they are now and syntax-highlighted with Pygments (token classes
only; colours live in the video theme). Runs come from ../runs/*.json written by capture.py.
   pip install pygments && python3 build_data.py"""
import glob, json, os
from pygments import lex
from pygments.lexers import PythonLexer, BashLexer, MakefileLexer, TextLexer
from pygments.token import Token

HERE = os.path.dirname(os.path.abspath(__file__))
S1 = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))
OUT = os.path.join(HERE, "..", "remotion", "src", "data.json")

FILES = ["presentation/workshop-lite/jev_client.py", "presentation/workshop-lite/jev_emulator.py",
         "presentation/workshop-lite/mock_rules.py", "presentation/workshop-lite/curl_example.sh",
         "presentation/workshop-lite/README.md", "workshop/ex3_cascade/cascade.py", "Makefile"]


def cls(tt):
    for name, t in [("comment", Token.Comment), ("string", Token.Literal.String), ("number", Token.Literal.Number),
                    ("keyword", Token.Keyword), ("builtin", Token.Name.Builtin), ("func", Token.Name.Function),
                    ("deco", Token.Name.Decorator), ("op", Token.Operator), ("var", Token.Name.Variable)]:
        if tt in t:
            return name
    return ""


def tokens(path, text):
    lexer = PythonLexer() if path.endswith(".py") else BashLexer() if path.endswith(".sh") else \
        MakefileLexer() if path.endswith("Makefile") else TextLexer()
    lines, cur = [], []
    for tt, val in lex(text, lexer):
        c = cls(tt)
        parts = val.split("\n")
        for i, p in enumerate(parts):
            if i:
                lines.append(cur); cur = []
            if p:
                if cur and cur[-1][0] == c:
                    cur[-1][1] += p
                else:
                    cur.append([c, p])
    if cur:
        lines.append(cur)
    while lines and not lines[-1]:
        lines.pop()
    return lines


files = {}
for f in FILES:
    text = open(os.path.join(S1, f)).read().expandtabs(4)
    files[f] = tokens(f, text)

tree = sorted(os.listdir(os.path.join(S1, "presentation", "workshop-lite")))
tree = [t for t in tree if not t.startswith(".") or t == ".env.example"]
runs = {os.path.basename(p)[:-5]: json.load(open(p)) for p in sorted(glob.glob(os.path.join(HERE, "..", "runs", "*.json")))}
json.dump({"files": files, "workshopLite": tree, "runs": runs}, open(OUT, "w"))
print("data.json:", {k: len(v) for k, v in files.items()}, "runs:", list(runs))
