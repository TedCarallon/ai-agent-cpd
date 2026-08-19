---
name: code-review
description: >-
  Reviews the workshop arcade games (Snake, Pong, Tetris) and supporting Python
  for correctness, terminal UX, tests, and maintainability. Use when the user
  asks for a code review, review of the game, PR-style feedback, or to run the
  code-review skill.
disable-model-invocation: true
---

# Workshop code review

Review the **current** game code in this repo. Do not rewrite the games unless the human asks you to apply the findings.

## Scope

- Read `src/workshop/games/` plus any logic modules those files import.
- Skim `src/workshop/game.py`, `grid.py`, and `app.py` only to see whether the game uses them correctly.
- Run `uv run pytest` if tests exist; include the result in the review.
- Ignore `bootstrap.ps1`, `.vscode`, and this skill unless they are clearly broken.

## Checklist

- [ ] The module exports `GameScreen` and the arcade menu can launch it
- [ ] `Q` / Escape return to the menu; the process does not hang
- [ ] The playfield fills a large part of the terminal (not a tiny 3x3 in a corner)
- [ ] Drawing uses `self.grid` (blocks / box drawing / colour). No emoji, no `print` spam
- [ ] Win, lose, restart, and score (or line count) behave correctly
- [ ] Out-of-bounds and collision cases do not crash
- [ ] Tick rate is reasonable (about 8–15 Hz)
- [ ] Tests cover pure logic; they do not need to drive Textual
- [ ] No extra dependencies, no `curses` / `keyboard` / `pygame`

## Output format

Lead with a 3–6 sentence summary (what was built, whether it runs, biggest risk).

Then list findings as:

- Critical: must fix before you would demo it
- Suggestion: worth doing in the workshop improve step
- Nice to have: optional polish

Each finding: file (and function if obvious), what is wrong, and a concrete fix. End with **three** follow-up prompts the human could paste next.

Do not apply code changes unless the human says to implement the review.
