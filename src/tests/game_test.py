import pygame
import sys

import numpy as np

from cpu.cpu import CPU
from tests import snake_6502


def get_image_pixels():
    from PIL import Image

    path = './src/test_img_3.png'

    image = Image.open(path)

    #image.show()

    image = np.asarray(image)

    return image[:, :, 0:3]




def main():
    pygame.init()

    W, H = 640, 480

    # WHITE = (135, 240, 20)
    # BLUE = (0, 132, 198)
    #
    # rect = pygame.Rect(300, 220, 40, 40)
    # speed = 10

    screen = pygame.display.set_mode((H, W))
    pygame.display.set_caption("Snake Game Test for 6502")

    clock = pygame.time.Clock()
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        #     keys = pygame.key.get_pressed()
        #     if keys[pygame.K_LEFT]:
        #         rect.x -= speed ## load in the memory
        #
        #     if keys[pygame.K_RIGHT]:
        #         rect.x += speed
        #
        #     if keys[pygame.K_UP]:
        #         rect.y -= speed
        #
        #     if keys[pygame.K_DOWN]:
        #         rect.y += speed
        #
        # #game_display = []
        # ## fill screen with White
        # screen.fill(WHITE)

        # w1, h1 = 640, 480
        # pixel_array = np.zeros((w1, h1, 3))
        ### Simulator uses 00-0f to represent 16 different colors ($00 is black, and $0f is white)
        pixel_array = get_image_pixels()
        ## draw a rectangle
        #pygame.draw.rect(screen, BLUE, rect)

        ## create a surface
        surface = pygame.surfarray.make_surface(pixel_array)

        ## update the screen
        screen.blit(surface, (0, 0))

        ##update the screen display
        pygame.display.flip()

        ## limit to 60 fps
        clock.tick(60)

    pygame.quit()
    sys.exit()


if __name__ == "__main__":
    main()

# pygame.init() ## initializes all pygame modules
#
# W, H =  1920, 1080
# screen = pygame.display.set_mode((W, H))
# pygame.display.set_caption("Snake Game test for 6502")
#
# ## test colors
# WHITE = (135, 240, 20)
# BLUE = (0, 132, 198)
# # BLUE  = (0, 0, 255)
#
#
# ## a rectangle
# rect = pygame.Rect(300, 220, 40, 40)
# speed = 5
#
# clock = pygame.time.Clock()
#
# ## main loop
# running = True
#
# while running:
#     for event in pygame.event.get():
#         if event.type == pygame.QUIT:
#             running = False
#
#     # Key States
#     keys = pygame.key.get_pressed()
#     if keys[pygame.K_LEFT]:
#        rect.x -= speed
#
#     if keys[pygame.K_RIGHT]:
#         rect.x += speed
#
#     if keys[pygame.K_UP]:
#         rect.y -= speed
#
#     if keys[pygame.K_DOWN]:
#         rect.y += speed
#
#     ## fill the screen with white
#     screen.fill(WHITE)
#
#     ## draw a rectangle
#     pygame.draw.rect(screen, BLUE, rect)
#
#     ## update the screen/display
#     pygame.display.flip()
#
#     ## limit frame rate
#     clock.tick(60)
#
# pygame.quit()
# sys.exit()



