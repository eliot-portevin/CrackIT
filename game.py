import random
import sys
import time
import pygame

from spritesheet import Spritesheet
from tilesheet import Tilesheet
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

        # Map
        self.tiles = Tilesheet('media/assets/tiles.png', w=64, h=64, rows=6, cols=6)
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
        self.tiles.draw(self.window)
        player.blit_player(self.window)

    def events(self, player):
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
                player.position += self.movement_input()

    def movement_input(self):
        movement = pygame.Vector2(0, 0)
        if self.keys.get(pygame.K_a):
            movement.x -= 4
        if self.keys.get(pygame.K_d):
            movement.x += 4
        return movement
