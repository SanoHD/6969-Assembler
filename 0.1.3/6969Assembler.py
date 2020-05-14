import sys, shlex
from os import getcwd

memory = []
pointer = {}  # {name:line}
commentsymbol = ";"
filename = sys.argv[1]
path = getcwd()
slash = "\\"  # / on Linux and MacOS

# Define String, Integer and Float
DFS = ""
DFI = 0
DFF = 0

errors = {
    "0": "Unknown error",

    # Parser GetVar
    "p:gv:0": "Unknown error",
    "p:gv:1": "Invalid environment variable",

    # Parser Memory
    "p:mem:1": "Invalid memory slot: Unreachable",
    "p:mem:2": "Invalid memory slot: Only integers allowed",

    # Instruction File Read
    "i:f:r:1": "Invalid variable",
    "i:f:1": "File not found",

    "p:cmp:1": "Invalid operator",

}

"""
MEM 5                Creates 5 Memory slots
DFS my text          Defines %s variable
DFI 42               Defines %i variable
DFF 3.141            Defines %f variable
MOV M*[0]::<var>     Pushes <var> (2,hello,%s,...) to memory slot 0
                       -> M*[X]    Memory with position X
                       -> C*        Output
ADD 1::2             Add data from mem slot 2 to mem slot 1 and safe it in %s
SPT mypoint          Set point at current line number
JPT mypoint          Jump to line number of mypoint -> If ? in pointname -> comparison
"""


def error(errorcode):
    try:
        print("[6969]", errorcode, errors[errorcode])
        sys.exit()
    except KeyError:
        print("[6969] Oh dear! An error-error occurred!")
        sys.exit()


"""
To-Do Errors
- lexer, invalid quotation-marks
- getvar, invalid number in memory
- Check if :: / C* or M* / ...
"""


def lexer(y):
    return shlex.split(y)


def getvar(v):
    v = str(v)
    try:
        if v == "%s":
            return str(DFS).replace("^n", "\n")
        elif v == "%i":
            return int(DFI)
        elif v == "%f":
            return float(DFF)
        elif v == "%?":
            return input()
        elif v[:3] == "M*[" and v[-1] == "]":
            try:
                m = memory[int(v[3:-1])]
                try:
                    return m.replace("^n", "\n")
                except AttributeError:
                    return m

            except IndexError:
                error("p:mem:1")
            except ValueError:
                error("p:mem:2")
        elif v[0] == "*" and v[-1] == "*":
            envvars={
            "path": sys.path,
            }
            try:
                return envvars[v[1:-1]]
            except KeyError:
                error("p:gv:1")

                
        else:
            return v.replace("^n", "\n")
    except:
        error("p:gv:0")


def getpath(filename):
    if slash in filename:
        return filename
    else:
        return path + slash + filename


def getpointer(p):
    try:
        return int(p)
    except ValueError:
        return int(pointer[p])


def parser(_line):
    global memory, DFS, DFI, DFF
    line = lexer(_line)
    c = line[0]

    if c == "DFS":
        DFS = _line[4:]
    elif c == "DFI":
        DFI = int(_line[4:])
    elif c == "DFF":
        DFF = float(_line[4:])

    elif c == "MOV":
        do, var = line[1].split("::")
        if do == "C*":
            # Console output
            print(getvar(var), end="")
        elif do[:3] == "M*[" and do[-1] == "]":
            # ValueError + IndexError
            memory[int(do[3:-1])] = getvar(var)
        else:
            error("Invalid MOV operator: " + str(do))
    elif c == "LOG":
        if line[1] == "M*[*]":
            print(memory)
        elif line[1][:3] == "M*[" and line[1][-1] == "]":
            print(memory[int(line[1][3:-1])])

    elif c == "MEM":
        memory = [""] * int(line[1])

    elif c == "ADD":
        a, b = line[1].split("::")
        DFS = getvar(a) + getvar(b)

    elif c == "FLW":
        src, dest = line[1].split("::")
        try:
            with open(getpath(getvar(dest)), "w+") as file:
                file.write(getvar(src))
        except FileNotFoundError:
            error("i:f:1")

    elif c == "FLR":
        src, dest = line[1].split("::")
        try:
            with open(getpath(getvar(src)), "r") as file:
                fr = file.read()
        except FileNotFoundError:
            error("i:f:1")

        if dest == "%s":
            DFS = fr
        elif dest == "%i" or dest == "%f":
            error("ERROR-TODO")
        elif dest[:3] == "M*[" and dest[-1] == "]":
            memory[int(dest[3:-1])] = fr
        else:
            error("ERROR-TODO")

    elif c == "CST":
        DFI = str(getvar(line[1]))
    elif c == "CIN":
        DFI = int(getvar(line[1]))
    elif c == "CFL":
        DFI = float(getvar(line[1]))

    elif c == "MAD":  # Math add
        DFF += float(line[1])
    elif c == "MSB":  # Math subtract
        DFF -= float(line[1])
    elif c == "MML":  # Math multiply
        DFF *= float(line[1])
    elif c == "MDV":  # Math divide
        DFF /= float(line[1])

    elif c == "CUT":
        DFS = DFS[int(line[1].split("/")[0]):line[1].split("/")[1]]

    elif c == "JMP":  # Jump
        # Use [JMP ()] to jump back. (like a function)
        if line[1][0] == "?":
            if DFI == 1:
                return getpointer(line[1][1:])
        else:
            return getpointer(line[1])

    elif c == "CMP":
        DFI = 0
        if "=" in line[1]:
            if getvar(line[1].split("=")[0]) == getvar(line[1].split("=")[1]): DFI = 1
        elif ">" in line[1]:
            if getvar(line[1].split(">")[0]) == getvar(line[1].split(">")[1]): DFI = 1
        elif "<" in line[1]:
            if getvar(line[1].split("<")[0]) == getvar(line[1].split("<")[1]): DFI = 1
        else:
            error("p:cmp:1")

with open(filename) as codefile:
    code = codefile.read().split("\n")

LN = 0
for line in code:
    LN += 1
    lline = lexer(line)
    if line != "" and line[0] != ";" and lline[0] == "PNT":  # Pointer
        pointer[lline[1]] = LN + 1

LN = 0
while True:
    try:
        line = code[LN]
    except:
        break
    if line != "" and line[0] != ";":
        while line[0] == " " or line[0] == "\t":
            line = line[1:]

    LN += 1
    if line != "" and line[0] != commentsymbol:
        if commentsymbol in line:
            line = line.split(commentsymbol)[0]
        jmp = parser(line)
        if jmp == None:
            continue
        LN = jmp - 1
    else:
        continue
