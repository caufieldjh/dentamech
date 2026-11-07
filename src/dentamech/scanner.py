"""Find curation items the scanner should leave alone.

The scanner tends the same few open items run after run. This counts the
agent comments on each item since a person last responded, so the workflow can
tell the scanner which items have reached the limit.

Run as ``python -m dentamech.scanner OWNER/REPO``. It prints the result and,
under GitHub Actions, sets the ``paused`` and ``final_comment`` step outputs.
"""

from __future__ import annotations

import json
import os
import subprocess
import sys
from dataclasses import dataclass

COMMENT_LIMIT = 3

# These accounts are typed "User" by GitHub, so the Bot type does not catch them.
AGENT_LOGINS = {"claude", "github-actions"}


@dataclass(frozen=True)
class Event:
    """One dated action on an issue or pull request."""

    timestamp: str
    by_agent: bool
    is_comment: bool


def is_agent(user: dict | None) -> bool:
    """Return whether a GitHub user object is an agent; no user counts as a person."""
    if not user:
        return False
    login = user.get("login", "")
    return user.get("type") == "Bot" or login.endswith("[bot]") or login in AGENT_LOGINS


def agent_streak(events: list[Event]) -> int:
    """Count agent comments since the latest action by a person.

    Agent commits do not count, and they do not end a streak either.
    """
    streak = 0
    for event in sorted(events, key=lambda e: e.timestamp, reverse=True):
        if not event.by_agent:
            break
        if event.is_comment:
            streak += 1
    return streak


def gh_list(path: str) -> list[dict]:
    """Fetch every item of a paginated GitHub list endpoint."""
    result = subprocess.run(
        ["gh", "api", "--paginate", path, "--jq", ".[]"],
        check=True,
        capture_output=True,
        text=True,
    )
    return [json.loads(line) for line in result.stdout.splitlines() if line.strip()]


def item_events(repo: str, number: int, is_pull: bool) -> list[Event]:
    """Collect the comments, reviews, and commits on one issue or pull request."""
    events = [
        Event(c["created_at"], is_agent(c["user"]), True)
        for c in gh_list(f"repos/{repo}/issues/{number}/comments?per_page=100")
    ]
    if is_pull:
        for review in gh_list(f"repos/{repo}/pulls/{number}/reviews?per_page=100"):
            if review.get("submitted_at"):
                events.append(
                    Event(review["submitted_at"], is_agent(review["user"]), bool(review.get("body")))
                )
        for commit in gh_list(f"repos/{repo}/pulls/{number}/commits?per_page=100"):
            events.append(Event(commit["commit"]["committer"]["date"], is_agent(commit["author"]), False))
    return events


def classify(streaks: dict[int, int], limit: int = COMMENT_LIMIT) -> tuple[list[int], list[int]]:
    """Split item numbers into those at the limit and those one comment short."""
    paused = sorted(n for n, streak in streaks.items() if streak >= limit)
    final_comment = sorted(n for n, streak in streaks.items() if streak == limit - 1)
    return paused, final_comment


def format_items(numbers: list[int]) -> str:
    """Render item numbers for the scanner prompt."""
    return " ".join(f"#{n}" for n in numbers) or "none"


def main() -> None:
    """Report the paused and final-comment items for a repository."""
    repo = sys.argv[1]
    streaks = {}
    for item in gh_list(f"repos/{repo}/issues?labels=curation&state=open&per_page=100"):
        is_pull = "pull_request" in item
        streaks[item["number"]] = agent_streak(item_events(repo, item["number"], is_pull))
        print(f"#{item['number']}: {streaks[item['number']]} consecutive agent comment(s)")

    paused, final_comment = classify(streaks)
    lines = [f"paused={format_items(paused)}", f"final_comment={format_items(final_comment)}"]
    print("\n".join(lines))
    if output := os.environ.get("GITHUB_OUTPUT"):
        with open(output, "a", encoding="utf-8") as handle:
            handle.write("\n".join(lines) + "\n")


if __name__ == "__main__":
    main()
