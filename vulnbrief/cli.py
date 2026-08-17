"""VulnBrief CLI — scan JSON -> plain-language briefing."""
from __future__ import annotations
import argparse, pathlib, sys
from .parser import parse
from .brief import render

def main(argv=None):
    ap = argparse.ArgumentParser(prog="vulnbrief", description="Scan JSON -> briefing de seguranca.")
    ap.add_argument("path", help="arquivo JSON (ex.: saida do 'npm audit --json')")
    ap.add_argument("--out", help="escrever briefing em arquivo .md")
    args = ap.parse_args(argv)
    text = pathlib.Path(args.path).read_text(encoding="utf-8")
    data = parse(text)
    md = render(data)
    print(md)
    if args.out:
        pathlib.Path(args.out).write_text(md, encoding="utf-8")
        print(f"\nBriefing salvo em: {args.out}")
    return 0

if __name__ == "__main__":
    raise SystemExit(main())
