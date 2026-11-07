"""dentamech command line tools."""

from __future__ import annotations

from pathlib import Path

import typer

from dentamech.yaml_io import APP_DIR, KB_DIR, PAGES_DIR, kb_files, load_kb

app = typer.Typer(help="Dental Materials Knowledge Base tools.", no_args_is_help=True)


@app.command("seed")
def seed_command(
    force: bool = typer.Option(False, "--force", help="Overwrite files that already exist."),
    include_root: bool = typer.Option(True, help="Also write the OHD root term as an entry."),
) -> None:
    """Create one stub file per OHD dental restoration material term."""
    from dentamech.seed import seed

    written = seed(force=force, include_root=include_root)
    for p in written:
        typer.echo(f"wrote {p.relative_to(Path.cwd()) if p.is_relative_to(Path.cwd()) else p}")
    typer.echo(f"{len(written)} file(s) written; {len(kb_files())} total in {KB_DIR}")


@app.command("list")
def list_command(
    status: str | None = typer.Option(None, help="Only entries with this curation_status."),
) -> None:
    """List materials with their category and curation status."""
    for name, data in load_kb().items():
        if status and data.get("curation_status") != status:
            continue
        term = data.get("material_term", {}).get("term", {}).get("id", "")
        typer.echo(f"{name}\t{data.get('category', '')}\t{data.get('curation_status', '')}\t{term}")


@app.command("render")
def render_command(
    files: list[Path] = typer.Argument(None, help="Specific KB files to render; default is all."),
    out: Path = typer.Option(PAGES_DIR, help="Output directory for pages."),
) -> None:
    """Render HTML pages for materials, plus the index page."""
    from dentamech.render import render_all

    n = render_all(out_dir=out, only=files or None)
    typer.echo(f"rendered {n} page(s) into {out}")


@app.command("export-browser")
def export_browser_command(
    out: Path = typer.Option(APP_DIR / "data.js", help="Output JS file for the browser."),
) -> None:
    """Write app/data.js for the faceted browser."""
    from dentamech.export import export_browser_data

    n = export_browser_data(out)
    typer.echo(f"exported {n} record(s) to {out}")


@app.command("check-links")
def check_links_command() -> None:
    """Check that every `parents` value names an existing entry, and report orphans."""
    kb = load_kb()
    bad = 0
    for name, data in kb.items():
        for parent in data.get("parents", []) or []:
            if parent not in kb:
                typer.echo(f"{name}: parent '{parent}' has no entry", err=True)
                bad += 1
    if bad:
        raise typer.Exit(code=1)
    typer.echo(f"{len(kb)} entries; all parent links resolve")


def main() -> None:
    app()


if __name__ == "__main__":
    main()
