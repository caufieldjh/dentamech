"""Convert the pre-mechmaker dentamech records into this Mech.

Reads `kb/materials/*.yaml` from a git ref of this repository, so the old layout
stays the fixed source. Keeps every curated section and its evidence unchanged.

    just convert scripts/convert_legacy.py --model <id> --apply
    LEGACY_REF=origin/curate/metal just convert scripts/convert_legacy.py --only Metal --apply

What changes on each record:

    material_term.term        -> id and record_term
    curation_status           -> status, which the helper sets to DRAFT
    creation_date (timestamp) -> creation_date (date)
    parents (record names)    -> parents (record ids)

The source key is the old filename stem. A record that already exists is left
alone, so remove a stub before converting a curated version of it.
"""

from __future__ import annotations

import os
import subprocess

from dentamech.convert import Entry, Skip, run
from dentamech.validate import loads

# The last commit of the old layout on main.
LEGACY_REF = os.environ.get("LEGACY_REF", "cddf481")
LEGACY_DIR = "kb/materials"


def git(*args: str) -> str:
    return subprocess.run(["git", *args], check=True, capture_output=True, text=True).stdout


def read_source() -> dict[str, dict]:
    """Every old record, by filename stem."""
    paths = git("ls-tree", "--name-only", LEGACY_REF, f"{LEGACY_DIR}/").split()
    return {
        path.rsplit("/", 1)[-1].removesuffix(".yaml"): loads(git("show", f"{LEGACY_REF}:{path}"))
        for path in paths
        if path.endswith(".yaml")
    }


def convert_record(old: dict, ids_by_name: dict[str, str]) -> dict:
    """The new record for one old one. Raises KeyError on a dangling parent."""
    term = old["material_term"]["term"]
    moved = {"name", "description", "material_term", "curation_status", "creation_date", "parents"}
    record = {
        "id": term["id"],
        "name": old["name"],
        "description": old["description"],
        "record_term": {"id": term["id"], "label": term["label"]},
    }
    record.update({key: value for key, value in old.items() if key not in moved})
    if old.get("parents"):
        record["parents"] = [ids_by_name[name] for name in old["parents"]]
    record["creation_date"] = old["creation_date"][:10]
    return record


def entries():
    source = read_source()
    ids_by_name = {old["name"]: old["material_term"]["term"]["id"] for old in source.values()}
    for stem, old in sorted(source.items()):
        try:
            yield Entry(stem, convert_record(old, ids_by_name))
        except KeyError as exc:
            yield Skip(stem, f"missing {exc}")


if __name__ == "__main__":
    raise SystemExit(run(entries(), source=f"dentamech at {LEGACY_REF}", script=__file__))
