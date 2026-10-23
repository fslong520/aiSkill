# Model Notes

This file is the entry point for provider/model experience. When a provider or model needs special handling, add a row here and put detailed notes under `references/models/`.

## Current Entries

| Provider / model | Capability | Note |
|---|---|---|
| CosyVoice2 | `speech.synthesize` | `--voice` uses `model-name:voice-name` |
| Video generation models | `video.generate` | Generation can take a long time; use a generous `--timeout` and keep operation id / JSON errors |
| Image edit models | `image.edit` | Requires `--image` and `--prompt`; pass repeated `--image` flags for multi-image edit. Per-provider limits below |
| ASR models | `speech.transcribe` | Input is `--audio`; output should be a text file |

## Reference Image Limits For `image.edit`

Generating with reference images always goes through `dim image edit`, never
`dim image generate` — the generate command takes no `--image` flag.

| Provider | References per edit |
|---|---|
| `google` (Gemini / Nano Banana) | Many; each `--image` becomes its own reference part |
| `openai` and OpenAI-compatible providers | Many; each `--image` becomes an `image[]` entry |
| `openai-codex` (`gpt-image-2`) | Many; not yet confirmed against the ChatGPT backend |
| `black-forest-labs` (`flux-2-*`) | Up to 8 |
| `siliconflow` | Up to 3 |
| `stepfun`, `stability-ai` | Exactly 1 |
| `grok-build` / `xai` (`grok-imagine-image-2.0`) | Up to 5 |
| `grok-build` / `xai` (older Imagine image models) | Up to 3 |

When the user supplies more references than the configured model accepts, say so and ask
whether to drop some or switch models. Do not silently discard reference images.

## Grok Build / xAI Imagine

Use `grok-imagine-image-2.0` for image generation/editing. Image `--size` accepts `auto`, `1k`, or `2k`, not pixel dimensions. Use an `--options` JSON file with `{"aspect_ratio":"16:9"}` for proportions. Image 2.0 accepts `--quality low|medium|auto`; older image models do not accept quality. Omit `--format` and use `--out-dir` to save the provider's native MIME format.

```bash
dim image generate --provider grok-build --model grok-imagine-image-2.0 --prompt "A red ceramic cup" --size 2k --quality low --out-dir ./artifacts --json
```

Video models support 1–15 seconds and a source `--image`. Use `grok-imagine-video-1.5` for 1080p through `--options` containing `{"resolution":"1080p"}`. Reference-to-video supports up to 720p. The CLI polls the returned task and saves the video. Grok Build uses its existing OAuth login; provider entitlement failures must be reported without repeatedly retrying unchanged requests.

## CosyVoice2 Voices

CosyVoice2 `--voice` format:

```text
model-name:voice-name
```

Available voice names:

```text
alex
benjamin
charles
david
anna
bella
claire
diana
```

`alex`, `benjamin`, `charles`, and `david` are male voices. `anna`, `bella`, `claire`, and `diana` are female voices.

Example:

```bash
dim speech synthesize --text "Hello, this is a test." --voice "CosyVoice2:anna" --out ./artifacts/speech.mp3 --json
```

If the configured model id is not exactly `CosyVoice2`, replace the part before `:` with the configured model name or model id.

## Adding Future Model Notes

When adding a model note:

1. Create a file under `references/models/` named after the provider and model.
2. Add a row to the table above.
3. Include:
   - Supported capability.
   - Required inputs.
   - Recommended output format.
   - Known slow paths or failure modes.
   - One runnable `dim ... --json` example.
