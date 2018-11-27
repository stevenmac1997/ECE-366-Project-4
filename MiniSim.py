def hexToBin(line):
    newLine = 0
    for i in range(0, len(line)):
        # print("Line: " + line[len(line) - i -1] + "\t# of chars:"+ str(len(line)))

        if (line[len(line) - i - 1] == 'A' or line[len(line) - i - 1] == 'a'):
            newLine += 10 * (16 ** i)
        elif (line[len(line) - i - 1] == 'B' or line[len(line) - i - 1] == 'b'):
            newLine += 11 * (16 ** i)
        elif (line[len(line) - i - 1] == 'C' or line[len(line) - i - 1] == 'c'):
            newLine += 12 * (16 ** i)
        elif (line[len(line) - i - 1] == 'D' or line[len(line) - i - 1] == 'd'):
            newLine += 13 * (16 ** i)
        elif (line[len(line) - i - 1] == 'E' or line[len(line) - i - 1] == 'e'):
            newLine += 14 * (16 ** i)
        elif (line[len(line) - i - 1] == 'F' or line[len(line) - i - 1] == 'f'):
            newLine += 15 * (16 ** i)
        else:
            newLine += int(line[len(line) - i - 1]) * (16 ** i)
    # print(str(newLine))
    newLine = format(int(newLine), "b")
    return newLine.rjust(32, '0')


