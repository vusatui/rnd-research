"""Lab 5: hybrid ML-KEM in TLS 1.3 and what post-quantum signatures cost - measured with OpenSSL >= 3.5, all on localhost.

    python ex5_pqc_tls/pqc_tls_lab.py [--n 30]

Part A  key exchange: for each client group (classical, hybrid, pure ML-KEM) x server certificate type, run N handshakes through a
        byte-counting TCP proxy: negotiated group, bytes client->server and server->client, median wall time.
Part B  interop: a hybrid-offering client against a server that only knows X25519 (fallback) and a client that offers ONLY the
        hybrid group (hard failure) - the two things that actually bite during migration.
Part C  signature/key sizes: public key, signature and certificate sizes for RSA-2048, ECDSA P-256, Ed25519, ML-DSA-44/65/87; ML-KEM sizes.
Part D  "inventory by probing": what a network probe sees (group + certificate signature type) for each local endpoint.

Timing includes the start of one `openssl s_client` process (~constant offset); compare rows, do not read absolute numbers as TLS latency.
Self-signed throw-away certificates in out/; nothing here is a production configuration.
"""
import argparse
import json
import re
import socket
import statistics
import subprocess
import sys
import threading
import time
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from common.paths import OUT, RESULTS  # noqa: E402

PKI = OUT / "pki"
CERTS = {"RSA-2048": ["-newkey", "rsa:2048"], "ECDSA-P256": ["-newkey", "ec", "-pkeyopt", "ec_paramgen_curve:P-256"],
         "Ed25519": ["-newkey", "ed25519"], "ML-DSA-44": ["-newkey", "ML-DSA-44"], "ML-DSA-65": ["-newkey", "ML-DSA-65"],
         "ML-DSA-87": ["-newkey", "ML-DSA-87"]}
GROUPS = ["X25519", "secp256r1", "X25519MLKEM768", "SecP256r1MLKEM768", "MLKEM768"]
BASE_PORT = 15000
ALL_GROUPS = ":".join(["X25519MLKEM768", "SecP256r1MLKEM768", "MLKEM768", "X25519", "secp256r1"])   # server must list non-default groups explicitly


def sh(*a, inp: bytes | None = None, check=True) -> subprocess.CompletedProcess:
    return subprocess.run(list(a), input=inp, capture_output=True, check=check)


def openssl_version() -> str:
    return sh("openssl", "version").stdout.decode().strip()


def make_certs():
    PKI.mkdir(exist_ok=True)
    for name, args in CERTS.items():
        k, c = PKI / f"{name}.key", PKI / f"{name}.pem"
        if not c.exists():
            sh("openssl", "req", "-x509", *args, "-keyout", str(k), "-out", str(c), "-nodes", "-subj", "/CN=localhost", "-days", "2")


class Server:
    def __init__(self, cert: str, port: int, groups: str | None = None):
        cmd = ["openssl", "s_server", "-accept", str(port), "-cert", str(PKI / f"{cert}.pem"), "-key", str(PKI / f"{cert}.key"),
               "-tls1_3", "-www", "-quiet"]
        if groups:
            cmd += ["-groups", groups]
        self.p = subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        for _ in range(50):
            try:
                socket.create_connection(("127.0.0.1", port), timeout=0.2).close(); break
            except OSError:
                time.sleep(0.1)

    def stop(self):
        self.p.terminate(); self.p.wait()


class CountingProxy:
    """Counts bytes in each direction between client and server (sum over connections)."""
    def __init__(self, listen: int, target: int):
        self.target, self.c2s, self.s2c = target, 0, 0
        self.srv = socket.socket(); self.srv.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.srv.bind(("127.0.0.1", listen)); self.srv.listen(64)
        threading.Thread(target=self._accept, daemon=True).start()

    def _accept(self):
        while True:
            try:
                c, _ = self.srv.accept()
            except OSError:
                return
            s = socket.create_connection(("127.0.0.1", self.target))
            threading.Thread(target=self._pipe, args=(c, s, "c2s"), daemon=True).start()
            threading.Thread(target=self._pipe, args=(s, c, "s2c"), daemon=True).start()

    def _pipe(self, a, b, d):
        try:
            while data := a.recv(65536):
                setattr(self, d, getattr(self, d) + len(data)); b.sendall(data)
        except OSError:
            pass
        finally:
            for x in (a, b):
                try: x.shutdown(socket.SHUT_RDWR)
                except OSError: pass

    def reset(self): self.c2s = self.s2c = 0
    def close(self): self.srv.close()


