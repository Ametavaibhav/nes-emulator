def merge_bytes(high_byte, low_byte):
    ## using bitwise operation
    return (high_byte << 8) | low_byte

def split_bytes(value):
    ## using bitwise operation
    high_byte = (value >> 8) & 0xff
    low_byte =  value & 0xff
    return high_byte, low_byte
