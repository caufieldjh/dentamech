"""YAML helpers shared by the CLI, seeder, renderer, and tests.

Uses the libyaml C loader when it is available so whole-KB sweeps stay fast,
and writes with a stable key order so diffs are readable.
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

try:  # pragma: no cover - depends on how PyYAML was built
    from yaml import CSafeDumper as _Dumper
    from yaml import CSafeLoader as _Loader
except ImportError:  # pragma: no cover
    from yaml import SafeDumper as _Dumper
    from yaml import SafeLoader as _Loader


class _KBDumper(_Dumper):
    """Dumper that indents lists under their parent key and never sorts keys."""

    def increase_indent(self, flow: bool = False, indentless: bool = False):
        return super().increase_indent(flow, False)


def _str_presenter(dumper: yaml.Dumper, data: str):
    if "\n" in data:
        return dumper.represent_scalar("tag:yaml.org,2002:str", data, style="|")
    return dumper.represent_scalar("tag:yaml.org,2002:str", data)


_KBDumper.add_representer(str, _str_presenter)


def safe_load(text: str) -> Any:
    return yaml.load(text, Loader=_Loader)


def safe_load_path(path: str | Path) -> Any:
    return safe_load(Path(path).read_text(encoding="utf-8"))


def dump(data: Any) -> str:
    return yaml.dump(
        data,
        Dumper=_KBDumper,
        sort_keys=False,
        allow_unicode=True,
        width=88,
        default_flow_style=False,
    )


def dump_path(data: Any, path: str | Path) -> None:
    Path(path).write_text(dump(data), encoding="utf-8")


# ---------------------------------------------------------------------------
# Repository layout
# ---------------------------------------------------------------------------
ROOT_DIR = Path(__file__).resolve().parents[2]
SCHEMA_PATH = ROOT_DIR / "src" / "dentamech" / "schema" / "dentamech.yaml"
KB_DIR = ROOT_DIR / "kb" / "materials"
PAGES_DIR = ROOT_DIR / "pages" / "materials"
APP_DIR = ROOT_DIR / "app"


def kb_files(kb_dir: Path = KB_DIR) -> list[Path]:
    """Every material file, sorted by name."""
    return sorted(p for p in kb_dir.glob("*.yaml") if not p.name.startswith("_"))


def load_kb(kb_dir: Path = KB_DIR) -> dict[str, dict[str, Any]]:
    """Load every material file, keyed by its `name`."""
    out: dict[str, dict[str, Any]] = {}
    for path in kb_files(kb_dir):
        data = safe_load_path(path)
        out[data["name"]] = data
    return out


def slugify(name: str) -> str:
    """File-safe slug for a material name. `3Y-TZP zirconia ceramic` -> `3Y-TZP_Zirconia_Ceramic`."""
    parts = name.replace("/", "-").split()
    return "_".join(p if p.isupper() or any(c.isdigit() for c in p) else p[:1].upper() + p[1:] for p in parts)
