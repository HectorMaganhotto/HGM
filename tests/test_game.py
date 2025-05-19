import os
import pickle

import pygame

from purrfect_leap import platform
from purrfect_leap.ui import SAVE_FILE, UI


def test_generate_platforms():
    pygame.init()
    pygame.display.set_mode((1, 1))
    platforms = platform.generate_platforms(800)
    assert len(platforms) > 0
    assert all(isinstance(p, platform.Platform) for p in platforms)
    pygame.quit()


def test_score_persistence(tmp_path):
    os.chdir(tmp_path)
    pygame.init()
    pygame.display.set_mode((1, 1))
    ui = UI()
    ui.save_best_score(42)
    assert os.path.exists(SAVE_FILE)
    assert ui.load_best_score() == 42
    pygame.quit()
