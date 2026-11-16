import os
from pathlib import Path

WORKSHOP = Path(__file__).resolve().parent.parent
OUT = WORKSHOP / "out"
OUT.mkdir(exist_ok=True)
RESULTS = WORKSHOP / "results"
DATA = WORKSHOP / "data"
SAMPLE = WORKSHOP / "sample_app"
TOOLS = WORKSHOP / ".tools" / "bin"


def tool(name: str) -> str:
    """Path of a scanner: ./.tools/bin first (setup_tools.sh), then $PATH."""
    import shutil
    p = TOOLS / name
    if p.exists():
        return str(p)
    found = shutil.which(name)
    if not found:
        raise SystemExit(f"{name} not found: run ./setup_tools.sh (installs syft, grype, osv-scanner into .tools/bin)")
    return found
