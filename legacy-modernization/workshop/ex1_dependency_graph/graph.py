"""Exercise 1: legacy code -> dependency graph (deterministic, no LLM required).

Scans the CardDemo tree (COBOL, copybooks, JCL, BMS) and builds a graph:
  JCL job --runs--> program --copies--> copybook
  program --calls/xctl/link--> program
  program --reads/writes--> dataset (batch: SELECT/ASSIGN + JCL DD; online: EXEC CICS ... DATASET/FILE)
Outputs out/graph.json and a Mermaid diagram for one program's neighbourhood.

Usage:
  python ex1_dependency_graph/graph.py                     # stats + out/graph.json
  python ex1_dependency_graph/graph.py --focus CBACT04C    # Mermaid neighbourhood -> out/CBACT04C.mmd
  python ex1_dependency_graph/graph.py --impact ACCTDATA   # who touches a dataset?
  python ex1_dependency_graph/graph.py --focus CBACT04C --explain   # + LLM summary grounded in the graph
"""
from __future__ import annotations

import argparse
import collections
import json
import pathlib
import re
import sys

sys.path.insert(0, str(pathlib.Path(__file__).resolve().parent.parent))
from common.paths import APP, OUT  # noqa: E402


def code_lines(path: pathlib.Path) -> list[str]:
    """Fixed-format COBOL: drop sequence area (1-6), comments (col 7 = '*' or '/'), cols 73+."""
    out = []
    for raw in path.read_text(encoding="latin-1").splitlines():
        if len(raw) > 6 and raw[6] in "*/":
            out.append("")
            continue
        out.append(raw[7:72] if len(raw) > 7 else "")
    return out


def literal_values(text: str) -> dict[str, str]:
    """Map data names to VALUE 'literal' so we can resolve dynamic names like LIT-ACCTFILENAME."""
    vals = {}
    for m in re.finditer(r"\b(\d\d)\s+([A-Z0-9-]+)\s+PIC\s+X\(\d+\)\s+VALUE\s+'([^']*)'", text):
        vals[m.group(2)] = m.group(3).strip()
    return vals


def analyse_program(path: pathlib.Path) -> dict:
    text = "\n".join(code_lines(path)).upper()
    flat = re.sub(r"\s+", " ", text)
    vals = literal_values(text)
    prog = {"copies": sorted(set(re.findall(r"\bCOPY\s+([A-Z0-9-]+)", flat))),
            "calls": [], "dynamic": [], "files": [], "cics_files": [], "sql": "EXEC SQL" in flat}
    for target in re.findall(r"\bCALL\s+'([A-Z0-9-]+)'", flat) + re.findall(r'\bCALL\s+"([A-Z0-9-]+)"', flat):
        prog["calls"].append(("call", target))
    for verb, arg in re.findall(r"\b(XCTL|LINK)\s+PROGRAM\s*\(\s*([^)]+?)\s*\)", flat):
        arg = arg.strip()
        if arg.startswith("'"):
            prog["calls"].append((verb.lower(), arg.strip("'")))
        elif arg in vals:
            prog["calls"].append((verb.lower(), vals[arg]))
        else:
            prog["dynamic"].append(f"{verb} PROGRAM({arg})")
    for name, dd, rest in re.findall(r"\bSELECT\s+([A-Z0-9-]+)\s+ASSIGN\s+TO\s+([A-Z0-9-]+)(.*?)\.", flat):
        prog["files"].append({"fd": name, "dd": dd})
    for verb, arg in re.findall(r"\b(READ|WRITE|REWRITE|DELETE|STARTBR|READNEXT|READPREV)\s+(?:DATASET|FILE)\s*\(\s*([^)]+?)\s*\)", flat):
        ds = arg.strip("'") if arg.startswith("'") else vals.get(arg, f"?{arg}")
        prog["cics_files"].append({"verb": verb, "dataset": ds})
    # batch file direction from OPEN statements
    opens = {}
    for mode, names in re.findall(r"\bOPEN\s+(INPUT|OUTPUT|I-O|EXTEND)\s+([A-Z0-9- ]+?)(?=\s+(?:IF|MOVE|PERFORM|DISPLAY|END-|EVALUATE|OPEN|READ)|\.|$)", flat):
        for n in names.split():
            opens[n] = mode
    for f in prog["files"]:
        f["mode"] = opens.get(f["fd"], "?")
    prog["calls"] = sorted(set(map(tuple, prog["calls"])))
    return prog


def analyse_jcl(path: pathlib.Path) -> list[dict]:
    steps, cur = [], None
    for line in path.read_text(encoding="latin-1").splitlines():
        if line.startswith("//*") or not line.startswith("//"):
            continue
        m = re.match(r"//(\S+)\s+EXEC\s+(?:PGM=)?([A-Z0-9$#@]+)", line)
        if m and "PROC=" not in line:
            cur = {"step": m.group(1), "pgm": m.group(2), "dds": {}}
            steps.append(cur)
            continue
        m = re.match(r"//(\S+)\s+DD\s+(.*)", line)
        if m and cur is not None:
            cur["_last_dd"] = m.group(1)
            dsn = re.search(r"DSN=([A-Z0-9.$#@()+-]+)", m.group(2))
            if dsn:
                cur["dds"][m.group(1)] = dsn.group(1)
            continue
        dsn = re.search(r"DSN=([A-Z0-9.$#@()+-]+)", line)  # continuation line
        if dsn and cur is not None and cur.get("_last_dd"):
            cur["dds"].setdefault(cur["_last_dd"], dsn.group(1))
    for s in steps:
        s.pop("_last_dd", None)
    return steps


