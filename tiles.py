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
        self.tiles, self.temporary_list = [], []
        self.image = pygame.image.load('media/assets/tiles.png').convert()
        self.image = pygame.transform.scale(self.image, (120, 120))
        self.tile_size = self.image.get_width() / 6
        self.blocks = []  # Tile images stored as separate surfaces
        self.tile_rects = []  # Tile rectangles, updated each frame
        self.scroll = pygame.Vector2(self.w/2, self.h/2)

        # Converting sprite-sheet into blocks
        for tile_x in range(0, 6):
            for tile_y in range(0, 6):
                rect = (tile_x * self.tile_size, tile_y * self.tile_size,
                        self.tile_size, self.tile_size)
                self.blocks.append(self.image.subsurface(rect))

    def create_map(self, level):
        filename = f'media/Levels/{level}.csv'
        line_nr = 0
        col_nr = 0
        # Reading map file
        with open(filename) as f:
            self.level_string = f.read().split('\n')
            col_nr = len(self.level_string[0].split(','))
        for line in self.level_string:
            line_nr += 1
            if len(line) != 0:
                for value in line.split(','):
                    self.temporary_list.append(int(value))
            self.tiles.append(self.temporary_list)
            self.temporary_list = []
        # Creating map
        self.map = pygame.surface.Surface((col_nr * self.tile_size, line_nr * self.tile_size))
        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                x += 1
                if tile != -1:
                    x_position = (x - 1) * self.tile_size - int(self.scroll.x)
                    y_position = (y - 1) * self.tile_size - int(self.scroll.y)
                    rect = pygame.rect.Rect(x_position, y_position, self.tile_size, self.tile_size)
                    self.map.blit(self.blocks[tile], (x_position, y_position))
                    self.tile_rects.append(rect)
            y += 1

    def scroll_camera(self, player_pos: pygame.Vector2, window: pygame.surface.Surface):
        self.scroll.x += (player_pos.x - self.scroll.x - self.w/2)/20
        self.scroll.y += (player_pos.y - self.scroll.y - self.h/2)/20

    def draw_map(self, window: pygame.Surface):
        window.blit(self.map, (self.scroll.x, self.scroll.y))
        print(self.scroll.x, self.scroll.y)
