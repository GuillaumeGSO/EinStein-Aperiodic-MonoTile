
import pygame as pg
from math import cos, sin, sqrt, pi
import sys


COLORS = [(0, 0, 255), (255, 255, 255), (255, 165, 0),
          (0, 128, 0), (255, 255, 0), (255, 0, 0)]
SIZE = 50
FPS = 60
ROTATE_ANGLE = 60
BACKGROUND_COLOR = "grey30"


class App:

    def __init__(self):
        pg.init()

        # Set the height and width of the screen
        screen_width = 800
        screen_height = 500
        self.screen = pg.display.set_mode([screen_width, screen_height])

        self.screen.fill(BACKGROUND_COLOR)

        self.clock = pg.time.Clock()
        self.game = Game(self)

    def update(self):
        self.game.update()
        self.clock.tick(FPS)

    def draw(self):
        self.game.draw()
        pg.display.flip()

    def check_events(self):
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                sys.exit()

            if event.type == pg.MOUSEBUTTONDOWN:
                self.game.mouse_click(pg.mouse.get_pos())

            if event.type == pg.KEYDOWN and self.game.player.tile != None:
                if event.key == pg.K_RIGHT:
                    self.game.player.tile.rotate_right()
                if event.key == pg.K_LEFT:
                    self.game.player.tile.rotate_left()
                if event.key == pg.K_SPACE:
                    self.game.player.tile.flip()

    def run(self):
        while True:
            self.check_events()
            self.update()
            self.draw()


class Game():
    def __init__(self, app):
        self.app = app
        self.player = Player()
        self.tiles_group = pg.sprite.Group()
        self.player_group = pg.sprite.GroupSingle()

    def update(self):
        self.player.can_drop = self.collision_test()
        self.player.update()

    def draw(self):
        self.app.screen.fill(BACKGROUND_COLOR)
        self.tiles_group.draw(self.app.screen)
        self.player_group.draw(self.app.screen)

    def collision_test(self):
        if self.player.tile == None:
            return False

        collide = pg.sprite.spritecollide(
            self.player.tile, self.tiles_group, False, pg.sprite.collide_mask)
        return len(collide) == 0

    def mouse_click(self, mouse_pos):

        if self.app.screen.get_at(mouse_pos) != pg.color.Color(BACKGROUND_COLOR):
            tile_found = False
            for tile in self.tiles_group:
                pos_in_mask = mouse_pos[0] - \
                    tile.rect.x, mouse_pos[1] - tile.rect.y
                touching = tile.rect.collidepoint(
                    *mouse_pos) and tile.tile_mask.get_at(pos_in_mask)
                if touching:
                    # grab existing tile
                    tile_found = True
                    self.player.tile = tile
                    self.player_group.add(self.player.tile)
                    # tile.kill()
            if not tile_found:
                # create a new player
                self.player.tile = Tile()
                self.player_group.add(self.player.tile)
        else:
            tile = self.player.generate_new_tile()
            self.tiles_group.add(tile)
            self.player_group.empty()
            self.player.tile = None


class Tile(pg.sprite.Sprite):

    def __repr__(self) -> str:
        return f"Rot:{self.rot}, flipped:{self.flipped}, image: {self.image}"

    def __init__(self):

        super().__init__()

        self.rot = 0
        self.flipped = False

        self.update_surface(self.rot, self.flipped)
        self.image_orig = self.image.copy()
        self.tile_mask = pg.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def generate_image_copy(self):
        image = self.image_orig.copy()
        image = pg.transform.rotate(image, self.rot)
        image = pg.transform.flip(image, self.flipped, False)
        return image

    def update_surface(self, rotation=0, flip=False):

        image = pg.Surface(
            (SIZE * 3.1, SIZE * 2.3), pg.SRCALPHA)
        pg.draw.polygon(image, COLORS[rotation//60], Tile.draw_hat(
            image.get_width() / 2, image.get_height() / 4.5))

        pg.draw.lines(image, "purple" if flip else "grey", True, Tile.draw_hat(
            image.get_width() / 2, image.get_height() / 4.5), 2)
        pg.draw.circle(image, "purple" if flip else "grey", (image.get_width(
        ) / 2, image.get_height() / 2), SIZE/10)
        image = pg.transform.rotate(image, rotation)
        image = pg.transform.flip(image, flip, False)

        self.rot = rotation
        self.flipped = flip
        self.image = image

    def rotate_left(self):
        rot = - ROTATE_ANGLE if self.flipped else ROTATE_ANGLE
        self.rot = (self.rot + rot) % 360
        self.update_surface(self.rot, self.flipped)

    def rotate_right(self):
        rot = ROTATE_ANGLE if self.flipped else -ROTATE_ANGLE
        self.rot = (self.rot + rot) % 360
        self.update_surface(self.rot, self.flipped)

    def flip(self):
        self.flipped = not self.flipped
        self.update_surface(self.rot, self.flipped)

    def draw_hat(x, y):

        half = SIZE / 2
        apotheme = SIZE * sqrt(3) / 2

        # starting point
        start_x = x
        start_y = y

        point1 = (start_x, start_y),
        point2 = (start_x + (half * sin(pi / 6)),
                  start_y - (half * cos(pi / 6)))
        point3 = (point2[0] + SIZE, point2[1] + 0)
        point4 = (point3[0] + half * cos(pi / 3),
                  point3[1] + half * sin(pi / 3))
        point5 = (point4[0] - apotheme * cos(pi / 6),
                  point4[1] + apotheme * sin(pi / 6))
        point6 = (point5[0],
                  point5[1] + apotheme)
        point7 = (point6[0] - half,
                  point6[1])
        point8 = (point7[0] - half * cos(pi / 3),
                  point7[1] + half * sin(pi / 3))
        point9 = (point8[0] - apotheme * cos(pi / 6),
                  point8[1] - apotheme * sin(pi / 6))
        point10 = (point9[0],
                   point9[1] - apotheme)
        point11 = (point10[0] - half,
                   point10[1])
        point12 = (point11[0] - half * cos(pi / 3),
                   point11[1] - half * sin(pi / 3))
        point13 = (point12[0] + apotheme * cos(pi / 6),
                   point12[1] - apotheme * sin(pi / 6))
        # print("size", size)
        # print(point4[0]-point12[0])
        # print(point8[1]-point13[1])
        return [point1, point2, point3, point4,
                point5, point6, point7, point8, point9, point10, point11, point12, point13]


class Player():

    def __init__(self):
        self.tile: Tile = None
        self.can_drop = True

    def generate_new_tile(self):
        tile = Tile()
        tile.update_surface()
        tile.rect = self.tile.rect.copy()
        return tile

    def update(self):
        if self.tile == None:
            return

        self.tile.update_surface(
            self.tile.rot, self.tile.flipped)
        pos = pg.mouse.get_pos()
        self.tile.rect.x = pos[0]
        self.tile.rect.y = pos[1]

        offset_x = self.tile.image.get_size()[0] - self.tile.rect.size[0]
        offset_y = self.tile.image.get_size()[1] - self.tile.rect.size[1]
        self.tile.rect.center = (self.tile.rect.x - offset_x / 2,
                                 self.tile.rect.y - offset_y / 2)


if __name__ == "__main__":
    app = App()
    app.run()
