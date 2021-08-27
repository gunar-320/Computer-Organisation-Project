import semantics
import opcode


def validName(string):

    st = string.split("_")

    for w in st:
        if not w.isalnum():
            return False

    return True


def gen_F(inst):

    unused = "0" * 11
    binry = opcode.opcode["F"][inst[0]]
    binry += unused
    return binry


def gen_E(inst, label):
    unused = "0" * 3
    binry = opcode.opcode["E"][inst[0]]
    binry += unused
    binry += label[inst[1]]
    return binry


def gen_D(inst, var):
    binry = opcode.opcode["D"][inst[0]]
    binry += opcode.register[inst[1]]
    binry += var[inst[2]]
    return binry


def gen_C(inst):
    unused = "0" * 5
    binry = opcode.opcode["C"][inst[0]]
    binry += unused
    binry += opcode.register[inst[1]]
    binry += opcode.register[inst[2]]
    return binry


def decToBin(n, num = 8):
    nBin = bin(n).replace("0b", "")
    con = "0" * (num-len(nBin)) + nBin
    return con


def gen_B(inst):

    binry = opcode.opcode["B"][inst[0]]
    binry += opcode.register[inst[1]]
    imm = int(inst[2][1:])
    binry += decToBin(imm)
    return binry


def gen_A(inst):
    unused = "00"
    binry = opcode.opcode["A"][inst[0]]
    binry += unused
    binry += opcode.register[inst[1]]
    binry += opcode.register[inst[2]]
    binry += opcode.register[inst[3]]
    return binry


def binary(inst, var, label):

    machine_code = ""

    if len(inst) == 1:
        machine_code = gen_F(inst)

    elif len(inst) == 2:
        machine_code = gen_E(inst, label)

    elif len(inst) == 3:

        if inst[1] in semantics.registers[0:-1]:

            if inst[0] in semantics.opcode_dic["B"] and inst[2][0] == "$" and inst[2][1:].isdigit():
                machine_code = gen_B(inst)

            elif inst[0] in semantics.opcode_dic["C"] and inst[2] in semantics.registers:
                machine_code = gen_C(inst)

            elif inst[0] in semantics.opcode_dic["D"] and validName(inst[2]):
                machine_code = gen_D(inst, var)

    elif len(inst) == 4:
        machine_code = gen_A(inst)

    return machine_code


if __name__ == "__main__":
    while True:

        instruction = input().split()

        variables = {}
        labels = {}

        code = binary(instruction, variables, labels)

        print(code)

        if instruction[0] == "hlt":
            break
