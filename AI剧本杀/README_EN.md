# Fated Codex (诡世命簿)

A turn-based isekai life simulation game engine. Each playthrough generates a unique world and background — make choices every turn and experience a complete life from birth to death.

## Quick Start

### Start a New Game
Say: **"Start a new game"** or **"Open the Codex"**

The system will:
1. Randomly generate an isekai world (you can specify preferences)
2. Randomly generate your background and origin
3. Enter your very first turn of life

### Continue Your Game
Say: **"Continue"** or **"Next turn"**

### Check Your Status
Say: **"Status"** or **"Attributes"**

### Generate Images
Say: **"Generate character card"** or **"Generate scene"**

## Commands

| Command | Description |
|---------|-------------|
| New game / Start | Begin a new life |
| Continue / Next turn | Advance time |
| Skip N turns | Fast-forward N turns |
| Status / Attributes | Show current status |
| Story | Show story records |
| World / World info | Show world information |
| Character [name] | Show character card |
| Relations | Show relationships |
| Save | Save game |
| Load [name] | Load a save |
| Generate character card | Generate character card image |
| Generate scene | Generate scene image |

## File Structure

```
Fated-Codex/
├── SKILL.md              # Core game engine specification
├── README.md             # This file
├── references/
│   ├── world_gen.md      # World generation rules
│   ├── event_system.md   # Event system rules
│   └── time_system.md    # Time system rules
├── assets/
│   ├── templates/
│   │   ├── character_template.md  # Character card template
│   │   └── event_template.md       # Event display template
│   └── prompts/
│       ├── image_prompt.md  # Image generation prompts
│       └── story_prompt.md   # Story narrative generation rules
├── saves/                # Save files
└── stories/              # Story archives
```

## Features

- **Random World Generation** — Every playthrough creates a brand-new world with unique magic systems, races, nations, and history
- **Random Origin** — Your fate is sealed from birth: race, family, talents, and traits
- **Turn-Based Progression** — Each turn advances one year, driving your life forward through six distinct life stages
- **Event & Choice System** — Random events, destiny milestones, and player-driven choices shape your story
- **Dynamic Story Generation** — A full narrative is auto-generated and recorded as you play
- **AI Image Generation** — Character cards and scene illustrations at key moments throughout the story
- **Save & Load** — Auto-saves every turn, with manual save slots for multiple playthroughs
- **Life Stage System** — Baby, Child, Teen, Young Adult, Middle Age, Elder — each with unique event pools and growth mechanics

## World Types

| World Type | Theme |
|------------|-------|
| Fantasy Medieval | Swords and sorcery |
| Eastern Xianxia | Cultivation and immortality |
| Steampunk | Gears and machinery |
| Dark Fantasy | Lovecraftian horror |
| Superpower Urban | Modern superpowers |
| Primitive Tribes | Ancient civilizations |
| Post-Apocalyptic | Ruins of civilization |

## Life Stages

| Stage | Age | Focus |
|-------|-----|-------|
| Baby | 0-3 | Passive events, talent awakening |
| Child | 4-12 | Learning, growth, early social |
| Teen | 13-17 | Education choices, first love, rebellion |
| Young Adult | 18-35 | Career, marriage, adventure |
| Middle Age | 36-55 | Family, legacy, succession |
| Elder | 56+ | Reflection, heritage, final acts |

## Developer Notes

This game is powered by a Skill-driven AI engine. The core logic is defined in `SKILL.md`, with detailed rules in the `references/` directory.

### Extending the Game

- **Add new event types** → Edit `references/event_system.md`
- **Add world-building elements** → Edit `references/world_gen.md`
- **Add event templates** → Edit `assets/templates/event_template.md`

### How It Works

This is an AI-driven game engine built entirely from markdown specifications and JSON data files. The Skill system acts as the runtime: it reads `SKILL.md` and reference files to understand game rules, uses JSON files for persistent state, and generates narrative content and images on-the-fly using LLM and image generation capabilities.

## License

[MIT](./Fated-Codex/LICENSE) — Copyright 2026 fslong

---

*May your isekai life be extraordinary!*
