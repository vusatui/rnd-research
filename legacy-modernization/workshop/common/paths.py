import pathlib

WORKSHOP = pathlib.Path(__file__).resolve().parent.parent
CARDDEMO = WORKSHOP / "vendor" / "carddemo"
APP = CARDDEMO / "app"
CBACT04C = APP / "cbl" / "CBACT04C.cbl"
OUT = WORKSHOP / "out"
OUT.mkdir(exist_ok=True)
