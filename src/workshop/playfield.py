"""Textual widget that paints a CellGrid as a full playfield."""

from __future__ import annotations

from rich.text import Text
from textual.widget import Widget

from workshop.grid import CellGrid


class Playfield(Widget):
    """Renders a ``CellGrid`` one terminal cell per grid cell."""

    DEFAULT_CSS = """
    Playfield {
        width: auto;
        height: auto;
        background: #031403;
        color: #33ff33;
    }
    """

    def __init__(self, grid: CellGrid, **kwargs: object) -> None:
        super().__init__(**kwargs)
        self.grid = grid

    def on_mount(self) -> None:
        self.styles.width = self.grid.cols
        self.styles.height = self.grid.rows

    def render(self) -> Text:
        return self.grid.as_rich_text()

    def refresh_grid(self) -> None:
        self.refresh()
