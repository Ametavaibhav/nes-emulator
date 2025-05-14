"""
# Relevant Links
1. http://www.6502.org/users/obelisk/6502/reference.html#ADC
2. http://www.6502.org/tutorials/6502opcodes.html#ADC
3. https://www.masswerk.at/6502/6502_instruction_set.html#ADC
4. https://tutorial-6502.sourceforge.io/specification/opcodes/#sorted-by-hex-code
"""
from src.instructions.helpers import merge_bytes, split_bytes

def to_signed_int8(value):
    value &= 0xff

    if value >= 128:
        return value - 256
    else:
        return value


class Instructions:
    @staticmethod
    def ADC(cpu, param):
        """
        add memory to accumulator with query
        affected-flag: N V Z C
        """
        ## If param is None, fetch value assuming immediate addressing mode
        if param is None:
            ## Immediate address
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        temp = cpu.accumulator + value + cpu.C

        cpu.C = int(temp > 0xff)
        cpu.V = int(((temp ^ value) & (cpu.accumulator ^ (temp & 0xff))) & 0x80 != 0)

        cpu.accumulator = temp & 0xff
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def AND(cpu, param):
        """
        bitwise AND with accumulator
        affects flags: N Z
        """
        ## If param is None, fetch value assuming immediate addressing mode
        if param is None:
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        cpu.accumulator = cpu.accumulator & value
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = int((cpu.accumulator & (1 << 7)) != 0)
        return

    @staticmethod
    def ASL(cpu, param):
        """
        Arithmetic Shift Left
        affected flags: C Z N
        """
        if param is None:
            # Use accumulator
            cpu.C = int((cpu.accumulator & 1 << 7) != 0)
            cpu.accumulator = (cpu.accumulator << 1) & 0xff
            cpu.Z = int(cpu.accumulator == 0)
            cpu.N = (cpu.accumulator >> 7) & 1
        else:
            value = cpu.read_memory(param)
            cpu.C = int((value & 1 << 7) != 0)
            shifted = (value << 1) & 0xff
            cpu.Z = int(shifted == 0)
            cpu.N = (shifted >> 7) & 1

            cpu.write_memory(param, shifted)
        return

    @staticmethod
    def BCC(cpu, _):
        """
        branch if carry clear.
        affected flags:
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if not cpu.C:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BCS(cpu, _):
        """
        branch if carry set
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if cpu.C:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BEQ(cpu, _):
        """
        branch if equal
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if cpu.Z:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BIT(cpu, param):
        """
        test BITs
        affects flags: N V Z
        """
        value = cpu.read_memory(param)
        temp = cpu.accumulator & value

        cpu.Z = int(temp == 0)
        cpu.N = (value >> 7) & 1
        cpu.V = (value >> 6) & 1
        return

    @staticmethod
    def BMI(cpu, _):
        """
        branch if minus
        """
        offset = cpu.read_memory(cpu.program_counter)
        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if cpu.N:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BNE(cpu, _):
        """
        branch if not equal
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if not cpu.Z:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BPL(cpu,_):
        """
        branch if positive
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff
        if not cpu.N:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BRK(cpu, _):
        """
        force interrupt
        """
        cpu.program_counter += 1
        cpu.program_counter &= 0xffff
        ## push program counter to the stack
        high_byte, low_byte = split_bytes(cpu.program_counter)
        cpu.push_stack(high_byte) ## high byte
        cpu.push_stack(low_byte) ## low byte

        ## push processor status to stack
        ## DONE: can it be done with ## PHP(cpu) instead?
        Instructions.PHP(cpu, _)
        # processor_status = cpu.status_reg_to_int()
        # cpu.push_stack(processor_status)

        ## set interrupt disable flag | NOTE: have conflicting information on which flags to set
        cpu.I = 1

        ## load ISR (interrupt service routine) address
        low_byte = cpu.read_memory(0xfffe)
        high_byte = cpu.read_memory(0xffff)
        cpu.program_counter = merge_bytes(high_byte, low_byte)
        return

    @staticmethod
    def BVC(cpu, _):
        """
        branch if overflow clear
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if not cpu.V:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def BVS(cpu, _):
        """
        branch if overflow set
        """
        offset = cpu.read_memory(cpu.program_counter)

        cpu.program_counter += 1
        cpu.program_counter &= 0xffff

        if cpu.V:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += to_signed_int8(offset)
            cpu.program_counter &= 0xffff
        return

    @staticmethod
    def CLC(cpu, _):
        """
        clear carry flag
        """
        cpu.C = 0
        return

    @staticmethod
    def CLD(cpu, _):
        """
        clear decimal mode
        """
        cpu.D = 0
        return

    @staticmethod
    def CLI(cpu, _):
        """
        clear interrupt disable
        """
        cpu.I = 0
        return

    @staticmethod
    def CLV(cpu, _):
        """
        clear overflow flag
        """
        cpu.V = 0
        return

    @staticmethod
    def CMP(cpu, param):
        """
        Compare Accumulator
        flags affected: C Z N
        """
        if param is None:
            ## Immediate address
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        result = cpu.accumulator - value

        if not result & 0xff:
            cpu.C = 1
            cpu.Z = 1
        elif result > 0:
            cpu.C = 1
            cpu.Z = 0
        else:
            cpu.C = 0
            cpu.Z = 0

        cpu.N = (result >> 7) & 1
        return

    @staticmethod
    def CPX(cpu, param):
        """
        compare Index Register X
        flags affected: Z C N
        ---
        param would be None for immediate addressing mode
        """
        ## If param is not None, fetch value assuming immediate addressing mode
        if param is None:
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        result = cpu.index_x - value

        # if not result & 0xff:
        #     cpu.Z = 1
        #     cpu.c = 1
        # elif result > 0:
        #     cpu.C = 1
        # # else:
        # #     cpu.C = 0
        # #     cpu.Z = 0
        cpu.C = int(result >= 0)
        cpu.Z = int(result == 0)
        cpu.N = (result >> 7) & 1
        return

    @staticmethod
    def CPY(cpu, param):
        """
        compare Index Register Y
        flags affected: Z C N
        """
        ## If param is None, fetch value assuming immediate addressing mode
        if param is None:
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        result = cpu.index_y - value

        cpu.C = int(result >= 0)
        cpu.Z = int(result == 0)
        cpu.N = (result >> 7) & 1
        return

    @staticmethod
    def DEC(cpu, param):
        """
        decrement memory
        flags affected: Z N
        """
        value = (cpu.read_memory(param) - 1) & 0xff
        cpu.write_memory(param, value)

        cpu.Z = int(value == 0)
        cpu.N = (value >> 7) & 1
        return

    @staticmethod
    def DEX(cpu, _):
        """
        decrement Index Register X
        flags affected: Z N
        """
        cpu.index_x -= 1
        cpu.index_x &= 0xff
        # if not cpu.index_x:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def DEY(cpu, _):
        """
        decrement Index Register Y
        flags affected Z N
        """
        cpu.index_y-= 1
        cpu.index_y &= 0xff

        cpu.Z = int(cpu.index_y == 0)
        cpu.N = (cpu.index_y >> 7) & 1
        return

    @staticmethod
    def EOR(cpu, param):
        """
        XOR with accumulator and memory value (bit by bit)
        flags affected: Z N
        """
        ## If param is None, fetch value assuming immediate addressing mode
        if param is None:
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        cpu.accumulator = cpu.accumulator ^ value

        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def INC(cpu, param):
        """
        increment memory
        flags affected: Z N
        """
        value = cpu.read_memory(param)
        value += 1
        value &= 0xff

        cpu.write_memory(param, value)
        # if not param:
        #     cpu.Z = 1
        cpu.Z = int(value == 0)
        cpu.N = (value >> 7) & 1
        return ## to save to the memory location

    @staticmethod
    def INX(cpu, _):
        """
        increment Index Register X
        flags affected: Z N
        """
        cpu.index_x += 1
        cpu.index_x &= 0xff
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def INY(cpu, _):
        """
        increment Index Register Y
        flags affected: Z N
        """
        cpu.index_y += 1
        cpu.index_y &= 0xff
        cpu.Z = int(cpu.index_y == 0)
        cpu.N = (cpu.index_y >> 7) & 1
        return

    @staticmethod
    def JMP(cpu, param):
        """
        Jump to {operand}
        """
        cpu.program_counter = param
        return

    @staticmethod
    def JSR(cpu, param):
        """
        Jump to Subroutine
        """
        high_byte, low_byte = split_bytes(cpu.program_counter - 1)
        cpu.push_stack(high_byte)
        cpu.push_stack(low_byte)
        cpu.program_counter = param
        return

    @staticmethod
    def LDA(cpu, param):
        """
        Load Accumulator
        flags affected: Z N
        """
        if param is None:
            # Immediate address
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        cpu.accumulator = value
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def LDX(cpu, param):
        """
        Load Index Register X
        flags affected: Z N
        """
        if param is None:
            # Immediate address
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        cpu.index_x = value
        # if not cpu.index_x:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def LDY(cpu, param):
        """
        Load Index Register Y
        flags affected: Z N
        """
        ## If param is None, fetch value assuming immediate addressing mode
        if param is None:
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        cpu.index_y = value
        # if not cpu.index_y:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_y == 0)
        cpu.N = (cpu.index_y >> 7) & 1
        return

    @staticmethod
    def LSR(cpu, param):
        """
        Logical Shift Right
        flags affecte: C Z N
        """
        if param is None:
            ## accumulator is used
            cpu.C = cpu.accumulator & 1
            cpu.accumulator >>= 1
            # if not cpu.accumulator:
            #     cpu.Z = 1
            cpu.Z = int(cpu.accumulator == 0)
            cpu.N = (cpu.accumulator >> 7) & 1
        else:
            value = cpu.read_memory(param)
            cpu.C = value & 1
            value >>= 1
            # if not param:
            #     cpu.Z = 1
            cpu.Z = int(value == 0)
            cpu.N = (value >> 7) & 1

            cpu.write_memory(param, value)
        return

    @staticmethod
    def NOP(cpu, _):
        """
        No Operation
        """
        return

    @staticmethod
    def ORA(cpu, param):
        """
        Logical Inclusive OR
        flags affected: Z N
        """
        if param is None:
            # Immediate address
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        cpu.accumulator |= value
        cpu.accumulator &= 0xff
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def PHA(cpu, _):
        """
        Push Accumulator
        """
        cpu.push_stack(cpu.accumulator)
        return

    @staticmethod
    def PHP(cpu, _):
        """
        Push Processor Status to Stack
        """
        temp_b = cpu.B
        cpu.B = 1
        processor_status = cpu.status_reg_to_int()
        cpu.push_stack(processor_status)
        cpu.B = temp_b
        return

    @staticmethod
    def PLA(cpu, _):
        """
        Pull Accumulator
        flags affected: Z N
        """
        cpu.accumulator = cpu.pull_stack()
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def PLP(cpu, _):
        """
        Pull Processor Status Register from stack
        """
        flags = cpu.pull_stack()
        cpu.int_to_status_reg(flags)
        cpu.B = 0
        return

    @staticmethod
    def ROL(cpu, param):
        """
        Rotate Left
        flags affected: C Z N
        """
        temp_c = cpu.C
        if param is None:
            cpu.C = (cpu.accumulator >> 7) & 1
            cpu.accumulator = ((cpu.accumulator << 1) | temp_c) & 0xff
            cpu.Z = int(cpu.accumulator == 0)
            cpu.N = (cpu.accumulator >> 7) & 1
        else:
            value = cpu.read_memory(param)

            cpu.C = (value >> 7) & 1
            value = (value << 1) | temp_c
            value &= 0xff
            cpu.N = (value >> 7) & 1
            cpu.Z = int(value == 0)

            cpu.write_memory(param, value)
        return

    @staticmethod
    def ROR(cpu, param):
        """
        Rotate Right
        flags affected: C Z N
        """
        temp_c = cpu.C

        if param is None:
            cpu.C = cpu.accumulator & 1
            cpu.accumulator = (cpu.accumulator >> 1) |  (temp_c << 7)
            cpu.Z = int(cpu.accumulator == 0)
            cpu.N = (cpu.accumulator >> 7) & 1
        else:
            value = cpu.read_memory(param)
            cpu.C = value & 1
            value = (value >> 1) | (temp_c << 7)
            cpu.Z = int(value == 0)
            cpu.N = (value >> 7) & 1
            cpu.write_memory(param, value)
        return

    @staticmethod
    def RTI(cpu, _):
        """
        Return From Interrupt
        """
        ## pull processor status
        Instructions.PLP(cpu, _)


        ## pull program-counter
        low_byte = cpu.pull_stack()
        high_byte = cpu.pull_stack()
        cpu.program_counter = merge_bytes(high_byte, low_byte)
        return

    @staticmethod
    def RTS(cpu, _):
        """
        Return from subroutine
        """
        low_byte = cpu.pull_stack()
        high_byte = cpu.pull_stack()
        #cpu.program_counter = high_byte*(0xff + 1) + low_byte + 1 ## note: +1
        cpu.program_counter = merge_bytes(high_byte, low_byte) + 1  ## note: +1
        return

    @staticmethod
    def SBC(cpu, param):
        """
        Subtract with Carry
        flags affected: C Z N
        """
        ## If param is None, fetch value assuming immediate addressing mode
        if param is None:
            value = cpu.read_program_counter()
            cpu.program_counter += 1
            cpu.program_counter &= 0xffff
        else:
            value = cpu.read_memory(param)

        temp = cpu.accumulator - value - (1 - cpu.C) ## 1-cpu.c to get a NOT of C

        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.C = 1 if (temp >= 0) else 0 ## Followed https://www.pagetable.com/c64ref/6502/?tab=2#SBC
        cpu.V = int(((cpu.accumulator ^ value) & (cpu.accumulator ^ (temp & 0xff))) & 0x80 != 0)

        cpu.accumulator = temp & 0xff

        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def SEC(cpu, _):
        """
        Set Carry Flag
        """
        cpu.C = 1
        return

    @staticmethod
    def SED(cpu, _):
        """
        set decimal flag
        """
        cpu.D = 1
        return

    @staticmethod
    def SEI(cpu, _):
        """
        set interrupt disable
        """
        cpu.I = 1
        return

    @staticmethod
    def STA(cpu, param):
        """
        store accumulator
        """
        cpu.write_memory(param, cpu.accumulator)
        return

    @staticmethod
    def STX(cpu, param):
        """
        Store Index Register X
        """
        cpu.write_memory(param, cpu.index_x)
        return

    @staticmethod
    def STY(cpu, param):
        """
        store Index Register Y
        """
        cpu.write_memory(param, cpu.index_y)
        return

    @staticmethod
    def TAX(cpu, _):
        """
        Transfer Accumulator to Index Register X
        flags affected: Z N
        """
        cpu.index_x = cpu.accumulator
        # if not cpu.index_x:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def TAY(cpu, _):
        """
        Transfer Accumulator to Index Register Y
        flags affected: Z N
        """
        cpu.index_y = cpu.accumulator
        # if not cpu.index_y:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_y == 0)
        cpu.N = (cpu.index_y >> 7) & 1
        return

    @staticmethod
    def TSX(cpu, _):
        """
        Transfer Stack Pointer to Index Register X
        flags affected: Z N
        """
        cpu.index_x = cpu.stack_pointer
        # if not cpu.index_x:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def TXA(cpu, _):
        """
        Transfer Index Register X to A
        flags affected: Z N
        """
        cpu.accumulator = cpu.index_x
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def TXS(cpu, _):
        """
        Transfer Index Register X to Stack Pointer
        """
        cpu.stack_pointer = cpu.index_x
        return

    @staticmethod
    def TYA(cpu, _):
        """
        Transfer Index Register Y to Accumulator
        flags affected: Z N
        """
        cpu.accumulator = cpu.index_y
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return




























        



