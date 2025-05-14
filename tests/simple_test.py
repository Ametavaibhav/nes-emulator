"""
A simple test borrowed from the eBook: https://skilldrick.github.io/easy6502/

This will load 3 values onto 3 locations in (0200 - 05ff, which is used to represent the screen and draw; values 00-0f represent 16 different colors)

--- Sample Code (the actual values may be different) ---
LDA #$01
STA $0200
LDA #$05
STA $0201
LDA #$ff
STA $0202
---
The hexdump of the code above: ```0600: a9 01 8d 00 02 a9 05 8d 01 02 a9 ff 8d 02 02``
"""
from src.cpu import CPU

INSTRUCTIONS = [0xa9, 0x01, 0x8d, 0x00, 0x02, 0xa9, 0x05, 0x8d, 0x01, 0x02, 0xa9, 0xff, 0x8d, 0x02, 0x02]


def main():
    cpu = CPU()

    cpu.load_program(INSTRUCTIONS)

    cpu.execute()




if __name__ == "__main__":
    main()



