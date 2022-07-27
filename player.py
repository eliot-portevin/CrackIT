import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface):
        super().__init__()
        self.window = window
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.image = pygame.image.load('media/Biker/idle.png').convert()
        self.player_w, self.player_h = 48, 48
        self.rect = pygame.rect.Rect(self.w/2, self.h*2/3, self.player_w, self.player_h)
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.speed = pygame.Vector2(0, 0)
        self.jumping = None
        self.state = 'idle'  # Possible states: idle, run, jump, climb

    def blit_player(self, scroll: pygame.Vector2, spritesheet, dt):
        self.image = spritesheet.animate(self.state, dt)
        self.window.blit(self.image, (self.rect.x + scroll.x, self.rect.y + scroll.y))

    def check_collisions(self, tiles):
        hit_list = []
        for tile in tiles:
            if self.rect.colliderect(tile):
                hit_list.append(tile)
        return hit_list

    def move(self, tile_rects, dt, keys):
        # Key input
        if keys.get(pygame.K_a):
            self.speed.x = -self.w / 300 * dt
            self.state = 'run_left'
        elif keys.get(pygame.K_d):
            self.speed.x = self.w / 300 * dt
            self.state = 'run_right'
        else:
            self.speed.x = 0
            self.state = 'idle'
        if keys.get(pygame.K_w) and not self.jumping:
            self.jumping = True
            self.state = 'jump'
            self.speed.y = - self.h / (200 * dt)
        if self.speed.y < self.h / 100:
            self.speed.y += 0.7 * dt  # Gravity

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
            self.speed.x = 0
        self.rect.y += self.speed.y
        hit_list = self.check_collisions(tile_rects)
        for tile in hit_list:
            if self.speed.y < 0:
                self.rect.top = tile.bottom
                collision_types['top'] = True
            elif self.speed.y > 0:
                self.rect.bottom = tile.top
                collision_types['bottom'] = True
                self.jumping = False
                self.speed.y = 0

        self.rect.x = round(self.rect.x)
        self.rect.y = round(self.rect.y)

        self.position.x = self.rect.x
        self.position.y = self.rect.y