def simulate(instr, output):
    DIC = 0  # Dynamic Instruction Count
    Reg = [0, 0, 0, 0, 0, 0, 0, 0]  # Registers $0 to $7
    Mem = [0] * 512  # Memory Addresses, each initialized at 0
    PC = 0  # Program Counter
    tot_cyc = 0  # total number of cycles in multicycle
    three_cyc = 0  # counts the three cycle instructions
    four_cyc = 0  # counts the four cycle instructions
    five_cyc = 0  # counts the five cycle instructions
    tot_cyc2 = 5  # Total Cycles for Pipeline
    rs_check = 0  # Holds previous rs
    rt_check = 0  # holds previous rt
    rd_check = 0  # holds previous rd
    lw_use = 0  # counts lw-use stalls
    compute_branch_compare = 0  # counts compute_brance compares
    branch_taken_flush = 0  # counts branch flushes
    DMHit4W = 0  # Hits for the blocks, with size of 4 words, a total of 2 blocks. 0/1
    DMMiss4W = 0  # Misses for the blocks, with size of 4 words, a total of 2 blocks. 0/1
    DMBlkI4W = ["", ""]  # The tags saved for the blocks, with size of 4 words, a total of 2 blocks. 0/1
    # DM4W2B => 16 bits: T T T T T T T T T T T T T | I | O O
    DMHit2W = 0  # Hits for the blocks, with size of 2 words, a total of 4 blocks. 00/01/10/11
    DMMiss2W = 0  # Misses for the blocks, with size of 2 words, a total of 4 blocks. 00/01/10/11
    DMBlkI2W = ["", "", "", ""] # The tags saved for the blocks, with size of 4 words, a total of 2 blocks. 00/01/10/11
    # DM2W4B => 16 bits: T T T T T T T T T T T T T | I I | O
    currTagDM = " "
    finished = False
    while (not (finished)):

        # input()
        line = instr[PC]
        # print(line)
        DIC += 1
        tot_cyc2 += 1

        if (line[0:6] == "000000"):
            tot_cyc += 4
            four_cyc += 4
            rs = int(line[6:11], 2)
            rt = int(line[11:16], 2)
            rd = int(line[16:21], 2)
            if ((rd_check == rs or rd_check == rt) and function == "lw"):
                lw_use += 1
                tot_cyc2 += 1
            else:
                rs_check = rs
                rt_check = rt
                rd_check = rd
            if (line[26:32] == "100000"):
                function = "add"
                Reg[rd] = Reg[rs] + Reg[rt]
                PC += 1
                print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
                function = "compare"
            elif (line[26:32] == "100010"):
                function = "sub"
                Reg[rd] = Reg[rs] - Reg[rt]
                PC += 1
                print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
                function = "compare"
            elif (line[26:32] == "100110"):
                function = "xor"
                Reg[rd] = Reg[rs] ^ Reg[rt]
                PC += 1
                print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
                function = "compare"
            elif (line[26:32] == "101010"):
                function = "slt"
                if (Reg[rs] < Reg[rt]):
                    Reg[rd] = 1
                else:
                    Reg[rd] = 0
                PC += 1
                print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
                function = "compare"
        elif (line[0:6] == "001000"):
            function = "addi"
            rs = int(line[6:11], 2)
            rt = int(line[11:16], 2)
            imm = int(line[16:32], 2)
            if (line[16] == "1"):
                imm = imm - 65536
            # print(imm)
            Reg[rt] = Reg[rs] + imm
            PC += 1
            print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
            function = "compare"
        elif (line[0:6] == "000100"):
            three_cyc += 3
            tot_cyc += 3
            rs = int(line[6:11], 2)
            rt = int(line[11:16], 2)
            imm = int(line[16:32], 2)
            if (function == "compare" and (rd_check == rs or rd_check == rt)):
                compute_branch_compare += 1
                tot_cyc2 += 1
            else:
                rs_check = rs
                rt_check = rt
            function = "beq"
            if (line[16] == "1"):
                imm = imm - 65536
            if (Reg[rs] == Reg[rt]):
                addThis = imm + 1
                branch_taken_flush += 1
                tot_cyc2 += 1
            else:
                addThis = 1
            if (addThis != 0):
                PC += addThis
            else:
                finished = True
            print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
        elif (line[0:6] == "000101"):

            three_cyc += 3
            tot_cyc += 3
            rs = int(line[6:11], 2)
            rt = int(line[11:16], 2)
            imm = int(line[16:32], 2)
            if (function == "compare" and (rd_check == rs or rd_check == rt)):
                compute_branch_compare += 1
                tot_cyc2 += 1
            else:
                rs_check = rs
                rd_check = rt
            function = "bne"
            if (line[16] == "1"):
                imm = imm - 65536
            if (Reg[rs] != Reg[rt]):
                addThis = imm + 1
                branch_taken_flush += 1
                tot_cyc2 += 1
            else:
                addThis = 1
            if (addThis != 0):
                PC += addThis
            else:
                finished = True
            print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
        elif (line[0:6] == "100011"):
            function = "lw"
            five_cyc += 5
            tot_cyc += 5
            rs = int(line[6:11], 2)
            rt = int(line[11:16], 2)
            imm = int(line[16:32], 2)
            if (line[16] == "1"):
                imm = imm - 65536
            imm = imm - 8192  # 0x2000
            # imm = imm / 4
            addr = int(round(Reg[rs] * 0.25)) + imm
            Reg[rt] = Mem[addr]
            PC += 1
            print(str(addr))
            print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))

            # 3.)
            # A.) DM4W2B => 16 bits: T T T T T T T T T T T T T | I | O O
            # B.) DM2W4B => 16 bits: T T T T T T T T T T T T T | I I | O
            # Add 0x2000 to the address and change it to binary
            if (line[16] == "1"):
                imm += 65536
            print(str(Reg[rs]) + "<- Reg[" + str(rs) + "]\timm ->" + str(imm))
            addr = Reg[rs] + imm + 8192
            print(str(addr))
            addr = format(int(addr), "b")
            addr = "00" + addr
            print(addr)

            # Get the tag from the address
            currTagDM = addr[0:14]

            # A.)
            if (DMBlkI4W[int(addr[14])] == currTagDM):
                DMHit4W += 1
            else:
                DMMiss4W += 1
                DMBlkI4W[int(addr[14])] = currTagDM

            #B.)
            if (DMBlkI2W[int(addr[14:16], 2)] == currTagDM):
                DMHit2W += 1
            else:
                DMMiss2W += 1
                DMBlkI2W[int(addr[14:16], 2)] = currTagDM

        elif (line[0:6] == "101011"):
            function = "sw"
            four_cyc += 4
            tot_cyc += 4
            rs = int(line[6:11], 2)
            rt = int(line[11:16], 2)
            imm = int(line[16:32], 2)
            if (line[16] == "1"):
                imm = imm - 65536
            imm = imm - 8192  # 0x2000
            dummyA = 0.25

            Mem[int(round(Reg[rs] * dummyA)) + imm] = Reg[rt]
            PC += 1
            print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))

    print("\nReg: " + str(Reg))
    print("PC: " + str(PC + 1))
    print("DIC: " + str(DIC))
    print("Mem: " + str(Mem))
    print("")
    print("\nMulticycle Simulation Results: ")
    print("Three Cycles: " + str(three_cyc))
    print("Four Cycles: " + str(four_cyc))
    print("Five Cycles: " + str(five_cyc))
    print("Total Cycles: " + str(tot_cyc))
    ###NOT WRITING YET###
    print("\nPipeline Simulation Results: ")
    print("lw-use: " + str(lw_use))
    print("compute-branch compare: " + str(compute_branch_compare))
    print("branch taken flush: " + str(branch_taken_flush))
    print("")
    print("Direct mapped cache, block size of 4 words, a total of 2 blocks:")
    print("HITS:     " + str(DMHit4W))
    print("MISS:     " + str(DMMiss4W))
    print("HIT Rate: " + str(DMHit4W / (DMHit4W + DMMiss4W)))
    print("\nDirect mapped cache, block size of 2 words, a total of 4 blocks:")
    print("HITS:     " + str(DMHit2W))
    print("MISS:     " + str(DMMiss2W))
    print("HIT Rate: " + str(DMHit2W / (DMHit2W + DMMiss2W)))

    output.write("Reg: " + str(Reg))
    output.write("\nPC : " + str(PC + 1))
    output.write("\nDIC: " + str(DIC))
    output.write("\nMulticycle Simulation Results: ")
    output.write("\n# Three Cycles: " + str(three_cyc))
    output.write("\n# Four Cycles: " + str(four_cyc))
    output.write("\n# Five Cycles: " + str(five_cyc))
    output.write("\nTotal Cycles: " + str(tot_cyc))


def main():
    print("ECE366 Fall 2018: MIPS Mini Assembler")
    print("\nMembers:")
    print("Francis Paul Amadeo")
    print("Steven Mac\n\n")

    # VARIABLES:
    Nlines = 0  # Number of lines
    instr = []  # Instructions will be here

    print("Reading in instruction file...")
    inFile = open("i_mem.txt", "r")
    outFile = open("output.txt", "w")

    for line in inFile:
        if (line == "\n"):
            continue
        line = line.replace("\n", "")
        line = line.replace("0x", "")
        instr.append(hexToBin(line))  # Copy all instruction into a list
        Nlines += 1

    print("...finished reading in instruction file")
    print("\nSimulating...")
    simulate(instr, outFile)
    print("\nSimulation done")

    inFile.close()
    outFile.close()

    exit()


if __name__ == "__main__":
    main()
