import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface):
        super().__init__()
        self.window = window
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.image = pygame.image.load('media/1 Biker/Biker_idle.png').convert()
        self.player_w, self.player_h = self.image.get_size()
        self.position = pygame.Vector2(0, 0)
        self.rect = pygame.rect.Rect(self.position.x, self.position.y, self.player_w, self.player_h)
        self.speed = pygame.Vector2(0, 0)
        self.moving_left = False
        self.moving_right = False
        self.jumping = False

    def blit_player(self, window):
        self.window.blit(self.image, self.position)

    def check_collisions(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tile_rects, dt, keys):
        # Key input
        if keys.get(pygame.K_a):
            self.speed.x = -self.w / 200 * dt
        elif keys.get(pygame.K_d):
            self.speed.x = self.w / 200 * dt
        else:
            self.speed.x = 0
        if keys.get(pygame.K_w) and not self.jumping:
            self.jumping = True
            self.speed.y = -self.h/200
        if self.speed.y < self.h / 70:
            self.speed.y += 0.2  # Gravity

        # Collision checks
        collision_types = {'top': False,
                           'bottom': False,
                           'right': False,
                           'left': False}
        self.rect.x += self.speed.x
        hit_list = self.check_collisions(tile_rects)
        for tile in hit_list:
            if self.speed.x > 0:
                self.rect.right = tile.left
                collision_types['right'] = True
            elif self.speed.x < 0:
                self.rect.left = tile.right
                collision_types['left'] = True
        self.rect.y += self.speed.y
        hit_list = self.check_collisions(tile_rects)
        for tile in hit_list:
            if self.speed.y > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
                self.jumping = False
            elif self.speed.y < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True

        self.position.x = self.rect.left
        self.position.y = self.rect.top
