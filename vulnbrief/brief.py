"""VulnBrief — render a plain-language briefing + remediation checklist (Markdown)."""
from __future__ import annotations
from .parser import SEV_RANK

SEV_PT = {"critical": "critica", "high": "alta", "moderate": "media", "low": "baixa", "info": "info"}

def counts(findings):
    c = {k: 0 for k in SEV_RANK}
    for f in findings:
        c[f["severity"]] = c.get(f["severity"], 0) + 1
    return c

def render(data: dict) -> str:
    findings = data["findings"]
    c = counts(findings)
    lines = [
        "# VulnBrief — Briefing de Seguranca (linguagem simples)",
        "",
        f"**Resumo:** {c['critical']} critica(s), {c['high']} alta(s), {c['moderate']} media(s), {c['low']} baixa(s).",
        "",
        "## O que fazer (por ordem de severidade)",
    ]
    for i, f in enumerate(findings, 1):
        lines.append(f"{i}. **[{SEV_PT.get(f['severity'], f['severity'])}]** `{f['package']}` — {f['title']}")
        lines.append(f"   - Correcao: `{f['fix']}`")
    lines += ["", "## Checklist de remediacao", ""]
    for f in findings:
        lines.append(f"- [ ] `{f['package']}` ({SEV_PT.get(f['severity'], f['severity'])}) -> {f['fix']}")
    return "\n".join(lines)
