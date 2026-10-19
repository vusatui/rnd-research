from pathlib import Path

WORKSHOP = Path(__file__).resolve().parent.parent
OUT = WORKSHOP / "out"
OUT.mkdir(exist_ok=True)
