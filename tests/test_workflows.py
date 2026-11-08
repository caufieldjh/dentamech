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


def test_review_never_runs_tools_from_the_pull_request():
    """Missing tools skip the review; they are never taken from the PR's checkout in pr/."""
    text = (ROOT / ".github" / "workflows" / "review.yaml").read_text(encoding="utf-8")
    steps = yaml.safe_load(text)["jobs"]["review"]["steps"]
    guarded = [s for s in steps if s.get("id") in ("prompt", "agent", "size", "run")]
    assert len(guarded) == 4
    assert all("steps.tools.outputs.ready == 'true'" in s["if"] for s in guarded)
    assert "pr/.github" not in text


def test_curation_prs_may_update_the_regulatory_table():
    """The curate-record skill adds a row to this table for each regulation it verifies."""
    text = (ROOT / ".github" / "workflows" / "qc.yaml").read_text(encoding="utf-8")
    assert "|docs/regulatory\\.md$)" in text
