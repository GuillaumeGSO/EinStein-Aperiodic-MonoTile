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
from random import randint

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SIZE = 50


class Tile(pygame.sprite.Sprite):

    def __init__(self, color, size):

        # Call the parent class (Sprite) constructor
        super().__init__()

        self.size = size
        self.rot = 0
        self.flipped = False

        self.init_surface = self.generate_surface(color)
        self.image = self.init_surf

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

    def generate_surface(self, color, rotation=0, flip=False):
        self.init_surf = pygame.Surface(
            (self.size * 3.1, self.size * 2.3), pygame.SRCALPHA)
        # self.init_surf.fill("pink")
        pygame.draw.polygon(self.init_surf, color, self.draw_hat(
            self.init_surf.get_width() / 2, self.init_surf.get_height() / 4.5, self.size))
        pygame.draw.lines(self.init_surf, "red" if flip else "white", True, self.draw_hat(
            self.init_surf.get_width() / 2, self.init_surf.get_height() / 4.5, self.size), 2)
        self.init_surf = pygame.transform.rotate(self.init_surf, rotation)
        return pygame.transform.flip(self.init_surf, flip, False)

    def rotate_left(self):
        self.rot = (self.rot + 30) % 360
        self.image = self.init_surf.copy()
        self.image = pygame.transform.rotate(self.image, self.rot)

    def rotate_right(self):
        self.rot = (self.rot - 30) % 360
        self.image = self.init_surf.copy()
        self.image = pygame.transform.rotate(self.image, self.rot)

    def flip(self):
        image_copy = self.image.copy()
        self.image_copy = pygame.transform.rotate(image_copy, self.rot)
        self.image = pygame.transform.flip(image_copy, True, False)
        self.flipped = not self.flipped
        print(self.rot, self.flipped)

    def update(self):
        pass

    def draw_hat(self, x, y, size):

        half = size / 2
        apotheme = size * sqrt(3) / 2

        # starting point
        start_x = x
        start_y = y

        point1 = (start_x, start_y),
        point2 = (start_x + (half * sin(pi / 6)),
                  start_y - (half * cos(pi / 6)))
        point3 = (point2[0] + size, point2[1] + 0)
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

    def generate_clone(self, color):
        tile = Tile(color, player.size)
        tile.image = tile.generate_surface(color, self.rot, self.flipped)
        tile.rect = player.rect.copy()
        return tile

    def update(self):
        pos = pygame.mouse.get_pos()
        self.rect.x = pos[0]
        self.rect.y = pos[1]


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


# Create a RED player block
# player = Player(RED, SIZE)
# player_group.add(player)

# Loop until the user clicks the close button.
done = False

# Used to manage how fast the screen updates
clock = pygame.time.Clock()

# Hide the mouse cursor
pygame.mouse.set_visible(False)

# -------- Main Program Loop -----------
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            (mx, my) = pygame.mouse.get_pos()
            if len(player_group) > 0:
                tile = player.generate_clone("blue")
                tiles_group.add(tile)
                player.kill()
            else:
                for tile in tiles_group:
                    if tile.rect.collidepoint(mx, my):
                        player = Player(RED, 50)
                        print(tile.rot, tile.flipped)
                        player.rot = tile.rot
                        player.flipped = tile.flipped
                        player_group.add(player)
                        tiles_group.remove(tile)
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT:
                player.rotate_right()
            if event.key == pygame.K_LEFT:
                player.rotate_left()
            if event.key == pygame.K_UP:
                player.flip()
            if event.key == pygame.K_SPACE:
                # create a new player
                player = Player(RED, SIZE)
                player_group.add(player)
            if event.key == pygame.K_ESCAPE:
                done = True

    if len(tiles_group) > 5:
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
        pygame.mouse.set_visible(False)
    player_group.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
