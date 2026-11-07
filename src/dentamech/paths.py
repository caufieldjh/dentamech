"""Repository constants, written by mechmaker. Edit freely."""

from pathlib import Path

SLUG = "dentamech"
MECH_NAME = "DentaMech"
RECORD_CLASS = "DentalMaterial"
RECORD_NOUN = "dental material"
# The prefix of the ontology that keys records, or "" when every id is minted.
# A record whose id has it names the same term in `record_term`.
IDENTITY_PREFIX = "OHD"
HAS_RECORD_TERM = bool(IDENTITY_PREFIX)
REPO_URL = "https://github.com/caufieldjh/dentamech"

PACKAGE_DIR = Path(__file__).resolve().parent
REPO_ROOT = PACKAGE_DIR.parents[1]
SCHEMA_DIR = PACKAGE_DIR / "schema"
SCHEMA_PATH = SCHEMA_DIR / f"{SLUG}.yaml"
HISTORY_SCHEMA_PATH = SCHEMA_DIR / "history.yaml"
RECORDS_DIR = REPO_ROOT / "kb/materials"
HISTORY_DIR = REPO_ROOT / "history"
REFERENCES_DIR = REPO_ROOT / "references_cache"
BUILD_DIR = REPO_ROOT / "build"
PAGES_DIR = REPO_ROOT / "pages"
