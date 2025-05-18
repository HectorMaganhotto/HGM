"""Platform generation and logic."""

from __future__ import annotations

import random
import math
from dataclasses import dataclass

import pygame

PLATFORM_WIDTH = 72
PLATFORM_HEIGHT = 18
VERTICAL_GAP = 100
MOVING_AMPLITUDE = 50


@dataclass
class Platform:
    """Represents a platform in the game world."""

    image: pygame.Surface
    rect: pygame.Rect
    kind: str = "normal"
    broken: bool = False
    phase: float = 0.0
    start_x: int = 0

    def update(self) -> None:
        if self.kind == "moving":
            self.phase += 0.05
            self.rect.x = self.start_x + int(MOVING_AMPLITUDE * math.sin(self.phase))
        if self.kind == "breakable" and self.broken:
            self.rect.y += 5

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


def load_platform_images() -> dict[str, pygame.Surface]:
    return {
        "normal": pygame.image.load("assets/sprites/platform_normal.png").convert_alpha(),
        "breakable": pygame.image.load("assets/sprites/platform_break.png").convert_alpha(),
        "boost": pygame.image.load("assets/sprites/spring.png").convert_alpha(),
    }


IMAGES = None


def get_images() -> dict[str, pygame.Surface]:
    global IMAGES
    if IMAGES is None:
        IMAGES = load_platform_images()
    return IMAGES


def spawn_platform(y: int) -> Platform:
    images = get_images()
    kind = random.choices(
        ["normal", "moving", "breakable", "boost"],
        weights=[70, 15, 10, 5],
        k=1,
    )[0]
    x = random.randint(0, 480 - PLATFORM_WIDTH)
    rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)
    image = images["normal"] if kind != "breakable" and kind != "boost" else images.get(kind, images["normal"])
    return Platform(image=image, rect=rect, kind=kind, start_x=x)


def generate_platforms(screen_height: int) -> list[Platform]:
    platforms = []
    y = screen_height - 40
    while y > -screen_height:
        platforms.append(spawn_platform(y))
        y -= random.randint(60, 120)
    return platforms
