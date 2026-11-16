"""Offline unit tests (no key, no network). Tests that need syft/grype/openssl>=3.5 skip themselves if the tool is missing."""
import json
import re
import shutil
import subprocess
from datetime import datetime, timedelta, timezone

import pytest

from common.paths import SAMPLE, TOOLS
from ex1_sbom.check_sbom import check, summary_pct
from ex1_sbom.enrich import enrich
from ex2_vuln_vex import vex
from ex3_reporting.cra_clock import Case, add_months, utc
from ex3_reporting.draft import advisory_guard
from ex4_crypto_inventory import scan_crypto as sc

UTC = timezone.utc
T0 = datetime(2026, 11, 16, 9, 0, tzinfo=UTC)


# ---- ex1 --------------------------------------------------------------------------------------------------------------------------
def tiny_bom():
    return {"bomFormat": "CycloneDX", "specVersion": "1.6", "version": 1, "serialNumber": "urn:uuid:1",
            "metadata": {"timestamp": "2026-11-16T00:00:00Z", "tools": {"components": [{"name": "t", "version": "1"}]}},
            "components": [{"bom-ref": "a", "type": "library", "name": "a", "version": "1", "purl": "pkg:npm/a@1"}]}


def test_check_sbom_gaps_then_enrich():
    b = tiny_bom()
    r = check(b)["checks"]
    assert r["BSI TR-03183-2 v2.1.0 (SBOM-level)"]["creator with e-mail or URL"] == (0, 1)
    assert r["BSI TR-03183-2 v2.1.0 (per component)"]["SHA-512 hash of the deployable"] == (0, 1)
    lock = {"packages": {"": {}, "node_modules/a": {"version": "1", "integrity": "sha512-AAEC", "resolved": "https://r/a-1.tgz"}}}
    stats = enrich(b, lock, "x@y.example", "X")
    assert stats == {"hashes_added": 1, "uris_added": 1}
    r2 = check(b)["checks"]
    assert r2["BSI TR-03183-2 v2.1.0 (SBOM-level)"]["creator with e-mail or URL"] == (1, 1)
    assert b["components"][0]["hashes"][0]["content"] == "000102"           # base64 'AAEC' -> bytes 00 01 02 -> hex
    assert summary_pct(check(b))["BSI TR-03183-2 v2.1.0 (per component)"] > summary_pct(check(tiny_bom()))["BSI TR-03183-2 v2.1.0 (per component)"]


def test_name_without_contact_is_not_a_creator():
    b = tiny_bom(); b["metadata"]["authors"] = [{"name": "Only A Name"}]
    assert check(b)["checks"]["BSI TR-03183-2 v2.1.0 (SBOM-level)"]["creator with e-mail or URL"] == (0, 1)


# ---- ex2 --------------------------------------------------------------------------------------------------------------------------
def test_vex_candidates_exclude_imported_packages():
    names = {c["name"] for c in vex.candidates()}
    assert "pillow" not in names and "cryptography" not in names and "jsonwebtoken" not in names   # imported by first-party code
    assert {"pyyaml", "requests", "jinja2", "lodash", "minimist", "express"} <= names


def test_openvex_shape():
    g = {"matches": [{"artifact": {"name": "pyyaml", "version": "5.3.1"}, "vulnerability": {"id": "GHSA-x"}}]}
    doc = vex.openvex([{"purl": "pkg:pypi/pyyaml@5.3.1", "name": "pyyaml", "version": "5.3.1"}], g)
    st = doc["statements"][0]
    assert doc["@context"].startswith("https://openvex.dev/ns") and st["status"] == "not_affected"
    assert st["justification"] == "vulnerable_code_not_in_execute_path" and "needs human review" in st["impact_statement"].lower()


# ---- ex3 --------------------------------------------------------------------------------------------------------------------------
def test_deadlines_vulnerability():
    c = Case("vulnerability", T0, corrective_measure_at=T0 + timedelta(days=3))
    d = c.deadlines()
    assert d["early_warning"] == T0 + timedelta(hours=24) and d["notification"] == T0 + timedelta(hours=72)
    assert d["final_report"] == T0 + timedelta(days=17)                       # 14 days after the corrective/mitigating measure


def test_final_report_clock_not_started():
    assert Case("vulnerability", T0).deadlines()["final_report"] is None
    st = {r["step"]: r for r in Case("incident", T0).status(T0)}
    assert st["final_report"]["state"].startswith("NOT STARTED")


def test_incident_final_report_one_month_after_72h_notification():
    c = Case("incident", datetime(2026, 1, 20, 8, tzinfo=UTC), notification_72h_sent_at=datetime(2026, 1, 31, 10, tzinfo=UTC))
    assert c.deadlines()["final_report"] == datetime(2026, 2, 28, 10, tzinfo=UTC)   # calendar-month clamp


def test_add_months_edges():
    assert add_months(datetime(2027, 12, 31, tzinfo=UTC), 2) == datetime(2028, 2, 29, tzinfo=UTC)


def test_status_states():
    c = Case("vulnerability", T0)
    now = T0 + timedelta(hours=30)
    s = {r["step"]: r["state"] for r in c.status(now)}
    assert s["early_warning"] == "OVERDUE" and s["notification"] == "open"
    c.sent["early_warning"] = T0 + timedelta(hours=25)
    assert {r["step"]: r["state"] for r in c.status(now)}["early_warning"] == "SENT LATE"
    c.sent["early_warning"] = T0 + timedelta(hours=23, minutes=59)
    assert {r["step"]: r["state"] for r in c.status(now)}["early_warning"] == "SENT ON TIME"


