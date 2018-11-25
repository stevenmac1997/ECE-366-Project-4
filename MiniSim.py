def hexToBin (line):
    newLine = 0
    for i in range(0, len(line)):
        #print("Line: " + line[len(line) - i -1] + "\t# of chars:"+ str(len(line)))

        if(line[len(line) - i -1] == 'A' or line[len(line) - i -1] == 'a'):
            newLine += 10 * (16 ** i)
        elif(line[len(line) - i -1] == 'B' or line[len(line) - i -1] == 'b'):
            newLine += 11 * (16 ** i)
        elif (line[len(line) - i -1] == 'C' or line[len(line) - i -1] == 'c'):
            newLine += 12 * (16 ** i)
        elif (line[len(line) - i -1] == 'D' or line[len(line) - i -1] == 'd'):
            newLine += 13 * (16 ** i)
        elif (line[len(line) - i -1] == 'E' or line[len(line) - i -1] == 'e'):
            newLine += 14 * (16 ** i)
        elif (line[len(line) - i -1] == 'F' or line[len(line) - i -1] == 'f'):
            newLine += 15 * (16 ** i)
        else:
            newLine += int(line[len(line) - i -1]) * (16**i)
    #print(str(newLine))
    newLine = format(int(newLine), "b")
    return newLine.rjust(32, '0')

def simulate(instr, output):
    DIC = 0 #Dynamic Instruction Count
    Reg = [0, 0, 0, 0, 0, 0, 0, 0] #Registers $0 to $7
    Mem = [0] * 512 #Memory Addresses, each initialized at 0
    PC = 0 #Program Counter
    tot_cyc = 0 #total number of cycles in multicycle
    three_cyc = 0 #counts the three cycle instructions
    four_cyc = 0 #counts the four cycle instructions
    five_cyc = 0 #counts the five cycle instructions
    lw_use = 0 
    compute_brance_compare = 0
    branch_taken_flush = 0    
    finished = False
    while(not(finished)):

            #input()
            line = instr[PC]
            #print(line)
            DIC += 1
            if(line[0:6] == "000000"):
                tot_cyc += 4
                four_cyc += 4
                if(line[26:32] == "100000"):
                  function = "add"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  Reg[rd] = Reg[rs] + Reg[rt]
                  PC += 1
                  print (str(function) + " " + str(rd) + "," + str(rs) + "," + str (rt))
                elif(line[26:32] == "100010"):
                  function = "sub"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  Reg[rd]=Reg[rs]-Reg[rt]
                  PC += 1
                  print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
                elif(line[26:32] == "100110"):
                  function = "xor"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  Reg[rd]=Reg[rs]^Reg[rt]
                  PC += 1
                  print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
                elif(line[26:32] == "101010"):
                  function = "slt"
                  rs = int(line[6:11],2)
                  rt = int(line[11:16],2)
                  rd = int(line[16:21],2)
                  if (Reg[rs] < Reg[rt]):
                       Reg[rd]=1
                  else:
                       Reg[rd]=0
                  PC += 1
                  print (str(function) + " " + str(rd) + "," + str(rs) + "," + str(rt))
            elif(line[0:6] == "001000"):
                function = "addi"
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if(line[16] == "1"):
                    imm = imm - 65536
                #print(imm)
                Reg[rt]=Reg[rs]+imm
                PC +=1
                print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
            elif(line[0:6] == "000100"):
                function = "beq"
                three_cyc += 3
                tot_cyc += 3
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (line[16] == "1"):
                    imm = imm - 65536
                if(Reg[rs] == Reg[rt]):
                    addThis = imm + 1
                else:
                    addThis = 1
                if(addThis != 0):
                    PC += addThis
                else:
                    finished = True
                print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
            elif(line[0:6] == "000101"):
                function = "bne"
                three_cyc += 3
                tot_cyc += 3
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if(line[16] == "1"):
                    imm = imm - 65536
                if (Reg[rs] != Reg[rt]):
                    addThis = imm + 1
                else:
                    addThis = 1
                if (addThis != 0):
                    PC += addThis
                else:
                    finished = True
                print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
            elif(line[0:6] == "100011"):
                function = "lw"
                five_cyc  += 5
                tot_cyc += 5
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (line[16] == "1"):
                    imm = imm - 65536
                imm = imm - 8192 #0x2000
                #imm = imm / 4
                dummyA=0.25
                Reg[rt]=Mem[round(Reg[rs]*dummyA)+imm]
                PC +=1
                print (str(function) + " " + str(rs) + "," + str(rt) + "," + str(imm))
            elif(line[0:6] == "101011"):
                function = "sw"
                four_cyc += 4
                tot_cyc += 4
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (line[16] == "1"):
                    imm = imm - 65536
                imm = imm - 8192 #0x2000
                dummyA=0.25

                Mem[round(Reg[rs]*dummyA)+imm]=Reg[rt]
                PC +=1
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
            print("")
    output.write("Reg: " + str(Reg))
    output.write("\nPC : " + str(PC+1))
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

    #VARIABLES:
    Nlines = 0  # Number of lines
    instr =[] #Instructions will be here

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
