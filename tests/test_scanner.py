"""The scanner's comment limit: what counts toward a streak and what ends one."""

from __future__ import annotations

from dentamech.scanner import (
    COMMENT_LIMIT,
    Event,
    agent_streak,
    classify,
    format_items,
    is_agent,
)


def comment(day: int, by_agent: bool = True) -> Event:
    return Event(f"2026-11-{day:02d}T00:00:00Z", by_agent, True)


def commit(day: int, by_agent: bool = True) -> Event:
    return Event(f"2026-11-{day:02d}T00:00:00Z", by_agent, False)


def test_is_agent_catches_user_typed_agent_accounts():
    assert is_agent({"login": "github-actions[bot]", "type": "Bot"})
    assert is_agent({"login": "claude", "type": "User"})
    assert not is_agent({"login": "caufieldjh", "type": "User"})
    assert not is_agent(None)


def test_streak_counts_agent_comments():
    assert agent_streak([comment(1), comment(2), comment(3)]) == 3


def test_person_comment_resets_streak():
    assert agent_streak([comment(1), comment(2), comment(3, by_agent=False), comment(4)]) == 1


def test_person_commit_resets_streak():
    assert agent_streak([comment(1), comment(2), commit(3, by_agent=False)]) == 0


def test_agent_commits_neither_count_nor_reset():
    assert agent_streak([comment(1), commit(2), comment(3), commit(4)]) == 2


def test_event_order_does_not_matter():
    assert agent_streak([comment(3), comment(1, by_agent=False), comment(2)]) == 2


def test_no_events():
    assert agent_streak([]) == 0


def test_classify_splits_at_the_limit():
    streaks = {2: COMMENT_LIMIT + 4, 4: COMMENT_LIMIT, 5: COMMENT_LIMIT - 1, 6: 0}
    assert classify(streaks) == ([2, 4], [5])


def test_format_items():
    assert format_items([2, 4]) == "#2 #4"
    assert format_items([]) == "none"
