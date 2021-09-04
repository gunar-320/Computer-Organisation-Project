import matplotlib.pyplot as plt

mem_addr = []
cycle = []
cyc = 0


MEM = ["0"*16]*256
PC = 0
RF = [0]*8


def RF_dump():
    global PC
    print(format(PC, "08b"), format(RF[0], "016b"), format(RF[1], "016b"), format(RF[2], "016b"), format(RF[3], "016b"), format(RF[4], "016b"), format(RF[5], "016b"), format(RF[6], "016b"), format(RF[7], "016b"))


def MEM_dump():
    for mem in MEM:
        print(mem)


def plot(cycle, mem_addr):
    plt.scatter(cycle, mem_addr)
    plt.xlabel("Cycle Number")
    plt.ylabel("Memory Address")
    plt.title("Scatter Plot")
    plt.show()


def do_add(ins):

    val = RF[int(ins[3:6], 2)] + RF[int(ins[6:], 2)]
    binary = bin(val)[2:]

    if len(binary) > 16:
        RF[int(ins[:3], 2)] = int(binary[- 16:], 2)
        RF[7] = 8

    else:
        RF[int(ins[:3], 2)] = val
        RF[7] = 0


def do_sub(ins):

    val = RF[int(ins[3:6], 2)] - RF[int(ins[6:], 2)]

    if val < 0:
        RF[int(ins[:3], 2)] = 0
        RF[7] = 8

    else:
        RF[int(ins[:3], 2)] = val
        RF[7] = 0


def do_mul(ins):

    val = RF[int(ins[3:6], 2)] * RF[int(ins[6:], 2)]
    binary = bin(val)[2:]

    if len(binary) > 16:
        RF[int(ins[:3], 2)] = int(binary[- 16:], 2)
        RF[7] = 8

    else:
        RF[int(ins[:3], 2)] = val
        RF[7] = 0


def do_xor(ins):

    RF[int(ins[:3], 2)] = RF[int(ins[3:6], 2)] ^ RF[int(ins[6:], 2)]
    RF[7] = 0


def do_or(ins):

    RF[int(ins[:3], 2)] = RF[int(ins[3:6], 2)] | RF[int(ins[6:], 2)]
    RF[7] = 0


def do_and(ins):

    RF[int(ins[:3], 2)] = RF[int(ins[3:6], 2)] & RF[int(ins[6:], 2)]
    RF[7] = 0


# B
def do_mov_imm(ins):

    RF[int(ins[:3], 2)] = int(ins[3:], 2)
    RF[7] = 0


def do_rs(ins):

    shift = int(ins[3:], 2)
    val = "0" * shift + format(RF[int(ins[:3], 2)], "016b")
    RF[int(ins[:3], 2)] = int(val[: - shift], 2)
    RF[7] = 0


def do_ls(ins):

    shift = int(ins[3:], 2)
    val = format(RF[int(ins[:3], 2)], "016b") + "0" * shift
    RF[int(ins[:3], 2)] = int(val[len(val) - 16:], 2)
    RF[7] = 0


# C
def do_mov_reg(ins):

    RF[int(ins[:3], 2)] = RF[int(ins[3:6], 2)]
    RF[7] = 0


def do_div(ins):

    RF[0] = (RF[int(ins[:3], 2)]) // (RF[int(ins[3:], 2)])
    RF[1] = (RF[int(ins[:3], 2)]) % (RF[int(ins[3:], 2)])
    RF[7] = 0


def do_not(ins):

    RF[int(ins[:3], 2)] = 65535 - RF[int(ins[3:6], 2)]
    RF[7] = 0


def do_cmp(ins):

    if RF[int(ins[:3], 2)] == RF[int(ins[3:6], 2)]:
        RF[7] = 1
    elif RF[int(ins[:3], 2)] > RF[int(ins[3:6], 2)]:
        RF[7] = 2
    else:
        RF[7] = 4


