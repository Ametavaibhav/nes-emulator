"""
# Relevant Links
1. http://www.6502.org/users/obelisk/6502/reference.html#ADC
2. http://www.6502.org/tutorials/6502opcodes.html#ADC
3. https://www.masswerk.at/6502/6502_instruction_set.html#ADC
4. https://tutorial-6502.sourceforge.io/specification/opcodes/#sorted-by-hex-code
"""
from instructions.helpers import merge_bytes, split_bytes

class Instructions:
    @staticmethod
    def ADC(cpu, param):
        """
        add memory to accumulator with query
        affected-flag: N V Z C
        """
        ## setting zero flag
        temp = cpu.accumulator + param + cpu.C
        cpu.accumulator = temp & 0xff
        cpu.Z = int(cpu.accumulator == 0) ## converting to int necessary? all the checks would work anyway...
        cpu.C = int(temp > 0xff)
        cpu.V = int((~(cpu.accumulator ^ param) & (cpu.accumulator ^ temp)) != 0)
        cpu.N = int((cpu.accumulator & (1 << 7)) != 0)
        return

    @staticmethod
    def AND(cpu, param):
        """
        bitwise AND with accumulator
        affects flags: N Z
        """
        cpu.accumulator = cpu.accumulator & param
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = int((cpu.accumulator & (1 << 7)) != 0)
        return

    @staticmethod
    def ASL(cpu, param):
        """
        Arithmetic Shift Left
        affected flags: C Z N
        """
        ## DONE: check this again!! does it work? what else can be done to identify accumulator vs memory operation
        if param is None:
            cpu.C = int((cpu.accumulator & 1 << 7) != 0)
            cpu.accumulator = (cpu.accumulator << 1) & 0xff
            cpu.Z = int(cpu.accumulator == 0)
            cpu.N = (cpu.accumulator >> 7) & 1
        else:
            cpu.C = int((cpu.param & 1 << 7) != 0)
            shifted = (param << 1) & 0xff
            cpu.Z = int(shifted == 0)
            cpu.N = (shifted >> 7) & 1
            return shifted
        return

    @staticmethod
    def BCC(cpu, param):
        """
        branch if carry clear.
        affected flags:
        """
        if not cpu.C:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BCS(cpu, param):
        """
        branch if carry set
        """
        if cpu.C:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BEQ(cpu, param):
        """
        branch if equal
        """
        if cpu.Z:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BIT(cpu, param):
        """
        test BITs
        affects flags: N V Z
        """
        temp = cpu.accumulator & param

        cpu.Z = int(temp == 0)
        cpu.N = (param >> 7) & 1
        cpu.V = (cpu.accumulator >> 6) & 1
        return

    @staticmethod
    def BMI(cpu, param):
        """
        branch if minus
        """
        if cpu.N:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BNE(cpu, param):
        """
        branch if not equal
        """
        if not cpu.Z:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BPL(cpu, param):
        """
        branch if positive
        """
        if not cpu.N:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BRK(cpu):
        """
        force interrupt
        """
        cpu.program_counter += 1
        ## push program counter to the stack
        cpu.push_stack(cpu.program_counter // (0xff + 1)) ## high byte
        cpu.push_stack(cpu.program_counter % (0xff + 1)) ## low byte

        ## push processor status to stack
        ## DONE: can it be done with ## PHP(cpu) instead?
        Instructions.PHP(cpu)
        # processor_status = cpu.status_reg_to_int()
        # cpu.push_stack(processor_status)

        ## set interrupt disable flag | NOTE: have conflicting information on which flags to set
        cpu.I = 1
        cpu.B = 1 ## unsure which flags need to be set

        ## load ISR (interrupt service routine) address
        low_byte = cpu.read_memory(0xfffe)
        high_byte = cpu.read_memory(0xffff)
        cpu.program_counter = merge_bytes(high_byte, low_byte)
        return

    @staticmethod
    def BVC(cpu, param):
        """
        branch if overflow clear
        """
        if not cpu.V:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def BVS(cpu, param):
        """
        branch if overflow set
        """
        if cpu.V:
            ## param = param if param < 0x80 else param - 0x100
            cpu.program_counter += param
        return

    @staticmethod
    def CLC(cpu):
        """
        clear carry flag
        """
        cpu.C = 0
        return

    @staticmethod
    def CLD(cpu):
        """
        clear decimal mode
        """
        cpu.D = 0
        return

    @staticmethod
    def CLI(cpu):
        """
        clear interrupt disable
        """
        cpu.I = 0
        return

    @staticmethod
    def CLV(cpu):
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
        result = cpu.accumulator - param

        if not result:
            cpu.C = 1
            cpu.Z = 1
        elif result > 0:
            cpu.Z = 1

        cpu.N = (result >> 7) & 1
        return

    @staticmethod
    def CPX(cpu, param):
        """
        compare Index Register X
        flags affected: Z C N
        """
        result = cpu.index_x - param

        if not result:
            cpu.C = 1
            cpu.Z = 1
        elif result > 0:
            cpu.Z = 1

        cpu.N = (result >> 7) & 1
        return

    @staticmethod
    def CPY(cpu, param):
        """
        compare Index Register Y
        flags affected: Z C N
        """
        result = cpu.index_y - param

        if not result:
            cpu.C = 1
            cpu.Z = 1
        elif result > 0:
            cpu.Z = 1

        cpu.N = (result >> 7) & 1
        return

    @staticmethod
    def DEC(cpu, param):
        """
        decrement memory
        flags affected: Z N
        """
        param-= 1

        cpu.Z = int(param == 0)
        cpu.N = (param >> 7) & 1
        return param

    @staticmethod
    def DEX(cpu):
        """
        decrement Index Register X
        flags affected: Z N
        """
        cpu.index_x -= 1
        # if not cpu.index_x:
        #     cpu.Z = 1
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def DEY(cpu):
        """
        decrement Index Register Y
        flags affected Z N
        """
        cpu.index_y-= 1
        cpu.Z = int(cpu.index_y == 0)
        cpu.N = (cpu.index_y >> 7) & 1
        return

    @staticmethod
    def EOR(cpu, param):
        """
        XOR with accumulator and memory value (bit by bit)
        flags affected: Z N
        """
        cpu.accumulator = cpu.accumulator ^ param
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
        param += 1
        # if not param:
        #     cpu.Z = 1
        cpu.Z = int(param == 0)
        cpu.N = (param >> 7) & 1
        return param ## to save to the memory location

    @staticmethod
    def INX(cpu):
        """
        increment Index Register X
        flags affected: Z N
        """
        cpu.index_x += 1
        cpu.Z = int(cpu.index_x == 0)
        cpu.N = (cpu.index_x >> 7) & 1
        return

    @staticmethod
    def INY(cpu):
        """
        increment Index Register Y
        flags affected: Z N
        """
        cpu.index_y += 1
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
        high_byte, low_byte = split_bytes(cpu.program_counter + 2)
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
        cpu.accumulator = param
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
        cpu.index_x = param
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
        cpu.index_y = param
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
            cpu.C = param & 1
            param >>= 1
            # if not param:
            #     cpu.Z = 1
            cpu.Z = int(param == 0)
            cpu.N = (param >> 7) & 1
            return param
        return

    @staticmethod
    def NOP(cpu):
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
        cpu.accumulator |= param
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def PHA(cpu):
        """
        Push Accumulator
        """
        cpu.push_stack(cpu.accumulator)
        return

    @staticmethod
    def PHP(cpu):
        """
        Push Processor Status to Stack
        """
        processor_status = cpu.status_reg_to_int()
        cpu.push_stack(processor_status)
        return

    @staticmethod
    def PLA(cpu):
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
    def PLP(cpu):
        """
        Pull Processor Status Register from stack
        """
        flags = cpu.pull_stack()
        cpu.int_to_status_reg(flags)
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
            cpu.accumulator = (cpu.accumulator << 1) | temp_c
            cpu.Z = int(cpu.accumulator == 1)
            cpu.N = (cpu.accumulator >> 7) & 1
        else:
            cpu.C = (param >> 7) & 1
            param = (param << 1) | temp_c
            cpu.N = (param >> 7) & 1
            cpu.Z = int(param == 0)
            return param
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
            cpu.C = param & 1
            param = (param >> 1) | (temp_c << 7)
            cpu.Z = int(param == 0)
            cpu.N = (param >> 7) & 1
            return param
        return

    @staticmethod
    def RTI(cpu):
        """
        Return From Interrupt
        """
        ## pull processor status
        ##Done: use PLP instead? ## PLP(cpu)
        # flags = cpu.pull_stack()
        # cpu.int_to_status_reg(flags)
        Instructions.PLP(cpu)

        ## pull program-counter
        low_byte = cpu.pull_stack()
        high_byte = cpu.pull_stack()
        cpu.program_counter = merge_bytes(high_byte, low_byte)
        return

    @staticmethod
    def RTS(cpu):
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
        cpu.accumulator = temp = cpu.accumulator - param - (1 - cpu.C) ## 1-cpu.c to get a NOT of C
        # if not cpu.accumulator:
        #     cpu.Z = 1
        cpu.Z = int(cpu.accumulator == 0)
        cpu.V = int((~(cpu.accumulator ^ param) & (cpu.accumulator ^ temp)) != 0)
        cpu.N = (cpu.accumulator >> 7) & 1
        return

    @staticmethod
    def SEC(cpu):
        """
        Set Carry Flag
        """
        cpu.C = 1
        return

    @staticmethod
    def SED(cpu):
        """
        set decimal flag
        """
        cpu.D = 1
        return

    @staticmethod
    def SEI(cpu):
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
    def TAX(cpu):
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
    def TAY(cpu):
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
    def TSX(cpu):
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
    def TXA(cpu):
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
    def TXS(cpu):
        """
        Transfer Index Register X to Stack Pointer
        """
        cpu.stack_pointer = cpu.index_x
        return

    @staticmethod
    def TYA(cpu):
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




























        



