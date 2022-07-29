import sys

import pygame

import screen_effects as sfx
from tiles import Map
from spritesheet import Spritesheet


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
        self.menu_map = self.map.create_map('menu')
        self.spritesheet = Spritesheet('Biker', int(self.map.tile_size))
        self.menu_spawn = pygame.Vector2(self.map.map_size[0] / 2,
                                         self.map.map_size[1] / 2) * self.map.tile_size
        self.map.scroll = self.menu_spawn

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

    def update(self) -> None:
        self.window.fill(self.black)

    def menu_page(self, dt: float, player) -> None:
        self.window.fill(self.black)
        player.move(self.map.get_neighbour_tiles, dt, self.keys)
        self.map.scroll_camera(player.position, player.rect)
        self.map.draw_map(self.window, player.rect)
        player.blit_player(self.map.scroll, self.spritesheet, dt)

    def events(self):
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
