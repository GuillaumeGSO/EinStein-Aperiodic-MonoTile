import pygame as pg
import math
from random import randint, randrange
import sys


class Hat(pg.sprite.Sprite):

    def __init__(self, screen, x, y, size, rot):
        super().__init__()
        self.screen = screen
        self.x = x
        self.y = y
        self.size = size
        self.rot = rot

    def update(self):
        # print("update")
        pass

    def draw(self):
        # print("draw")
        self.draw_hat(self.screen, self.screen.get_rect(),
                      self.x, self.y, self.size)

    def draw_hat(self, surface, rect,  x, y, size):
        # set the diameter and number of sides for the polygons
        side = size
        half = side / 2
        apotheme = side * math.sqrt(3) / 2

        # starting point
        start_x = x
        start_y = y

        pi = math.pi

        point1 = (start_x, start_y),
        # point2 = (start_x + 100, start_y + 200)
        point2 = (start_x + (half * math.sin(pi / 6)),
                  start_y - (half * math.cos(pi / 6)))
        point3 = (point2[0] + side, point2[1] + 0)
        point4 = (point3[0] + half * math.cos(pi / 3),
                  point3[1] + half * math.sin(pi / 3))
        point5 = (point4[0] - apotheme * math.cos(pi / 6),
                  point4[1] + apotheme * math.sin(pi / 6))
        point6 = (point5[0],
                  point5[1] + apotheme)
        point7 = (point6[0] - half,
                  point6[1])
        point8 = (point7[0] - half * math.cos(pi / 3),
                  point7[1] + half * math.sin(pi / 3))
        point9 = (point8[0] - apotheme * math.cos(pi / 6),
                  point8[1] - apotheme * math.sin(pi / 6))
        point10 = (point9[0],
                   point9[1] - apotheme)
        point11 = (point10[0] - half,
                   point10[1])
        point12 = (point11[0] - half * math.cos(pi / 3),
                   point11[1] - half * math.sin(pi / 3))
        point13 = (point12[0] + apotheme * math.cos(pi / 6),
                   point12[1] - apotheme * math.sin(pi / 6))

        pointList = [point1, point2, point3, point4,
                     point5, point6, point7, point8, point9, point10, point11, point12, point13]

        target_rect = pg.Rect(rect)
        shape_surf = pg.Surface(target_rect.size, pg.SRCALPHA)
        pg.draw.aalines(shape_surf, (0, 255, 0), True,
                        pointList)
        surface.blit(shape_surf, shape_surf.get_rect(
            center=target_rect.center))


class App:

    def __init__(self):
        pg.init()
        pg.display.set_caption("Einstein Hat")
        self.screen = pg.display.set_mode((640, 480))

        # This hides bachground
        color = (20, 20, 20)
        self.screen.fill(color)
        self.clock = pg.time.Clock()
        self.hat = None

    def update(self):
        # self.hat = Hat(self.screen, randint(0, self.screen.get_width()), randint(
        #     0, self.screen.get_height()), 30, randrange(0, 360, 30))
        # self.hat.update()
        self.clock.tick(60)

    def draw(self):
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():

            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()
            if event.type == pg.MOUSEBUTTONDOWN:
                pos = pg.mouse.get_pos()
                self.hat = Hat(
                    self.screen, pos[0], pos[1], 30, randrange(0, 360, 30))
                self.hat.draw()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


if __name__ == "__main__":
    app = App()
    app.run()
