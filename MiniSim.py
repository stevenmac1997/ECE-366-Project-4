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
    tot_cyc2 = 5 #Total Cycles for Pipeline
    #rs_check = 0 # Holds previous rs
    #rt_check = 0 # holds previous rt
    rd_check = 0 # holds previous rd
    lw_use = 0  # counts lw-use stalls
    compute_branch_compare = 0 # counts compute_brance compares
    branch_taken_flush = 0 # counts branch flushes
    tot_delay = 0 #Total numbers of delays
    forward = 0 #
    #forward_check_rs = [0,0,0,0,0,0,0] #forward check for rs
    #forward_check_rt = [0,0,0,0,0,0,0] #forward check for rt
    forward_check_rd = [0, 0, 0, 0, 0, 0, 0, 0] #forward check for rd
    forward_check = False # Did a forward occur?
    lu_check = False #Did lw_use occur?
    cbc_check = False # Did compute_Branch_compare occur?
    flush_check = False
    finished = False
    while(not(finished)):

            #input()
            line = instr[PC]
            #print(line)
            DIC += 1
            tot_cyc2 += 1
            if(line[0:6] == "000000"):
                #R-TYPES
                tot_cyc += 4
                four_cyc += 1
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                rd = int(line[16:21],2)
                if (forward_check_rd[rs] == Reg[rs] or forward_check_rd[rt] == Reg[rt]):
                  forward += 1
                  forward_check = True
                else:
                  forward_check = False
                forward_check_rd [rd] = Reg[rd]
                if ((rd_check == rs or rd_check == rt) and function == "lw"):
                  lw_use += 1
                  tot_cyc2 += 1
                  tot_delay += 1
                  lu_check = True
                else:
                  lu_check = False
                rd_check = rd
                if(line[26:32] == "100000"):
                  function = "add"
                  Reg[rd] = Reg[rs] + Reg[rt]
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str (rt))
                  function = "compare"
                elif(line[26:32] == "100010"):
                  function = "sub"
                  Reg[rd]=Reg[rs]-Reg[rt]
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt))
                  function = "compare"
                elif(line[26:32] == "100110"):
                  function = "xor"
                  Reg[rd]=Reg[rs]^Reg[rt]
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt))
                  function = "compare"
                elif(line[26:32] == "101010"):
                  function = "slt"
                  if (Reg[rs] < Reg[rt]):
                       Reg[rd]=1
                  else:
                       Reg[rd]=0
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt))
                  function = "compare"
                print ("Cycles in Multi-Cycle: 4")
                if (forward_check == True):
                      print ("Forwarded?: $" + str (rd) + " was forwarded")
                else:
                      print ("Forwarded?: No")
                if (lu_check == True):
                    print ("lw-use Stall?: Yes")
                else:
                    print ("lw-use Stall?: No")
                    
            elif(line[0:6] == "001000"):
                four_cyc += 1
                tot_cyc += 4
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if ((rd_check == rt) and function == "lw"):
                  lw_use += 1
                  tot_cyc2 += 1
                  tot_delay += 1
                  lu_check = True
                else:
                  lu_check = False
                rd_check = rt
                function = "addi"
                if(forward_check_rd[rt] == Reg[rt]):
                    forward += 1
                    forward_check = True
                else:
                    forward_check = False
                forward_check_rd[rt]=Reg[rt]
                if(line[16] == "1"):
                    imm = imm - 65536
                #print(imm)
                Reg[rt]=Reg[rs]+imm
                PC +=1
                print (str(function) + " $" + str(rs) + ",$" + str(rt) + "," + str(imm))
                print ("Cycles in Multi-Cycle: 4")
                if (forward_check == True):
                      print ("Forwarded?: $" + str (rt) + " was forwarded")
                else:
                      print ("Forwarded?: No")
                if (lu_check == True):
                    print ("lw-use Stall?: Yes")
                else:
                    print ("lw-use Stall?: No")
                function = "compare"
                
            elif(line[0:32] == "00010000000000001111111111111111"):
                finished = True
                three_cyc += 1
                tot_cyc += 3
            elif(line[0:6] == "000100"):
                three_cyc += 1
                tot_cyc += 3
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (function == "compare" and (rd_check == rs or rd_check == rt)):
                    compute_branch_compare += 1
                    tot_delay += 1
                    tot_cyc2 += 1
                    cbc_check = True
                else:
                    cbc_check = False
                function = "beq"
                if (line[16] == "1"):
                    imm = imm - 65536
                if(Reg[rs] == Reg[rt]):
                    addThis = imm + 1
                    branch_taken_flush += 1
                    tot_cyc2 += 1
                    tot_delay += 1
                    flush_check = True
                else:
                    addThis = 1
                    flush_check = False
                if(addThis != 0):
                    PC += addThis
                else:
                    finished = True
                print (str(function) + " $" + str(rs) + ",$" + str(rt) + "," + str(imm))
                print ("Cycles in Multi-Cycle: 3")
                if (cbc_check == True):
                    print ("Compute-Branch Compare Hazard?: Yes")
                else:
                    print ("Compute-Branch Compare Hazard?: No")
                if (flush_check == True):
                    print ("Flush?: Yes")
                else:
                    print ("Flush?: No")
            elif(line[0:6] == "000101"):
                
                three_cyc += 1
                tot_cyc += 3
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (function == "compare" and (rd_check == rs or rd_check == rt)):
                    compute_branch_compare += 1
                    tot_delay += 1
                    tot_cyc2 += 1
                    cbc_check = True
                else:
                    cbc_check = False
                function = "bne"
                if(line[16] == "1"):
                    imm = imm - 65536
                if (Reg[rs] != Reg[rt]):
                    addThis = imm + 1
                    branch_taken_flush += 1
                    tot_cyc2 += 1
                    tot_delay += 1
                    flush_check = True
                else:
                    addThis = 1
                    flush_check = False
                if (addThis != 0):
                    PC += addThis
                else:
                    finished = True
                print (str(function) + " $" + str(rs) + ",$" + str(rt) + "," + str(imm))
                print ("Cycles in Multi-Cycle: 3")
                if (cbc_check == True):
                    print ("Compute-Branch Compare Hazard?: Yes")
                else:
                    print ("Compute-Branch Compare Hazard?: No")
                if (flush_check == True):
                    print ("Flush?: Yes")
                else:
                    print ("Flush?: No")
            elif(line[0:6] == "100011"):
                function = "lw"
                five_cyc  += 1
                tot_cyc += 5
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                rd_check = rt
                if (forward_check_rd [rs] == Reg[rs]):
                  forward += 1
                  forward_check = True
                else:
                  forwrad_check = False
                forward_check_rd [rt] == Reg[rt]
                if (line[16] == "1"):
                    imm = imm - 65536
                imm = imm - 8192 #0x2000
                #imm = imm / 4
                dummyA=0.25
                Reg[rt]=Mem[round(Reg[rs]*dummyA)+imm]
                PC +=1
                print (str(function) + " $" + str(rs) + "," + str(imm) + "($" + str(rt)+ ")")
                print ("Cycles in Multi-Cycle: 5")
                
            elif(line[0:6] == "101011"):
                function = "sw"
                four_cyc += 1
                tot_cyc += 4
                rs = int(line[6:11],2)
                rt = int(line[11:16],2)
                imm = int(line[16:32],2)
                if (forward_check_rd [rs] == Reg[rs]):
                  forward += 1
                  forward_check = True
                else:
                  forward_check = False
                forward_check_rd [rt] = Reg[rt]
                if (line[16] == "1"):
                    imm = imm - 65536
                imm = imm - 8192 #0x2000
                dummyA=0.25

                Mem[round(Reg[rs]*dummyA)+imm]=Reg[rt]
                PC +=1
                print (str(function) + " $" + str(rs) + "," + str(imm) + "($" + str(rt) + ")")
                print ("Cycles in Multi-Cycle: 4")
                if (forward_check == True):
                      print ("Forwarded?: $" + str (rt) + " was forwarded")
                else:
                      print ("Forwarded?: No")
            print ("")

    print("\nReg: " + str(Reg))
    print("PC: " + str(PC + 1))
    print("DIC: " + str(DIC))
    #print("Mem: " + str(Mem))
    print("")
    print("\nMulticycle Simulation Results: ")
    print("Three Cycles: " + str(three_cyc))
    print("Four Cycles: " + str(four_cyc))
    print("Five Cycles: " + str(five_cyc))
    print("Total Cycles: " + str(tot_cyc))
    print("\nPipeline Simulation Results: ")
    print("Total Forwards: " + str(forward))
    print("lw-use: " + str(lw_use))
    print("compute-branch compare: " + str(compute_branch_compare))
    print("branch taken flush: " + str(branch_taken_flush))
    print("Total Delays: " +str(tot_delay) + " Cycles")
    print("Total Cycles: " + str(tot_cyc2))
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
