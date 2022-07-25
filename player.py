import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface):
        super().__init__()
        self.window = window
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.image = pygame.image.load('media/1 Biker/Biker_idle.png').convert()
        self.rect = self.image.get_rect()
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.speed = pygame.Vector2(0, 0)
        self.moving_left = False
        self.moving_right = False
        self.jumping = False

    def blit_player(self, window):
        self.window.blit(self.image, self.position)

    def move(self, dt: float, keys):
        if keys.get(pygame.K_a):
            self.position.x -= self.w/300
        if keys.get(pygame.K_d):
            self.position.x += self.w/300

        # self.speed.y += 0.2 Gravity
        self.position += self.speed * dt
