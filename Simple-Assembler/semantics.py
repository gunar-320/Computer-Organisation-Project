opcode_list = ["add", "sub", "mul", "xor", "or", "and", "mov", "rs", "ls", "mov", "div", "not", "cmp", "ld", "st", "jmp", "jlt", "jgt", "je", "hlt"]

registers = ["R0", "R1", "R2", "R3", "R4", "R5", "R6", "FLAGS"]

opcode_dic = {
    "A": ["add", "sub", "mul", "xor", "or", "and"],
    "B": ["mov", "rs", "ls"],
    "C": ["mov", "div", "not", "cmp"],
    "D": ["ld", "st"],
    "E": ["jmp", "jlt", "jgt", "je"],
    "F": ["hlt"]
    }
