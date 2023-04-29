#!/usr/bin/python3.4
# setup #
from pygame.locals import *
import pygame
import sys
# setup pygame/window #
mainClock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption('Physics Explanation')
screen = pygame.display.set_mode((500, 500), 0, 32)

player = pygame.Rect(100, 100, 40, 80)

tiles = [pygame.Rect(200, 350, 50, 50), pygame.Rect(260, 320, 50, 50)]


def collision_test(rect, tiles):
    collisions = []
    for tile in tiles:
        if rect.colliderect(tile):
            collisions.append(tile)
    return collisions


def move(rect, movement, tiles):  # movement = [5,2]

    # pos = pygame.mouse.get_pos()
    # rect.x = pos[0]
    # rect.y = pos[1]
    # rect.center = (rect.x, rect.y)

    rect.x += movement[0]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[0] > 0:
            rect.right = tile.left
        if movement[0] < 0:
            rect.left = tile.right

    rect.y += movement[1]
    collisions = collision_test(rect, tiles)
    for tile in collisions:
        if movement[1] > 0:
            rect.bottom = tile.top
        if movement[1] < 0:
            rect.top = tile.bottom

    return rect


right = False
left = False
up = False
down = False

last_mouse_pos = [0, 0]
# loop #
while True:

    # clear display #
    screen.fill((0, 0, 0))

    mouse_pos = pygame.mouse.get_pos()
    movement = [0, 0]

    movement[0] = mouse_pos[0] - last_mouse_pos[0]
    movement[1] = mouse_pos[1] - last_mouse_pos[1]

    last_mouse_pos = pygame.mouse.get_pos()

    player = move(player, movement, tiles)

    pygame.draw.rect(screen, (255, 255, 255), player)

    for tile in tiles:
        pygame.draw.rect(screen, (255, 0, 0), tile)

    # event handling #
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        # if event.type == KEYDOWN:
        #     if event.key == K_RIGHT:
        #         right = True
        #     if event.key == K_LEFT:
        #         left = True
        #     if event.key == K_DOWN:
        #         down = True
        #     if event.key == K_UP:
        #         up = True
        # if event.type == KEYUP:
        #     if event.key == K_RIGHT:
        #         right = False
        #     if event.key == K_LEFT:
        #         left = False
        #     if event.key == K_DOWN:
        #         down = False
        #     if event.key == K_UP:
        #         up = False

    # update display #
    pygame.display.update()
    mainClock.tick(60)
