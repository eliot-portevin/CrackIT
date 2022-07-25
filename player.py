import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface):
        super().__init__()
        self.window = window
        self.image = pygame.image.load('media/1 Biker/Biker_idle.png').convert()
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.speed = pygame.Vector2(0, 0)
        self.moving_left = False
        self.moving_right = False
        self.jumping = False

    def blit_player(self, window):
        self.window.blit(self.image, self.position)

    def move(self, dt: float):
        if self.moving_left:
            self.speed.x = -5
        if self.moving_right:
            self.speed.x = 5
        if self.jumping:
            self.speed.y = 10
        self.position += self.speed * dt