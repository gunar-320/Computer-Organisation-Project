import binarygen
import error_gen
import errormsg


def validName(string):

    st = string.split("_")

    for w in st:
        if not w.isalnum():
            return False

    return True


def main():
    inError = []
    errory = False
    prog_count = 0
    halt = False
    var_accept = True
    inst_list = []
    variables = {}
    labels = {}

    while True:

        try:
            inst = input()

        except EOFError:
            break

        else:
            if len(inst) == 0:
                inst_list.append([-1, inst])

            else:
                inst = inst.strip().split()
                if inst[0] == "var":
                    if len(inst) == 1:
                        address = binarygen.decToBin(prog_count, 8)
                        inst_list.append([address, inst])
                        errormsg.error_note("k", len(inst_list))
                        errory = True

                    elif not validName(inst[1]):
                        errormsg.error_note("k", len(inst_list)+1)
                        address = binarygen.decToBin(prog_count, 8)
                        inst_list.append([address, inst])
                        errory = True

                    elif inst[1] in variables:
                        errormsg.error_note("m", len(inst_list)+1)
                        errory = True
                        inst_list.append([-1, inst])
                        continue

                    else:
                        inst_list.append([-1, inst])
                        variables[inst[1]] = None

                elif inst[0][-1] == ":" and validName(inst[0][:-1]):
                    if inst[0][:-1] in labels:
                        inst_list.append([-1, inst])
                        errory = True
                        errormsg.error_note("l", len(inst_list)+1)
                        continue

                    else:
                        address = binarygen.decToBin(prog_count, 8)
                        inst_list.append([address, inst])
                        labels[inst[0][:-1]] = address
                        prog_count += 1

                else:
                    address = binarygen.decToBin(prog_count, 8)
                    inst_list.append([address, inst])
                    prog_count += 1

    for i in range(len(inst_list)-1, -1, -1):
        if len(inst_list[i][1]) != 0:
            inst_list = inst_list[:i+1]
            break

    for i in range(len(inst_list)):
        if len(inst_list[i][1]) != 0:
            if (len(inst_list[i][1]) == 1 and inst_list[i][1][0] == "hlt") or (len(inst_list[i][1]) == 2 and inst_list[i][1][0][:-1] in labels.keys() and inst_list[i][1][1] == "hlt"):
                if halt:
                    errormsg.error_note("n", i+1)
                    errory = True
                    break
                else:
                    halt = True

                    if i != len(inst_list)-1:
                        errormsg.error_note("i", i+1)
                        errory = True

    if not halt:
        errormsg.error_no_halt()
        errory = True

    for i in range(len(inst_list)):

        if len(inst_list[i][1]) != 0 and len(inst_list[i][1]) != 1:
            if inst_list[i][1][0] == "var":
                if var_accept:
                    address = binarygen.decToBin(prog_count, 8)
                    variables[inst_list[i][1][1]] = address
                    prog_count += 1

                else:
                    errormsg.error_note("g", i+1)
                    errory = True

            else:
                var_accept = False

    for i in range(len(inst_list)):

        if inst_list[i][0] != -1:

            if inst_list[i][1][0][:-1] in labels:
                line = inst_list[i][1][1:]
            else:
                line = inst_list[i][1]

            inError.append(error_gen.error_trace(line, variables, labels, (i + 1)))

    if errory or (True in inError):
        return

    for inst in inst_list:
        if inst[0] != -1:

            if inst[1][0][:-1] in labels:
                line = inst[1][1:]
            else:
                line = inst[1]

            machine_code = binarygen.binary(line, variables, labels)
            print(machine_code)


if __name__ == "__main__":
    main()
