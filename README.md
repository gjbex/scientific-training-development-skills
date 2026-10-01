# Scientific Training Development Skills

A skills-only plugin for designing, reviewing, and editing scientific-computing
training material. It uses the portable
[Agent Plugins layout](https://developers.openai.com/plugins/build/plugins) and does
not require an MCP server.

## Included skills

| Skill | Purpose |
| --- | --- |
| `jupyter-notebook-editing` | Create, edit, or restructure instructional Jupyter notebooks while preserving a navigable, collapsible section structure. Includes a notebook structure validator. |
| `scientific-computing-training-design-and-review` | Design or review concept-led scientific-computing training for realistic scope, sound learning objectives, meaningful exercises, and participant value. |

## Install in Codex

### From GitHub

Add this repository as a plugin marketplace:

```bash
codex plugin marketplace add gjbex/scientific-training-development-skills
```

Then start Codex, run `/plugins`, select **Scientific Training Development
Skills**, and install **Scientific Training Development Skills**. Start a new chat
after installation so the skills are discovered.

To update an existing marketplace checkout:

```bash
codex plugin marketplace upgrade scientific-training-development-skills
```

### From a local checkout

For development or testing, add the repository directory directly:

```bash
codex plugin marketplace add /absolute/path/to/scientific-training-development-skills
```

Restart the ChatGPT desktop app if you use Codex there, then install the plugin
from `/plugins`. The marketplace entry points at the repository root, so keep the
portable `plugin.json` and `skills/` directory there.

### Install only the skills

If plugin marketplaces are unavailable, copy the individual skill directories into
the Codex skills directory:

```bash
mkdir -p ~/.codex/skills
cp -R skills/jupyter-notebook-editing ~/.codex/skills/
cp -R skills/scientific-computing-training-design-and-review ~/.codex/skills/
```

Restart Codex or start a new chat after copying them.

## Install in other agentic frameworks

Frameworks that support the portable Agent Plugins specification can install this
repository as a plugin. Point the framework at the repository root, which contains
`plugin.json` and the conventional `skills/` directory.

Frameworks that support Agent Skills but not plugin manifests can install the two
directories under `skills/` into their configured skills directory. Preserve each
directory intact: `SKILL.md` may refer to files in `agents/`, `references/`, or
`scripts/` by relative path.

The `agents/openai.yaml` files provide Codex-specific display metadata. Other hosts
may ignore them; the operational instructions remain in each `SKILL.md`. Exact
installation commands and skill-discovery behavior vary by framework, so consult the
host's documentation rather than assuming Codex marketplace commands are portable.

## Repository layout

```text
.
|-- plugin.json
|-- .agents/plugins/marketplace.json
`-- skills/
    |-- jupyter-notebook-editing/
    `-- scientific-computing-training-design-and-review/
```

## Development notes

- Keep the plugin skills-only unless a real tool dependency justifies adding an MCP
  server.
- Validate both `SKILL.md` files after changing their frontmatter or directory names.
- Run the notebook validator's help command as a quick smoke test:

  ```bash
  python3 skills/jupyter-notebook-editing/scripts/check_notebook_structure.py --help
  ```

## License

Licensed under the Apache License, Version 2.0. See [LICENSE](LICENSE). Attribution
information is provided in [NOTICE](NOTICE).
