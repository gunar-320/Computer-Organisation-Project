import semantics
import errormsg


def valid(string):
    st = string.split("_")
    for w in st:
        if not w.isalnum():
            return False

    return True


def typo_Error(inst_list):

    if len(inst_list) == 0:
        return False

    if inst_list[0] in semantics.opcode_list:
        if inst_list[0] == "mov":
            if len(inst_list) == 3:
                if inst_list[1] in semantics.registers:
                    if inst_list[2][0] == '$':
                        return False
                    if inst_list[2] in semantics.registers:
                        return False
                    elif inst_list[2] not in semantics.registers:
                        return True
                else:
                    return True
            else:
                return False

        if inst_list[0] in semantics.opcode_dic["A"]:
            if len(inst_list) == 4:
                if inst_list[1] in semantics.registers and inst_list[2] in semantics.registers and inst_list[3] in semantics.registers:
                    return False
                else:
                    return True
            else:
                return False

        elif inst_list[0] in semantics.opcode_dic["B"]:
            if len(inst_list) == 3:
                if inst_list[1] in semantics.registers:
                    if inst_list[2][0] == "$":
                        return False
                    else:
                        return True
                else:
                    return True
            else:
                return False

        elif inst_list[0] in semantics.opcode_dic["C"]:
            if len(inst_list) == 3:
                if inst_list[1] in semantics.registers and inst_list[2] in semantics.registers:
                    return False
                else:
                    return True

            else:
                return False

        elif inst_list[0] in semantics.opcode_dic["D"]:
            if len(inst_list) == 3:
                if inst_list[1] in semantics.registers:
                    return False
                else:
                    return True

            else:
                return False

        elif inst_list[0] in semantics.opcode_dic["E"]:
            return False

        elif inst_list[0] in semantics.opcode_dic["F"]:
            return False

    else:
        return True


def syntax_error_check(inst_list):
    if len(inst_list) == 0:
        return True
    elif inst_list[0] in semantics.opcode_list:

        if inst_list[0] == "mov":
            if len(inst_list) == 3:
                return False
            else:
                return True
        elif inst_list[0] in semantics.opcode_dic["A"]:
            if len(inst_list) == 4:
                return False
            else:
                return True
        elif inst_list[0] in semantics.opcode_dic["B"]:
            if len(inst_list) == 3:
                return False
            else:
                return True
        elif inst_list[0] in semantics.opcode_dic["C"]:
            if len(inst_list) == 3:
                return False
            else:
                return True
        elif inst_list[0] in semantics.opcode_dic["D"]:
            if len(inst_list) == 3:
                return False
            else:
                return True
        elif inst_list[0] in semantics.opcode_dic["E"]:
            if len(inst_list) == 2:
                return False
            else:
                return True
        elif inst_list[0] in semantics.opcode_dic["F"]:
            if len(inst_list) == 1:
                return False
            else:
                return True

    else:
        return False


def undef_Var(inst_list, var):

    if len(inst_list) == 3:
        if inst_list[0] in semantics.opcode_dic["D"]:
            if inst_list[2] in var.keys():
                return False
            else:
                return True
        else:
            return False
    else:
        return False


def undef_Lab(inst_list, labels):
    if len(inst_list) == 2:
        if inst_list[0] in semantics.opcode_dic["E"]:
            if inst_list[1] in labels.keys():
                return False
            else:
                return True
        else:
            return False
    else:
        return False


def illegal_Flag(inst_list):

    if "FLAGS" in inst_list:
        if inst_list.index("FLAGS") == 2:
            if inst_list[0] == "mov":
                return False
            else:
                return True
        else:
            return True
    else:
        return False

# mov R5 FLAGS


def mis_var_labels(inst_list, var, labels):
    if len(inst_list) == 3:
        if inst_list[0] in semantics.opcode_dic["D"]:
            if inst_list[2] in labels.keys():
                return True
            else:
                return False
        else:
            return False

    elif len(inst_list) == 2:
        if inst_list[0] in semantics.opcode_dic["E"]:
            if inst_list[1] in var.keys():
                return True
            else:
                return False
        else:
            return False
    else:
        return False


def illegal_immediate_value(inst_list):
    if len(inst_list) == 3 and inst_list[0] in semantics.opcode_dic["B"]:
        if inst_list[2] in semantics.registers:
            return False

        if inst_list[2][1:].isdigit() and inst_list[2][0] == "$":
            if int(inst_list[2][1:]) < 0 or int(inst_list[2][1:]) > 255:
                return True
            else:
                return False
        else:
            return True
    else:
        return False


def error_trace(inst_list, var, labels, line):

    a = typo_Error(inst_list)
    if a:
        errormsg.error_note("a", line)
    # print("typo_Error", a)

    b = undef_Var(inst_list, var)
    if b:
        errormsg.error_note("b", line)
    # print("undef_Var", b)

    c = undef_Lab(inst_list, labels)
    if c:
        errormsg.error_note("c", line)
    # print("undef_Lab", c)

    d = illegal_Flag(inst_list)
    if d:
        errormsg.error_note("d", line)
    # print("illegal_Flag", d)

    e = illegal_immediate_value(inst_list)
    if e:
        errormsg.error_note("e", line)
    # print("illegal_immediate_value", e)

    f = mis_var_labels(inst_list, var, labels)
    if f:
        errormsg.error_note("f", line)
    # print("mis_var_labels", f)

    j = syntax_error_check(inst_list)
    if j:
        errormsg.error_note("j", line)
    # print("syntax", j)

    return a or b or c or d or e or f or j


if __name__ == "__main__":
    labls = {"my1label": None, "my_lab": None, "my_1label_loop": None}
    varbs = {"XY": None, "X1_Y": None, "X_Y_Z": None, "XYZ": None}
    while True:
        x = input()
        e1 = typo_Error(x.split())
        print("typo", e1)

        e2 = syntax_error_check(x.split())
        print("syntax", e2)

        e3 = undef_Lab(x.split(), labls)
        print("undef_Lab", e3)

        e4 = undef_Var(x.split(), varbs)
        print("undef_Var", e4)

        e5 = illegal_Flag(x.split())
        print("illegal_Flag", e5)

        e6 = mis_var_labels(x.split(), varbs, labls)
        print("mis_var_labels", e6)

        e7 = illegal_immediate_value(x.split())
        print("illegal_immediate_value", e7)
