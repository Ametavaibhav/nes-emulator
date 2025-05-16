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


COLORS_DICT = {
    0x0: np.array((0, 0, 0)),
    0x1: np.array((125,192,211)),
    0x2: np.array((174,154,99)),
    0x3: np.array((107,5,235)),
    0x4: np.array((63,204,37)),
    0x5: np.array((152,31,9)),
    0x6: np.array((106,48,83)),
    0x7: np.array((98,106,70)),
    0x8: np.array((105,62,13)),
    0x9: np.array((0,248,153)),
    0xa: np.array((216,42,179)),
    0xb: np.array((163,192,47)),
    0xc: np.array((36,159,199)),
    0xd: np.array((241,247,165)),
    0xe: np.array((117,104,222)),
    0xf: np.array((255, 255, 255)),
}

# COLORS_DICT = {
#     0x0: (0, 0, 0),
#     0x1: (125,192,211),
#     0x2: (174,154,99),
#     0x3: (107,5,235),
#     0x4: (63,204,37),
#     0x5: (152,31,9),
#     0x6: (106,48,83),
#     0x7: (98,106,70),
#     0x8: (105,62,13),
#     0x9: (0,248,153),
#     0xa: (216,42,179),
#     0xb: (163,192,47),
#     0xc: (36,159,199),
#     0xd: (241,247,165),
#     0xe: (117,104,222),
#     0xf: (255, 255, 255)
# }

def map_int_colors(value):
    return COLORS_DICT.get(value, (255, 255, 255))

vectorized_color_map = np.vectorize(map_int_colors)


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

    paused = False
    game_over = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                continue

            # Look for key-presses (WASD) | update memory location
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    paused = True

                elif event.key == pygame.K_r:
                    paused = False

                elif not paused:
                    if event.key == pygame.K_w or event.key == pygame.K_UP:
                        update_movementDir(cpu, 0x77)
                        break
                    elif event.key == pygame.K_d or event.key == pygame.K_RIGHT:
                        update_movementDir(cpu, 0x64)
                        break
                    elif event.key == pygame.K_s or event.key == pygame.K_DOWN:
                        update_movementDir(cpu, 0x73)
                        break
                    elif event.key == pygame.K_a or event.key == pygame.K_LEFT:
                        update_movementDir(cpu, 0x61)
                        break
                ## Needed ?
                # if event.key == pygame.K_ESCAPE:
                #     running = False
            elif event.type == pygame.WINDOWFOCUSLOST:  # pygame ≥ 2.1
                paused = True

        if game_over:
            overlay = pygame.Surface(scaled_screen, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 50 % black
            font = pygame.font.SysFont(None, 72)

            score = (cpu.read_memory(0x03) - 4) // 2
            text_array = [
                "GAME OVER!",
                f"Score: {score}",
            ]

            # random_colors = [(152,31,9), (36,159,199), (107,5,235), (66,105,88), (53,180,92), (188,1,237)]
            random_colors = [(152, 31, 9), (36, 159, 199), (107, 5, 235)]
            line_spacing = font.get_linesize()
            center_offset = len(text_array) // 2
            for i, txt in enumerate(text_array):
                text = font.render(txt, True, random.choice(random_colors))
                rect = text.get_rect(
                    center=((scaled_screen[0] // 2), (scaled_screen[1] // 2) + (i - center_offset) * line_spacing))
                overlay.blit(text, rect)
            screen.blit(overlay, (0, 0))

        elif paused:
            # -------- translucent “PAUSED” overlay --------
            overlay = pygame.Surface(scaled_screen, pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 128))  # 50 % black
            font = pygame.font.SysFont(None, 72)

            score = (cpu.read_memory(0x03) - 4) // 2
            text_array = [
                "PAUSED",
                f"Score: {score}",
                "Press R to resume",
            ]

            #random_colors = [(152,31,9), (36,159,199), (107,5,235), (66,105,88), (53,180,92), (188,1,237)]
            random_colors = [(152, 31, 9), (36, 159, 199), (107, 5, 235)]
            line_spacing = font.get_linesize()
            center_offset = len(text_array)//2
            for i, txt in enumerate(text_array):
                text = font.render(txt, True, random.choice(random_colors))
                rect = text.get_rect(center=((scaled_screen[0] // 2), (scaled_screen[1] // 2) + (i - center_offset)*line_spacing ))
                overlay.blit(text, rect)
            screen.blit(overlay, (0, 0))


        else:
            # Update with a random value in the memory location 0xfe
            try:
                set_random_byte(cpu)

                ## Step through instructions, and render the screen after execution of every instruction
                ## Execute 50 instructions first
                i = 0
                while i < 150:
                    cpu.execute(step=True, debug=False)
                    i += 1

                # Old
                # screen_data = np.array(cpu.memory[0x0200: 0x0600]).reshape(screen_size)
                # screen_data = get_rgb_values(screen_data) ## Should be (32, 32, 3)

                # New
                # screen_data = vectorized_color_map(np.array(cpu.memory[0x0200: 0x0600])).reshape(screen_size)
                # screen_data = np.array(list(map(map_int_colors, cpu.memory[0x0200: 0x0600]))).reshape(32, 32, 3).T
                # ChatGPT
                # --- build a 32×32 uint8 view of video RAM --------------------------
                video = np.frombuffer(cpu.memory,  # raw bytes
                                      dtype=np.uint8,
                                      count=0x400,  # 0x0200–0x05FF
                                      offset=0x0200).reshape(screen_size)  # [row][col]

                video &= 0x0F
                # --- map 0-F pixel values to RGB from COLORS_DICT -------------------
                palette = np.array(list(COLORS_DICT.values()), dtype=np.uint8)  # shape (16,3)
                screen_data = palette[video].transpose(1, 0, 2)  # swap axes → (x, y, 3)

                # Debug Stuff
                # print(f"{counter=}\n{cpu=}")
                # if counter == 15:
                #     print("Here")

                pygame.surfarray.blit_array(surface, screen_data)

                scaled_surface = pygame.transform.scale(surface, scaled_screen)

                screen.blit(scaled_surface, (0, 0))

            except Exception as e:
                print(f"Error: {str(e)}")
                game_over = True


        pygame.display.flip()

        # Limit the game to 60 fps
        clock.tick(60)

    pygame.quit()
    sys.exit()


def main():
    run_game()

    # a = np.random.randint(0, 16, (32, 32))
    # z = get_rgb_values(a)
    # print("here")


if __name__ == '__main__':
    main()