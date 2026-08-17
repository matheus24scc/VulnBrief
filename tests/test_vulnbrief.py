"""Testes do VulnBrief (oracle)."""
from vulnbrief.parser import parse, SEV_RANK
from vulnbrief.brief import render, counts

SAMPLE = {
  "vulnerabilities": {
    "lodash": {"name": "lodash", "severity": "high", "title": "Prototype Pollution", "fixAvailable": {"name": "lodash", "version": "4.17.21"}},
    "minimist": {"name": "minimist", "severity": "critical", "title": "Prototype Pollution", "fixAvailable": True},
    "semver": {"name": "semver", "severity": "low", "title": "ReDoS", "fixAvailable": False},
  },
  "metadata": {"vulnerabilities": {"critical": 1, "high": 1, "moderate": 0, "low": 1}},
}

def test_parse_counts():
    d = parse(SAMPLE)
    c = counts(d["findings"])
    assert c["critical"] == 1 and c["high"] == 1 and c["low"] == 1

def test_parse_sorted_by_severity():
    d = parse(SAMPLE)
    sevs = [SEV_RANK[f["severity"]] for f in d["findings"]]
    assert sevs == sorted(sevs, reverse=True)

def test_fix_commands():
    d = parse(SAMPLE)
    fixes = {f["package"]: f["fix"] for f in d["findings"]}
    assert fixes["minimist"] == "npm audit fix"
    assert fixes["lodash"].startswith("npm install lodash@")
    assert "sem correcao" in fixes["semver"]

def test_render_contains_all_packages():
    md = render(parse(SAMPLE))
    assert "lodash" in md and "minimist" in md and "semver" in md
    assert "Resumo" in md and "Checklist" in md
