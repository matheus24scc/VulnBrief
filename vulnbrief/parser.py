"""VulnBrief — parse security-scan output (npm audit JSON / simple list) into findings."""
from __future__ import annotations
import json

SEV_RANK = {"critical": 4, "high": 3, "moderate": 2, "low": 1, "info": 0}

def _fix(fix) -> str:
    if isinstance(fix, dict) and fix.get("name"):
        return f"npm install {fix['name']}@{fix.get('version','latest')}"
    if fix is True:
        return "npm audit fix"
    return "sem correcao automatica disponivel"

def parse(text: str) -> dict:
    data = text if isinstance(text, dict) else json.loads(text)
    vulns = data.get("vulnerabilities", {})
    findings = []
    for name, v in vulns.items():
        findings.append({
            "package": name,
            "severity": v.get("severity", "low"),
            "title": v.get("title", name),
            "fix": _fix(v.get("fixAvailable")),
        })
    findings.sort(key=lambda f: SEV_RANK.get(f["severity"], 0), reverse=True)
    return {"findings": findings, "metadata": data.get("metadata", {})}
