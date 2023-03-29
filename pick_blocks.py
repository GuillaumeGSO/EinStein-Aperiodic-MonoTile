"""
Use sprites to pick up blocks
 
Sample Python/Pygame Programs
Simpson College Computer Science
http://programarcadegames.com/
http://simpson.edu/computer-science/
 
Explanation video: http://youtu.be/iwLj7iJCFQM
"""
import pygame
import random
from math import cos, sin, sqrt, pi
from random import randint

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)

SIZE = 100


class Tile(pygame.sprite.Sprite):

    def __init__(self, color, size):

        # Call the parent class (Sprite) constructor
        super().__init__()

        surf4 = pygame.Surface((size * 3.1, size * 2.3), pygame.SRCALPHA)
        # surf4.fill("pink")
        # pygame.draw.polygon(surf4, color, self.draw_hat(
        #     surf4.get_width() / 2, surf4.get_height() / 4.5, size))
        pygame.draw.aalines(surf4, color, True, self.draw_hat(
            surf4.get_width() / 2, surf4.get_height() / 4.5, size))
        self.image = surf4

        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values
        # of rect.x and rect.y
        self.rect = self.image.get_rect()

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
        print("size", size)
        print(point4[0]-point12[0])
        print(point8[1]-point13[1])
        return [point1, point2, point3, point4,
                point5, point6, point7, point8, point9, point10, point11, point12, point13]


class Player(Tile):
    """ This class represents the player. It derives from block and thus gets
    the same ___init___ method we defined above. """

    # List of all the blocks we are carrying
    carry_block_list = []

    def update(self):
        """ Method called when updating a sprite. """

        # Get the current mouse position. This returns the position
        # as a list of two numbers.
        pos = pygame.mouse.get_pos()

        # Now see how the mouse position is different from the current
        # player position. (How far did we move?)
        diff_x = self.rect.x - pos[0]
        diff_y = self.rect.y - pos[1]

        # Loop through each block that we are carrying and adjust
        # it by the amount we moved.
        for block in self.carry_block_list:
            block.rect.x -= diff_x
            block.rect.y -= diff_y

        # Now wet the player object to the mouse location
        self.rect.x = pos[0]
        self.rect.y = pos[1]


# Initialize Pygame
pygame.init()

# Set the height and width of the screen
screen_width = 700
screen_height = 400
screen = pygame.display.set_mode([screen_width, screen_height])

# This is a list of 'sprites.' Each block in the program is
# added to this list. The list is managed by a class called 'Group.'
block_list = pygame.sprite.Group()

# This is a list of every sprite.
# All blocks and the player block as well.
all_sprites_list = pygame.sprite.Group()

for i in range(randint(10, 20)):
    # This represents a block
    block = Tile(BLACK, SIZE)

    # Set a random location for the block
    block.rect.x = random.randrange(screen_width)
    block.rect.y = random.randrange(screen_height)

    # Add the block to the list of objects
    block_list.add(block)
    all_sprites_list.add(block)

# Create a RED player block
player = Player(RED, SIZE)
all_sprites_list.add(player)

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

        elif event.type == pygame.MOUSEBUTTONDOWN:
            # When the mouse button is pressed, see if we are in contact with
            # other sprites:
            blocks_hit_list = pygame.sprite.spritecollide(
                player, block_list, False)

            # Set the list of blocks we are in contact with as the list of
            # blocks being carried.
            player.carry_block_list = blocks_hit_list

        elif event.type == pygame.MOUSEBUTTONUP:
            # When we let up on the mouse, set the list of blocks we are
            # carrying as empty.
            player.carry_block_list = []

    all_sprites_list.update()

    # Clear the screen
    screen.fill(WHITE)

    # Draw all the spites
    all_sprites_list.draw(screen)

    # Limit to 60 frames per second
    clock.tick(60)

    # Go ahead and update the screen with what we've drawn.
    pygame.display.flip()

pygame.quit()
