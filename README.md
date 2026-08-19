# Arcade 2D — agentic coding workshop

A small **Windows** Python starter you can clone, bootstrap, and run in VS Code. The app is a **full-screen arcade menu**. Snake, Pong, and Tetris are **not** included on purpose: you will ask an AI agent to build one of them, play it, improve it, and review it.

You stay in control. Read the diffs, run the game yourself, and reject changes you do not want.

## What you will do

1. Clone this repo and run the bootstrap script (Python, `uv`, `.venv`).
2. Open the folder in VS Code, install the recommended extensions, press **F5**.
3. Confirm the arcade menu fills the terminal (`NOT BUILT` next to each game).
4. Pick **one** game. Paste its prompt into GitHub Copilot Chat in **Agent** mode.
5. Play the game. Note bugs and ideas.
6. Ask the agent to fix and extend it.
7. Invoke the included **code-review** skill.

Plan on about 60–90 minutes.

## Prerequisites

- Windows 10 or 11
- [Git](https://git-scm.com/)
- [VS Code](https://code.visualstudio.com/)
- [GitHub Copilot](https://code.visualstudio.com/docs/copilot/setup) in VS Code (**Chat**, with **Agent** mode)
- VS Code’s integrated terminal (colour and Unicode)

You do **not** need a global Python install. `bootstrap.ps1` installs `uv` if it is missing, fetches Python **3.12** into a user cache (once per machine), and creates `.venv` in this repo.

## 1. Clone and bootstrap

```powershell
git clone https://github.com/chaylescar/ai-agent-cpd.git ai-agent-cpd
cd ai-agent-cpd
powershell -ExecutionPolicy Bypass -File .\bootstrap.ps1
```

Bootstrap will:

- install `uv` if it is missing (user-local, no admin)
- install CPython 3.12 if it is not already cached (`uv python install` — **not** committed in git)
- create `.venv` in the repo and install `textual`, `rich`, `pytest`, and `ruff`

If Python 3.12 is already on the machine from a previous `uv` run, that step is effectively instant.

## 2. Open in VS Code and run

1. File → Open Folder → this repo.
2. Install the **recommended extensions** (Python, Debugger, Pylance, Ruff, Copilot, Copilot Chat):
   - If VS Code shows **This workspace has extension recommendations**, click **Install**.
   - If that banner is gone: **View → Extensions**, then in the search box type `@recommended` and install each one listed under **Workspace Recommendations**.
   - Or Command Palette (`Ctrl+Shift+P`) → **Extensions: Show Recommended Extensions**.
3. Sign in to GitHub Copilot when asked.
4. Open a Python file once so VS Code picks `.venv` (status bar interpreter).
5. Run and Debug: choose **Arcade cabinet** and press **F5**.

The game **must** run in the **integrated terminal**, not the Debug Console. Full-screen input and colour do not work in the Debug Console. Drag the terminal panel taller so the arcade cabinet is not squashed.

You should see SNAKE / PONG / TETRIS marked `NOT BUILT`. Quit with `Q`.

Without the debugger:

```powershell
uv run workshop
```

## 3. How to work with the agent

- Open **GitHub Copilot Chat** and set the mode to **Agent**.
- Paste **one** prompt from below. Let it edit files. **Approve** commands you understand.
- When it finishes, press **F5** again and play.
- If something is wrong, say so in the same thread (“the snake ignores the bottom wall”) rather than starting over.

The agent should add `src/workshop/games/snake.py` (or `pong.py` / `tetris.py`) exporting `GameScreen`. The menu lights up `READY` after a reload.

## 4. Pick one game

Cannot decide? Build **Snake**.

After it works, do **not** start a second game unless you have time. Use the improve step instead.

### Shared rules (already in each prompt)

Use the existing `workshop` package, `GameScreen`, and `self.grid`. Keep F5 working. No new packages, no emoji, no `curses` / `pygame` / `keyboard`.

---

### Prompt: Snake

Copy everything in the block below.

```text
Build SNAKE as a full-screen terminal game in this workshop repo.

Add src/workshop/games/snake.py that exports GameScreen(workshop.game.GameScreen).
The arcade menu loads that class when the file exists.

Use self.grid (CellGrid) to draw: set_cell, fill_rect, blit_text, draw_border.
Use Unicode block characters (█) and box drawing, plus Rich colours. No emoji.
Keep python -m workshop / F5 launching the menu. Q or Escape must pop back to the menu.

Game rules:
- Full-window playfield with a border, score, and length on a status row inside the grid.
- Snake moves on a timer (TICK_HZ around 10–12). Arrow keys or WASD change direction.
- Ignore a 180-degree reverse (do not let the snake step into itself in one keystroke).
- Food appears on a random empty cell. Eating grows the snake by one and scores.
- Collision with walls or the snake’s own body is game over. Show the score and a restart hint.
- Press R to restart after game over. The snake must not move while dead until R.
- Do not wrap around the edges.

Add pytest tests for pure logic (direction, growth, wall/self collision, food not spawning on the snake). Do not try to test the Textual UI.

Do not modify bootstrap.ps1, .vscode, AGENTS.md, or .agents/skills unless required for F5.
```

---

### Prompt: Pong

Copy everything in the block below.

```text
Build PONG as a full-screen terminal game in this workshop repo.

Add src/workshop/games/pong.py that exports GameScreen(workshop.game.GameScreen).
The arcade menu loads that class when the file exists.

Use self.grid (CellGrid) to draw: set_cell, fill_rect, blit_text, draw_border.
Use Unicode block characters (█) and box drawing, plus Rich colours. No emoji.
Keep python -m workshop / F5 launching the menu. Q or Escape must pop back to the menu.

Game rules:
- Full-window court with top/bottom walls, a dotted centre line, two paddles, and one ball.
- Left paddle: W and S. Right paddle: up and down arrows.
- Ball moves on a timer (TICK_HZ around 12–15). Bounce off top/bottom walls and paddles.
- Reverse X velocity on paddle hits. Add a little Y deflection from where the paddle is struck.
- If the ball passes a paddle, the other player scores. Serve again from centre.
- First to 5 wins. Freeze on win, show the winner, R restarts a match.
- Paddles must not leave the court.

Add pytest tests for pure logic (bounce, score, paddle clamping, win at 5). Do not try to test the Textual UI.

Do not modify bootstrap.ps1, .vscode, AGENTS.md, or .agents/skills unless required for F5.
```

---

### Prompt: Tetris

Copy everything in the block below.

```text
Build TETRIS as a full-screen terminal game in this workshop repo.

Add src/workshop/games/tetris.py that exports GameScreen(workshop.game.GameScreen).
The arcade menu loads that class when the file exists.

Use self.grid (CellGrid) to draw: set_cell, fill_rect, blit_text, draw_border.
Use Unicode block characters (█) and box drawing, plus Rich colours. No emoji.
Keep python -m workshop / F5 launching the menu. Q or Escape must pop back to the menu.

Keep the rules small so this fits a workshop:
- Well size 10 x 20 (or 10 x 16 if you need space for a status column).
- Seven tetrominoes. Store four precomputed orientations each. No wall-kicks, no SRS, no hold, no T-spins.
- Left/right arrows move, up or X rotates, down soft-drops. Optional space = hard drop.
- Gravity on a timer (TICK_HZ around 8–10).
- Clear full rows, add score, show score and lines on a status column beside the well.
- Game over when a new piece cannot spawn. R restarts.
- Draw the well with a border; colour each piece type.

Add pytest tests for pure logic (rotate inside the well, line clear, lock, game over). Do not try to test the Textual UI.

Do not modify bootstrap.ps1, .vscode, AGENTS.md, or .agents/skills unless required for F5.
```

## 5. Playtest, then improve

Play for a few minutes. Write down what broke and what you wish it did.

Example follow-ups (paste one at a time):

- Snake: pause on `P`; increasing speed; wrap-around mode as an option.
- Pong: a one-player mode with an AI paddle; serve delay; louder “miss” feedback on the court.
- Tetris: next-piece preview; ghost piece; speed-up every N lines.

Ask for a **small** change, run the game, then ask for the next one.

## 6. Code review skill

In Copilot Chat (Agent mode):

```text
Use the code-review skill in .agents/skills/code-review to review the game we just built. Do not change code unless I ask.
```

Read the findings. Pick one Critical or Suggestion item and ask Copilot to fix **that** item only.

## Stretch (only if you finish early)

Mini Space Invaders is optional. Same stack: `GameScreen`, `self.grid`, no extra packages.

Keep it tiny: 4×6 aliens, one player bullet, one alien bullet, no bunkers, no mystery ship. Add `src/workshop/games/` only if you also wire a fourth menu entry — otherwise replace nothing; put it behind a key on the menu only if you have time. Prefer extra polish on Snake/Pong/Tetris instead.

## Troubleshooting

| Problem | What to try |
| --- | --- |
| `uv` not found after bootstrap | Close the terminal, open a new one, re-run `bootstrap.ps1`. `uv` is on your user PATH (`%USERPROFILE%\.local\bin`). |
| VS Code says no interpreter | Command Palette → Python: Select Interpreter → `.venv\Scripts\python.exe`. Reload the window if it was opened before bootstrap. |
| Recommended extensions not offered | View → Extensions, search `@recommended`, install **Workspace Recommendations**. |
| Blank or garbled “game” in the Debug Console | Use the **Arcade cabinet** launch config (`console`: integrated terminal) and press F5 again. |
| Keys do nothing | Click the terminal panel so it has focus. |
| Execution policy blocks `bootstrap.ps1` | Use `powershell -ExecutionPolicy Bypass -File .\bootstrap.ps1` as in step 1. |
| Copilot has no Agent mode | Install the **GitHub Copilot** and **GitHub Copilot Chat** extensions, sign in, and pick **Agent** in the Chat mode dropdown. |

## Why these Python packages

Declared in `pyproject.toml` so the agent does not need to invent a stack:

| Package | Role |
| --- | --- |
| **textual** | Full-screen app, screens, keyboard, tick timer |
| **rich** | Colours and cell rendering (used by the playfield) |
| **pytest** | Tests for game logic |
| **ruff** | Format/lint in VS Code |

Do not add `curses`, `windows-curses`, `keyboard`, or `pygame`. They fight Windows and the VS Code terminal.

Python itself is **not** stored in git. `uv` pins 3.12 via `.python-version` and caches the interpreter per user. `.venv` in this repo is the project environment.

## Facilitator notes

- This workshop is **Windows-only** for now (PowerShell bootstrap, `.venv\Scripts\python.exe`).
- Do not implement the games in the starter. The `NOT BUILT` menu is the hook.
- Confirm GitHub Copilot access **before** the day. Bootstrap cannot install that.
- Default suggestion: Snake. Tetris is the longest of the three; keep the prompt caps (no SRS/hold).
- If a lab network blocks `astral.sh`, pre-install `uv` and run `uv python install 3.12` plus `uv sync` on a golden machine image.

## Layout

```text
bootstrap.ps1                  Windows environment setup
src/workshop/app.py            arcade menu
src/workshop/game.py           GameScreen base (tick + keys + grid)
src/workshop/grid.py           character-cell buffer
src/workshop/games/            empty until the agent adds snake/pong/tetris
.agents/skills/code-review/    review skill for the last step
AGENTS.md                      instructions for the coding agent
```
