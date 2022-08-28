import pygame

class Moving_Sprite(pygame.sprite.Sprite):
    def __init__(self, pos: pygame.Vector2, image: pygame.Surface, resize: int, tiles: list, tile_size: int,
                 groups_colliding: list[pygame.sprite.Group], groups_including: list[pygame.sprite.Group]):
        super().__init__()
        for sprite_group in groups_colliding:
            self.add(sprite_group)
        self.sprite_elements = groups_colliding
        self.tiles = tiles
        self.tile_size = tile_size
        self.pos = pos
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = pos.x, pos.y
        self.speed = pygame.Vector2(0, 0)

    def collide_with_mask(self, mask: pygame.mask.Mask, pos: pygame.Vector2):
        return self.mask.overlap(mask, (pos.x - self.rect.x, pos.y - self.rect.y))

