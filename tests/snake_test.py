from src.cpu import CPU

from tests.snake_6502 import game_code


import pygame, sys

import random

import numpy as np

pygame.init()


def set_random_byte(cpu):
    # Set a randon byte at location 0xfe
    cpu.write_memory(0xfe, random.randint(0, 255))


def update_movementDir(cpu, value):
    ## Update the memory location $ff with a value representing movement from user input
    cpu.write_memory(0xff, value)


def int_to_rgb(value):
    ## Expects the value to be in range [0-15]
    multiplier = (0 + value)/15

    return (int(255*multiplier), int(255*multiplier), int(255*multiplier))

vectorized_int_to_rgb = np.vectorize(int_to_rgb)


def get_rgb_values(array):
    return np.moveaxis(np.array(vectorized_int_to_rgb(array)), 0, -1)


def run_game():
    cpu = CPU()

    cpu.program_counter = 0x0600
    cpu.load_program(game_code)


    screen_size = width, height = 32, 32
    scaled_screen = 640, 640

    running = True

    screen = pygame.display.set_mode(scaled_screen)
    clock = pygame.time.Clock()

    surface = pygame.Surface(screen_size)

    counter = 0
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            # Look for key-presses (WASD) | update memory location
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    update_movementDir(cpu, 1)
                elif event.key == pygame.K_RIGHT:
                    update_movementDir(cpu, 2)
                elif event.key == pygame.K_DOWN:
                    update_movementDir(cpu, 4)
                elif event.key == pygame.K_LEFT:
                    update_movementDir(cpu, 8)
                ## Needed ?
                # if event.key == pygame.K_ESCAPE:
                #     running = False


        # Update with a random value in the memory location 0xfe
        set_random_byte(cpu)

        ## Step through instructions, and render the screen after execution of every instruction
        cpu.execute(step=True, debug=False)

        # Render the game state
        if counter < 10 == 0:
            screen.fill('black')
        else:
            screen.fill('white')

        screen_data = np.array(cpu.memory[0x0200: 0x0600]).reshape(screen_size)
        screen_data = get_rgb_values(screen_data) ## Should be (32, 32, 3)

        # Debug Stuff
        print(f"{counter=}\n{cpu=}")
        if counter == 15:
            print("Here")

        if screen_data.any():
            print("Here now!")

        if cpu.program_counter == 0:
            print(f"Here")
            break



        pygame.surfarray.blit_array(surface, screen_data)

        scaled_surface = pygame.transform.scale(surface, scaled_screen)

        screen.blit(scaled_surface, (0, 0))
        pygame.display.flip()

        # Limit the game to 60 fps
        clock.tick(60)

        counter += 1




    pygame.quit()
    sys.exit()


def main():
    run_game()

    # a = np.random.randint(0, 16, (32, 32))
    # z = get_rgb_values(a)
    # print("here")


if __name__ == '__main__':
    main()