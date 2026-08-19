"""Cell-grid helpers for full-screen terminal games."""

from __future__ import annotations

from rich.style import Style
from rich.text import Text

StyleLike = str | Style | None

_HEAVY = {
    "tl": "┏",
    "tr": "┓",
    "bl": "┗",
    "br": "┛",
    "h": "━",
    "v": "┃",
}


class CellGrid:
    """A 2D character-cell buffer. One terminal cell per (x, y).

    Games should draw with ``set_cell``, ``fill_rect``, ``blit_text``, and
    ``draw_border``. Out-of-bounds writes are ignored so a sprite can clip
    at the edge without crashing.
    """

    def __init__(self, cols: int, rows: int) -> None:
        if cols < 3 or rows < 3:
            raise ValueError("grid must be at least 3x3")
        self.cols = cols
        self.rows = rows
        self._chars = [[" " for _ in range(cols)] for _ in range(rows)]
        self._styles: list[list[StyleLike]] = [[None for _ in range(cols)] for _ in range(rows)]

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.cols and 0 <= y < self.rows

    def clear(self, char: str = " ", style: StyleLike = None) -> None:
        cell = _as_cell(char)
        for y in range(self.rows):
            for x in range(self.cols):
                self._chars[y][x] = cell
                self._styles[y][x] = style

    def set_cell(self, x: int, y: int, char: str, style: StyleLike = None) -> None:
        if not self.in_bounds(x, y):
            return
        self._chars[y][x] = _as_cell(char)
        self._styles[y][x] = style

    def get_char(self, x: int, y: int) -> str:
        if not self.in_bounds(x, y):
            return ""
        return self._chars[y][x]

    def fill_rect(
        self,
        x: int,
        y: int,
        width: int,
        height: int,
        char: str,
        style: StyleLike = None,
    ) -> None:
        for row in range(y, y + height):
            for col in range(x, x + width):
                self.set_cell(col, row, char, style)

    def blit_text(self, x: int, y: int, text: str, style: StyleLike = None) -> None:
        for offset, glyph in enumerate(text):
            self.set_cell(x + offset, y, glyph, style)

    def draw_border(self, style: StyleLike = "bold #33ff33", inset: int = 0) -> None:
        x0, y0 = inset, inset
        x1, y1 = self.cols - 1 - inset, self.rows - 1 - inset
        if x1 - x0 < 2 or y1 - y0 < 2:
            return
        box = _HEAVY
        self.set_cell(x0, y0, box["tl"], style)
        self.set_cell(x1, y0, box["tr"], style)
        self.set_cell(x0, y1, box["bl"], style)
        self.set_cell(x1, y1, box["br"], style)
        for x in range(x0 + 1, x1):
            self.set_cell(x, y0, box["h"], style)
            self.set_cell(x, y1, box["h"], style)
        for y in range(y0 + 1, y1):
            self.set_cell(x0, y, box["v"], style)
            self.set_cell(x1, y, box["v"], style)

    def as_rich_text(self) -> Text:
        result = Text()
        last_row = self.rows - 1
        for y, row in enumerate(self._chars):
            line = Text()
            for x, char in enumerate(row):
                line.append(char, style=self._styles[y][x] or "")
            result.append_text(line)
            if y < last_row:
                result.append("\n")
        return result


def _as_cell(char: str) -> str:
    if not char:
        return " "
    return char[0]
