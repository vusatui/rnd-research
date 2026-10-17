"""Fixed-width record layouts from the CardDemo copybooks + zoned-decimal codec.

COBOL `PIC S9(n)V99` DISPLAY fields store the sign in the last byte ("overpunch").
On z/OS (and with GnuCOBOL -fsign=EBCDIC) '{','A'..'I' mean +0..+9 and '}','J'..'R' mean -0..-9.
Getting this wrong is the classic "below the business rules" failure: a modern
service that writes "-1025.00" instead of "00000102}" breaks every downstream consumer.
"""
from __future__ import annotations

from dataclasses import dataclass
from decimal import Decimal

_POS = "{ABCDEFGHI"
_NEG = "}JKLMNOPQR"


def decode_zoned(text: str, scale: int) -> Decimal:
    last = text[-1]
    if last in _POS:
        digit, sign = _POS.index(last), 1
    elif last in _NEG:
        digit, sign = _NEG.index(last), -1
    elif last.isdigit():  # unsigned
        digit, sign = int(last), 1
    else:
        raise ValueError(f"bad zoned decimal {text!r}")
    digits = int(text[:-1] + str(digit))
    return Decimal(sign * digits).scaleb(-scale)


def encode_zoned(value: Decimal, int_digits: int, scale: int) -> str:
    """Encode like a COBOL MOVE into PIC S9(int_digits)V9(scale): truncate, never round."""
    q = int((abs(value) * (10 ** scale)).to_integral_value(rounding="ROUND_DOWN"))
    width = int_digits + scale
    s = str(q % (10 ** width)).rjust(width, "0")  # high-order truncation, like COBOL
    table = _NEG if value < 0 and q != 0 else _POS
    return s[:-1] + table[int(s[-1])]


@dataclass(frozen=True)
class Field:
    name: str
    start: int  # 1-based like COBOL docs
    length: int
    kind: str = "X"  # X = alphanumeric, 9 = unsigned display, S = signed zoned
    scale: int = 0


def _layout(*spec):
    pos, out = 1, []
    for name, length, kind, scale in spec:
        out.append(Field(name, pos, length, kind, scale))
        pos += length
    return out, pos - 1


# CVACT01Y ACCOUNT-RECORD (300)
ACCOUNT, ACCOUNT_LEN = _layout(
    ("acct_id", 11, "9", 0), ("active_status", 1, "X", 0), ("curr_bal", 12, "S", 2),
    ("credit_limit", 12, "S", 2), ("cash_credit_limit", 12, "S", 2), ("open_date", 10, "X", 0),
    ("expiration_date", 10, "X", 0), ("reissue_date", 10, "X", 0), ("curr_cyc_credit", 12, "S", 2),
    ("curr_cyc_debit", 12, "S", 2), ("addr_zip", 10, "X", 0), ("group_id", 10, "X", 0),
    ("filler", 178, "X", 0))
# CVTRA01Y TRAN-CAT-BAL-RECORD (50)
TCATBAL, TCATBAL_LEN = _layout(
    ("acct_id", 11, "9", 0), ("type_cd", 2, "X", 0), ("cat_cd", 4, "9", 0),
    ("balance", 11, "S", 2), ("filler", 22, "X", 0))
# CVACT03Y CARD-XREF-RECORD (50)
XREF, XREF_LEN = _layout(
    ("card_num", 16, "X", 0), ("cust_id", 9, "9", 0), ("acct_id", 11, "9", 0), ("filler", 14, "X", 0))
# CVTRA02Y DIS-GROUP-RECORD (50)
DISCGRP, DISCGRP_LEN = _layout(
    ("group_id", 10, "X", 0), ("type_cd", 2, "X", 0), ("cat_cd", 4, "9", 0),
    ("int_rate", 6, "S", 2), ("filler", 28, "X", 0))
# CVTRA05Y TRAN-RECORD (350)
TRAN, TRAN_LEN = _layout(
    ("tran_id", 16, "X", 0), ("type_cd", 2, "X", 0), ("cat_cd", 4, "9", 0), ("source", 10, "X", 0),
    ("desc", 100, "X", 0), ("amount", 11, "S", 2), ("merchant_id", 9, "9", 0),
    ("merchant_name", 50, "X", 0), ("merchant_city", 50, "X", 0), ("merchant_zip", 10, "X", 0),
    ("card_num", 16, "X", 0), ("orig_ts", 26, "X", 0), ("proc_ts", 26, "X", 0), ("filler", 20, "X", 0))


def parse(line: str, layout) -> dict:
    out = {}
    for f in layout:
        raw = line[f.start - 1: f.start - 1 + f.length]
        if f.kind == "S":
            out[f.name] = decode_zoned(raw, f.scale)
        elif f.kind == "9":
            out[f.name] = raw
        else:
            out[f.name] = raw.rstrip()
    return out


def render(rec: dict, layout) -> str:
    parts = []
    for f in layout:
        v = rec.get(f.name, "")
        if f.kind == "S":
            parts.append(encode_zoned(Decimal(v or 0), f.length - f.scale, f.scale))
        elif f.kind == "9":
            parts.append(str(v or 0).rjust(f.length, "0")[-f.length:])
        else:
            parts.append(str(v or "").ljust(f.length)[: f.length])
    return "".join(parts)


def read_fixed(path, length: int) -> list[str]:
    """Read a CardDemo ASCII extract: strip CR/LF, right-pad to the record length."""
    with open(path, encoding="latin-1") as fh:
        return [ln.rstrip("\r\n").ljust(length)[:length] for ln in fh if ln.strip("\r\n")]
