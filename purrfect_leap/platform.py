"""Platform generation and logic."""

from __future__ import annotations

import math
import random
from dataclasses import dataclass
from pathlib import Path

import pygame

ASSET_DIR = Path(__file__).resolve().parent / "assets"
PLATFORM_WIDTH = 72
PLATFORM_HEIGHT = 18
VERTICAL_GAP = 100
AMPLITUDE = 50


@dataclass
class Platform:
    """Represents a platform in the game world."""

    image: pygame.Surface
    rect: pygame.Rect
    kind: str = "normal"
    broken: bool = False
    phase: float = 0.0
    start_x: int = 0

    def __post_init__(self) -> None:
        self.start_x = self.rect.x

    def update(self) -> None:
        if self.kind == "moving":
            self.phase += 0.05
            self.rect.x = self.start_x + int(AMPLITUDE * math.sin(self.phase))
        if self.kind == "breakable" and self.broken:
            self.rect.y += 5

    def draw(self, surface: pygame.Surface) -> None:
        surface.blit(self.image, self.rect)


def load_platform_images() -> dict[str, pygame.Surface]:
    return {
        "normal": pygame.image.load(ASSET_DIR / "sprites" / "platform_normal.png").convert_alpha(),
        "breakable": pygame.image.load(ASSET_DIR / "sprites" / "platform_break.png").convert_alpha(),
        "boost": pygame.image.load(ASSET_DIR / "sprites" / "spring.png").convert_alpha(),
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
    if kind == "boost":
        image = images["boost"]
    elif kind == "breakable":
        image = images["breakable"]
    else:
        image = images["normal"]
    return Platform(image=image, rect=rect, kind=kind)


def generate_platforms(screen_height: int) -> list[Platform]:
    """Generate an initial list of platforms including a base platform."""
    images = get_images()
    base_img = pygame.transform.scale(images["normal"], (480, PLATFORM_HEIGHT))
    base_rect = pygame.Rect(0, screen_height - PLATFORM_HEIGHT, 480, PLATFORM_HEIGHT)
    platforms = [Platform(image=base_img, rect=base_rect, kind="normal")]
    y = base_rect.top - random.randint(60, 120)
    while y > -screen_height:
        platforms.append(spawn_platform(y))
        y -= random.randint(60, 120)
    return platforms