def short_ds(dsn: str) -> str:
    """AWS.M2.CARDDEMO.ACCTDATA.VSAM.KSDS -> ACCTDATA (drop HLQs and VSAM/GDG suffixes)."""
    parts = [p for p in re.sub(r"\(.*\)", "", dsn).split(".") if p not in {"AWS", "M2", "CARDDEMO"}]
    return parts[0] if parts else dsn


def build_graph(app: pathlib.Path = APP) -> dict:
    nodes, edges = {}, set()

    def node(nid, kind):
        nodes.setdefault(nid, {"id": nid, "kind": kind})

    programs = {}
    for p in sorted(list(app.glob("cbl/*.cbl")) + list(app.glob("cbl/*.CBL"))):
        name = p.stem.upper()
        programs[name] = analyse_program(p)
        node(name, "program")
        info = programs[name]
        for c in info["copies"]:
            node(c, "copybook"); edges.add((name, c, "copies"))
        for verb, tgt in info["calls"]:
            node(tgt, "program" if (app / "cbl" / f"{tgt}.cbl").exists() else "external")
            edges.add((name, tgt, verb))
        for cf in info["cics_files"]:
            ds = cf["dataset"].upper()
            node(ds, "dataset")
            rel = "reads" if cf["verb"] in {"READ", "STARTBR", "READNEXT", "READPREV"} else "writes"
            edges.add((name, ds, rel))
        nodes[name]["dynamic_calls"] = info["dynamic"]
        nodes[name]["sql"] = info["sql"]
    jobs = {}
    for j in sorted(list(app.glob("jcl/*.jcl")) + list(app.glob("jcl/*.JCL"))):
        steps = analyse_jcl(j)
        if not steps:
            continue
        job = f"JOB:{j.stem.upper()}"
        jobs[job] = steps
        node(job, "job")
        for s in steps:
            pgm = s["pgm"]
            node(pgm, "program" if pgm in programs else "utility")
            edges.add((job, pgm, "runs"))
            files = {f["dd"]: f for f in programs.get(pgm, {}).get("files", [])}
            for dd, dsn in s["dds"].items():
                if dd in {"STEPLIB", "SYSPRINT", "SYSOUT", "SYSIN", "SYSUDUMP"}:
                    continue
                ds = short_ds(dsn)
                node(ds, "dataset")
                if pgm in programs and dd not in files:
                    rel = "dd-only"  # DD in JCL but no SELECT in the program (e.g. a VSAM AIX path)
                else:
                    mode = files.get(dd, {}).get("mode", "?")
                    rel = {"INPUT": "reads", "OUTPUT": "writes", "EXTEND": "writes", "I-O": "updates"}.get(mode, "uses")
                edges.add((pgm, ds, rel))
    return {"nodes": sorted(nodes.values(), key=lambda n: n["id"]),
            "edges": [dict(src=a, dst=b, rel=r) for a, b, r in sorted(edges)], "jobs": jobs}


def neighbourhood(g: dict, focus: str) -> list[dict]:
    return [e for e in g["edges"] if focus in (e["src"], e["dst"])]


def mermaid(edges: list[dict]) -> str:
    lines = ["graph LR"]
    sid = lambda s: re.sub(r"[^A-Za-z0-9]", "_", s)  # noqa: E731
    for e in edges:
        lines.append(f'  {sid(e["src"])}["{e["src"]}"] -->|{e["rel"]}| {sid(e["dst"])}["{e["dst"]}"]')
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--focus")
    ap.add_argument("--impact")
    ap.add_argument("--explain", action="store_true")
    a = ap.parse_args()
    g = build_graph()
    (OUT / "graph.json").write_text(json.dumps(g, indent=1))
    kinds = collections.Counter(n["kind"] for n in g["nodes"])
    rels = collections.Counter(e["rel"] for e in g["edges"])
    dyn = [n["id"] for n in g["nodes"] if n.get("dynamic_calls")]
    print(f"nodes: {dict(kinds)}")
    print(f"edges: {dict(rels)}")
    print(f"programs with unresolved dynamic XCTL/LINK targets: {len(dyn)} -> {', '.join(dyn[:8])}{' ...' if len(dyn) > 8 else ''}")
    print("wrote out/graph.json")
    if a.impact:
        ds = a.impact.upper()
        hits = [e for e in g["edges"] if e["dst"] == ds]
        print(f"\nimpact analysis for dataset {ds}:")
        for e in hits:
            jobs = [j for j in g["edges"] if j["dst"] == e["src"] and j["rel"] == "runs"]
            names = [j["src"] for j in jobs]
            more = f" +{len(names) - 3} more" if len(names) > 3 else ""
            via = f" (batch, via {', '.join(names[:3])}{more})" if jobs else " (online/CICS)"
            print(f"  {e['src']:10} {e['rel']:8}{via}")
    if a.focus:
        f = a.focus.upper()
        edges = neighbourhood(g, f)
        (OUT / f"{f}.mmd").write_text(mermaid(edges))
        print(f"\n{f}: {len(edges)} edges -> out/{f}.mmd\n" + mermaid(edges))
        if a.explain:
            from common.llm import chat
            src = (APP / "cbl" / f"{f}.cbl").read_text(encoding="latin-1")
            prompt = ("You are a mainframe modernization analyst. Using ONLY the dependency edges and the source "
                      "below, write a 6-bullet summary of what this program does, which datasets it reads and "
                      "updates, and what would break downstream if it changed. Cite edges you rely on.\n\n"
                      f"EDGES:\n{json.dumps(edges)}\n\nSOURCE:\n{src}")
            text, model = chat([{"role": "user", "content": prompt}], max_tokens=1500)
            print(f"--- LLM summary ({model}) ---\n{text}")


if __name__ == "__main__":
    main()
