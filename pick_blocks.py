"""
Use sprites to pick up blocks
 
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Explanation video: http://youtu.be/iwLj7iJCFQM
"""
import pygame
from math import cos, sin, sqrt, pi
from random import choice

colors = ["blue", "aqua", "chocolate", "darkblue",
          "yellow", "orange", "red", "fuchsia"]
MAX_NUMBER_OF_TILE = 10
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SIZE = 50


class Tile(pygame.sprite.Sprite):

    def __repr__(self) -> str:
        return f"Rot:{self.rot}, flipped:{self.flipped}, color: {self.color}, image: {self.image}"

    def __init__(self, color):

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.color = color
        self.rot = 0
        self.flipped = False

        self.image = self.generate_surface(color, self.rot, self.flipped)
        self.image_orig = self.image.copy()
        # self.tile_mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()

    def generate_image_copy(self):
        image = self.image_orig.copy()
        image = pygame.transform.rotate(image, self.rot)
        image = pygame.transform.flip(image, self.flipped, False)
        return image

    def generate_surface(self, color, rotation=0, flip=False):
        image = pygame.Surface(
            (SIZE * 3.1, SIZE * 2.3), pygame.SRCALPHA)
        # self.rect.center
        image.fill("pink")
        pygame.draw.polygon(image, color, self.draw_hat(
            image.get_width() / 2, image.get_height() / 4.5))
        pygame.draw.lines(image, "green" if flip else "white", True, self.draw_hat(
            image.get_width() / 2, image.get_height() / 4.5), 2)
        pygame.draw.circle(image, "green", (image.get_width(
        ) / 2, image.get_height() / 2), SIZE/10)
        image = pygame.transform.rotate(image, rotation)
        image = pygame.transform.flip(image, flip, False)
        self.rot = rotation
        self.flipped = flip
        return image

    def rotate_left(self):
        print(self)
        image_copy = self.generate_image_copy()
        self.rot = (self.rot + 30) % 360
        self.image = pygame.transform.rotate(image_copy, self.rot)
        print(self)

    def rotate_right(self):
        image_copy = self.generate_image_copy()
        self.rot = (self.rot - 30) % 360
        self.image = pygame.transform.rotate(image_copy, self.rot)

    def flip(self):
        image_copy = self.generate_image_copy()
        self.image = pygame.transform.flip(image_copy, True, False)
        self.flipped = not self.flipped

    def update(self):
        self.tile_mask = pygame.mask.from_surface(self.image)

    def draw_hat(self, x, y):

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


class Player(Tile):
    """ This class represents the player. It derives from block and thus gets
    the same ___init___ method we defined above. """

    def generate_new_tile(self, color):
        tile = Tile(color)
        tile.image = tile.generate_surface(color, self.rot, self.flipped)
        tile.rect = self.rect.copy()

        return tile

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]
        self.rect.center = (self.rect.x, self.rect.y)


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 800
screen_height = 500
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
tiles_group = pygame.sprite.Group()


player_group = pygame.sprite.GroupSingle()


# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(True)


# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = pygame.mouse.get_pos()

            if player_group.sprite:
                player = player_group.sprite
                # when having a moving player
                if player.color == "black":  # this is brand new player
                    color = choice(colors)
                else:
                    color = player.color

                tile = player.generate_new_tile(color)
                tiles_group.add(tile)
                player.kill()
            else:
                tile_found = False
                for tile in tiles_group:
                    if tile.rect.collidepoint(mx, my):
                        tile_found = True
                        player = Player(tile.color)
                        player.image = tile.generate_image_copy()
                        player.rot = tile.rot
                        player.flipped = tile.flipped
                        player.rect = tile.rect
                        player_group.add(player)
                        tile.kill()
                if not tile_found:
                    # create a new player
                    player = Player("black")
                    player_group.add(player)

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.rotate_right()
            if event.key == pygame.K_LEFT:
                player.rotate_left()
            if event.key == pygame.K_SPACE:
                player.flip()
            if event.key == pygame.K_ESCAPE:
                done = True

    if len(tiles_group) > MAX_NUMBER_OF_TILE:
        tiles_group.remove(tiles_group.sprites()[0])

    tiles_group.update()
    player_group.update()

    # Clear the screen
    screen.fill(BLACK)

    # Draw all the spites
    tiles_group.draw(screen)
    if (len(player_group) == 0):
        pygame.mouse.set_visible(True)
    else:
        pygame.mouse.set_visible(True)
    player_group.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
