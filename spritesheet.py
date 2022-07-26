import pygame


class Spritesheet:
    def __init__(self, character):
        # Single image size: 48*48
        self.number_of_frames = 4
        self.path = f'media/{character}/'
        self.animations = {'idle': [],
                           'run': [],
                           'jump': [],
                           'fall': []}

        for animation in self.animations.keys():
            print(f'{self.path}{animation}.png')
            img = pygame.image.load(f'{self.path}{animation}.png')
            imgs = []
            for x in range(0, self.number_of_frames):
                rect = pygame.rect.Rect(x * 48, 0, 48, 48)
                imgs.append(img.subsurface(rect))
            self.animations[animation] = imgs

        self.frame_idx = 0
        self.animation_speed = 1 / self.number_of_frames

    def animate(self, state, dt):
        animation = self.animations[state]
        self.frame_idx += self.animation_speed * dt
        if self.frame_idx >= len(animation):
            self.frame_idx = 0
        return animation[int(self.frame_idx)]
