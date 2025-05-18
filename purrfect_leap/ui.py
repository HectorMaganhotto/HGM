"""UI elements like score display and sounds."""

from __future__ import annotations

import os
import pickle

import pygame

SAVE_FILE = "save.dat"


class UI:
    """Handles UI rendering and score persistence."""

    def __init__(self) -> None:
        self.font = pygame.font.Font(None, 36)
        self.sounds = {
            "jump": pygame.mixer.Sound("assets/sounds/jump.wav"),
            "powerup": pygame.mixer.Sound("assets/sounds/powerup.wav"),
            "gameover": pygame.mixer.Sound("assets/sounds/gameover.wav"),
        }
        self.score = 0

    def update_score(self, score: int) -> None:
        self.score = score

    def draw(self, surface: pygame.Surface, score: int, best: int) -> None:
        text = self.font.render(f"Score: {score}", True, (0, 0, 0))
        surface.blit(text, (10, 10))
        best_text = self.font.render(f"Best: {best}", True, (0, 0, 0))
        surface.blit(best_text, (10, 40))

    def save_best_score(self, score: int) -> None:
        with open(SAVE_FILE, "wb") as f:
            pickle.dump(score, f)

    def load_best_score(self) -> int:
        if not os.path.exists(SAVE_FILE):
            return 0
        with open(SAVE_FILE, "rb") as f:
            return pickle.load(f)

    def play_sound(self, name: str) -> None:
        self.sounds[name].play()
