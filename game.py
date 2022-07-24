import random
import time
import pygame

from spritesheet import Spritesheet
import screen_effects as sfx


class Game:
    def __init__(self, display: pygame.Surface, window: pygame.Surface) -> None:
        self.display = display
        self.window = window
        self.W, self.H = self.window.get_width(), self.window.get_height()
        self.welcomePage = True
        self.intro = True
        self.transitionToMenu = False
        self.menu = False
        self.playing = False

        # Screen shaking
        self.screen_shake = False
        self.xShake = 0
        self.yShake = 0
        self.shake_strength = 0
        self.shakeTimer = 30

        # Colours
        self.white = (200, 200, 200)
        self.black = pygame.Color('grey12')
        self.black_transparent = (0, 0, 0, 30)

        # Fonts
        self.font = pygame.font.Font('media/fonts/Retro Gaming.ttf', 15)
        self.titleFont = pygame.font.Font('media/fonts/Retro Gaming.ttf', 45)
        self.cursor = '_'

        # Welcoming Page
        self.timer = 0
        self.welcomeText = 'Press Space to Start'

    def welcome_page(self, dt: float) -> None:
        self.timer += dt
        self.timer %= 60
        self.window.fill(self.black)
        if self.intro:
            sfx.hacky_text(self, self.welcomeText, self.titleFont, self.white, (self.W / 2, self.H / 2))
            self.intro = False
        else:
            sfx.blit_text(self, self.welcomeText, self.titleFont, self.white, (self.W / 2, self.H / 2))
            if self.timer < 30:
                sfx.blit_text(self, self.cursor, self.titleFont, self.white,
                              ((self.W + self.titleFont.size(self.welcomeText + self.cursor)[0]) / 2, self.H / 2))
        if self.transitionToMenu and not self.screen_shake:
            self.welcomePage, self.transitionToMenu = False, False
            self.menu = True

    def update(self, dt: float) -> None:
        self.window.fill(self.black)

    def menu_page(self, dt: float, player) -> None:
        self.window.fill(self.black)
        sfx.blit_text(self, 'Menu', self.font, self.white, (self.W / 2, self.H / 2 - self.titleFont.get_height()))
        sfx.blit_text(self, 'Press Escape to Quit', self.font, self.white,
                      (self.W / 2, self.H / 2 + self.titleFont.get_height()))
        player.blit_player(self.window)
