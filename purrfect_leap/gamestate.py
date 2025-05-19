"""Game state management for Purr-fect Leap."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

import pygame

from .player import MOVE_SPEED


class GameState:
    """Base class for game states."""

    def __init__(self, game: "Game") -> None:
        self.game = game

    def handle_event(self, event: pygame.event.Event) -> None:
        pass

    def update(self) -> None:
        pass

    def draw(self, surface: pygame.Surface) -> None:
        pass


class StartMenuState(GameState):
    """Start menu state."""

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.game.change_state(PlayingState(self.game))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_state(PlayingState(self.game))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((50, 50, 100))
        title = self.game.ui.font.render("Purr-fect Leap", True, (255, 255, 255))
        prompt = self.game.ui.font.render("Press SPACE or Click", True, (255, 255, 0))
        rect = title.get_rect(center=(self.game.width // 2, self.game.height // 2 - 40))
        surface.blit(title, rect)
        rect = prompt.get_rect(center=(self.game.width // 2, self.game.height // 2 + 10))
        surface.blit(prompt, rect)


class PausedState(GameState):
    """Paused state."""

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self.game.change_state(self.game.previous_state)

    def draw(self, surface: pygame.Surface) -> None:
        self.game.previous_state.draw(surface)
        overlay = pygame.Surface((self.game.width, self.game.height), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        surface.blit(overlay, (0, 0))
        text = self.game.ui.font.render("Paused", True, (255, 255, 255))
        rect = text.get_rect(center=(self.game.width // 2, self.game.height // 2))
        surface.blit(text, rect)


class GameOverState(GameState):
    """Game over state."""

    def __init__(self, game: "Game", score: int) -> None:
        super().__init__(game)
        self.score = score
        if score > self.game.best_score:
            self.game.best_score = score
            self.game.ui.save_best_score(score)
        self.game.ui.play_sound("gameover")

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN and event.key in (pygame.K_SPACE, pygame.K_RETURN):
            self.game.change_state(PlayingState(self.game))
        elif event.type == pygame.MOUSEBUTTONDOWN:
            self.game.change_state(PlayingState(self.game))

    def draw(self, surface: pygame.Surface) -> None:
        surface.fill((30, 0, 0))
        over = self.game.ui.font.render("Game Over", True, (255, 0, 0))
        score_text = self.game.ui.font.render(f"Score: {self.score}", True, (255, 255, 255))
        best_text = self.game.ui.font.render(f"Best: {self.game.best_score}", True, (0, 255, 0))
        rect = over.get_rect(center=(self.game.width // 2, self.game.height // 2 - 40))
        surface.blit(over, rect)
        rect = score_text.get_rect(center=(self.game.width // 2, self.game.height // 2))
        surface.blit(score_text, rect)
        rect = best_text.get_rect(center=(self.game.width // 2, self.game.height // 2 + 40))
        surface.blit(best_text, rect)


class PlayingState(GameState):
    """Active gameplay state."""

    def __init__(self, game: "Game") -> None:
        super().__init__(game)
        self.game.reset()
        self.first_jump = False

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                self.game.previous_state = self
                self.game.change_state(PausedState(self.game))
            elif event.key == pygame.K_SPACE and not self.first_jump:
                self.game.player.jump()
                self.first_jump = True

    def update(self) -> None:
        keys = pygame.key.get_pressed()
        dx = 0
        if keys[pygame.K_LEFT] or keys[pygame.K_a]:
            dx -= MOVE_SPEED
        if keys[pygame.K_RIGHT] or keys[pygame.K_d]:
            dx += MOVE_SPEED
        if dx:
            self.game.player.move(dx)
        self.game.update_world()

    def draw(self, surface: pygame.Surface) -> None:
        self.game.draw_world(surface)


@dataclass
class Game:
    """Main game container."""

    width: int = 480
    height: int = 800
    state: GameState | None = None
    previous_state: Optional[GameState] = None

    def __post_init__(self) -> None:
        pygame.init()
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Purr-fect Leap")
        self.clock = pygame.time.Clock()
        self.ui = __import__("purrfect_leap.ui", fromlist=["UI"]).UI()
        self.best_score = self.ui.load_best_score()
        self.player = None
        self.platforms = []
        self.powerups = []
        self.scroll_y = 0
        self.score = 0

    def change_state(self, state: GameState) -> None:
        self.state = state

    # Game world logic
    def reset(self) -> None:
        module = __import__("purrfect_leap.player", fromlist=["Cat"])
        self.player = module.Cat(self.width // 2, self.height - 100)
        platform_module = __import__("purrfect_leap.platform", fromlist=["Platform", "generate_platforms"])
        self.platforms = platform_module.generate_platforms(self.height)
        powerups_module = __import__("purrfect_leap.powerups", fromlist=["PowerUpManager"])
        self.powerups = powerups_module.PowerUpManager()
        self.scroll_y = 0
        self.score = 0

    def update_world(self) -> None:
        self.player.update()
        for platform in list(self.platforms):
            platform.update()
        self._handle_platform_collisions()
        self.powerups.update(self.player, self.platforms, self)
        self._scroll_world()
        self.ui.update_score(self.score)

    def draw_world(self, surface: pygame.Surface) -> None:
        surface.fill((135, 206, 235))
        for platform in self.platforms:
            platform.draw(surface)
        self.powerups.draw(surface)
        self.player.draw(surface)
        self.ui.draw(surface, self.score, self.best_score)

    def _scroll_world(self) -> None:
        if self.player.rect.top <= self.height // 2:
            dy = self.height // 2 - self.player.rect.top
            self.player.rect.top = self.height // 2
            self.scroll_y += dy
            self.score += dy
            for platform in self.platforms:
                platform.rect.y += dy
            self.powerups.scroll(dy)
            self._spawn_platforms()

        # Remove off-screen platforms
        self.platforms = [p for p in self.platforms if p.rect.top < self.height]

        if self.player.rect.top > self.height:
            self.change_state(GameOverState(self, self.score))

    def _spawn_platforms(self) -> None:
        platform_module = __import__("purrfect_leap.platform", fromlist=["spawn_platform"])
        while len(self.platforms) < 10:
            y = min(p.rect.y for p in self.platforms) - platform_module.VERTICAL_GAP
            self.platforms.append(platform_module.spawn_platform(y))

    def _handle_platform_collisions(self) -> None:
        """Apply jumping when landing on platforms."""
        cat = self.player
        if cat.vel_y >= 0:
            for plat in self.platforms:
                if (
                    cat.rect.bottom <= plat.rect.top + 5
                    and cat.rect.bottom + cat.vel_y >= plat.rect.top
                    and cat.rect.colliderect(plat.rect)
                ):
                    cat.jump()
                    if plat.kind == "boost":
                        cat.vel_y = JUMP_VELOCITY - 6
                    if plat.kind == "breakable":
                        plat.broken = True
                    break

    def run(self) -> None:
        self.change_state(StartMenuState(self))
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                else:
                    if self.state:
                        self.state.handle_event(event)
            if self.state:
                self.state.update()
                self.state.draw(self.screen)
            pygame.display.flip()
            self.clock.tick(60)
        pygame.quit()


if __name__ == "__main__":
    Game().run()