def test_naive_datetime_rejected():
    with pytest.raises(ValueError):
        Case("vulnerability", datetime(2026, 11, 16, 9, 0))


def test_utc_parse():
    assert utc("2026-11-16T12:00:00+03:00") == T0


def test_advisory_guard_flags_inflation():
    facts = {"cve": "CVE-1", "exploited": True}
    assert set(advisory_guard("A critical flaw allows remote code execution. Act immediately.", facts)) == {"critical", "remote code execution", "immediately"}
    assert advisory_guard("CVE-1 is being exploited. Update.", facts) == []


# ---- ex4 --------------------------------------------------------------------------------------------------------------------------
def test_scan_finds_expected_algorithms():
    fams = {(f["family"], f["file"]) for f in sc.scan(SAMPLE)}
    for exp in (("RSA", "py/app.py"), ("RSA", "web/server.js"), ("RSA", "java/Pairing.java"), ("ECDH", "py/app.py"),
                ("MD5", "py/app.py"), ("SHA-1", "web/server.js"), ("ECDH", "deploy/nginx.conf"), ("RSA", "deploy/sshd_config")):
        assert exp in fams, exp
    assert not any(f["family"] == "RSA" and f["file"].endswith("requirements.txt") for f in sc.scan(SAMPLE))


def test_rsa_key_size_detected():
    bits = {f["key_bits"] for f in sc.scan(SAMPLE) if f["family"] == "RSA" and f["key_bits"]}
    assert {2048, 3072} <= bits


def test_mosca_ranking_depends_on_z():
    f = sc.scan(SAMPLE); assets = json.loads(sc.ASSETS.read_text())["assets"]
    rows = {r["asset"]: r for r in sc.rank(f, assets, [8, 15])}
    tel = rows["session key agreement device<->cloud (telemetry with customer data)"]
    assert (tel["x"], tel["y"]) == (12, 3) and tel["verdict"] == {"8": "MIGRATE NOW", "15": "plan"}   # 12+3 = 15 is not > 15
    assert rows["operator session tokens (JWT RS256)"]["verdict"]["8"] == "plan"                    # short-lived: no harvest risk


def test_cbom_is_valid_cyclonedx_1_6():
    from cyclonedx.schema import SchemaVersion
    from cyclonedx.validation.json import JsonStrictValidator
    bom = sc.cbom(sc.scan(SAMPLE), SAMPLE)
    assert JsonStrictValidator(SchemaVersion.V1_6).validate_str(json.dumps(bom)) is None
    rsa = [c for c in bom["components"] if c["name"] == "RSA"]
    assert rsa and all(c["cryptoProperties"]["algorithmProperties"]["nistQuantumSecurityLevel"] == 0 for c in rsa)


# ---- ex5 / tools -----------------------------------------------------------------------------------------------------------------
def _ossl35():
    if not shutil.which("openssl"):
        return False
    m = re.search(r"OpenSSL (\d+)\.(\d+)", subprocess.run(["openssl", "version"], capture_output=True, text=True).stdout)
    return bool(m) and (int(m[1]), int(m[2])) >= (3, 5)


@pytest.mark.skipif(not _ossl35(), reason="needs OpenSSL >= 3.5")
def test_hybrid_group_is_negotiated_by_default():
    from ex5_pqc_tls import pqc_tls_lab as lab
    lab.CERTS = {"ECDSA-P256": lab.CERTS["ECDSA-P256"]}
    lab.make_certs()
    srv = lab.Server("ECDSA-P256", 15900)
    try:
        r = lab.client(15900, None)
    finally:
        srv.stop()
    assert r["ok"] and r["group"] == "X25519MLKEM768"


@pytest.mark.skipif(not _ossl35(), reason="needs OpenSSL >= 3.5")
def test_ml_kem_768_sizes():
    from ex5_pqc_tls import pqc_tls_lab as lab
    from common.paths import OUT
    k = OUT / "t_mlkem.key"; lab.sh("openssl", "genpkey", "-algorithm", "ML-KEM-768", "-out", str(k))
    pub = OUT / "t_mlkem.pub"; lab.sh("openssl", "pkey", "-in", str(k), "-pubout", "-out", str(pub))
    lab.sh("openssl", "pkeyutl", "-encap", "-pubin", "-inkey", str(pub), "-out", str(OUT / "t_ct"), "-secret", str(OUT / "t_ss"))
    assert (OUT / "t_ct").stat().st_size == 1088 and (OUT / "t_ss").stat().st_size == 32      # FIPS 203 ML-KEM-768


@pytest.mark.skipif(not (TOOLS / "syft").exists() and not shutil.which("syft"), reason="needs syft (./setup_tools.sh)")
def test_syft_finds_pinned_packages(tmp_path):
    from common.paths import tool
    out = tmp_path / "s.json"
    subprocess.run([tool("syft"), f"dir:{SAMPLE}", "-q", "-o", f"cyclonedx-json={out}"], check=True)
    comps = {(c["name"], c.get("version")) for c in json.loads(out.read_text())["components"]}
    assert {("lodash", "4.17.15"), ("pillow", "8.1.0"), ("cryptography", "3.3.2")} <= comps
