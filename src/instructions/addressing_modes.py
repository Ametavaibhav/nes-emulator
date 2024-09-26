from instructions.helpers import merge_bytes, split_bytes

class AddressingModes:
    @staticmethod
    def absolute(cpu):
        ## not sure if it is needed; get params, and set them for little endian?
        lsb = cpu.read_program_counter()
        cpu.program_counter += 1
        msb = cpu.read_program_counter()
        cpu.program_counter += 1
        return merge_bytes(msb, lsb)

    @staticmethod
    def zero_page(cpu):
        ## do nothing
        address = cpu.read_program_counter()
        cpu.program_counter += 1
        return address

    @staticmethod
    def zero_page_x(cpu):
        ## add param to index x; wrap around if the value exceeds one byte
        address = (cpu.read_program_counter() + cpu.index_x) & 0xff ## wrap around if it exceeds one byte
        cpu.program_counter += 1
        return address

    @staticmethod
    def zero_page_y(cpu):
        ## can only be used with LDX, and STX. not enforced here.
        address = (cpu.read_program_counter() + cpu.index_y) & 0xff
        cpu.program_counter += 1
        return address

    @staticmethod
    def absolute_x(cpu):
        lsb = cpu.read_program_counter()
        cpu.program_counter += 1
        msb = cpu.read_program_counter()
        cpu.program_counter += 1
        address = merge_bytes(msb, lsb)
        return (address + cpu.index_x) & 0xffff

    @staticmethod
    def absolute_y(cpu):
        lsb = cpu.read_program_counter()
        cpu.program_counter += 1
        msb = cpu.read_program_counter()
        cpu.program_counter += 1
        address = merge_bytes(msb, lsb)
        return (address + cpu.index_y) & 0xffff

    @staticmethod
    def immediate(cpu):
        ## for instruction that take value instead of an address
        address = cpu.read_program_counter()
        cpu.program_counter += 1
        return address

    @staticmethod
    def relative():
        ## used from branching... no transformation needed..
        return None

    @staticmethod
    def implicit():
        ## no need to implement
        return None

    @staticmethod
    def indirect(cpu):
        ## assuming params are in orders, and need to set for little endian fashion
        lsb = cpu.read_program_counter()
        cpu.program_counter += 1
        msb = cpu.read_program_counter()
        cpu.program_counter += 1
        address = merge_bytes(msb, lsb)
        return cpu.read_memory(address)

    @staticmethod
    def indexed_indirect(cpu):
        ## not sure if a wrap around is needed
        address = cpu.read_program_counter()
        cpu.program_counter += 1
        zero_page_address = (address + cpu.index_x) & 0xff
        lsb = cpu.read_memory(zero_page_address)
        msb = cpu.read_memory(zero_page_address + 1)
        return merge_bytes(msb, lsb) & 0xffff

    @staticmethod
    def indirect_indexed(cpu):
        ## not sure if wrap around is needed
        address = cpu.read_program_counter()
        cpu.program_counter += 1
        lsb = cpu.read_memory(address)
        msb = cpu.read_memory(address + 1)
        address = merge_bytes(msb, lsb)
        return (address + cpu.index_y) & 0xffff