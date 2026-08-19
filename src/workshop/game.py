"""Base screen for Snake, Pong, and Tetris."""

from __future__ import annotations

from textual.app import ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle, Vertical
from textual.events import Key
from textual.screen import Screen
from textual.widgets import Static

from workshop.grid import CellGrid
from workshop.playfield import Playfield


class GameScreen(Screen):
    """Subclass this in ``workshop.games.<slug>`` as ``GameScreen``.

    Set ``COLS``, ``ROWS``, ``TICK_HZ``, and ``TITLE``. Implement ``on_tick``
    and ``on_game_key``. Draw into ``self.grid``; the playfield refreshes after
    each tick and key press.
    """

    BINDINGS = [
        Binding("q", "quit_game", "Quit", show=True),
        Binding("escape", "quit_game", "Quit", show=False),
    ]

    COLS = 48
    ROWS = 20
    TICK_HZ = 12
    TITLE = "GAME"

    CSS = """
    GameScreen {
        background: #050805;
        align: center middle;
    }

    #game-frame {
        width: auto;
        height: auto;
        align: center middle;
    }

    #game-title, #game-hint {
        width: 100%;
        content-align: center middle;
        color: #33ff33;
        text-style: bold;
    }

    #game-hint {
        text-style: none;
        color: #7cff7c;
    }
    """

    def __init__(self) -> None:
        super().__init__()
        self.grid = CellGrid(self.COLS, self.ROWS)

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                with Vertical(id="game-frame"):
                    yield Static(self.TITLE, id="game-title")
                    yield Playfield(self.grid, id="playfield")
                    yield Static("Q  back to menu", id="game-hint")

    def on_mount(self) -> None:
        interval = 1.0 / max(self.TICK_HZ, 1)
        self.set_interval(interval, self._tick)
        self.on_start()
        self._draw()

    def _tick(self) -> None:
        self.on_tick()
        self._draw()

    def _draw(self) -> None:
        self.query_one("#playfield", Playfield).refresh_grid()

    def on_key(self, event: Key) -> None:
        if event.key in {"q", "escape"}:
            return
        self.on_game_key(event.key)
        self._draw()

    def action_quit_game(self) -> None:
        self.app.pop_screen()

    def on_start(self) -> None:
        """Optional setup after the screen is mounted."""

    def on_tick(self) -> None:
        """Advance game state. Draw into ``self.grid``."""

    def on_game_key(self, key: str) -> None:
        """Handle a key press. ``key`` is a Textual key name such as ``left``."""
