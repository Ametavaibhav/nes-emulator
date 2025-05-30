class Memory:
    def __init__(self):
        self.memory = bytearray(0x10000) ## size: 65536

        # self.program_counter_address =
        # self.stack_pointer_address =
        # self.index_x_address =
        # self.index_y_address =
        # self.status_register_address =


    def read_memory(self, address: int):
        return self.memory[address & 0xffff]


    def write_memory(self, address: int, value: int):
        address &= 0xffff
        if isinstance(value, int):
            self.memory[address] = value
        elif isinstance(value, list):
            self.memory[address: address + len(value)] = value
        else:
            raise Exception(f"unexpected value type!")
        return
