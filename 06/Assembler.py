#!/usr/bin/python

import fileinput
import re

##############################################################################
# Static translation tables.
##############################################################################

# "comp" part of C-instruction.
comp = {"0":   "0101010",
        "1":   "0111111",
        "-1":  "0111010",
        "D":   "0001100",
        "A":   "0110000",    "M":   "1110000",
        "!D":  "0001101",
        "!A":  "0110001",    "!M":  "1110001",
        "-D":  "0001111",
        "-A":  "0110011",    "-M":  "1110011",
        "D+1": "0011111",
        "A+1": "0110111",    "M+1": "1110111",
        "D-1": "0001110",
        "A-1": "0110010",    "M-1": "1110010",
        "D+A": "0000010",    "D+M": "1000010",
        "D-A": "0010011",    "D-M": "1010011",
        "A-D": "0000111",    "M-D": "1000111",
        "D&A": "0000000",    "D&M": "1000000",
        "D|A": "0010101",    "D|M": "1010101"}

# "dest" part of C-instruction.
dest = {None:  "000",
        "M":   "001",
        "D":   "010",
        "MD":  "011",
        "A":   "100",
        "AM":  "101",
        "AD":  "110",
        "AMD": "111"}

# "jump" part of C-instruction.
jump = {None:  "000",
        "JGT": "001",
        "JEQ": "010",
        "JGE": "011",
        "JLT": "100",
        "JNE": "101",
        "JLE": "110",
        "JMP": "111"}

# Regexp for symbols.
symbol_re = "[a-zA-Z_.$:][a-zA-Z0-9_.$:]*"

##############################################################################
# First pass: Count instructions and use labels to populate symbol table.
##############################################################################

# The symbol table. Key: Symbol. Value: Address (int). Start with
# the predefined symbols.
symbols = {"SP":        0,
           "LCL":       1,
           "ARG":       2,
           "THIS":      3,
           "THAT":      4,
           "R0":        0, "R1":   1, "R2":   2, "R3":   3,
           "R4":        4, "R5":   5, "R6":   6, "R7":   7,
           "R8":        8, "R9":   9, "R10": 10, "R11": 11,
           "R12":       12, "R13": 13, "R14": 14, "R15": 15,
           "SCREEN": 16384,
           "LBD":    24576}

# The program counter.
pc = 0

# A- and C-instructions.
instructions = []

for line in fileinput.input():
    # Ignore everything from // to end of line.
    line = re.sub("//.*", "", line)

    # Ignore all whitespace.
    line = re.sub("\s+", "", line)

    # Ignore empty lines.
    if line == "": continue

    # Is it a label?
    m = re.match("\((" + symbol_re + ")\)", line)
    if m:
        label = m.group(1)

        # Label has to be new.
        if label in symbols:
            raise Exception("'" + label + "' is already defined.")

        # Bind label to current program counter.
        symbols[label] = pc

    else:
        # It's not a label, so it has to be an A- or C-instruction.
        # Store for translation in seond pass and increase program
        # counter.
        instructions.append(line)
        pc += 1

##############################################################################
# Second pass: Resolve symbols and translate instructions to binary
##############################################################################

# Address of the next variable.
variable = 16

for instruction in instructions:
    # Is it an A-instruction with symbolic address?
    m = re.match("@(" + symbol_re + ")", instruction)
    if m:
        symbol = m.group(1)

        # If symbol not defined yet, it has to be a variable.
        if not symbol in symbols:
            # Allocate new variable.
            symbols[symbol] = variable
            variable += 1

        # Now the symbol is defined.
        address = symbols[symbol]

        # Print as binary.
        print bin(address)[2:].zfill(16)
        continue

    # Is it an A-instruction with constant address?
    m = re.match("@([0-9]+)", instruction)
    if m:
        address = int(m.group(1))

        # Print as binary. No symbol resolution required.
        print bin(address)[2:].zfill(16)
        continue

    # Is it a C-instruction? It has the form "dest=comp;jump"
    # with "dest=" and ";jump" being optional.
    m = re.match("((.+)=)?([^;]+)(;(.+))?", instruction)
    if m:
        # Construct binary representation from the three parts.
        # Lookup will fail with "KeyError" if a part is invalid. 
        print "111%s%s%s" % (comp[m.group(3)],
                             dest[m.group(2)],
                             jump[m.group(5)])
        continue

    # Not A- or C-instruction? Must be something invalid.
    raise Exception("Syntax error: " + instruction)
