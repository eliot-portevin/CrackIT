import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface):
        super().__init__()
        self.window = window
        self.image = pygame.image.load('media/1 Biker/Biker_idle.png').convert()
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(self.rect.x, self.rect.y)

    def blit_player(self, window):
        self.window.blit(self.image, self.position)