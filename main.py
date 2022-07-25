import sys
import time
import pygame

from game import Game
from player import Player
import screen_effects as sfx
from tiles import Map

pygame.init()
display = pygame.display.set_mode((0, 0), pygame.SRCALPHA, pygame.FULLSCREEN)
window = display.copy()
clock = pygame.time.Clock()


def display_fps(game, dt):
    fps_text = game.font.render(str(round(60 / dt)), False, game.white)
    display.blit(fps_text, (0, 0))
    pygame.display.update(fps_text.get_rect())


def exit_game():
    pygame.display.quit()
    pygame.quit()
    sys.exit()


def main():
    playing = True
    fps = 60
    game = Game(display, window)
    player = Player(window)
    before = time.time()
    while playing:
        clock.tick(120)
        dt = (time.time() - before) * fps
        before = time.time()
        dt = round(dt, 4)
        # Avoid skipping too many frames
        if dt > 5:
            dt = 5.0

        if game.screen_shake:
            sfx.shake(game)
        if game.welcomePage:
            game.welcome_page(dt)
        elif game.menu:
            game.menu_page(dt, player)

        game.events(dt, player)
        display.blit(window, (game.xShake, game.yShake))
        display_fps(game, dt)
        pygame.display.update()
    exit_game()


if __name__ == '__main__':
    main()
