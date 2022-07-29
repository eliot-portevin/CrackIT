import pygame


class Player(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface, spawn: pygame.Vector2, tile_size):
        super().__init__()
        self.window = window
        self.w, self.h = self.window.get_width(), self.window.get_height()
        self.image = None
        self.player_w, self.player_h = 2 * tile_size, 2 * tile_size
        self.rect = pygame.rect.Rect(spawn.x, spawn.y, self.player_w, self.player_h)
        self.position = pygame.Vector2(self.rect.x, self.rect.y)
        self.speed = pygame.Vector2(0, 0)
        self.jumping = None
        self.state = 'idle'  # Possible states: idle, run, jump, climb

    def blit_player(self, scroll: pygame.Vector2, spritesheet, dt):
        self.image = spritesheet.animate(self.state, dt)
        self.window.blit(self.image, (self.rect.x - scroll.x - self.rect.w / 2, self.rect.y - scroll.y - self.rect.h))

    def check_collisions(self, neighbour_tiles, tile_types):
        hit_list = []
        for idx, tile in enumerate(neighbour_tiles):
            if self.rect.colliderect(tile):
                hit_list.append([tile, tile_types[idx]])
        return hit_list

    def move(self, get_neighbour_tiles: classmethod, dt, keys):
        # Key input
        if keys.get(pygame.K_a):
            self.speed.x = -2
            #self.speed.x = -self.w / 300 * dt
            self.state = 'run_left'
        elif keys.get(pygame.K_d):
            self.speed.x = 2
            #self.speed.x = self.w / 300 * dt
            self.state = 'run_right'
        else:
            self.speed.x = 0
            self.state = 'idle'
        if keys.get(pygame.K_w) and not self.jumping:
            self.jumping = True
            self.state = 'jump'
            self.speed.y = - self.h / 70 * dt
        if self.speed.y < self.h / 100:
            self.speed.y += 0.7 * dt  # Gravity

        # Collision checks
        neighbour_tiles, tile_types = get_neighbour_tiles(self.position, ramps=False)
        collision_types = {'top': False,
                           'bottom': False,
                           'right': False,
                           'left': False}

        self.rect.x += self.speed.x
        hit_list = self.check_collisions(neighbour_tiles, tile_types)
        for tile in hit_list:
            if self.speed.x > 0:
                self.rect.right = tile[0].left
                collision_types['right'] = True
            elif self.speed.x < 0:
                self.rect.left = tile[0].right
                collision_types['left'] = True
            self.speed.x = 0

        self.rect.y += self.speed.y
        hit_list = self.check_collisions(neighbour_tiles, tile_types)
        for tile in hit_list:
            if self.speed.y < 0:
                self.rect.top = tile[0].bottom
                collision_types['top'] = True
            elif self.speed.y > 0:
                self.rect.bottom = tile[0].top
                collision_types['bottom'] = True
                self.speed.y = 0

        neighbour_ramps, tile_types = get_neighbour_tiles(self.position, ramps=True)
        ramps = self.check_collisions(neighbour_ramps, tile_types)
        for ramp in ramps:
            if self.rect.colliderect(ramp[0]):
                rel_x = self.rect.x - ramp[0].x
                pos_height = 0
                if ramp[1] == 0:
                    pos_height = rel_x + self.rect.width  # go by player right edge on right ramps
                if ramp[1] == 1:
                    pos_height = ramp[0].w - rel_x  # is already left edge by default

                # add constraints
                pos_height = min(pos_height, ramp[0].w)
                pos_height = max(pos_height, 0)
                target_y = ramp[0].y + ramp[0].w - pos_height

                self.rect.bottom = target_y
                self.speed.y = self.speed.x
                collision_types['bottom'] = True

        if collision_types['bottom']:
            self.jumping = False
            self.speed.y = 0

        self.rect.x = round(self.rect.x)
        self.rect.y = round(self.rect.y)

        self.position.x = self.rect.x
        self.position.y = self.rect.y