def client(port: int, groups: str | None) -> dict:
    cmd = ["openssl", "s_client", "-connect", f"127.0.0.1:{port}", "-brief", "-tls1_3"]
    if groups:
        cmd += ["-groups", groups]
    t0 = time.perf_counter()
    r = sh(*cmd, inp=b"", check=False)
    dt = (time.perf_counter() - t0) * 1000
    txt = (r.stdout + r.stderr).decode(errors="replace")
    g = re.search(r"Negotiated TLS1\.3 group: (\S+)", txt) or re.search(r"Peer Temp Key: ([^,\n]+(?:, [^,\n]+)?)", txt)   # classical groups print "Peer Temp Key"
    s = re.search(r"Signature type: (\S+)", txt)
    return {"ok": "CONNECTION ESTABLISHED" in txt, "group": g.group(1) if g else None, "sig": s.group(1) if s else None,
            "ms": dt, "err": None if "CONNECTION ESTABLISHED" in txt else txt.strip().splitlines()[-1:][:1]}


def part_a(n: int) -> list[dict]:
    rows, port = [], BASE_PORT
    for cert in CERTS:
        srv = Server(cert, port, groups=ALL_GROUPS); proxy = CountingProxy(port + 1000, port)
        for g in GROUPS:
            proxy.reset(); res = [client(port + 1000, g) for _ in range(n)]
            ok = [r for r in res if r["ok"]]
            rows.append({"cert": cert, "client_groups": g, "ok": f"{len(ok)}/{n}", "negotiated": ok[0]["group"] if ok else None,
                         "sig": ok[0]["sig"] if ok else None, "bytes_c2s": round(proxy.c2s / n) if ok else None,
                         "bytes_s2c": round(proxy.s2c / n) if ok else None,
                         "median_ms": round(statistics.median(r["ms"] for r in ok), 1) if ok else None})
        proxy.close(); srv.stop(); port += 1
    return rows


def part_b(n: int = 5) -> list[dict]:
    srv = Server("ECDSA-P256", BASE_PORT + 100, groups="X25519"); out = []
    for label, groups in (("client default (offers hybrid + X25519 shares)", None), ("client offers ONLY X25519MLKEM768", "X25519MLKEM768"),
                          ("client offers X25519MLKEM768:X25519", "X25519MLKEM768:X25519")):
        res = [client(BASE_PORT + 100, groups) for _ in range(n)]
        out.append({"server": "classical-only (groups=X25519)", "client": label, "ok": f"{sum(r['ok'] for r in res)}/{n}",
                    "negotiated": next((r["group"] for r in res if r["ok"]), None), "err": res[0]["err"]})
    srv.stop()
    srv = Server("ECDSA-P256", BASE_PORT + 101)      # server with OpenSSL 3.5 DEFAULT group list
    for label, groups in (("client offers ONLY MLKEM768 (pure ML-KEM)", "MLKEM768"), ("client offers ONLY SecP256r1MLKEM768", "SecP256r1MLKEM768")):
        res = [client(BASE_PORT + 101, groups) for _ in range(n)]
        out.append({"server": "OpenSSL 3.5 default groups", "client": label, "ok": f"{sum(r['ok'] for r in res)}/{n}",
                    "negotiated": next((r["group"] for r in res if r["ok"]), None), "err": res[0]["err"]})
    srv.stop(); return out


def der_len(pem: Path) -> int:
    return len(sh("openssl", "x509", "-in", str(pem), "-outform", "DER").stdout)


