# Femboy Dress-Up Game (Python + Tkinter)

A simple, wholesome dress-up game built with Python's built-in `tkinter` library.

## Features

- Character customization (skin, hair, top, bottom, stockings, accessory)
- Pose selection (`Shy`, `Confident`, `Cheerful`)
- Random style challenges
- Scoring system based on style matches
- Zero external dependencies

## Requirements

- Python 3.8+
- Tkinter (included with most standard Python installs on Windows)

## Run Locally

```powershell
py game.py
```

If `py` does not work:

```powershell
python game.py
```

## Project Structure

```text
femboy_game/
  game.py
  README.md
  .gitignore
```

## Controls

- Click color swatches to customize outfit parts
- Use the `Pose` dropdown to change expression/arm position
- `Randomize Outfit` creates a random look
- `Submit Style` checks your match against the target style
- `New Challenge` creates a new target style

## Notes

- This is intentionally a single-file beginner-friendly project.
- You can easily expand it with sounds, more clothing categories, save/load, or sprite art.
