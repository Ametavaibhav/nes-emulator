from src.memory import Memory
from src.instructions.opcode_table import OPCODE_TABLE


class CPU(Memory):
    def __init__(self):
        ## using addresses
        super().__init__()
        self.program_counter = 0x0800 ## internal register; usually 0x0800
        self.stack_pointer = 0xff  ## internal register, holds address to the stack. range is $0100-$01FF
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

    ## To set CPU to a certain stat; Using it for testing/debug purposes only
    def set_cpu_state(self, pc, s, a, x, y, p, memory_locs):
        """
        set the cpu state (all registers), and memory with provided values

        Args:
            memory_locs (list[tuple[int]]): list of tuples containing memory locations and values
        """
        self.program_counter = pc
        self.stack_pointer = s
        self.accumulator = a
        self.index_x = x
        self.index_y = y
        self.int_to_status_reg(p)

        for memory_loc in memory_locs:
            self.write_memory(memory_loc[0], memory_loc[1])


    def get_cpu_state(self):
        """
        Get the state of the CPU/RAM at any given point
        """
        cpu_state = {'pc': self.program_counter,
                     's': self.stack_pointer,
                     'a': self.accumulator,
                     'x': self.index_x,
                     'y': self.index_y,
                     'p': self.status_reg_to_int(),
                     'ram': []
                     }


        for i, val in enumerate(self.memory):
            if val != 0:
                cpu_state['ram'].append([i, val])

        return cpu_state



    def __repr__(self):
        return  f"PC: {self.program_counter}\nSP: {self.stack_pointer}\nA: {self.accumulator}\nX: {self.index_x}\nY: {self.index_y}"



    def push_stack(self, value, debug=False):
        # Set the addresss
        address = 0x0100 | self.stack_pointer

        self.write_memory(address, value)

        if debug:
            print(f"pushed {value} to address {address}")

        self.stack_pointer = (self.stack_pointer - 1) & 0xff

        return


    def pull_stack(self, debug=False):
        self.stack_pointer = (self.stack_pointer + 1) & 0xff

        address = 0x0100 | self.stack_pointer
        value = self.read_memory(address)

        if debug:
            print(f"pulled {value} from address {address}")


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
        ## what all to reset? memory? just the registers? only some of the registers?
        pass

    def read_program_counter(self):
        return self.read_memory(self.program_counter)


    def load_program(self, program: int):
        """
        loads the program into the memory, starting from the program_counter
        """
        ## TODO: check if the program counter needs to be updated
        self.write_memory(self.program_counter, program)


    def execute(self, step=False, debug=False):
        """
        Execute the program loaded in the memory.

        If step is true, only execute one instruction at a time
        """
        while True:
            current_instruction = self.read_memory(self.program_counter)
            self.program_counter += 1
            self.program_counter &= 0xffff ## wrap up to 0

            instruction, addressmode = OPCODE_TABLE.get(current_instruction)

            address = addressmode(self)

            instruction(self, address)

            if debug:
                print(f"CPU exectued the instruction {instruction.__name__} with addressmode {addressmode.__name__} at address {address}")

            if step:
                break


            ## address = self.addressing_modes.absolute(self)
            ## fetch details for the current_instruction: how many bytes to fetch for parameters
            ## how much to increment the program counter by

            ## execute instruction (with the parameter)

            ## exit condition..?



    # def step(self):
    #     """
    #     Execute one instruction at a time
    #     """
    #     current_instruction = self.read_memory(self.program_counter)
    #     self.program_counter += 1
    #
    #     instruction, addressmode = OPCODE_TABLE.get(current_instruction)
    #
    #     address = addressmode(self)
    #
    #     instruction(self, address)

