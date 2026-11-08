"""The review publisher, run under Node against a fake GitHub.

The point under test: an approving verdict lifts the reviewer's own earlier
CHANGES_REQUESTED reviews, even when GitHub refuses the approval itself, and
never touches anyone else's review.
"""

import json
import shutil
import subprocess
from pathlib import Path

import pytest

SCRIPT = Path(__file__).resolve().parents[1] / ".github" / "scripts" / "review-publish.js"
SHA = "a" * 40
BOT = "github-actions[bot]"

HARNESS = r"""
const { publish } = require(process.argv[1]);
const opts = JSON.parse(process.argv[2]);
const calls = { created: [], dismissed: [] };
const existing = opts.reviews;
const github = {
  paginate: async (fn) =>
    fn === github.rest.pulls.listFiles ? [{ filename: 'kb/materials/x.yaml' }] : existing,
  rest: { pulls: {
    get: async () => ({ data: { state: 'open', head: { sha: opts.sha, repo: { full_name: 'o/r' } } } }),
    listFiles: () => {},
    listReviews: () => {},
    createReview: async (a) => {
      if (a.event === 'APPROVE' && opts.refuseApprove)
        throw new Error('GitHub Actions is not permitted to approve pull requests.');
      calls.created.push(a.event);
      return { data: { id: 999, user: { login: opts.bot } } };
    },
    dismissReview: async (a) => { calls.dismissed.push(a.review_id); },
  } },
};
const quiet = () => {};
publish(github, { owner: 'o', repo: 'r' }, opts.review, { pr: 1, sha: opts.sha, log: quiet, warn: quiet })
  .then(result => console.log(JSON.stringify({ result, calls })));
"""

EARLIER = [
    {"id": 1, "state": "CHANGES_REQUESTED", "user": {"login": BOT}},
    {"id": 2, "state": "CHANGES_REQUESTED", "user": {"login": "a-person"}},
    {"id": 3, "state": "COMMENTED", "user": {"login": BOT}},
    {"id": 4, "state": "DISMISSED", "user": {"login": BOT}},
]
CLEAN = {"verdict": "approve", "checklist": {}, "summary": "Fine.",
         "findings": [{"severity": "note", "body": "A small thing."}]}
BLOCKING = {"verdict": "approve", "checklist": {}, "summary": "Not yet.",
            "findings": [{"severity": "warning", "body": "Fix this."}]}


def run(review, refuse_approve=False):
    if not shutil.which("node"):
        pytest.skip("node is not installed")
    opts = {"review": review, "reviews": EARLIER, "sha": SHA, "bot": BOT, "refuseApprove": refuse_approve}
    out = subprocess.run(["node", "-e", HARNESS, str(SCRIPT), json.dumps(opts)],
                         capture_output=True, text=True, check=True).stdout
    return json.loads(out)


def test_an_approval_lifts_only_the_reviewers_own_blocks():
    out = run(CLEAN)
    assert out["calls"]["created"] == ["APPROVE"]
    assert out["calls"]["dismissed"] == [1]


def test_a_refused_approval_still_lifts_the_reviewers_own_blocks():
    out = run(CLEAN, refuse_approve=True)
    assert out["calls"]["created"] == ["COMMENT"]
    assert out["calls"]["dismissed"] == [1]


def test_a_blocking_finding_lifts_nothing():
    out = run(BLOCKING)
    assert out["calls"]["created"] == ["REQUEST_CHANGES"]
    assert out["calls"]["dismissed"] == []
