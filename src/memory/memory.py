class Memory:
    def __init__(self):
        self.memory = bytearray(0xffff) ## size: 65536

        # self.program_counter_address =
        # self.stack_pointer_address =
        # self.index_x_address =
        # self.index_y_address =
        # self.status_register_address =


    def read_memory(self, address: int):
        return self.memory[address]


    def write_memory(self, address: int, value):
        if isinstance(value, int):
            return self.memory[address] = value
        elif isinstance(value, list):
            return self.memory[address: address + len(value)] = value
        else:
            raise Exception(f"unexpected value type!")
