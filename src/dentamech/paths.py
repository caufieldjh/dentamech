"""Repository constants, written by mechmaker. Edit freely."""

import os
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
# Names the checkout explicitly; wins over the working directory.
ROOT_ENV_VAR = f"{SLUG.upper()}_ROOT"


def repo_root() -> Path:
    """The checkout a command reads from and writes to.

    ``$DENTAMECH_ROOT`` if set, else the nearest directory at or above the
    working directory that holds a justfile and the records directory, else the
    tree this package was loaded from. Not ``__file__`` first: git worktrees
    share one virtualenv, whose editable install points at the primary
    checkout, so paths built from ``__file__`` would send a worktree's reads
    and writes there. Use ``__file__`` only for files inside the package.
    """
    override = os.environ.get(ROOT_ENV_VAR)
    if override:
        return Path(override).expanduser().resolve()
    here = Path.cwd().resolve()
    for candidate in (here, *here.parents):
        if (candidate / "justfile").is_file() and (candidate / "kb/materials").is_dir():
            return candidate
    return PACKAGE_DIR.parents[1]


REPO_ROOT = repo_root()
SCHEMA_DIR = PACKAGE_DIR / "schema"
SCHEMA_PATH = SCHEMA_DIR / f"{SLUG}.yaml"
HISTORY_SCHEMA_PATH = SCHEMA_DIR / "history.yaml"
PAPER_LOG_SCHEMA_PATH = SCHEMA_DIR / "paper_log.yaml"
RECORDS_DIR = REPO_ROOT / "kb/materials"
HISTORY_DIR = REPO_ROOT / "history"
PAPER_LOG_PATH = REPO_ROOT / "curation/paper_log.tsv"
REFERENCES_DIR = REPO_ROOT / "references_cache"
BUILD_DIR = REPO_ROOT / "build"
PAGES_DIR = REPO_ROOT / "pages"
