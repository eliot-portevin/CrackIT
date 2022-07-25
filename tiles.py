import pygame, csv


class Map(pygame.sprite.Sprite):
    def __init__(self, window: pygame.Surface, level):
        self.map = window.copy()
        self.tile_size = 64
        self.filename = f'media/Levels/{level}.csv'
        # Colour palette
        # "cad2c5"
        # "84a98c"
        # "52796f"
        # "354f52"
        # "2f3e46"

        # Converting spritesheet into blocks
        self.image = pygame.image.load('media/assets/tiles.png').convert()
        self.blocks = []
        for tile_x in range(0, 6):
            for tile_y in range(0, 6):
                rect = (tile_x * self.tile_size, tile_y * self.tile_size, 6, 6)
                self.blocks.append(self.image.subsurface(rect))

        # Reading map file
        with open(self.filename) as f:
            self.level_string = f.readlines()

        print(self.level_string)
        self.tiles = []
        for value in self.level_string:
            self.tiles.append(int(value))

        self.tile_numbers = {-1, 0, 1, 2, 3, 4, 5, 6, 7}

        y = 0
        for row in self.tiles:
            x = 0
            for tile in row:
                x += 1
                if tile != -1:
                    self.map.blit(self.blocks[tile], x * self.tile_size, y * self.tile_size)
            y += 1
