# Codex V2 Pet Contract

## Sprite Atlas

- Version: Codex v2 (`pet.json` contains `spriteVersionNumber: 2`).
- File: WebP.
- Dimensions: `1536x2288`.
- Grid: 8 columns x 11 rows.
- Cell: `192x208`.
- Background: transparent.
- Rows `0-8`: standard animation states.
- Rows `9-10`: 16 clockwise look directions.
- Unused standard-row cells: fully transparent.

Rows `0-8` follow `references/animation-rows.md`; row `1` is `running-right` and row `2` is `running-left`.

The 8x9 `1536x1872` atlas is an intermediate assembly artifact only. Never package it as a newly hatched pet.

## Look Directions

- Row `9`: `000`, `022.5`, `045`, `067.5`, `090`, `112.5`, `135`, `157.5` degrees.
- Row `10`: `180`, `202.5`, `225`, `247.5`, `270`, `292.5`, `315`, `337.5` degrees.
- `000` means up / 12 o'clock, not neutral/front.
- Neutral/front is the no-vector deadzone and falls back to idle.

## Local Custom Pet Package

Place files under:

```text
${DIMCODE_HOME:-$HOME/.dimcode/v2}/pets/<pet-id>/
├── pet.json
└── spritesheet.webp
```

Required manifest shape:

```json
{
  "id": "pet-id",
  "displayName": "Pet Name",
  "description": "A short sentence describing the Pet.",
  "spriteVersionNumber": 2,
  "spritesheetPath": "spritesheet.webp"
}
```

The app reads the row layout and playback cadence from its own animation contract. Omitting `spriteVersionNumber` means Codex v1 with 9 rows (`1536x1872`); newly generated Pets set it to `2` for 11 rows (`1536x2288`). `spritesheetPath` must be `spritesheet.webp`. Newly generated Pets include a non-empty `description` of at most 160 Unicode code points. Custom pet ids may not start with `bundled-`.
