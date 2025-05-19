"""Simple particle effects."""

from __future__ import annotations

import random
from dataclasses import dataclass

import pygame


@dataclass
class Particle:
    """A simple particle represented by a colored circle."""

    pos: pygame.Vector2
    vel: pygame.Vector2
    radius: int
    color: tuple[int, int, int]
    lifetime: int

    def update(self) -> None:
        self.pos += self.vel
        self.lifetime -= 1

    def draw(self, surface: pygame.Surface) -> None:
        if self.lifetime > 0:
            pygame.draw.circle(surface, self.color, (int(self.pos.x), int(self.pos.y)), self.radius)


class ParticleSystem:
    """Maintains a list of particles."""

    def __init__(self) -> None:
        self.particles: list[Particle] = []

    def spawn_dust(self, x: int, y: int) -> None:
        for _ in range(5):
            vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(-2, 0))
            self.particles.append(Particle(pygame.Vector2(x, y), vel, 3, (200, 200, 200), 30))

    def spawn_flame(self, x: int, y: int) -> None:
        for _ in range(5):
            vel = pygame.Vector2(random.uniform(-1, 1), random.uniform(1, 3))
            self.particles.append(Particle(pygame.Vector2(x, y), vel, 4, (255, 100, 0), 30))

    def update(self) -> None:
        for p in list(self.particles):
            p.update()
            if p.lifetime <= 0:
                self.particles.remove(p)

    def draw(self, surface: pygame.Surface) -> None:
        for p in self.particles:
            p.draw(surface)
