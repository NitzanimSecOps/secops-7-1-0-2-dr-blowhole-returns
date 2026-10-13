#!/usr/bin/env python3
"""Self-check for solve.sh. Run:  python3 selftest.py"""
import os
import subprocess
import sys
import tempfile
from pathlib import Path

SOLVE = Path(__file__).resolve().parent / "solve.sh"
LEN = 100


def main():
    with tempfile.TemporaryDirectory() as wd:
        target = Path(wd) / "secret.key"
        orig = os.urandom(LEN)
        target.write_bytes(orig)
        r = subprocess.run(["bash", str(SOLVE), str(target)],
                           capture_output=True, timeout=60)
        out = r.stdout.decode(errors="replace")
        data = target.read_bytes()

    checks = [
        ("Key Length: 100 characters, expected 100" in out, "prints the Key Length line"),
        (len(data) == LEN, "key is 100 bytes"),
        (all(0x20 <= b <= 0x7E for b in data), "all characters printable"),
        (data != orig and len(set(data)) >= 10, "random and changed"),
        ("Successfully ruined" in out, "prints the success line"),
    ]
    for ok, name in checks:
        print(("PASS" if ok else "FAIL"), name)
    passed = sum(ok for ok, _ in checks)
    print(f"\n{passed}/{len(checks)} checks passed.")
    return 0 if passed == len(checks) else 1


if __name__ == "__main__":
    sys.exit(main())
