#!/usr/bin/env python3
"""Validate Jupyter notebook structure without executing notebook code."""

from __future__ import annotations

import argparse
import copy
import html
import json
import os
import re
import sys
import tempfile
import uuid
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Iterable, Sequence
from urllib.parse import unquote


ATX_HEADING = re.compile(r"^(#{1,6})(?:[ \t]+(.*?))?[ \t]*$")
FENCE = re.compile(r"^\s*(`{3,}|~{3,})")
NUMBERED_TITLE = re.compile(r"^\d{1,3}(?:(?:\.\d+)+)?[.)]?[ \t]+")
SETEXT_UNDERLINE = re.compile(r"^\s*(=+|-+)\s*$")
MARKDOWN_INTERNAL_LINK = re.compile(
    r"\[([^\]]*)\]\(\s*<?#([^)>\s]+)>?(?:\s+[^)]*)?\)"
)
HTML_INTERNAL_LINK = re.compile(r"\bhref\s*=\s*['\"]#([^'\"]+)['\"]", re.I)
HTML_ANCHOR = re.compile(
    r"<(?:a|span)\b[^>]*\b(?:id|name)\s*=\s*['\"]([^'\"]+)['\"][^>]*>",
    re.I,
)
CUSTOM_HEADING_ID = re.compile(r"\s*\{#([^}\s]+)\}\s*$")
SEVERITY_RANK = {"info": 0, "warning": 1, "error": 2}
METADATA_KEY = "jupyter_notebook_editing"


@dataclass(frozen=True)
class Heading:
    cell_index: int
    line_number: int
    level: int
    title: str
    cell_id: str | None


@dataclass(frozen=True)
class Diagnostic:
    path: Path
    severity: str
    code: str
    message: str
    cell_index: int | None = None
    cell_id: str | None = None
    line_number: int | None = None

    def render(self) -> str:
        location = str(self.path)
        if self.cell_index is not None:
            location += f": cell {self.cell_index}"
            if self.cell_id:
                location += f" ({self.cell_id})"
        if self.line_number is not None:
            location += f", line {self.line_number}"
        return f"{location}: {self.severity.upper()} [{self.code}] {self.message}"


@dataclass(frozen=True)
class CheckOptions:
    allow_numbered_headings: bool = False
    check_skipped_levels: bool = True
    check_multiple_h1: bool = True
    check_anchors: bool = True
    require_nbformat: bool = False


@dataclass
class Analysis:
    diagnostics: list[Diagnostic]
    headings: list[Heading]
    schema_engine: str


def source_text(cell: dict[str, Any]) -> str:
    source = cell.get("source", "")
    return "".join(str(part) for part in source) if isinstance(source, list) else str(source)


def source_like(original: Any, text: str) -> str | list[str]:
    return text.splitlines(keepends=True) if isinstance(original, list) else text


def markdown_structure(
    source: str,
) -> tuple[list[tuple[int, int, str]], list[tuple[int, int, str]]]:
    """Find ATX and Setext headings outside fenced code blocks."""
    lines = source.splitlines()
    atx: list[tuple[int, int, str]] = []
    setext: list[tuple[int, int, str]] = []
    fence_character: str | None = None
    fence_length = 0
    for line_number, line in enumerate(lines, start=1):
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character, fence_length = marker[0], len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character, fence_length = None, 0
            continue
        if fence_character is not None:
            continue
        heading = ATX_HEADING.match(line)
        if heading:
            title = (heading.group(2) or "").strip()
            title = re.sub(r"[ \t]+#+[ \t]*$", "", title).strip()
            atx.append((line_number, len(heading.group(1)), title))
        if line_number > 1:
            underline = SETEXT_UNDERLINE.match(line)
            preceding = lines[line_number - 2].strip()
            if underline and preceding:
                level = 1 if underline.group(1).startswith("=") else 2
                setext.append((line_number - 1, level, preceding))
    return atx, setext


