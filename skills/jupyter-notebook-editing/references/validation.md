# Notebook Structure Validation

Use this reference when configuring the bundled validator beyond its default check.
The validator never executes notebook code.

## Inspection and strictness

```bash
python3 scripts/check_notebook_structure.py --outline notebook.ipynb
python3 scripts/check_notebook_structure.py --fail-on warning notebook.ipynb
```

`--outline` prints the heading level, title, zero-based cell index, cell ID, and
inclusive section range. A section ends immediately before the next heading of the
same or a higher level.

Diagnostics have `error`, `warning`, or `info` severity and a stable code. Errors fail
by default. `--fail-on warning` also makes heuristic warnings fail; `--fail-on never`
is useful for exploratory audits but should not be used to claim validation passed.

The default hierarchy checks warn about skipped heading levels and multiple H1 cells.
Use `--no-skipped-level-check` or `--allow-multiple-h1` only for intentional notebook
structures. Use `--no-anchor-check` when the target renderer uses anchor rules that
the validator cannot model. Anchor checks approximate common Jupyter and GitHub
rendering and inspect Markdown and HTML links to headings or explicit anchors.

`nbformat` schema validation is used when the package is installed. Otherwise the
validator checks essential JSON structure without installing anything. Use
`--require-nbformat` when CI must fail if full schema validation is unavailable.

## Per-cell exemptions

Suppress a known false positive with cell metadata rather than weakening checks for
the entire notebook:

```json
{
  "metadata": {
    "jupyter_notebook_editing": {
      "ignore": ["numbered-heading", "unresolved-anchor"]
    }
  }
}
```

Use the diagnostic code printed in square brackets. `"ignore": true`, `"all"`, or
`"*"` suppresses every cell-level diagnostic and should be rare. Schema-level
problems cannot be exempted because the cell metadata may itself be invalid.

## Safe fix mode

Always preview first:

```bash
python3 scripts/check_notebook_structure.py --fix --dry-run notebook.ipynb
python3 scripts/check_notebook_structure.py --fix notebook.ipynb
```

The fixer reports every proposed or applied change. It only converts a cell that
contains one simple Setext heading, or splits a leading ATX heading from body content
when that cell has no metadata or attachments. Existing IDs and metadata remain on
the original heading cell. A split body receives a new unique ID only when the
notebook format uses cell IDs.

The fixer deliberately does not remove heading numbers, rewrite internal links, move
sections, or split ambiguous cells. Those operations require semantic review. Writing
a fixed notebook reserializes its JSON, so inspect the resulting version-control diff
for formatting or metadata churn as well as semantic changes.

## Optional pre-commit use

Do not install or modify hooks automatically. If the user wants this validator in a
repository, add a local hook deliberately and replace the placeholder with a stable
path available to every contributor:

```yaml
repos:
  - repo: local
    hooks:
      - id: notebook-structure
        name: notebook structure
        entry: python3 /absolute/path/to/check_notebook_structure.py --fail-on warning
        language: system
        files: '\.ipynb$'
```

An absolute path into one user's personal skill directory is not portable. For a
shared hook, keep a reviewed copy or project-owned wrapper in the repository, document
how it is updated, and ensure `python3` plus any required `nbformat` version comes from
the repository's normal development environment.
