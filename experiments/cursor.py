import pygame
import math


def draw_hat(x, y, size):
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

    return [point1, point2, point3, point4,
            point5, point6, point7, point8, point9, point10, point11, point12, point13]


pygame.init()
# Creating a canvas of 600*400
screen = pygame.display.set_mode((600, 400))
clock = pygame.time.Clock()

# old type, "bitmap" cursor
cursor1 = pygame.cursors.diamond

# new type, "system" cursor
cursor2 = pygame.SYSTEM_CURSOR_HAND

# new type, "color" cursor
surf = pygame.Surface((30, 25), pygame.SRCALPHA)
pygame.draw.rect(surf, (0, 255, 0), [0, 0, 10, 10])
pygame.draw.rect(surf, (0, 255, 0), [20, 0, 10, 10])
pygame.draw.rect(surf, (255, 0, 0), [5, 5, 20, 20])
cursor3 = pygame.cursors.Cursor((15, 5), surf)

# aperiodic tile
surf4 = pygame.Surface((120, 90), pygame.SRCALPHA)
surf4.fill("pink")
pygame.draw.polygon(surf4, (0, 255, 0), draw_hat(60, 20, 40))
rot = 0
surf4 = pygame.transform.rotate(surf4, rot)
cursor4 = pygame.cursors.Cursor((50, 50), surf4)

cursors = [cursor4, cursor1, cursor2, cursor3]
cursor_index = 0

# the arguments to set_cursor can be a Cursor object
# or it will construct a Cursor object
# internally from the arguments
pygame.mouse.set_cursor(cursors[cursor_index])

while True:
    screen.fill("black")

    for event in pygame.event.get():
        if event.type == pygame.MOUSEBUTTONDOWN:
            cursor_index += 1
            cursor_index %= len(cursors)
            pygame.mouse.set_cursor(cursors[cursor_index])
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                flip_surf = surf4.copy()
                flip_surf = pygame.transform.flip(flip_surf, True, False)
                flip_surf = pygame.transform.rotate(flip_surf, rot)
                cursor4 = pygame.cursors.Cursor((50, 50), flip_surf)
                pygame.mouse.set_cursor(cursor4)
            if event.key == pygame.K_DOWN:
                back_surf = surf4.copy()
                back_surf = pygame.transform.rotate(back_surf, rot)
                cursor4 = pygame.cursors.Cursor((50, 50), back_surf)
                pygame.mouse.set_cursor(cursor4)
            if event.key == pygame.K_SPACE:
                rot += 30
                rot_surf = surf4.copy()
                rot_surf = pygame.transform.rotate(rot_surf, rot)
                cursor4 = pygame.cursors.Cursor((50, 50), rot_surf)
                pygame.mouse.set_cursor(cursor4)

        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit

    pygame.display.flip()
    clock.tick(144)
