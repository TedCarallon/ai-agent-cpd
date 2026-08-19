# Workshop agent notes

This repository is a **starter arcade cabinet** for a hands-on agentic-coding workshop. The menu runs today. Snake, Pong, and Tetris are **not** implemented until the human asks.

## When the human wants a game

1. Read the matching prompt in `README.md` (do not invent a different game).
2. Add `src/workshop/games/<slug>.py` where `<slug>` is `snake`, `pong`, or `tetris`.
3. Export a `GameScreen` subclass of `workshop.game.GameScreen`.
4. Draw with `self.grid` (`set_cell`, `fill_rect`, `blit_text`, `draw_border`). Call nothing else to paint.
5. Keep `python -m workshop` / F5 launching the menu. `Q` on a game must return to the menu.
6. Add pytest tests for **pure logic** (movement, collision, line clear). Do not try to test the Textual UI.
7. Do not add dependencies unless the human agrees. Use **textual**, **rich**, and the standard library. Do not use `curses`, `keyboard`, `pygame`, or emoji.

## Project conventions

- Python 3.12, environment is `.venv` at the repo root, managed with `uv`.
- Install/run: `uv sync`, `uv run workshop`, `uv run pytest`.
- Full-screen **character-cell** graphics: one glyph per cell, Unicode blocks (`█`) and box drawing, named or hex Rich colours.
- Default playfield is `COLS = 48`, `ROWS = 20` on `GameScreen`. Increase those so the game fills the terminal; keep a Tetris well at 10×20 inside a larger grid.
- Real-time games use `TICK_HZ` on `GameScreen` (about 10–15). Do not chase 60 fps.
- Leave `bootstrap.ps1`, `.vscode/`, `AGENTS.md`, and `.agents/skills/` alone unless the human asks.

## Code review

When the human asks for a review, follow `.agents/skills/code-review/SKILL.md`. Do not apply review findings until they ask.
