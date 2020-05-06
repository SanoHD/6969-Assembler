import sys, shlex

memory = []
pointer = {}  # {name:line}
commentsymbol = ";"
filename = sys.argv[1]

# Define String, Integer and Float
DFS = ""
DFI = 0
DFF = 0

def error(txt):
    print("[6969]", txt)
    sys.exit()

def lexer(y):
    return shlex.split(y)

def getvar(v):
    if v == "%s":
        return DFS
    elif v == "%i":
        return DFI
    elif v == "%f":
        return DFF

    if v[:3] == "M*[" and v[-1] == "]":
        return memory[int(v[3:-1])]
    else:
        return v


def parser(_line):
    global memory, DFS, DFI, DFF
    line = lexer(_line)
    c = line[0]
    if c == "DFS":
        DFS = _line[4:]
    elif c == "DFI":
        DFS = int(_line[4:])
    elif c == "DFF":
        DFS = float(_line[4:])
    elif c == "MOV":
        do, var = line[1].split("::")
        if do == "C*":
            # Console output
            print(getvar(var),end="")
        elif do[:3] == "M*[" and do[-1] == "]":
            # ValueError + IndexError
            memory[int(do[3:-1])] = getvar(var)
        else:
            error("Invalid MOV operator: "+str(do))
    elif c == "LOG":
        if line[1] == "M*[*]":
            print(memory)
        elif line[1][:3] == "M*[" and line[1][-1] == "]":
            print(memory[int(line[1][3:-1])])
    elif c == "MEM":
        memory = [""]*int(line[1])
    
    elif c == "ADD":

with open(filename) as codefile:
    code = codefile.read().split("\n")

LN = 0
while True:
    try:
        line = code[LN]
    except:
        break

    LN += 1
    if line != "" and line[0] != commentsymbol:
        parser(line)
    else:
        continue
