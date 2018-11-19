def hexToBin (line):
    newLine = 0
    for i in (0, len(line)):
        if(line[len(line) - i] == 'A'):
            newLine += 10 * (16 ** i)
        elif(line[len(line) - i] == 'B'):
            newLine += 11 * (16 ** i)
        elif (line[len(line) - i] == 'C'):
            newLine += 12 * (16 ** i)
        elif (line[len(line) - i] == 'D'):
            newLine += 13 * (16 ** i)
        elif (line[len(line) - i] == 'E'):
            newLine += 14 * (16 ** i)
        elif (line[len(line) - i] == 'F'):
            newLine += 15 * (16 ** i)
        else:
            newLine += line[len(line) - i] * (16**i)
    return format(int(newLine), "32b")


def main():
    print("ECE366 Fall 2018: MIPS Mini Assembler")
    print()
    print("Members:")
    print("Francis Paul Amadeo")
    print("Steven Mac\n\n")
    print("Reading in instruction file:")





if __name__ == "__main__":
    main()