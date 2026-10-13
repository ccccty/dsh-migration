#!/usr/bin/env python3
# -*- coding: utf-8 -*-
r"""
build_paper.py -- Tectonic compile + artifact acceptance (skill: paper-generation-cn)

Usage (run from INSIDE the paper dir, pass "." to avoid GBK arg mangling):
    cd <paper dir>
    python <skill>\tools\build_paper.py . --tex main.tex

Exit code: 0 = compiled and acceptance clean; 1 = compile failed or hard issues found.
Output is ASCII-only on purpose (DSH pwsh consoles are GBK; Chinese would mojibake).
"""
import argparse
import os
import re
import subprocess
import sys

TECTONIC = r"D:\devtools\tectonic\tectonic.exe"
CACHE = r"D:\devtools\tectonic\cache"
REPLACEMENT_CHAR = chr(0xFFFD)


def ascii_safe(s: str) -> str:
    return s.encode("ascii", "backslashreplace").decode("ascii")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("project", help="paper project dir (pass '.' after cd)")
    ap.add_argument("--tex", default="main.tex", help="main tex file, WITH extension")
    args = ap.parse_args()

    proj = os.path.abspath(args.project)
    tex = args.tex
    if not tex.endswith(".tex"):
        print("[FAIL] --tex must include the .tex extension (Tectonic does not append it)")
        return 1
    if not os.path.isfile(os.path.join(proj, tex)):
        print("[FAIL] not found: " + ascii_safe(os.path.join(proj, tex)))
        return 1

    env = dict(os.environ)
    env.setdefault("TECTONIC_CACHE_DIR", CACHE)
    env.pop("ELECTRON_RUN_AS_NODE", None)

    print("[build] " + tex + " in " + ascii_safe(proj))
    r = subprocess.run(
        [TECTONIC, "-X", "compile", "--synctex", "--keep-logs", tex],
        cwd=proj, env=env, capture_output=True, text=True, errors="replace",
    )
    for line in (r.stdout + r.stderr).strip().splitlines()[-6:]:
        print("  " + ascii_safe(line))
    if r.returncode != 0:
        print(f"[FAIL] tectonic exit={r.returncode}")
        return 1

    stem = tex[:-4]
    pdf = os.path.join(proj, stem + ".pdf")
    log = os.path.join(proj, stem + ".log")
    if not os.path.isfile(pdf):
        print("[FAIL] PDF not generated")
        return 1

    problems = 0
    if os.path.isfile(log):
        raw = open(log, encoding="utf-8", errors="replace").read()
        for name, pat in [
            ("Missing character", r"Missing character"),
            ("LaTeX Warning", r"LaTeX Warning"),
            ("Overfull hbox", r"Overfull \\hbox"),
            ("multiply defined", r"multiply"),
            ("Undefined citation", r"Citation .* undefined"),
        ]:
            n = len(re.findall(pat, raw))
            flag = "OK " if n == 0 else "!! "
            print(f"  [{flag}]{name}: {n}")
            if n and name != "Overfull hbox":
                problems += n

    try:
        import pymupdf
        doc = pymupdf.open(pdf)
        text = "".join(p.get_text() for p in doc)
        bad = [i + 1 for i, p in enumerate(doc) if REPLACEMENT_CHAR in p.get_text()]
        print(f"  [info] pages={doc.page_count} chars={len(text)} "
              f"replacement-char-pages={bad or 'none'}")
        if bad:
            problems += len(bad)
    except ImportError:
        print("  [warn] pymupdf unavailable, PDF text acceptance skipped")

    print("[PASS] compile + acceptance clean" if problems == 0
          else f"[FAIL] acceptance issues={problems}")
    return 0 if problems == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
