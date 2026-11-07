"""Keep the automation honest: workflows parse and the comment limit stays wired in."""

from __future__ import annotations

import re
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
WORKFLOWS = sorted((ROOT / ".github" / "workflows").glob("*.y*ml"))
SKILLS = ROOT / ".claude" / "skills"


def test_workflows_parse():
    assert WORKFLOWS
    for wf in WORKFLOWS:
        assert "jobs" in yaml.safe_load(wf.read_text(encoding="utf-8")), wf.name


def test_skills_named_in_prompts_exist():
    prompts = (ROOT / ".github" / "prompts").glob("*.md")
    text = "\n".join(p.read_text(encoding="utf-8") for p in prompts)
    for name in set(re.findall(r"`([a-z]+-record)` skill", text)):
        assert (SKILLS / name / "SKILL.md").exists(), name


def test_scanner_applies_the_comment_limit():
    text = (ROOT / ".github" / "workflows" / "curation-scanner.yaml").read_text(encoding="utf-8")
    assert "python3 -m dentamech.scanner" in text
    assert "QUEUE_PAUSED: ${{ steps.limits.outputs.paused }}" in text
    assert "PROMPT_FINAL_COMMENT: ${{ steps.limits.outputs.final_comment }}" in text
    queue = (ROOT / ".github" / "scripts" / "curation_queue.py").read_text(encoding="utf-8")
    assert "QUEUE_PAUSED" in queue


def test_issue_template_does_not_apply_the_curation_label():
    """The label hands an item to an agent with write access, so a person adds it."""
    template = ROOT / ".github" / "ISSUE_TEMPLATE" / "curate-material.yml"
    assert "curation" not in (yaml.safe_load(template.read_text(encoding="utf-8")).get("labels") or [])


def test_comment_guard_reads_its_gate_from_the_default_branch():
    text = (ROOT / ".github" / "workflows" / "comment-guard.yaml").read_text(encoding="utf-8")
    assert "ref: ${{ github.event.repository.default_branch }}" in text
    assert (ROOT / ".github" / "scripts" / "trust-gate.js").exists()
