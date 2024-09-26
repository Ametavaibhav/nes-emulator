from instructions import addressing_modes, instructions

addressingModes = addressing_modes.AddressingModes()
instruct = instructions.Instructions()

OPCODE_TABLE = {
    0x69: (instruct.ADC, addressingModes.immediate),
    0x65: (instruct.ADC, addressingModes.zero_page),
    0x75: (instruct.ADC, addressingModes.zero_page_x),
    0x6D: (instruct.ADC, addressingModes.absolute),
    0x7D: (instruct.ADC, addressingModes.absolute_x),
    0x79: (instruct.ADC, addressingModes.absolute_y),
    0x61: (instruct.ADC, addressingModes.indexed_indirect),
    0x71: (instruct.ADC, addressingModes.indirect_indexed),

    0x29: (instruct.AND, addressingModes.immediate),
    0x25: (instruct.AND, addressingModes.zero_page),
    0x35: (instruct.AND, addressingModes.zero_page_x),
    0x2D: (instruct.AND, addressingModes.absolute),
    0x3D: (instruct.AND, addressingModes.absolute_x),
    0x39: (instruct.AND, addressingModes.absolute_y),
    0x21: (instruct.AND, addressingModes.indexed_indirect),
    0x31: (instruct.AND, addressingModes.indirect_indexed),

    0x0A: (instruct.ASL, addressingModes.implicit),
    0x06: (instruct.ASL, addressingModes.zero_page),
    0x16: (instruct.ASL, addressingModes.zero_page_x),
    0x0E: (instruct.ASL, addressingModes.absolute),
    0x1E: (instruct.ASL, addressingModes.absolute_x),

    0x90: (instruct.BCC, addressingModes.relative),

    0xB0: (instruct.BCS, addressingModes.relative),

    0xF0: (instruct.BEQ, addressingModes.relative),

    0x24: (instruct.BIT, addressingModes.zero_page),
    0x2C: (instruct.BIT, addressingModes.absolute),

    0x30: (instruct.BMI, addressingModes.relative),

    0xD0: (instruct.BNE, addressingModes.relative),

    0x10: (instruct.BPL, addressingModes.relative),

    0x00: (instruct.BRK, addressingModes.implicit),

    0x50: (instruct.BVC, addressingModes.relative),

    0x70: (instruct.BVS, addressingModes.relative),

    0x18: (instruct.CLC, addressingModes.implicit),

    0xD8: (instruct.CLD, addressingModes.implicit),

    0x58: (instruct.CLI, addressingModes.implicit),

    0xB8: (instruct.CLV, addressingModes.implicit),

    0xC9: (instruct.CMP, addressingModes.immediate),
    0xC5: (instruct.CMP, addressingModes.zero_page),
    0xD5: (instruct.CMP, addressingModes.zero_page_x),
    0xCD: (instruct.CMP, addressingModes.absolute),
    0xDD: (instruct.CMP, addressingModes.absolute_x),
    0xD9: (instruct.CMP, addressingModes.absolute_y),
    0xC1: (instruct.CMP, addressingModes.indexed_indirect),
    0xD1: (instruct.CMP, addressingModes.indirect_indexed),

    0xE0: (instruct.CPX, addressingModes.immediate),
    0xE4: (instruct.CPX, addressingModes.zero_page),
    0xEC: (instruct.CPX, addressingModes.absolute),

    0xC0: (instruct.CPY, addressingModes.immediate),
    0xC4: (instruct.CPY, addressingModes.zero_page),
    0xCC: (instruct.CPY, addressingModes.absolute),

    0xC6: (instruct.DEC, addressingModes.zero_page),
    0xD6: (instruct.DEC, addressingModes.zero_page_x),
    0xCE: (instruct.DEC, addressingModes.absolute),
    0xDE: (instruct.DEC, addressingModes.absolute_x),

    0xCA: (instruct.DEX, addressingModes.implicit),

    0x88: (instruct.DEY, addressingModes.implicit),

    0x49: (instruct.EOR, addressingModes.immediate),
    0x45: (instruct.EOR, addressingModes.zero_page),
    0x55: (instruct.EOR, addressingModes.zero_page_x),
    0x4D: (instruct.EOR, addressingModes.absolute),
    0x5D: (instruct.EOR, addressingModes.absolute_x),
    0x59: (instruct.EOR, addressingModes.absolute_y),
    0x41: (instruct.EOR, addressingModes.indexed_indirect),
    0x51: (instruct.EOR, addressingModes.indirect_indexed),

    0xE6: (instruct.INC, addressingModes.zero_page),
    0xF6: (instruct.INC, addressingModes.zero_page_x),
    0xEE: (instruct.INC, addressingModes.absolulte),
    0xFE: (instruct.INC, addressingModes.absolute_x),

    0xE8: (instruct.INX, addressingModes.implicit),

    0xC8: (instruct.INY, addressingModes.implicit),

    0x4C: (instruct.JMP, addressingModes.absolute),
    0x6C: (instruct.INC, addressingModes.indirect),

    0x20: (instruct.JSR, addressingModes.absolute),

    0xA9: (instruct.LDA, addressingModes.immediate),
    0xA5: (instruct.LDA, addressingModes.zerop_page),
    0xB5: (instruct.LDA, addressingModes.zero_page_x),
    0xAD: (instruct.LDA, addressingModes.absolute),
    0xBD: (instruct.LDA, addressingModes.absolute_x),
    0xB9: (instruct.LDA, addressingModes.absolute_y),
    0xA1: (instruct.LDA, addressingModes.indexed_indirect),
    0xB1: (instruct.LDA, addressingModes.indirect_indexed),

    0xA2: (instruct.LDX, addressingModes.immediate),
    0xA6: (instruct.LDX, addressingModes.zero_page),
    0xB6: (instruct.LDX, addressingModes.zero_page_y),
    0xAE: (instruct.LDX, addressingModes.absolute),
    0xBE: (instruct.LDX, addressingModes.absolute_y),

    0xA0: (instruct.LDY, addressingModes.immediate),
    0xA4: (instruct.LDY, addressingModes.zero_page),
    0xB4: (instruct.LDY, addressingModes.zero_page_x),
    0xAC: (instruct.LDY, addressingModes.absolute),
    0xBC: (instruct.LDY, addressingModes.absolute_x),

    0x4A: (instruct.LSR, addressingModes.implicit),
    0x46: (instruct.LSR, addressingModes.zero_page),
    0x56: (instruct.LSR, addressingModes.zero_page_x),
    0x4E: (instruct.LSR, addressingModes.absolute),
    0x5E: (instruct.LSR, addressingModes.absolute_x),

    0xEA: (instruct.NOP, addressingModes.implicit),

    0x09: (instruct.ORA, addressingModes.immediate),
    0x05: (instruct.ORA, addressingModes.zero_page),
    0x15: (instruct.ORA, addressingModes.zero_page_x),
    0x0D: (instruct.ORA, addressingModes.absolute),
    0x1D: (instruct.ORA, addressingModes.absolute_x),
    0x19: (instruct.ORA, addressingModes.absolute_y),
    0x01: (instruct.ORA, addressingModes.indexed_indirect),
    0x11: (instruct.ORA, addressingModes.indirect_indexed),

    0x48: (instruct.PHA, addressingModes.implicit),

    0x08: (instruct.PHP, addressingModes.implicit),

    0x68: (instruct.PLA, addressingModes.implicit),

    0x28: (instruct.PLP, addressingModes.implicit),

    0x2A: (instruct.ROL, addressingModes.implicit),
    0x26: (instruct.ROL, addressingModes.zero_page),
    0x36: (instruct.ROL, addressingModes.zero_page_x),
    0x2E: (instruct.ROL, addressingModes.absolute),
    0x3E: (instruct.ROL, addressingModes.absolute_x),

    0x6A: (instruct.ROR, addressingModes.implicit),
    0x66: (instruct.ROR, addressingModes.zero_page),
    0x76: (instruct.ROR, addressingModes.zero_page_x),
    0x6E: (instruct.ROR, addressingModes.absolute),
    0x7E: (instruct.ROR, addressingModes.absolute_x),

    0x40: (instruct.RTI, addressingModes.implicit),

    0x60: (instruct.RTS, addressingModes.implicit),

    0xE9: (instruct.SRC, addressingModes.immediate),
    0xE5: (instruct.SRC, addressingModes.zero_page),
    0xF5: (instruct.SRC, addressingModes.zero_page_x),
    0xED: (instruct.SRC, addressingModes.absolute),
    0xFD: (instruct.SRC, addressingModes.absolute_x),
    0xF9: (instruct.SRC, addressingModes.absolute_y),
    0xE1: (instruct.SRC, addressingModes.indexed_indirect),
    0xF1: (instruct.SRC, addressingModes.indirect_indexed),

    0x38: (instruct.SEC, addressingModes.implicit),

    0xF8: (instruct.SED, addressingModes.implicit),

    0x78: (instruct.SEI, addressingModes.implicit),

    0x85: (instruct.STA, addressingModes.zero_page),
    0x95: (instruct.STA, addressingModes.zero_page_x),
    0x8D: (instruct.STA, addressingModes.absolute),
    0x9D: (instruct.STA, addressingModes.absolute_x),
    0x99: (instruct.STA, addressingModes.absolute_y),
    0x81: (instruct.STA, addressingModes.indexed_indirect),
    0x91: (instruct.STA, addressingModes.indirect_indexed),

    0x86: (instruct.STX, addressingModes.zero_page),
    0x96: (instruct.STX, addressingModes.zero_page_x),
    0x8E: (instruct.STX, addressingModes.absolute),

    0x84: (instruct.STY, addressingModes.zero_page),
    0x94: (instruct.STY, addressingModes.zero_page_x),
    0x8C: (instruct.STY, addressingModes.absolute),

    0xAA: (instruct.TAX, addressingModes.implicit),

    0xA8: (instruct.TAY, addressingModes.implicit),

    0xBA: (instruct.TSX, addressingModes.implicit),

    0x8A: (instruct.TXA, addressingModes.implicit),

    0x9A: (instruct.TXS, addressingModes.implicit),

    0x98: (instruct.TYA, addressingModes.implicit),
}