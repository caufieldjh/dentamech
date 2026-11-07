"""Data model package for dentamech."""

from pathlib import Path

from .dentamech import *

THIS_PATH = Path(__file__).parent

SCHEMA_DIRECTORY = THIS_PATH.parent / "schema"
MAIN_SCHEMA_PATH = SCHEMA_DIRECTORY / "dentamech.yaml"
