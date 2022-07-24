from random import randint
import time
import pygame


def blit_text(game, string: str, font, colour, position: tuple[float, float]):
    text = font.render(string, True, colour)
    xCoord = position[0] - text.get_width() / 2
    yCoord = position[1] - text.get_height() / 2
    game.window.blit(text, (xCoord, yCoord))


def hacky_text(game, string: str, font, colour, position: tuple[float, float]):
    text = font.render(string, True, colour)
    xCoord = position[0] - text.get_width() / 2
    yCoord = position[1] - text.get_height() / 2
    for c in string:
        character = font.render(c, True, colour)
        game.window.blit(character, (xCoord, yCoord))
        game.display.blit(game.window, (game.xShake, game.yShake))
        xCoord += character.get_width()
        time.sleep(1 / len(string))
        pygame.display.update()
    game.intro = False


def initiate_shake(game, frames, strength):
    game.screen_shake = True
    game.shakeTimer = frames
    game.shake_strength = int(strength)


def shake(game):
    if game.shakeTimer > 0:
        game.shakeTimer -= 1
        game.xShake = randint(-game.shake_strength, game.shake_strength)
        game.yShake = randint(-game.shake_strength, game.shake_strength)
    else:
        game.xShake, game.yShake = 0, 0
        game.screen_shake = False


def fps_change(dt: float) -> float:
    return dt