def text_outside_fences(source: str) -> str:
    kept: list[str] = []
    fence_character: str | None = None
    fence_length = 0
    for line in source.splitlines():
        fence = FENCE.match(line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character, fence_length = marker[0], len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character, fence_length = None, 0
            continue
        if fence_character is None:
            kept.append(line)
    return "\n".join(kept)


def ignored_codes(cell: dict[str, Any]) -> set[str]:
    metadata = cell.get("metadata", {})
    configuration = metadata.get(METADATA_KEY) if isinstance(metadata, dict) else None
    if not isinstance(configuration, dict):
        return set()
    ignored = configuration.get("ignore", [])
    if ignored is True:
        return {"*"}
    if isinstance(ignored, str):
        return {ignored}
    if isinstance(ignored, list):
        return {item for item in ignored if isinstance(item, str)}
    return set()


def add_cell_diagnostic(
    diagnostics: list[Diagnostic], *, path: Path, cell: dict[str, Any],
    cell_index: int, severity: str, code: str, message: str,
    line_number: int | None = None,
) -> None:
    ignored = ignored_codes(cell)
    if "*" in ignored or "all" in ignored or code in ignored:
        return
    cell_id = cell.get("id")
    diagnostics.append(Diagnostic(
        path, severity, code, message, cell_index,
        cell_id if isinstance(cell_id, str) else None, line_number,
    ))


def basic_schema_diagnostics(notebook: Any, path: Path) -> list[Diagnostic]:
    """Perform a small structural fallback when nbformat is unavailable."""
    if not isinstance(notebook, dict):
        return [Diagnostic(path, "error", "invalid-notebook", "top level is not an object")]
    diagnostics: list[Diagnostic] = []
    if not isinstance(notebook.get("nbformat"), int):
        diagnostics.append(Diagnostic(path, "error", "invalid-nbformat", "top-level 'nbformat' must be an integer"))
    if not isinstance(notebook.get("metadata"), dict):
        diagnostics.append(Diagnostic(path, "error", "invalid-notebook-metadata", "top-level 'metadata' must be an object"))
    cells = notebook.get("cells")
    if not isinstance(cells, list):
        diagnostics.append(Diagnostic(path, "error", "invalid-cells", "top-level 'cells' must be a list"))
        return diagnostics
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            diagnostics.append(Diagnostic(path, "error", "invalid-cell", "cell is not an object", index))
            continue
        cell_id = cell.get("id")
        common = dict(path=path, cell_index=index, cell_id=cell_id if isinstance(cell_id, str) else None)
        if cell.get("cell_type") not in {"markdown", "code", "raw"}:
            diagnostics.append(Diagnostic(severity="error", code="invalid-cell-type", message="cell_type must be 'markdown', 'code', or 'raw'", **common))
        if not isinstance(cell.get("metadata"), dict):
            diagnostics.append(Diagnostic(severity="error", code="invalid-cell-metadata", message="cell metadata must be an object", **common))
        if not isinstance(cell.get("source"), (str, list)):
            diagnostics.append(Diagnostic(severity="error", code="invalid-cell-source", message="cell source must be a string or list of strings", **common))
    return diagnostics


def schema_diagnostics(notebook: Any, path: Path, *, require_nbformat: bool) -> tuple[list[Diagnostic], str]:
    try:
        import nbformat  # type: ignore[import-not-found]
    except ImportError:
        diagnostics = basic_schema_diagnostics(notebook, path)
        if require_nbformat:
            diagnostics.append(Diagnostic(path, "error", "nbformat-unavailable", "nbformat is required by --require-nbformat but is not installed"))
        return diagnostics, "basic JSON fallback"
    try:
        nbformat.validate(notebook)
    except Exception as error:  # nbformat exposes version-dependent error classes
        return [Diagnostic(path, "error", "schema-validation", f"nbformat schema validation failed: {error}")], "nbformat"
    return [], "nbformat"


def heading_slug(title: str) -> tuple[str, str | None]:
    explicit_match = CUSTOM_HEADING_ID.search(title)
    explicit = explicit_match.group(1) if explicit_match else None
    if explicit_match:
        title = title[:explicit_match.start()]
    plain = html.unescape(title)
    plain = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", plain)
    plain = re.sub(r"<[^>]+>", "", plain).replace("`", "")
    plain = re.sub(r"[^\w\- ]", "", plain, flags=re.UNICODE)
    return re.sub(r"\s+", "-", plain.strip().casefold()).strip("-"), explicit


def analyze_notebook(notebook: Any, path: Path, options: CheckOptions) -> Analysis:
    diagnostics, engine = schema_diagnostics(notebook, path, require_nbformat=options.require_nbformat)
    headings: list[Heading] = []
    if not isinstance(notebook, dict) or not isinstance(notebook.get("cells"), list):
        return Analysis(diagnostics, headings, engine)
    cells = notebook["cells"]
    seen_ids: dict[str, int] = {}
    markdown_cells: list[tuple[int, dict[str, Any], str]] = []
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict):
            continue
        cell_id_value = cell.get("id")
        cell_id = cell_id_value if isinstance(cell_id_value, str) else None
        if cell_id:
            if cell_id in seen_ids:
                add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=index, severity="error", code="duplicate-cell-id", message=f"cell ID was first used by cell {seen_ids[cell_id]}")
            else:
                seen_ids[cell_id] = index
        if cell.get("cell_type") != "markdown":
            continue
        source = source_text(cell)
        markdown_cells.append((index, cell, source))
        atx, setext = markdown_structure(source)
        headings.extend(Heading(index, line, level, title, cell_id) for line, level, title in atx)
        if setext:
            add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=index, severity="error", code="setext-heading", message="Setext heading detected; use one ATX heading line in its own Markdown cell", line_number=setext[0][0])
        if not atx:
            continue
        if len(atx) != 1 or len([line for line in source.splitlines() if line.strip()]) != 1:
            add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=index, severity="error", code="mixed-heading-cell", message="a heading cell must contain exactly one heading line and no body content")
        for line_number, _level, title in atx:
            if not title:
                add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=index, severity="error", code="empty-heading", message="heading title is empty", line_number=line_number)
            if not options.allow_numbered_headings and NUMBERED_TITLE.match(title):
                add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=index, severity="error", code="numbered-heading", message=f"heading appears manually numbered: {title!r}", line_number=line_number)
    if options.check_skipped_levels:
        for previous, current in zip(headings, headings[1:]):
            if current.level > previous.level + 1:
                cell = cells[current.cell_index]
                if isinstance(cell, dict):
                    add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=current.cell_index, severity="warning", code="skipped-heading-level", message=f"heading level jumps from H{previous.level} to H{current.level}", line_number=current.line_number)
    if options.check_multiple_h1:
        for heading in [item for item in headings if item.level == 1][1:]:
            cell = cells[heading.cell_index]
            if isinstance(cell, dict):
                add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=heading.cell_index, severity="warning", code="multiple-h1", message="notebook contains more than one H1 heading", line_number=heading.line_number)
    if options.check_anchors:
        valid: set[str] = set()
        counts: Counter[str] = Counter()
        for heading in headings:
            slug, explicit = heading_slug(heading.title)
            if explicit:
                valid.add(unquote(explicit).casefold())
            if slug:
                occurrence = counts[slug]
                valid.add(slug if occurrence == 0 else f"{slug}-{occurrence}")
                counts[slug] += 1
        for _index, _cell, source in markdown_cells:
            valid.update(unquote(anchor).casefold() for anchor in HTML_ANCHOR.findall(text_outside_fences(source)))
        for index, cell, source in markdown_cells:
            visible = text_outside_fences(source)
            links = [(match.group(1), match.group(2)) for match in MARKDOWN_INTERNAL_LINK.finditer(visible)]
            links.extend(("HTML link", anchor) for anchor in HTML_INTERNAL_LINK.findall(visible))
            for label, anchor in links:
                if unquote(anchor).casefold() not in valid:
                    add_cell_diagnostic(diagnostics, path=path, cell=cell, cell_index=index, severity="warning", code="unresolved-anchor", message=f"internal link {label!r} targets missing anchor #{unquote(anchor)}; check manual TOCs after renaming or unnumbering headings")
    return Analysis(diagnostics, headings, engine)


