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
        self.map = window.copy()
        self.tile_size = 16
        self.tiles, self.temporary_list = [], []
        self.image = pygame.image.load('media/assets/tiles.png').convert()
        self.image = pygame.transform.scale(self.image, (96, 96))
        self.blocks = []  # Tile images stored as separate surfaces
        self.tile_rects = []  # Tile rectangles, updated each frame
        self.scroll = pygame.Vector2(0, 0)
        self.camera = pygame.rect.Rect(0, 0, window.get_width()/2, window.get_height()/2)
        self.camera.center = window.get_rect().center

        # Converting sprite-sheet into blocks
        for tile_x in range(0, 6):
            for tile_y in range(0, 6):
                rect = (tile_x * self.tile_size, tile_y * self.tile_size,
                        self.tile_size, self.tile_size)
                self.blocks.append(self.image.subsurface(rect))

    def create_map(self, level):
        filename = f'media/Levels/{level}.csv'
        # Reading map file
        with open(filename) as f:
            self.level_string = f.read().split('\n')
        for line in self.level_string:
            for value in line.split(','):
                self.temporary_list.append(int(value))
            self.tiles.append(self.temporary_list)
            self.temporary_list = []
        # Creating map
        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                x += 1
                if tile != -1:
                    x_position = (x - 1) * self.tile_size
                    y_position = (y - 1) * self.tile_size
                    rect = pygame.rect.Rect(x_position, y_position, self.tile_size, self.tile_size)
                    self.map.blit(self.blocks[tile], (x_position, y_position))
                    self.tile_rects.append(rect)
            y += 1

    def scroll_camera(self, player_rect: pygame.rect.Rect, player_speed: pygame.Vector2):
        if not player_rect.colliderect(self.camera):
            self.scroll -= player_speed

    def draw_map(self, window: pygame.Surface, player_rect, player_speed):
        self.scroll_camera(player_rect, player_speed)
        window.blit(self.map, (self.scroll.x, self.scroll.y))
