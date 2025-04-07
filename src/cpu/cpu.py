from memory import Memory
from instructions import addressing_modes, instructions


class CPU(Memory):
    def __init__(self):
        ## using addresses
        self.program_counter = 0x0800 ## internal register; usually 0x0800
        self.stack_pointer = 0xff  ## internal register, holds address to the stack. range is $0100-$01FF (only 8 bits would do, too)
        self.accumulator = 0x00 ## internal register; no in memory
        self.index_x = 0x00
        self.index_y = 0x00
        self.C = 0 ## carry flag
        self.Z = 0 ## zero flag
        self.I = 0 ## interrupt flag
        self.D = 0 ## decimal flag
        self.B = 0 ## break command flag
        self.V = 0 ## overflow flag
        self.N = 0 ## negative flag

        ##self.addressing_modes = addressing_modes.AddressingModes()

    def push_stack(self, value):
        address = 0x01*(0xff + 1) + self.stack_pointer
        self.write_memory(address, value)

        self.stack_pointer -= 1
        if self.stack_pointer < 0x00:
            self.stack_pointer = 0xff
        return

    def pull_stack(self):
        address = 0x01*(0xff + 1) + self.stack_pointer
        value = self.read_memory(address)

        self.stack_pointer += 1
        if self.stack_pointer > 0xff:
            self.stack_pointer = 0xff
        return value

    def status_reg_to_int(self):
        """
        converting all the status registers to int, to represent the status-register byte
        flags are N V _ B D I Z C
        """
        flags = 0
        flags |= (self.N << 7)
        flags |= (self.V << 6)
        flags |= (1 << 5)
        flags |= (self.B << 4)
        flags |= (self.D << 3)
        flags |= (self.I << 2)
        flags |= (self.Z << 1)
        flags |= self.C
        return flags

    def int_to_status_reg(self, value):
        """
        set status register flags from an integer
        """
        self.N = (value >> 7) & 1
        self.V = (value >> 6) & 1
        self.B = (value >> 4) & 1
        self.D = (value >> 3) & 1
        self.I = (value >> 2) & 1
        self.Z = (value >> 1) & 1
        self.C = value & 1
        return


    def reset(self):
        ## implement reset...
        ## current questions
        ## what all the reset? memory? just the registers? only some of the registers?
        pass

    def read_program_counter(self):
        return self.read_memory(self.program_counter)


    def load_program(self, program: bytes):
        """
        loads the program into the memory, starting from the program_counter
        """
        ## TODO: check if the program counter needs to be updated
        self.write_memory(self.program_counter, program)


    def execute(self):
        while True:
            current_instruction = self.read_memory(self.program_counter)
            self.program_counter += 1

            # TODO: ## lookup instruction, and addressing mode
            # TODO: address = self.addressing_modes.*funct*(self)

            # TODO: ## execute instruction


            ## address = self.addressing_modes.absolute(self)
            ## fetch details for the current_instruction: how many bytes to fetch for parameters
            ## how much to increment the program counter by

            ## execute instruction (with the parameter)

            ## exit condition..?
