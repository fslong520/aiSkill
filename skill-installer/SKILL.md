---
name: skill-installer
description: Install Agents skills from a curated list or a GitHub repo, either loose or packaged as one plugin. Use when a user asks to list installable skills, install a curated skill, install a skill from another repo (including private repos), or import a whole collection of skills.
metadata:
  short-description: Install curated skills from openai/skills or other repos
---

# Skill Installer

Helps install skills. By default these are from https://github.com/openai/skills/tree/main/skills/.curated, but users can also provide other locations. Experimental skills live in https://github.com/openai/skills/tree/main/skills/.experimental and can be installed the same way.

Use the helper scripts based on the task:
- List skills when the user asks what is available, or if the user uses this skill without specifying what to do. Default listing is `.curated`, but you can pass `--path skills/.experimental` when they ask about experimental skills.
- Install from the curated list when the user provides a skill name.
- Install from another repo when the user provides a GitHub repo/path (including private repos).

## Step 1: Classify the source before installing

Not every path a user points at is a single skill. Check what it actually is:

| What is at the path | How to tell | What to do |
| --- | --- | --- |
| One skill | the directory contains `SKILL.md` | install it directly, no questions |
| A collection / category | no `SKILL.md`, but subdirectories have one | **ask how to import** (step 2) |
| A plugin | repo root has `.codex-plugin/plugin.json` or `.claude-plugin/plugin.json` | not this skill's job — use `dim plugin install <source>` |
| A marketplace | repo has a `marketplace.json` catalog | not this skill's job — use `dim plugin marketplace add <source>` |

`scripts/install-skill-from-github.py --list-candidates --path <dir>` prints the
skills under a directory (add `--format json` to read it back reliably). Use it
when the path is not itself a skill.

## Step 2: Ask how to import a collection

When two or more skills come from the same place, ask once — the answer changes
how the user manages them afterwards, and it can't be inferred. Use a structured
question tool if one is available; otherwise ask in plain text:

```
Found a skill collection at vercel-labs/agent-skills (web/, 5 skills):
  better-ui, better-colors, better-layout, better-typography, better-writing

How should these be installed?
1. As one plugin "agent-skills-web" (recommended)
   Appears under Plugins: enable, disable or remove all five together,
   with per-skill switches on its detail page.
2. Loose
   Appears as five separate entries under Skills, managed one by one.
3. Loose, into the shared ~/.agents/skills directory
   Other agents (Codex and so on) can see them, but Dim no longer
   manages their updates.
```

When to ask:

| Situation | What to do |
| --- | --- |
| One skill | install loose, don't ask |
| Two or more skills from one source | ask once, then reuse that answer for the rest of the conversation |
| The user already said how they want it | don't ask |
| No one is there to answer | install loose and mention `--as-plugin` in the result |

## Step 3: Install

Install skills with the helper scripts.

Loose (default — installs into Dim's own skills directory):

```
scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]
```

As one plugin:

```
scripts/install-skill-from-github.py --repo <owner>/<repo> --path <dir>/<skill-a> <dir>/<skill-b> --as-plugin [--plugin-name <name>]
```

`--as-plugin` packages the skills into a plugin bundle and hands it to
`dim plugin install`, so the bundle goes through the same manifest check,
conflict check and provenance the plugin market uses. Upgrading it later is a
reinstall: `dim plugin install <source> --overwrite`.

## Communication

When listing skills, output approximately as follows, depending on the context of the user's request. If they ask about experimental skills, list from `.experimental` instead of `.curated` and label the source accordingly:
"""
Skills from {repo}:
1. skill-1
2. skill-2 (already installed)
3. ...
Which ones would you like installed?
"""

After installing a skill, tell the user: "Restart Agents to pick up new skills."

## Scripts

All of these scripts use network, so when running in the sandbox, request escalation when running them.

- `scripts/list-skills.py` (prints skills list with installed annotations)
- `scripts/list-skills.py --format json`
- Example (experimental list): `scripts/list-skills.py --path skills/.experimental`
- `scripts/install-skill-from-github.py --repo <owner>/<repo> --path <path/to/skill> [<path/to/skill> ...]`
- `scripts/install-skill-from-github.py --url https://github.com/<owner>/<repo>/tree/<ref>/<path>`
- Example (experimental skill): `scripts/install-skill-from-github.py --repo openai/skills --path skills/.experimental/<skill-name>`
- Example (collection as a plugin): `scripts/install-skill-from-github.py --repo vercel-labs/agent-skills --path web/better-ui web/better-colors --as-plugin`

## Behavior and Options

- Defaults to direct download for public GitHub repos.
- If download fails with auth/permission errors, falls back to git sparse checkout.
- Aborts if the destination skill directory already exists.
- Installs into `<dimcodeHome>/skills/<skill-name>` (default `~/.dimcode/v2/skills`), which is where Dim keeps the skills it manages. `--shared` installs into `~/.agents/skills` instead, so other agents can see the skill — at the cost of Dim no longer managing its updates.
- `--as-plugin` installs one plugin into `<dimcodeHome>/plugins/<name>` instead of loose skills; `--plugin-name` overrides the derived name and `--overwrite` replaces an existing plugin of that name.
- Multiple `--path` values install multiple skills in one run, each named from its `SKILL.md` unless `--name` is supplied.
- Options: `--ref <ref>` (default `main`), `--dest <path>`, `--method auto|download|git`.

## Notes

- Curated listing is fetched from `https://github.com/openai/skills/tree/main/skills/.curated` via the GitHub API. If it is unavailable, explain the error and exit.
- Private GitHub repos can be accessed via existing git credentials or optional `GITHUB_TOKEN`/`GH_TOKEN` for download.
- Git fallback tries HTTPS first, then SSH.
- The skills at https://github.com/openai/skills/tree/main/skills/.system are preinstalled, so no need to help users install those. If they ask, just explain this. If they insist, you can download and overwrite.
- Installed annotations come from every directory the runtime scans — Dim's own skills dir, the shared `~/.agents/skills`, and skills carried by installed plugins — and match on the `name` in `SKILL.md`, not the directory name.
- **A name clash aborts the install.** Skills resolve by name, so a second skill under an existing name would never load. The script reports which skill already owns the name and where it lives; the user removes or renames it (or drops it from the install) before retrying. Do not work around this by renaming silently.
