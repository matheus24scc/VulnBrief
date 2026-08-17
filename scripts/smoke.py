"""Smoke test end-to-end do VulnBrief (uso real, nao so unittest)."""
from __future__ import annotations
import sys, json, tempfile
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
from vulnbrief.parser import parse
from vulnbrief.brief import render


def chk(name, cond):
    print(("PASS " if cond else "FAIL ") + name)
    return bool(cond)


def main() -> int:
    scan = {"vulnerabilities": {
        "lodash": {"severity": "high", "title": "Prototype Pollution",
                   "fixAvailable": {"name": "lodash", "version": "4.17.21"}},
        "minimist": {"severity": "critical", "title": "Prototype Pollution", "fixAvailable": True},
        "leftpad": {"severity": "low", "title": "x", "fixAvailable": False},
    }, "metadata": {"totalDependencies": 100}}
    data = parse(json.dumps(scan))
    ok = True
    ok &= chk("parse 3 findings", len(data["findings"]) == 3)
    ok &= chk("ordem por severidade (critical primeiro)", data["findings"][0]["severity"] == "critical")
    ok &= chk("fix command gerado", "npm install lodash@4.17.21" in data["findings"][1]["fix"])
    md = render(data)
    ok &= chk("briefing tem resumo", "critica" in md and "alta" in md)
    ok &= chk("briefing lista pacotes", "lodash" in md and "minimist" in md)
    # CLI real
    tf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump(scan, tf); tf.close()
    try:
        from vulnbrief.cli import main as cli_main
        ok &= chk("cli roda", cli_main([tf.name]) == 0)
    finally:
        Path(tf.name).unlink(missing_ok=True)
    print("\nSMOKE VulnBrief:", "PASS" if ok else "FAIL")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