def section_end(headings: Sequence[Heading], position: int, cell_count: int) -> int:
    current = headings[position]
    for following in headings[position + 1:]:
        if following.level <= current.level:
            return max(current.cell_index, following.cell_index - 1)
    return max(current.cell_index, cell_count - 1)


def render_outline(headings: Sequence[Heading], cell_count: int) -> list[str]:
    return [
        f"H{heading.level} cell={heading.cell_index} id={heading.cell_id or 'no-id'} section={heading.cell_index}-{section_end(headings, position, cell_count)} title={heading.title or '<empty>'}"
        for position, heading in enumerate(headings)
    ]


def new_cell_id(existing: set[str]) -> str:
    while True:
        candidate = uuid.uuid4().hex[:8]
        if candidate not in existing:
            existing.add(candidate)
            return candidate


def simple_setext_replacement(source: str) -> str | None:
    nonempty = [(i, line.strip()) for i, line in enumerate(source.splitlines()) if line.strip()]
    if len(nonempty) != 2:
        return None
    (title_index, title), (underline_index, underline) = nonempty
    match = SETEXT_UNDERLINE.match(underline)
    if underline_index != title_index + 1 or not match:
        return None
    return f"{'#' if match.group(1).startswith('=') else '##'} {title}"


def split_heading_and_body(source: str) -> tuple[str, str] | None:
    atx, setext = markdown_structure(source)
    if len(atx) != 1 or setext:
        return None
    line_number, _level, _title = atx[0]
    lines = source.splitlines(keepends=True)
    index = line_number - 1
    if any(line.strip() for line in lines[:index]):
        return None
    body = "".join(lines[index + 1:])
    return (lines[index].rstrip("\r\n"), body) if body.strip() else None