# D
def do_ld(ins):

    global cyc
    cycle.append(cyc)
    mem_addr.append(int(MEM[int(ins[3:], 2)], 2))

    RF[int(ins[:3], 2)] = int(MEM[int(ins[3:], 2)], 2)
    RF[7] = 0


# st R1 x
def do_st(ins):

    global cyc
    cycle.append(cyc)
    mem_addr.append(int(ins[3:], 2))

    MEM[int(ins[3:], 2)] = format(RF[int(ins[:3], 2)], '016b')
    RF[7] = 0


# E  0000 0000
def do_jmp(ins):

    global PC

    val = int(ins, 2)
    RF[7] = 0
    RF_dump()

    PC = val


def do_jlt(ins):

    global PC

    if RF[7] == 4:
        RF[7] = 0
        val = int(ins, 2)
        RF_dump()

        PC = val
    else:
        RF[7] = 0
        RF_dump()

        PC += 1


def do_jgt(ins):

    global PC

    if RF[7] == 2:
        RF[7] = 0
        val = int(ins, 2)
        RF_dump()

        PC = val
    else:
        RF[7] = 0
        RF_dump()

        PC += 1


def do_je(ins):

    global PC

    if RF[7] == 1:
        RF[7] = 0
        val = int(ins, 2)
        RF_dump()

        PC = val
    else:
        RF[7] = 0
        RF_dump()

        PC += 1


def main():
    global PC
    global cyc

    count = 0
    while True:
        try:
            line = input()
            if len(line.split()) > 0:
                MEM[count] = line
                count += 1

        except EOFError:
            break

    while True:

        mem_addr.append(PC)
        cycle.append(cyc)

        inst = MEM[PC]
        opcode = inst[:5]

        # halt
        if opcode == "10011":
            #Added a change in Simulator File Here
            RF[7]=0
            RF_dump()
            PC += 1
            break
# A
        # add
        elif opcode == "00000":
            do_add(inst[7:])
            RF_dump()
            PC += 1

        # sub
        elif opcode == "00001":
            do_sub(inst[7:])
            RF_dump()
            PC += 1

        # mul
        elif opcode == "00110":
            do_mul(inst[7:])
            RF_dump()
            PC += 1

        # xor
        elif opcode == "01010":
            do_xor(inst[7:])
            RF_dump()
            PC += 1

        # or
        elif opcode == "01011":
            do_or(inst[7:])
            RF_dump()
            PC += 1

        # and
        elif opcode == "01100":
            do_and(inst[7:])
            RF_dump()
            PC += 1

# B
        # mov(imm)
        elif opcode == "00010":
            do_mov_imm(inst[5:])
            RF_dump()
            PC += 1

        # rs
        elif opcode == "01000":
            do_rs(inst[5:])
            RF_dump()
            PC += 1

        # ls
        elif opcode == "01001":
            do_ls(inst[5:])
            RF_dump()
            PC += 1
# C
        # mov(reg)
        elif opcode == "00011":
            do_mov_reg(inst[10:])
            RF_dump()
            PC += 1

        # div
        elif opcode == "00111":
            do_div(inst[10:])
            RF_dump()
            PC += 1

        # not
        elif opcode == "01101":
            do_not(inst[10:])
            RF_dump()
            PC += 1

        # cmp
        elif opcode == "01110":
            do_cmp(inst[10:])
            RF_dump()
            PC += 1

# D
        # ld
        elif opcode == "00100":
            do_ld(inst[5:])
            RF_dump()
            PC += 1

        # st
        elif opcode == "00101":
            do_st(inst[5:])
            RF_dump()
            PC += 1

# E
        # jmp
        elif opcode == "01111":
            do_jmp(inst[8:])

        # jlt
        elif opcode == "10000":
            do_jlt(inst[8:])

        # jgt
        elif opcode == "10001":
            do_jgt(inst[8:])

        # je
        elif opcode == "10010":
            do_je(inst[8:])

        cyc += 1

    MEM_dump()

    plot(cycle, mem_addr)


if __name__ == "__main__":
    main()
