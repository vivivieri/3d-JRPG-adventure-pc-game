# ACE-Step prompt — `bgm_ending_anchor`

| Field | Value |
|-------|-------|
| Scene | SC-17b Anchor ending movie |
| Category | ending |
| Output | `game/assets/audio/bgm/bgm_ending_anchor.ogg` |
| Duration | 90 s |
| Loop | False |
| BPM | 80 |
| Key | C major |

## Prompt

ending movie dawn hope, box shatters spirit light scatters, soft piano and koto sapling planting, gentle rebuild 80 BPM instrumental fade ending

## Negative

vocals, lyrics, singing, upbeat pop, EDM drop, heavy metal, bright cheerful, cartoon comedy, European fantasy brass, copyrighted melody

## ACE-Step Gradio / API

1. `bash tools/install_ace_step.sh`
2. `cd .cache/ace-step-1.5 && uv run acestep` (or `uv run acestep-api`)
3. Paste prompt; set duration/BPM/key; export WAV
4. `ffmpeg -i track.wav -c:a libvorbis -q:a 4 game/assets/audio/.../track.ogg`
5. `python3 tools/register_asset.py add ...`
