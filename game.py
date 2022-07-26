import random
import sys
import time
import pygame

from spritesheet import Spritesheet
from tiles import Map
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
        self.keys: dict = {}

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

        # Menu Page
        self.map = Map(self.window)
        self.menu_map, self.menu_rects = self.map.create_map('menu')

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
        self.map.draw_map(self.window, self.menu_map)
        sfx.blit_text(self, 'Menu', self.font, self.white, (self.W / 2, self.H / 2 - self.titleFont.get_height()))
        sfx.blit_text(self, 'Press Escape to Quit', self.font, self.white,
                      (self.W / 2, self.H / 2 + self.titleFont.get_height()))
        player.move(self.menu_rects, dt, self.keys)
        player.blit_player(self.window)

    def events(self, dt, player):
        for event in pygame.event.get():
            # Quit game
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()

            # Welcome Page
            if self.welcomePage:
                if event.type == pygame.KEYDOWN:
                    if not self.transitionToMenu:
                        if event.key == pygame.K_SPACE:
                            sfx.initiate_shake(self, 30, self.W / 150)
                            self.transitionToMenu = True

            # Menu page
            if self.menu:
                if event.type == pygame.KEYDOWN:
                    self.keys[event.key] = True
                elif event.type == pygame.KEYUP:
                    self.keys[event.key] = False
