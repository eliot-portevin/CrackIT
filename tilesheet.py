import pygame

class Tilesheet:
    def __init__(self, filename, w, h, rows, cols):
        # Colour palette
        # "cad2c5"
        # "84a98c"
        # "52796f"
        # "354f52"
        # "2f3e46"
        self.image = pygame.image.load(filename).convert()
        self.menu_level = open('media/Levels/menu.txt', 'r').readlines()
        self.tile_table = []
        self.tile_names = {'up', 'down', 'ladder', 'rock1', 'rock2', 'rock3', 'grass', 'block'}
        for tile_x in range(0, cols):
            line = []
            self.tile_table.append(line)
            for tile_y in range(0, rows):
                rect = (tile_x * w, tile_y * h, w, h)
                line.append(self.image.subsurface(rect))

    def draw(self, window):
        for x, row in enumerate(self.tile_table):
            for y, tile in enumerate(row):
                window.blit(tile, (x*72, y*72))
            print(self.menu_level)