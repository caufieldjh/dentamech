## Project-specific recipes, imported by the main justfile.

schema_path := "src/dentamech/schema/dentamech.yaml"
kb_dir := "kb/materials"
oak_config := "conf/oak_config.yaml"
ref_validator_config := "conf/reference_validator_config.yaml"
term_validator := "scripts/run_term_validator.sh"
research_dir := "research"
templates_dir := "templates"
dr_client := "uv run deep-research-client"
# Resolve every citation in a report as it is generated, sharing the KB's
# reference cache so later `just fetch-reference` calls are cache hits.
dr_validation := "--validate-references --validation-cache-dir references_cache"

# Seed one stub per OHD dental restoration material term (never overwrites)
[group('curation')]
seed *args:
    uv run dentamech seed {{args}}

# List materials with category and curation status
[group('curation')]
list-materials *args:
    uv run dentamech list {{args}}

# Schema + term validation of every material file
[group('QC')]
validate-all:
    #!/usr/bin/env bash
    set -euo pipefail
    files=({{kb_dir}}/*.yaml)
    echo "Schema validation (${#files[@]} files)..."
    uv run linkml-validate --schema {{schema_path}} --target-class DentalMaterial "${files[@]}"
    echo "Term validation..."
    {{term_validator}} validate-data "${files[@]}" -s {{schema_path}} -t DentalMaterial --labels -c {{oak_config}}
    echo "Parent links..."
    uv run dentamech check-links
    echo "✓ All files validated"

# Schema + term validation of one material file
[group('QC')]
validate file:
    uv run linkml-validate --schema {{schema_path}} --target-class DentalMaterial {{file}}
    {{term_validator}} validate-data {{file}} -s {{schema_path}} -t DentalMaterial --labels -c {{oak_config}}

# Validate ontology terms referenced by the schema itself (enum meanings, source nodes)
[group('QC')]
validate-terms-schema:
    {{term_validator}} validate-schema {{schema_path}} -c {{oak_config}}

# Reference validation: check evidence snippets against fetched PubMed abstracts
[group('QC')]
validate-references *files:
    uv run linkml-reference-validator validate data {{files}} --schema {{schema_path}} --target-class DentalMaterial --config {{ref_validator_config}}

# Reference validation over every material file
[group('QC')]
validate-references-all:
    uv run linkml-reference-validator validate data {{kb_dir}}/*.yaml --schema {{schema_path}} --target-class DentalMaterial --config {{ref_validator_config}}

# Full QC: validate-all plus the fast pytest suite
[group('QC')]
qc: validate-all
    uv run pytest -q

# Render every material page plus the index
[group('site')]
render:
    uv run dentamech render

# Render a single material page
[group('site')]
render-one file:
    uv run dentamech render {{file}}

# Regenerate app/data.js for the faceted browser
[group('site')]
export-browser:
    uv run dentamech export-browser

# Build everything the static site needs: pages, browser data, schema docs
[group('site')]
site-all: render export-browser gen-doc

# Serve the repository root so pages/ and app/ links resolve
[group('site')]
serve-pages:
    uv run python -m http.server 8765 -d .

# ---------------------------------------------------------------------------
# Deep research
# ---------------------------------------------------------------------------

# `material` is a file stem in kb/materials/ (e.g. Amalgam). Providers: claude_code
# (no extra key), falcon (EDISON_API_KEY), openai, perplexity, asta, mock.
# Deep research report for one material: just research-material <provider> <material>
[group('research')]
research-material provider material *args="":
    #!/usr/bin/env bash
    set -euo pipefail
    mkdir -p {{research_dir}}
    yaml_file="{{kb_dir}}/{{material}}.yaml"
    if [ ! -f "$yaml_file" ]; then
        echo "Error: material file not found: $yaml_file" >&2
        echo "Known materials:" >&2
        for f in {{kb_dir}}/*.yaml; do basename "$f" .yaml; done | sort >&2
        exit 1
    fi
    eval "$(uv run python -c "
    import shlex
    from dentamech.yaml_io import safe_load_path
    d = safe_load_path('$yaml_file')
    t = d['material_term']['term']
    print('material_name=' + shlex.quote(d['name']))
    print('ohd_id=' + shlex.quote(t['id']))
    print('ohd_label=' + shlex.quote(t['label']))
    print('category=' + shlex.quote(d.get('category', '')))
    print('ohd_definition=' + shlex.quote(d.get('description', '')))
    ")"
    output_file="{{research_dir}}/{{material}}-deep-research-{{provider}}.md"
    echo "Researching: $material_name ({{provider}}) -> $output_file"
    {{dr_client}} research \
        --template {{templates_dir}}/dental_material_research.md \
        --var "material_name=$material_name" \
        --var "ohd_id=$ohd_id" \
        --var "ohd_label=$ohd_label" \
        --var "category=$category" \
        --var "ohd_definition=$ohd_definition" \
        --provider {{provider}} \
        --output "$output_file" \
        --separate-citations "$output_file.citations.md" \
        {{dr_validation}} \
        {{args}}

# Add a Reference Validation section to an existing report (idempotent)
[group('research')]
validate-research-reference file:
    {{dr_client}} validate-references {{file}} --in-place --cache-dir references_cache

# Which materials have a research report, and from which providers
[group('research')]
research-status:
    #!/usr/bin/env bash
    for f in {{kb_dir}}/*.yaml; do
        m=$(basename "$f" .yaml)
        reports=$(ls {{research_dir}}/"$m"-deep-research-*.md 2>/dev/null | grep -v citations | sed -E 's/.*-deep-research-([a-z_]+)\.md/\1/' | tr '\n' ' ')
        printf '%-55s %s\n' "$m" "${reports:--}"
    done

# Fetch and cache one or more references (PMID:, DOI:, PMC:). Never hand-write
# references_cache/ files; always go through this.
[group('curation')]
fetch-reference +identifiers:
    #!/usr/bin/env bash
    for identifier in {{identifiers}}; do
        echo "Fetching reference: $identifier"
        uv run linkml-reference-validator cache reference "$identifier"
    done
