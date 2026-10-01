---
name: jupyter-notebook-editing
description: Create, edit, or restructure Jupyter notebooks, especially training and tutorial notebooks, while preserving a navigable outline and reliable section collapsing. Use for changes to instructional content, Markdown, code cells, exercises, or section order. This skill does not cover broader output policy, reproducible execution, CI, dependencies, data provenance, or reusable-module extraction.
---

# Jupyter Notebook Editing

## Purpose

Keep Jupyter notebooks, particularly training and tutorial notebooks, easy to navigate
and reorganize. Treat the cell sequence and heading hierarchy as part of the
notebook's user interface, not merely as serialized content.

Apply repository instructions and the user's requested content first. This skill adds
structural notebook conventions; it does not prescribe the scientific content or the
repository's output-commit policy.

## Routing

- Use this skill for direct notebook editing: instructional explanations, examples,
  exercises, Markdown or code cells, heading structure, and section order.
- For workflow-level concerns such as output policy, clean reproducible execution,
  CI, dependencies, data provenance, generated artifacts, or extracting reusable
  code into modules, follow the repository's workflow guidance and use a suitable
  notebook-workflow or reproducibility skill when one is available. Combine that
  guidance with this skill when a notebook edit also changes those concerns.
- Use `scientific-computing-training-design-and-review` alongside this skill when the
  request concerns learning objectives, instructional sequence, cognitive load,
  exercise quality, prerequisites, or course scope rather than cell editing alone.

Do not activate workflow or training-design guidance merely because the file is a
notebook used for teaching; route according to the requested work.

## Structural invariants

### Keep every heading in its own Markdown cell

- A heading cell contains exactly one ATX-style heading line, such as
  `## Memory use`.
- Do not put prose, lists, equations, links, images, tables, callouts, code fences, or
  a second heading in that cell.
- Put the section's introductory text in the following Markdown cell, even when it is
  only one sentence.
- Use heading levels to express hierarchy, not to make text visually larger. Avoid
  skipping levels when the surrounding notebook permits a consistent hierarchy.

This boundary is operational: notebook interfaces can collapse a section reliably
only when the heading is a separate cell from the section body.

### Use unnumbered headings by default

- Write `## Memory use`, not `## 3. Memory use` or `## 3.2 Memory use`.
- Do not add or maintain manual section numbers merely to communicate order; the cell
  sequence already provides order, and unnumbered headings remain correct when content
  moves.
- When editing a partially numbered notebook, use unnumbered headings for the touched
  structure. Do not renumber or rewrite unrelated headings unless the task includes a
  structural cleanup.
- Preserve numbering only when the user explicitly requests it or an external
  publishing standard requires it.

### Use dollar delimiters for Markdown mathematics

- In notebook Markdown cells, write inline mathematics between single dollar signs,
  for example `$\alpha$`.
- Write display mathematics between double dollar signs, with both delimiters on
  their own lines:

  ```markdown
  $$
  E = m c^2
  $$
  ```

  Here, $E$ is energy, $m$ is mass, and $c$ is the speed of light.
- Do not use `\(...\)` for inline mathematics or `\[...\]` for display mathematics in
  notebooks handled by this skill. Although some Markdown and MathJax configurations
  support those delimiters, they have not rendered reliably in the target JupyterLab
  workflow and their backslashes are easier to damage during programmatic notebook
  editing.
- The fenced block above illustrates literal Markdown syntax. Do not wrap an actual
  formula in a code fence, because a code fence prevents mathematical rendering.
- After programmatic edits, inspect the serialized Markdown source to confirm that
  LaTeX backslashes were preserved, and preview the rendered cell in JupyterLab when
  practical. Define every symbol when it is first introduced in instructional text.

## Editing workflow

1. Inspect the full heading outline and the cells around the target section before
   editing. Do not infer section boundaries from one cell alone.
2. When adding a section, create a heading-only Markdown cell followed by separate
   Markdown, code, raw, or output-bearing cells for its contents.
3. When moving a section, move its heading and every subordinate cell up to, but not
   including, the next heading of the same or higher level. Do not orphan a heading or
   leave its explanatory cells behind.
4. Preserve existing cell IDs and relevant metadata when moving or editing cells.
   Give new cells unique IDs when the notebook format uses them. Avoid unrelated
   metadata and output churn.
5. Preserve the notebook's established output policy. A Markdown-only structural edit
   does not by itself justify rerunning expensive code; a code change should receive
   execution validation proportionate to its cost and risk.
6. Inspect the resulting outline as a reader would. Confirm that collapsing each
   heading hides the intended section and that moving a section would not require
   renumbering later headings.

## Validation

Run the included structural check after creating or editing a notebook. Resolve the
script path relative to this `SKILL.md`, rather than assuming the current working
directory is the skill directory:

```bash
python3 <skill-directory>/scripts/check_notebook_structure.py path/to/notebook.ipynb
```

The checker validates the notebook schema with `nbformat` when available and otherwise
uses a basic JSON-structure fallback. It reports heading cells that also contain body
content, Setext-style headings, empty or apparently numbered headings, duplicate cell
IDs, hierarchy warnings, and unresolved internal links such as manual table-of-contents
entries left stale after a heading rename.

Use `--outline` before and after structural edits to inspect each heading's level,
title, cell index, cell ID, and computed section range. Errors fail by default;
warnings are visible but non-failing. Use `--fail-on warning` for a stricter check, and
disable individual heuristic warnings only when the notebook intentionally uses a
different structure.

The optional fix mode is deliberately narrow. Run `--fix --dry-run` first, inspect
every reported change, and use `--fix` only when the proposed mechanical changes are
appropriate. It can convert a simple Setext heading or split an unambiguous leading
ATX heading from body text. It does not remove section numbers, repair anchors, infer
semantic section boundaries, or move sections. It preserves existing cell IDs and
metadata and reports every change; a split creates a new ID only for the new body cell
when the notebook format uses IDs.

For all command-line options, per-cell diagnostic exemptions, severity behavior, fix
limitations, and optional pre-commit configuration, read
[references/validation.md](references/validation.md). Never install or modify a
project's pre-commit hooks unless the user explicitly asks.

Also validate at the appropriate notebook layer:

- parse the notebook and validate its schema with `nbformat` when available;
- inspect the serialized Markdown cell sources after programmatic edits;
- execute the smallest representative path needed for code changes;
- state clearly when a full clean-kernel run or rendered preview was not practical.

The structural checker does not understand the semantic meaning of a section. Manual
outline review remains necessary after moving or splitting content. Internal-anchor
matching is renderer-dependent, so treat unresolved-anchor warnings as prompts for
manual preview rather than proof that a link is broken.

## Avoid

- `## Results` followed by result prose in the same Markdown cell;
- several headings in one Markdown cell;
- manually numbered headings whose numbers become stale after reordering;
- moving a heading without its complete section body;
- rewriting execution counts, outputs, cell IDs, or metadata as a side effect of an
  otherwise Markdown-only edit.