def part_c() -> dict:
    msg = OUT / "msg.bin"; msg.write_bytes(b"firmware manifest v1")
    sizes = {}
    for name in CERTS:
        k, c = PKI / f"{name}.key", PKI / f"{name}.pem"
        pub = len(sh("openssl", "pkey", "-in", str(k), "-pubout", "-outform", "DER").stdout)
        sigf = OUT / f"{name}.sig"
        if name.startswith("ML-DSA") or name == "Ed25519":
            sh("openssl", "pkeyutl", "-sign", "-rawin", "-inkey", str(k), "-in", str(msg), "-out", str(sigf))
        else:
            sh("openssl", "dgst", "-sha256", "-sign", str(k), "-out", str(sigf), str(msg))
        sizes[name] = {"public_key_der_bytes": pub, "signature_bytes": sigf.stat().st_size, "self_signed_cert_der_bytes": der_len(c)}
    kem = {}
    for alg in ("ML-KEM-512", "ML-KEM-768", "ML-KEM-1024", "X25519"):
        k = OUT / f"{alg}.key"
        sh("openssl", "genpkey", "-algorithm", alg, "-out", str(k))
        pubf = OUT / f"{alg}.pub"; sh("openssl", "pkey", "-in", str(k), "-pubout", "-out", str(pubf))
        entry = {"public_key_der_bytes": len(sh("openssl", "pkey", "-in", str(k), "-pubout", "-outform", "DER").stdout)}
        if alg.startswith("ML-KEM"):
            sh("openssl", "pkeyutl", "-encap", "-pubin", "-inkey", str(pubf), "-out", str(OUT / "ct.bin"), "-secret", str(OUT / "ss.bin"))
            entry["ciphertext_bytes"] = (OUT / "ct.bin").stat().st_size; entry["shared_secret_bytes"] = (OUT / "ss.bin").stat().st_size
        kem[alg] = entry
    return {"signatures": sizes, "kem": kem}


def part_d() -> list[dict]:
    rows, port = [], BASE_PORT + 200
    for cert in CERTS:
        srv = Server(cert, port); r = client(port, None); srv.stop(); port += 1
        rows.append({"endpoint_cert": cert, "default_client_negotiated_group": r["group"], "certificate_signature_type": r["sig"]})
    return rows


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=30); a = ap.parse_args()
    make_certs()
    base = statistics.median(((lambda t0: (sh("openssl", "version"), (time.perf_counter() - t0) * 1000)[1])(time.perf_counter())) for _ in range(a.n))
    res = {"date": str(date.today()), "openssl": openssl_version(), "n": a.n, "process_start_baseline_ms": round(base, 1),
           "A_handshakes": part_a(a.n), "B_interop": part_b(), "C_sizes": part_c(), "D_probe": part_d()}
    (RESULTS / f"ex5_pqc_tls_{date.today()}.json").write_text(json.dumps(res, indent=2))
    print(res["openssl"], f"| n={a.n} | `openssl version` process baseline {res['process_start_baseline_ms']} ms\n")
    print("A. handshake cost (bytes are per handshake, whole TCP session incl. close)")
    print(f"{'cert':<11}{'client groups':<19}{'ok':<7}{'negotiated':<19}{'c->s':>6}{'s->c':>7}{'ms':>7}")
    for r in res["A_handshakes"]:
        print(f"{r['cert']:<11}{r['client_groups']:<19}{r['ok']:<7}{str(r['negotiated']):<19}{str(r['bytes_c2s']):>6}{str(r['bytes_s2c']):>7}{str(r['median_ms']):>7}")
    print("\nB. interop"); [print(" ", json.dumps(r)) for r in res["B_interop"]]
    print("\nC. sizes (bytes)"); [print(f"  {k:<11}", v) for k, v in res["C_sizes"]["signatures"].items()]
    [print(f"  {k:<11}", v) for k, v in res["C_sizes"]["kem"].items()]
    print("\nD. probe"); [print(" ", json.dumps(r)) for r in res["D_probe"]]


if __name__ == "__main__":
    main()
