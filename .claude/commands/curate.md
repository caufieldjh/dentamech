---
description: Curate a dental material entry (research, fill, verify FDA status, validate, PR). A deep research provider may be named.
argument-hint: [MATERIAL_FILE_STEM] ( using [PROVIDER] )
---

Curate the material named in $ARGUMENTS.

You MUST follow the `curate-material` skill step by step. If the user names a
deep research provider, use at least that provider; otherwise default to
`claude_code`.

Before opening the PR, run the `dentamech-pr-review` skill in a fresh
subagent and fix what it finds.
