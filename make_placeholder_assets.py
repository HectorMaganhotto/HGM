"""Generate placeholder sprites and sounds for Purr-fect Leap."""

from __future__ import annotations

import math
import os
import wave
import struct

import pygame

SPRITE_PATH = "purrfect_leap/assets/sprites"
SOUND_PATH = "purrfect_leap/assets/sounds"


def ensure_dirs() -> None:
    os.makedirs(SPRITE_PATH, exist_ok=True)
    os.makedirs(SOUND_PATH, exist_ok=True)


def make_sprites() -> None:
    pygame.init()
    size = (40, 40)
    for i in range(4):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 200, 200), (5, 5, 30, 30))
        pygame.draw.circle(surf, (0, 0, 0), (20, 35), 5)
        pygame.image.save(surf, f"{SPRITE_PATH}/cat_walk_{i}.png")
    for i in range(2):
        surf = pygame.Surface(size, pygame.SRCALPHA)
        pygame.draw.rect(surf, (255, 150, 150), (5, 5, 30, 30))
        pygame.draw.rect(surf, (255, 100, 0), (15, 35, 10, 10))
        pygame.image.save(surf, f"{SPRITE_PATH}/cat_rocket_{i}.png")
    plat = pygame.Surface((72, 18), pygame.SRCALPHA)
    plat.fill((255, 175, 200))
    pygame.draw.rect(plat, (255, 150, 180), plat.get_rect(), 3)
    pygame.image.save(plat, f"{SPRITE_PATH}/platform_normal.png")
    breakp = pygame.Surface((72, 18), pygame.SRCALPHA)
    breakp.fill((255, 175, 200))
    pygame.draw.line(breakp, (0, 0, 0), (0, 9), (72, 9), 2)
    pygame.image.save(breakp, f"{SPRITE_PATH}/platform_break.png")
    spring = pygame.Surface((72, 18), pygame.SRCALPHA)
    pygame.draw.rect(spring, (0, 255, 0), (0, 10, 72, 8))
    pygame.image.save(spring, f"{SPRITE_PATH}/spring.png")
    rocket = pygame.Surface((20, 40), pygame.SRCALPHA)
    pygame.draw.polygon(rocket, (200, 0, 0), [(10, 0), (20, 30), (0, 30)])
    pygame.image.save(rocket, f"{SPRITE_PATH}/rocket.png")
    bubble = pygame.Surface((30, 30), pygame.SRCALPHA)
    pygame.draw.circle(bubble, (150, 150, 255, 128), (15, 15), 15)
    pygame.image.save(bubble, f"{SPRITE_PATH}/bubble.png")
    coin = pygame.Surface((20, 20), pygame.SRCALPHA)
    pygame.draw.circle(coin, (255, 255, 0), (10, 10), 10)
    pygame.image.save(coin, f"{SPRITE_PATH}/coin.png")
    enemy = pygame.Surface((40, 30), pygame.SRCALPHA)
    pygame.draw.circle(enemy, (100, 50, 0), (20, 15), 15)
    pygame.image.save(enemy, f"{SPRITE_PATH}/enemy_hairball.png")
    pygame.quit()


def write_wav(filename: str, freq: float) -> None:
    sample_rate = 44100
    duration = 0.2
    n_samples = int(sample_rate * duration)
    data = bytearray()
    for n in range(n_samples):
        value = int(32767.0 * math.sin(2 * math.pi * freq * n / sample_rate))
        data.extend(struct.pack('<h', value))
    with wave.open(filename, 'wb') as f:
        f.setnchannels(1)
        f.setsampwidth(2)
        f.setframerate(sample_rate)
        f.writeframes(data)


def make_sounds() -> None:
    write_wav(f"{SOUND_PATH}/jump.wav", 880)
    write_wav(f"{SOUND_PATH}/powerup.wav", 660)
    write_wav(f"{SOUND_PATH}/gameover.wav", 220)


if __name__ == "__main__":
    ensure_dirs()
    make_sprites()
    make_sounds()
    print("Assets generated.")
