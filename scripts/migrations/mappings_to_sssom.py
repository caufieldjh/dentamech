"""Move each record's `mappings` to the SSSOM field names (mechmaker #109).

Before: {id, label, predicate: EXACT_MATCH, source}
After:  {predicate_id: skos:exactMatch, object_id, object_label,
         mapping_justification, notes}

Every existing mapping was made by an agent (claude-code) reading sources, so
its justification is semapv:UnspecifiedMatching, the value mechmaker's
`curate-mappings` skill gives an agent's mapping. The old free-text `source`
is kept in `notes`, which the SSSOM export writes as the row's comment.

Run once from the repository root:

    uv run python scripts/migrations/mappings_to_sssom.py [--apply]
"""

from __future__ import annotations

import argparse
import sys

import yaml

from dentamech.paths import RECORDS_DIR
from dentamech.records import append_curation_event, write_validated_record

PREDICATES = {
    "EXACT_MATCH": "skos:exactMatch",
    "CLOSE_MATCH": "skos:closeMatch",
    "BROAD_MATCH": "skos:broadMatch",
    "NARROW_MATCH": "skos:narrowMatch",
    "RELATED_MATCH": "skos:relatedMatch",
}
OLD_KEYS = {"id", "label", "predicate", "source"}


def migrate(mapping: dict) -> dict:
    extra = set(mapping) - OLD_KEYS
    if extra:
        raise ValueError(f"unexpected keys in a mapping: {sorted(extra)}")
    new = {
        "predicate_id": PREDICATES[mapping["predicate"]],
        "object_id": mapping["id"],
    }
    if mapping.get("label"):
        new["object_label"] = mapping["label"]
    new["mapping_justification"] = "semapv:UnspecifiedMatching"
    if mapping.get("source"):
        new["notes"] = f"Source: {mapping['source']}"
    return new


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--apply", action="store_true", help="write the records (default: dry run)")
    parser.add_argument("--model", default="claude-opus-5-5")
    args = parser.parse_args(argv)

    changed = 0
    for path in sorted(RECORDS_DIR.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8"))
        old = data.get("mappings")
        if not old or all("object_id" in m for m in old):
            continue
        data["mappings"] = [m if "object_id" in m else migrate(m) for m in old]
        append_curation_event(
            data,
            action="EDIT",
            curator="claude-code",
            llm_assisted=True,
            model=args.model,
            description=(
                "Schema migration: mappings moved to SSSOM fields (predicate_id, object_id, "
                "object_label, mapping_justification); old source kept in notes."
            ),
        )
        write_validated_record(data, path, dry_run=not args.apply)
        changed += 1
        print(f"{'migrated' if args.apply else 'would migrate'} {path.name}: {len(old)} mapping(s)")
    print(f"{changed} record(s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