def apply_safe_fixes(notebook: Any) -> list[str]:
    if not isinstance(notebook, dict) or not isinstance(notebook.get("cells"), list):
        return []
    cells = notebook["cells"]
    existing_ids = {cell["id"] for cell in cells if isinstance(cell, dict) and isinstance(cell.get("id"), str)}
    uses_ids = bool(existing_ids) or (notebook.get("nbformat") == 4 and isinstance(notebook.get("nbformat_minor"), int) and notebook["nbformat_minor"] >= 5)
    actions: list[str] = []
    fixed_cells: list[Any] = []
    for index, cell in enumerate(cells):
        if not isinstance(cell, dict) or cell.get("cell_type") != "markdown":
            fixed_cells.append(cell)
            continue
        original = cell.get("source", "")
        source = source_text(cell)
        replacement = simple_setext_replacement(source)
        if replacement is not None:
            updated = copy.deepcopy(cell)
            updated["source"] = source_like(original, replacement)
            fixed_cells.append(updated)
            actions.append(f"cell {index}: converted a simple Setext heading to ATX")
            continue
        split = split_heading_and_body(source)
        if split is None or cell.get("metadata", {}) not in ({}, None) or bool(cell.get("attachments")):
            fixed_cells.append(cell)
            continue
        heading_source, body_source = split
        heading_cell = copy.deepcopy(cell)
        heading_cell["source"] = source_like(original, heading_source)
        body_cell: dict[str, Any] = {"cell_type": "markdown", "metadata": {}, "source": source_like(original, body_source)}
        if uses_ids:
            body_cell["id"] = new_cell_id(existing_ids)
        fixed_cells.extend((heading_cell, body_cell))
        actions.append(f"cell {index}: split a leading ATX heading from its body; preserved the original cell ID and metadata")
    notebook["cells"] = fixed_cells
    return actions


def write_notebook_atomic(path: Path, notebook: Any) -> None:
    serialized = json.dumps(notebook, ensure_ascii=False, indent=1) + "\n"
    mode = path.stat().st_mode
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as stream:
            stream.write(serialized)
        os.chmod(temporary_name, mode)
        os.replace(temporary_name, path)
    except BaseException:
        try:
            os.unlink(temporary_name)
        except FileNotFoundError:
            pass
        raise


def load_notebook(path: Path) -> tuple[Any | None, list[Diagnostic]]:
    try:
        return json.loads(path.read_text(encoding="utf-8")), []
    except (OSError, UnicodeError, json.JSONDecodeError) as error:
        return None, [Diagnostic(path, "error", "notebook-read", f"cannot read notebook JSON: {error}")]


