"""Keep the automation honest: workflows parse, skills they name exist, and
the research template carries every variable the just recipe passes."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.y*ml"))
SKILLS = ROOT / ".claude" / "skills"
TEMPLATE = ROOT / "templates" / "dental_material_research.md"
JUSTFILE = ROOT / "project.justfile"


def test_workflows_parse():
    for wf in WORKFLOWS:
        data = yaml.safe_load(wf.read_text(encoding="utf-8"))
        assert "jobs" in data, wf.name


def test_workflows_reference_existing_skills():
    text = "\n".join(wf.read_text(encoding="utf-8") for wf in WORKFLOWS)
    for name in re.findall(r"\.claude/skills/([a-z0-9-]+)/SKILL\.md", text):
        assert (SKILLS / name / "SKILL.md").exists(), name


def test_claude_workflows_use_oauth_fallback():
    for wf in WORKFLOWS:
        text = wf.read_text(encoding="utf-8")
        if "claude-code-action" in text:
            assert "CLAUDE_CODE_OAUTH_TOKEN" in text, wf.name
            assert "--model" in text, wf.name


def test_research_template_variables_match_recipe():
    template_vars = set(re.findall(r"\{([a-z_]+)\}", TEMPLATE.read_text(encoding="utf-8")))
    recipe = JUSTFILE.read_text(encoding="utf-8")
    recipe_vars = set(re.findall(r'--var "([a-z_]+)=', recipe))
    assert template_vars == recipe_vars, (template_vars ^ recipe_vars)


def test_research_template_has_regulatory_section():
    text = TEMPLATE.read_text(encoding="utf-8")
    assert "21 CFR" in text
    assert "product code" in text.lower()
    assert "verbatim" in text


def test_scanner_receives_comment_limit_results():
    text = (ROOT / ".github" / "workflows" / "curation-scanner.yml").read_text(encoding="utf-8")
    assert "python -m dentamech.scanner" in text
    assert "steps.limits.outputs.paused" in text
    assert "steps.limits.outputs.final_comment" in text
