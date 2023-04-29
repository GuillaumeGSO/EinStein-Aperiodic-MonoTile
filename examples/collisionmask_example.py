import pygame


class SpriteObject(pygame.sprite.Sprite):
    def __init__(self, x, y, w, h, color):
        pygame.sprite.Sprite.__init__(self)
        self.angle = 0
        self.original_image = pygame.Surface([w, h], pygame.SRCALPHA)
        self.original_image.fill(color)
        self.image = self.original_image
        self.rect = self.image.get_rect(center=(x, y))
        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rotate()

    def rotate(self):
        self.angle += 0.3
        self.image = pygame.transform.rotate(self.original_image, self.angle)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.mask = pygame.mask.from_surface(self.image)


pygame.init()
clock = pygame.time.Clock()
window = pygame.display.set_mode((400, 400))
size = window.get_size()

moving_object = SpriteObject(0, 0, 50, 50, (128, 0, 255))
static_objects = [
    SpriteObject(size[0] // 2, size[1] // 3, 100, 50, (128, 128, 128)),
    SpriteObject(size[0] // 4, size[1] * 2 // 3, 100, 50, (128, 128, 128)),
    SpriteObject(size[0] * 3 // 4, size[1] * 2 // 3, 100, 50, (128, 128, 128))
]
all_sprites = pygame.sprite.Group([moving_object] + static_objects)
static_sprites = pygame.sprite.Group(static_objects)

run = True
while run:
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    moving_object.rect.center = pygame.mouse.get_pos()
    all_sprites.update()
    collide = pygame.sprite.spritecollide(
        moving_object, static_sprites, True, pygame.sprite.collide_mask)

    window.fill((255, 0, 0) if collide else (255, 255, 255))
    all_sprites.draw(window)
    pygame.display.update()

pygame.quit()
exit()
