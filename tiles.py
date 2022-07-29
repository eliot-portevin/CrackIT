import pygame


class Map:
    def __init__(self, window: pygame.Surface):
        # Colour palette
        # "cad2c5"
        # "84a98c"
        # "52796f"
        # "354f52"
        # "2f3e46"
        self.level_string = None
        self.w, self.h = window.get_size()
        self.map = None
        self.map_size = [0, 0]
        self.tiles, self.temporary_list = [], []
        self.image = pygame.image.load('media/assets/tiles.png').convert()
        self.image = pygame.transform.scale(self.image, (int(self.w/4), int(self.w/4)))
        self.tile_size = self.image.get_width() / 6
        self.blocks = []  # Tile images stored as separate surfaces
        self.tile_rects = []  # Tile rectangles, updated each frame
        self.scroll = pygame.Vector2(self.w/2, self.h/2)
        self.camera = None

        # Converting sprite-sheet into blocks
        for tile_y in range(0, 6):
            for tile_x in range(0, 6):
                rect = (tile_x * self.tile_size, tile_y * self.tile_size,
                        self.tile_size, self.tile_size)
                self.blocks.append(self.image.subsurface(rect))

    def create_map(self, level):
        filename = f'media/Levels/{level}.csv'
        # Reading map file
        with open(filename) as f:
            self.level_string = f.read().split('\n')
            self.map_size[0] = len(self.level_string[0].split(','))
        for line in self.level_string:
            self.map_size[1] += 1
            if len(line) != 0:
                for value in line.split(','):
                    self.temporary_list.append(int(value))
            self.tiles.append(self.temporary_list)
            self.temporary_list = []
        # Creating map
        self.map = pygame.surface.Surface((self.map_size[0] * self.tile_size, self.map_size[1] * self.tile_size))
        y = 0
        for row in self.tiles:
            tmp = []
            x = 0
            for tile in row:
                if tile != -1:
                    x_position = x * self.tile_size
                    y_position = y * self.tile_size
                    rect = pygame.rect.Rect(x_position, y_position, self.tile_size, self.tile_size)
                    self.map.blit(self.blocks[tile], (x_position, y_position))
                    tmp.append(rect)
                else:
                    tmp.append(None)
                x += 1
            self.tile_rects.append(tmp)
            y += 1
        map_w, map_h = self.map.get_size()
        self.camera = pygame.rect.Rect(0, 0, map_w - self.w, map_h - self.h)
        self.camera.center = self.map.get_rect().center

    def scroll_camera(self, player_pos: pygame.Vector2, player_rect: pygame.rect.Rect):
        if self.camera.left < player_rect.x < self.camera.right:
            self.scroll.x += (player_pos.x - self.scroll.x - self.w / 2)/40
        if self.camera.top < player_rect.y < self.camera.bottom:
            self.scroll.y += (player_pos.y - self.scroll.y - self.h/2)/40

    def draw_map(self, window: pygame.Surface, player_rect: pygame.rect.Rect):
        window.blit(self.map, (-self.scroll.x - player_rect.w/2, -self.scroll.y - player_rect.h))

    def get_neighbour_tiles(self, pos: pygame.Vector2, ramps: bool):
        neighbours = []
        tile_types = []
        ramp_nrs = [0, 1]
        for x_nr in range(0, 8):
            for y_nr in range(0, 8):
                y_idx, x_idx = self.get_tile_index(pos + pygame.Vector2((x_nr-3) * self.tile_size, (y_nr-3) * self.tile_size))
                if self.tiles[x_idx][y_idx] != -1:
                    if ramps: # Find neighbour ramps for collision check
                        if self.tiles[x_idx][y_idx] in ramp_nrs:
                            neighbours.append(self.tile_rects[x_idx][y_idx])
                            tile_types.append(self.tiles[x_idx][y_idx])
                    elif self.tiles[x_idx][y_idx] not in ramp_nrs:
                        neighbours.append(self.tile_rects[x_idx][y_idx])
                        tile_types.append(self.tiles[x_idx][y_idx])
        return neighbours, tile_types

    def get_tile_index(self, pos: pygame.Vector2):
        x = int(pos.x / self.tile_size)
        y = int(pos.y / self.tile_size)
        return x, y