def check_notebook(path: Path, *, allow_numbered_headings: bool = False) -> list[str]:
    """Compatibility wrapper returning rendered diagnostics for one notebook."""
    notebook, diagnostics = load_notebook(path)
    if notebook is not None:
        diagnostics.extend(analyze_notebook(notebook, path, CheckOptions(allow_numbered_headings=allow_numbered_headings)).diagnostics)
    return [diagnostic.render() for diagnostic in diagnostics]


def parse_args(arguments: Iterable[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Check notebook heading isolation, hierarchy, internal anchors, cell IDs, and schema without executing code.")
    parser.add_argument("notebooks", nargs="+", type=Path)
    parser.add_argument("--outline", action="store_true", help="print each heading's level, title, cell index, ID, and section range")
    parser.add_argument("--allow-numbered-headings", action="store_true", help="permit headings that begin with apparent section numbers")
    parser.add_argument("--no-skipped-level-check", action="store_true", help="disable warnings for jumps such as H2 to H4")
    parser.add_argument("--allow-multiple-h1", action="store_true", help="disable warnings when a notebook contains multiple H1 headings")
    parser.add_argument("--no-anchor-check", action="store_true", help="disable approximate checks for unresolved internal links")
    parser.add_argument("--require-nbformat", action="store_true", help="fail instead of using basic JSON validation when nbformat is unavailable")
    parser.add_argument("--fail-on", choices=("error", "warning", "info", "never"), default="error", help="lowest severity producing a nonzero exit (default: error)")
    parser.add_argument("--fix", action="store_true", help="apply documented mechanical fixes and report every change")
    parser.add_argument("--dry-run", action="store_true", help="with --fix, report and validate proposed changes without writing")
    args = parser.parse_args(arguments)
    if args.dry_run and not args.fix:
        parser.error("--dry-run requires --fix")
    return args


def main(arguments: Iterable[str] | None = None) -> int:
    args = parse_args(arguments)
    all_diagnostics: list[Diagnostic] = []
    for path in args.notebooks:
        notebook, read_diagnostics = load_notebook(path)
        all_diagnostics.extend(read_diagnostics)
        if notebook is None:
            continue
        if args.fix:
            actions = apply_safe_fixes(notebook)
            if actions:
                if args.dry_run:
                    for action in actions:
                        print(f"{path}: WOULD FIX: {action}")
                else:
                    try:
                        write_notebook_atomic(path, notebook)
                    except OSError as error:
                        all_diagnostics.append(
                            Diagnostic(
                                path,
                                "error",
                                "notebook-write",
                                f"cannot write fixed notebook: {error}",
                            )
                        )
                    else:
                        for action in actions:
                            print(f"{path}: FIXED: {action}")
            else:
                print(f"{path}: no safe automatic fixes available")
        options = CheckOptions(
            allow_numbered_headings=args.allow_numbered_headings,
            check_skipped_levels=not args.no_skipped_level_check,
            check_multiple_h1=not args.allow_multiple_h1,
            check_anchors=not args.no_anchor_check,
            require_nbformat=args.require_nbformat,
        )
        analysis = analyze_notebook(notebook, path, options)
        all_diagnostics.extend(analysis.diagnostics)
        cells = notebook.get("cells", []) if isinstance(notebook, dict) else []
        if args.outline:
            print(f"{path}: outline")
            outline = render_outline(analysis.headings, len(cells) if isinstance(cells, list) else 0)
            print("\n".join(f"  {line}" for line in outline) if outline else "  <empty>")
        counts = Counter(item.severity for item in analysis.diagnostics)
        print(f"{path}: checked with {analysis.schema_engine}; {counts['error']} error(s), {counts['warning']} warning(s), {counts['info']} info message(s)")
    for diagnostic in all_diagnostics:
        print(diagnostic.render(), file=sys.stderr)
    if args.fail_on == "never":
        return 0
    threshold = SEVERITY_RANK[args.fail_on]
    return int(any(SEVERITY_RANK[item.severity] >= threshold for item in all_diagnostics))


if __name__ == "__main__":
    raise SystemExit(main())
