"""Power-up items and manager."""

from __future__ import annotations

import random
from dataclasses import dataclass
from pathlib import Path

import pygame


@dataclass
class PowerUp:
    """Base class for a power-up."""

    image: pygame.Surface
    rect: pygame.Rect
    kind: str

    def apply(self, cat: "Cat") -> None:
        pass


class PowerUpManager:
    """Manages power-ups in the world."""

    ASSET_DIR = Path(__file__).resolve().parent / "assets"

    def __init__(self) -> None:
        self.images = {
            "rocket": pygame.image.load(self.ASSET_DIR / "sprites" / "rocket.png").convert_alpha(),
            "bubble": pygame.image.load(self.ASSET_DIR / "sprites" / "bubble.png").convert_alpha(),
            "coin": pygame.image.load(self.ASSET_DIR / "sprites" / "coin.png").convert_alpha(),
        }
        self.powerups: list[PowerUp] = []
        self.scroll_y = 0

    def update(self, cat: "Cat", platforms: list["Platform"], game: "Game") -> None:
        for p in list(self.powerups):
            if p.rect.colliderect(cat.rect):
                if p.kind == "rocket":
                    cat.apply_rocket()
                elif p.kind == "coin":
                    game.score += 100
                self.powerups.remove(p)
        if random.random() < 0.01:
            y = min(platform.rect.top for platform in platforms) - random.randint(60, 120)
            x = random.randint(0, 480 - 32)
            kind = random.choice(["rocket", "bubble", "coin"])
            rect = self.images[kind].get_rect(topleft=(x, y))
            self.powerups.append(PowerUp(self.images[kind], rect, kind))

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.powerups:
            surface.blit(p.image, p.rect)

    def scroll(self, dy: int) -> None:
        for p in self.powerups:
            p.rect.y += dy

