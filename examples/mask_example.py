import pygame as pg

# Transparent surfaces with a circle and a triangle.
circle_surface = pg.Surface((60, 60), pg.SRCALPHA)
pg.draw.circle(circle_surface, (30, 90, 200), (30, 30), 30)
triangle_surface = pg.Surface((60, 60), pg.SRCALPHA)
pg.draw.polygon(triangle_surface, (160, 250, 0), ((30, 0), (60, 60), (0, 60)))


def main():
    screen = pg.display.set_mode((640, 480))
    clock = pg.time.Clock()

    # Use `pygame.mask.from_surface` to get the masks.
    circle_mask = pg.mask.from_surface(circle_surface)
    triangle_mask = pg.mask.from_surface(triangle_surface)

    # Also create rects for the two images/surfaces.
    circle_rect = circle_surface.get_rect(center=(320, 240))
    triangle_rect = triangle_surface.get_rect(center=(0, 0))

    done = False

    while not done:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                done = True
            elif event.type == pg.MOUSEMOTION:
                triangle_rect.center = event.pos

        # Now calculate the offset between the rects.
        offset_x = triangle_rect.x - circle_rect.x
        offset_y = triangle_rect.y - circle_rect.y

        # And pass the offset to the `overlap` method of the mask.
        overlap = circle_mask.overlap(triangle_mask, (offset_x, offset_y))
        if overlap:
            print('The two masks overlap!', overlap)

        screen.fill((30, 30, 30))
        screen.blit(circle_surface, circle_rect)
        screen.blit(triangle_surface, triangle_rect)

        pg.display.flip()
        clock.tick(30)


if __name__ == '__main__':
    pg.init()
    main()
    pg.quit()
