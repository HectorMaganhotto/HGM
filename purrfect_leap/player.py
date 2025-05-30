"""Player module containing the Cat class."""

from __future__ import annotations

from pathlib import Path

import pygame

GRAVITY = 0.45
JUMP_VELOCITY = -12
BOOST_VELOCITY = -20

CAT_SIZE = 40
COLLISION_SIZE = 32
MOVE_SPEED = 5
ASSET_DIR = Path(__file__).resolve().parent / "assets"


class Cat:
    """Represents the cat controlled by the player."""

    def __init__(self, x: int, y: int) -> None:
        self.images = [
            pygame.image.load(ASSET_DIR / "sprites" / f"cat_walk_{i}.png").convert_alpha()
            for i in range(4)
        ]
        self.rocket_images = [
            pygame.image.load(ASSET_DIR / "sprites" / f"cat_rocket_{i}.png").convert_alpha()
            for i in range(2)
        ]
        self.frame = 0
        self.rect = pygame.Rect(0, 0, COLLISION_SIZE, COLLISION_SIZE)
        self.rect.center = (x, y)
        self.vel_y = 0.0
        self.rocket_time = 0
        self.started = False

    def jump(self) -> None:
        if self.vel_y > 0:
            return
        self.vel_y = JUMP_VELOCITY
        pygame.mixer.Sound(ASSET_DIR / "sounds" / "jump.wav").play()

    def apply_rocket(self) -> None:
        self.rocket_time = 180  # 3 seconds at 60fps
        self.vel_y = BOOST_VELOCITY

    def update(self, keys: pygame.key.ScancodeWrapper, started: bool) -> None:
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            self.rect.x -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            self.rect.x += MOVE_SPEED

        if started:
            if self.rocket_time > 0:
                self.rocket_time -= 1
                self.vel_y += GRAVITY * 0.1
            else:
                self.vel_y += GRAVITY
            self.rect.y += int(self.vel_y)
        else:
            self.vel_y = 0

        if self.rect.left < -CAT_SIZE:
            self.rect.right = 480 + CAT_SIZE
        elif self.rect.right > 480 + CAT_SIZE:
            self.rect.left = -CAT_SIZE
        self.frame = (self.frame + 1) % 60

    def draw(self, surface: pygame.Surface) -> None:
        if self.rocket_time > 0:
            img = self.rocket_images[(self.frame // 30) % 2]
        else:
            img = self.images[(self.frame // 15) % 4]
        draw_rect = img.get_rect(center=self.rect.center)
        surface.blit(img, draw_rect)

