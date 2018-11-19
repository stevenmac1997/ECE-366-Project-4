def hexToBin (line):
    newLine = 0
    for i in range(0, len(line)):
        print("Line: " + line[len(line) - i -1] + "\t# of chars:"+ str(len(line)))

        if(line[len(line) - i -1] == 'A'):
            newLine += 10 * (16 ** i)
        elif(line[len(line) - i -1] == 'B'):
            newLine += 11 * (16 ** i)
        elif (line[len(line) - i -1] == 'C'):
            newLine += 12 * (16 ** i)
        elif (line[len(line) - i -1] == 'D'):
            newLine += 13 * (16 ** i)
        elif (line[len(line) - i -1] == 'E'):
            newLine += 14 * (16 ** i)
        elif (line[len(line) - i -1] == 'F'):
            newLine += 15 * (16 ** i)
        else:
            newLine += int(line[len(line) - i -1]) * (16**i)
    print(str(newLine))
    newLine = format(int(newLine), "b")
    return newLine.rjust(32, '0')


def main():
    print("ECE366 Fall 2018: MIPS Mini Assembler")
    print("\nMembers:")
    print("Francis Paul Amadeo")
    print("Steven Mac\n\n")

   """"
    #START TEST
    var = ["05","AB","AC", "19", "161"]

    for i in range(0,5):
        print (hexToBin(var[i]))
    print("FINISHED")
    #END TEST
    """""

    #VARIABLES:
    Nlines = 0  # Number of lines
    instr =[] #Instructions will be here

    print("Reading in instruction file...")
    inFile = open("i_mem.txt", "r")
    outFile = open("output.txt", "w")

    for line in iFile:
        if (line == "\n"):
            continue
        line = line.replace("\n", "")
        instr.append(hexToBin(line))  # Copy all instruction into a list
        Nlines += 1

    print("...finished reading in instruction file")
    print("\nSimulating...")
    exit()


if __name__ == "__main__":
    main()