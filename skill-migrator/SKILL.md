---
name: skill-migrator
description: Migrate existing Codex, Claude, or npx skills into Dim. Use when a user wants to bring skills from ~/.codex/skills, ~/.claude/skills, ~/.agents/skills, project skill directories, or another local skill folder into Dim, especially when several skills should be managed together as one plugin.
metadata:
  short-description: Migrate Codex and Claude skills into Dim
---

# Skill Migrator

Move existing skills into Dim's managed installation model without losing the
source files, metadata, scripts, references, or assets.

This skill is for migration, not for silently copying a directory. Always inspect
the source first, explain what will happen, and preserve the original until the
Dim installation has been verified.

## Supported sources

Check these locations in this order when the user says "my Codex skills",
"my Claude skills", or "skills installed with npx skills":

1. `~/.agents/skills/` — the usual shared user-level skills directory.
2. `~/.codex/skills/` — Codex-specific user skills, when present.
3. `~/.claude/skills/` — Claude user-level skills, when present.
4. `<project>/.agents/skills/` — shared project-scoped skills.
5. `<project>/.claude/skills/` — Claude project-scoped skills.
6. A local directory or repository path explicitly supplied by the user.

Do not assume that a directory name is the skill identity. Read each
`SKILL.md` frontmatter and use its canonical `name`. A valid skill directory
must contain a readable `SKILL.md` with non-empty `name` and `description`
fields.

## Classify before migrating

Inspect the source root and classify it:

- A directory containing `SKILL.md` is one skill.
- A directory without `SKILL.md` whose child directories contain two or more
  valid `SKILL.md` files is a skill collection.
- A root containing `.codex-plugin/plugin.json` or
  `.claude-plugin/plugin.json` is already a plugin. Do not wrap it in another
  plugin; use the existing plugin install flow.
- A repository containing a marketplace catalog is a plugin marketplace source,
  not a loose skill collection.

If the source is ambiguous, show the discovered paths and ask the user to
choose. Never guess a nested directory or silently skip invalid entries.

## Choose the destination

For one skill, install it as a standalone Dim skill unless the user requests a
plugin.

For two or more skills from the same source, recommend one plugin:

```text
Found N skills from <source>.
Recommended: import them as one plugin
  - one enable/disable switch
  - one uninstall boundary
  - individual skill switches on the plugin detail page

Alternative: import them as standalone skills
  - each skill is managed separately in Skills
```

If the user chooses a plugin, derive a stable lower-case hyphenated plugin name
from the source or collection directory. Ask for a name when the derived name
would be empty, ambiguous, or already installed. Use the real collection name
as the plugin display name when it is available.

Do not offer `~/.agents/skills` as a Dim installation destination by default.
That directory is shared with other agents and should only be written when the
user explicitly asks for cross-agent sharing. Dim-managed output belongs in its
private skills or plugins root.

## Migration procedure

1. Discover candidate directories and read their `SKILL.md` files.
2. Report the canonical names, source paths, and any invalid or duplicate names.
3. Check all skill discovery roots for canonical-name conflicts, including
   existing Dim skills, shared skills, project skills, and skills inside plugins.
4. Stop on a conflict. Report both paths and ask the user to rename, remove, or
   exclude one. Never silently rename a skill because the runtime resolves
   skills by canonical name.
5. Preserve the complete skill directory. Copy `SKILL.md`, `scripts/`,
   `references/`, `assets/`, `agents/`, and other files unless the user
   explicitly asks for a minimal import.
6. Install through the existing Dim skill/plugin installer. Do not implement a
   second ad-hoc copy protocol in the conversation.
7. Verify the installed result by rescanning Dim's skills and plugins, checking
   canonical names and the plugin component list.
8. Only after verification, offer to archive or remove the original. Never
   delete `~/.codex/skills`, `~/.claude/skills`, `~/.agents/skills`, or a
   project directory without explicit confirmation.

## Plugin layout

When importing a collection as one plugin, the resulting bundle should have
this shape:

```text
<plugin>/
├── .codex-plugin/plugin.json
└── skills/
    ├── <skill-a>/SKILL.md
    ├── <skill-b>/SKILL.md
    └── ...
```

For a skills-only migration, this is the complete Dim manifest contract. Use it
directly; do not pause to research or reconfirm the format after the user has
already selected the skills and the plugin installation mode:

```json
{
  "name": "<lower-case-hyphenated-plugin-id>",
  "version": "0.0.0",
  "description": "",
  "interface": {
    "displayName": "<real collection or user-facing title>"
  },
  "skills": "./skills"
}
```

Manifest rules:

- Write the file at `<bundle>/.codex-plugin/plugin.json`.
- `name` is the stable internal id and plugin directory name. It must be
  non-empty, lower-case hyphen-case, and contain only letters, digits, `.`, `_`,
  or `-`.
- `interface.displayName` is the real user-facing collection title. It does not
  need to match `name`.
- Use `version: "0.0.0"` for a generated migration bundle unless the source
  provides a meaningful bundle version.
- Keep `description: ""` when no collection description exists; do not insert
  placeholder text.
- Use exactly `skills: "./skills"` and place every migrated skill at
  `<bundle>/skills/<directory>/SKILL.md`.
- Do not add `hooks`, `mcpServers`, `agents`, or other manifest fields for a
  skills-only migration.
- Keep each skill's canonical frontmatter name unchanged.

After creating the temporary bundle, install it through:

```bash
dim plugin install <bundle-path> --generated --provenance-source <source-path>
```

Use `--overwrite` only when the user explicitly chose to replace an existing
plugin with the same internal name. The plugin installer owns final validation,
conflict checks, provenance, and destination placement. Do not manually copy the
finished bundle into Dim's plugins directory.

Once the user has selected the skills and chosen "install as one plugin", proceed
with bundle creation and installation. Do not answer with "let me confirm the
manifest format" or ask the same installation-mode question again.

## npx skills guidance

When the user says they installed skills with `npx skills`, first inspect the
user and project skill roots above. The CLI may have installed a single skill,
several skills from a collection, or a plugin-shaped source. Use the files that
are actually present as the source of truth rather than reconstructing the
repository URL from memory.

If only a repository URL is available, use the existing `skill-installer` flow
to fetch and classify it. If the user asks for a plugin result, pass the
collection's skill directories through the plugin bundle path instead of
installing them loose and then copying them a second time.

## Communication

Tell the user:

- what was found and where;
- whether the result is a standalone skill or a plugin;
- the Dim-managed destination;
- which original files remain untouched;
- whether a new session or reload is needed before the migrated skill can be
  used by the agent.

If migration is blocked, report the exact conflict or invalid file and stop.
