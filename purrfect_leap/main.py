"""Entry point for Purr-fect Leap."""

from __future__ import annotations

from .gamestate import Game


def main() -> None:
    """Start the game."""
    game = Game()
    game.run()


if __name__ == "__main__":
    main()
