"""Game catalogue. A title is playable once ``workshop.games.<slug>`` exists."""

from __future__ import annotations

from dataclasses import dataclass
from importlib import import_module
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from workshop.game import GameScreen


@dataclass(frozen=True)
class GameSpec:
    slug: str
    title: str
    key: str
    tagline: str


GAMES: tuple[GameSpec, ...] = (
    GameSpec("snake", "SNAKE", "1", "Eat. Grow. Don't crash."),
    GameSpec("pong", "PONG", "2", "Two paddles. One ball."),
    GameSpec("tetris", "TETRIS", "3", "Stack. Clear. Repeat."),
)


def load_game_screen(slug: str) -> type[GameScreen] | None:
    """Return the game's ``GameScreen`` class, or None if it is not built yet."""
    try:
        module = import_module(f"workshop.games.{slug}")
    except ModuleNotFoundError:
        return None
    screen = getattr(module, "GameScreen", None)
    if screen is None:
        return None
    return screen
