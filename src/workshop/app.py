"""Full-screen arcade menu. Games light up after an agent creates them."""

from __future__ import annotations

import sys
from pathlib import Path

from textual.app import App, ComposeResult
from textual.binding import Binding
from textual.containers import Center, Middle, Vertical
from textual.events import Key
from textual.widgets import Static

from workshop.games import GAMES, load_game_screen

CABINET_CSS = """
Screen {
    background: #050805;
}

#cabinet {
    width: 62;
    height: auto;
    border: heavy #33ff33;
    background: #031403;
    padding: 1 2;
}

#banner, #status, #hint, #menu {
    width: 100%;
    color: #33ff33;
}

#banner {
    text-style: bold;
    content-align: center middle;
    color: #7cff7c;
}

#menu {
    height: auto;
    margin: 1 0;
}

#status {
    color: #9cff9c;
}

#hint {
    color: #6adf6a;
    content-align: center middle;
}
"""

BANNER = """
┏━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓
┃           A R C A D E   2 D                  ┃
┃        full-screen terminal games            ┃
┗━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┛
""".strip()


class ArcadeApp(App):
    TITLE = "Arcade 2D"
    CSS = CABINET_CSS
    BINDINGS = [
        Binding("q", "quit", "Quit", show=True),
        Binding("up", "cursor_up", "Up", show=False),
        Binding("down", "cursor_down", "Down", show=False),
        Binding("enter", "select", "Play", show=True),
    ]

    def __init__(self) -> None:
        super().__init__()
        self.cursor = 0

    def compose(self) -> ComposeResult:
        with Middle():
            with Center():
                with Vertical(id="cabinet"):
                    yield Static(BANNER, id="banner")
                    yield Static(self._menu_text(), id="menu")
                    yield Static(self._status_text(), id="status")
                    yield Static(
                        "↑↓  select    Enter  play    1–3  jump    Q  quit",
                        id="hint",
                    )

    def _menu_text(self) -> str:
        lines: list[str] = []
        for index, spec in enumerate(GAMES):
            built = load_game_screen(spec.slug) is not None
            pointer = "▶" if index == self.cursor else " "
            marker = "READY" if built else "NOT BUILT"
            lines.append(f" {pointer}  {spec.key}  {spec.title:<8}  {marker:<9}  {spec.tagline}")
        return "\n".join(lines)

    def _status_text(self) -> str:
        python = sys.version.split()[0]
        venv = Path(sys.prefix)
        in_venv = sys.prefix != sys.base_prefix
        venv_state = "yes" if in_venv else "no"
        return (
            f" Python {python}    .venv {venv_state}    {venv}\n"
            " Paste a game prompt from README.md into Copilot Chat (Agent mode) to build a title."
        )

    def _refresh_menu(self) -> None:
        self.query_one("#menu", Static).update(self._menu_text())

    def on_key(self, event: Key) -> None:
        if event.character in {spec.key for spec in GAMES}:
            self.cursor = _index_for_key(event.character)
            self._refresh_menu()
            self.action_select()
            event.stop()

    def action_cursor_up(self) -> None:
        self.cursor = (self.cursor - 1) % len(GAMES)
        self._refresh_menu()

    def action_cursor_down(self) -> None:
        self.cursor = (self.cursor + 1) % len(GAMES)
        self._refresh_menu()

    def action_select(self) -> None:
        spec = GAMES[self.cursor]
        screen_cls = load_game_screen(spec.slug)
        if screen_cls is None:
            self.notify(
                f"{spec.title} is not built yet. Copy the {spec.title} prompt "
                "from README.md into Copilot Chat (Agent mode), then run the app again.",
                title="Insert coin",
                severity="warning",
                timeout=8,
            )
            return
        self.push_screen(screen_cls())


def _index_for_key(key: str) -> int:
    for index, spec in enumerate(GAMES):
        if spec.key == key:
            return index
    return 0


def main() -> None:
    ArcadeApp().run()
