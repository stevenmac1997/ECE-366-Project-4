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
    DMHit4W = 0  # Hits for the blocks, with size of 4 words, a total of 2 blocks. 0/1
    DMMiss4W = 0  # Misses for the blocks, with size of 4 words, a total of 2 blocks. 0/1
    DMBlkI4W = ["",""]  # The tags saved for the blocks, with size of 4 words, a total of 2 blocks. 0/1
    # DM4W2B => 16 bits: T T T T T T T T T T T | I | O O | B B
    DMHit2W = 0  # Hits for the blocks, with size of 2 words, a total of 4 blocks. 00/01/10/11
    DMMiss2W = 0  # Misses for the blocks, with size of 2 words, a total of 4 blocks. 00/01/10/11
    DMBlkI2W = ["", "", "", ""] # The tags saved for the blocks, with size of 4 words, a total of 2 blocks. 00/01/10/11
    # DM2W4B => 16 bits: T T T T T T T T T T T | I I | O | B B
    FAHit2W = 0  # Hits for the sets, with size of 2 words, a total of 8 blocks. 00/01/10/11
    FAMiss2W = 0  # Misses for the sets, with size of 2 words, a total of 8 blocks. 00/01/10/11
    FABlkI2W = ["", "", "", ""]  # The tags saved for the sets, with size of 2 words, a total of 8 blocks. 00/01/10/11
    FALRU = []
    i = 0
    # FA2W4B => 16 bits: T T T T T T T T T T T | I I | O | B B
    SAHit2W = 0  # Hits for the sets, with size of 2 words, a total of 8 blocks. 00/01/10/11
    SAMiss2W = 0  # Misses for the sets, with size of 2 words, a total of 8 blocks. 00/01/10/11
    SASetI2W = ["", "", "", "", "", "", "", ""]  # The tags saved for the sets, with size of 2 words, a total of 8 blocks. 00/01/10/11
    SALRU = [1,1,1,1]
    # SA2W4B => 16 bits: T T T T T T T T T T T | I I | O | B B
    currTagDM = " "
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
                  output.write (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt) + "\n")
                  function = "compare"
                elif(line[26:32] == "100010"):
                  function = "sub"
                  Reg[rd]=Reg[rs]-Reg[rt]
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt))
                  output.write (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt)+ "\n")
                  function = "compare"
                elif(line[26:32] == "100110"):
                  function = "xor"
                  Reg[rd]=Reg[rs]^Reg[rt]
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt))
                  output.write (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt)+ "\n")
                  function = "compare"
                elif(line[26:32] == "101010"):
                  function = "slt"
                  if (Reg[rs] < Reg[rt]):
                       Reg[rd]=1
                  else:
                       Reg[rd]=0
                  PC += 1
                  print (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt))
                  output.write (str(function) + " $" + str(rd) + ",$" + str(rs) + ",$" + str(rt)+ "\n")
                  function = "compare"
                print ("Cycles in Multi-Cycle: 4")
                output.write ("Cycles in Multi-Cycle: 4"+ "\n")
                if (forward_check == True):
                      print ("Forwarded?: $" + str (rd) + " was forwarded")
                      output.write ("Forwarded?: $" + str(rd) + " was forwarded"+ "\n")
                else:
                      print ("Forwarded?: No")
                      output.write ("Forwarded?: No"+ "\n")
                if (lu_check == True):
                    print ("lw-use Stall?: Yes")
                    output.write ("lw-use Stall?: Yes"+ "\n")
                else:
                    print ("lw-use Stall?: No")
                    output.write ("lw-use Stall?: No"+ "\n")

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
                output.write (str(function) + " $" + str(rs) + ",$" + str(rt) + "," + str(imm)+ "\n")
                output.write ("Cycles in Multi-Cycle: 4"+ "\n")
                if (forward_check == True):
                      print ("Forwarded?: $" + str (rt) + " was forwarded")
                      output.write ("Forwarded?: $" + str(rt) + " was forwarded"+ "\n")
                else:
                      print ("Forwarded?: No")
                      output.write ("Forwarded?: No"+ "\n")
                if (lu_check == True):
                    print ("lw-use Stall?: Yes")
                    output.write ("lw-use Stall?: Yes"+ "\n")
                else:
                    print ("lw-use Stall?: No")
                    output.write ("lw-use Stall?: No"+ "\n")
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
                output.write (str(function) + " $" + str(rs) + ",$" + str(rt) + "," + str(imm)+ "\n")
                output.write ("Cycles in Multi-Cycle: 3"+ "\n")
                if (cbc_check == True):
                    print ("Compute-Branch Compare Hazard?: Yes")
                    output.write ("Compute-Branch Compare Hazard?: Yes"+ "\n")
                else:
                    print ("Compute-Branch Compare Hazard?: No")
                    output.write ("Compute-Branch Compare Hazard?: No"+ "\n")
                if (flush_check == True):
                    print ("Flush?: Yes")
                    output.write ("Flush?: Yes"+ "\n")
                else:
                    print ("Flush?: No")
                    output.write ("Flush?: No"+ "\n")
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
                output.write (str(function) + " $" + str(rs) + ",$" + str(rt) + "," + str(imm)+ "\n")
                output.write ("Cycles in Multi-Cycle: 3"+ "\n")
                if (cbc_check == True):
                    print ("Compute-Branch Compare Hazard?: Yes")
                    output.write ("Compute-Branch Compare Hazard?: Yes"+ "\n")
                else:
                    print ("Compute-Branch Compare Hazard?: No")
                    output.write ("Compute-Branch Compare Hazard?: No"+ "\n")
                if (flush_check == True):
                    output.write ("Flush?: Yes"+ "\n")
                    print ("Flush?: Yes")
                else:
                    print ("Flush?: No")
                    output.write ("Flush?: No"+ "\n")
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
                forward_check_rd [rt] = Reg[rt]
                if (line[16] == "1"):
                    imm = imm - 65536
                imm = imm - 8192 #0x2000
                #imm = imm / 4
                addr = int(round(Reg[rs] * 0.25)) + imm
                Reg[rt] = Mem[addr]
                PC += 1
                print (str(function) + " $" + str(rs) + "," + str(imm) + "($" + str(rt)+ ")")
                print ("Cycles in Multi-Cycle: 5")
                output.write (str(function) + " $" + str(rs) + "," + str(imm) + "($" + str(rt) + ")\n")
                output.write ("Cycles in Multi-Cycle: 5\n")
                # 3.)
                # A.) DM4W2B => 16 bits: T T T T T T T T T T T | I | O O | B B
                # B.) DM2W4B => 16 bits: T T T T T T T T T T T | I I | O | B B
                # C.) FA2W4B => 16 bits: T T T T T T T T T T T T T | O | B B
                # D.) SA2W4S => 16 bits: T T T T T T T T T T T | I I | O | B B
                # Add 0x2000 to the address and change it to binary
                if (line[16] == "1"):
                    imm += 65536
                addr = Reg[rs] + imm + 8192
                addr = format(int(addr), "b")
                addr = "00" + addr
                print("Cache Access log:")
                print("Memory Address: " + addr)
                output.write("Cache Access log:\n")
                output.write("Memory Address: " + addr+ "\n")
                # Get the tag from the address
                currTagDM = addr[0:11]
                currTagFA = addr[0:13]
                hit = "No"
                valid = 0
                # A.)
                if (DMBlkI4W[int(addr[12])] != ""):
                    valid = 1
                else:
                    valid = 0
                if (DMBlkI4W[int(addr[12])] == currTagDM):
                    DMHit4W += 1
                    hit = "Yes"

                else:
                    DMMiss4W += 1
                    DMBlkI4W[int(addr[12])] = currTagDM
                    hit = "No"
                print("Direct Mapped Cache, 2 blocks with size of 4 words: ")
                print("Block accessed: " + addr[12])
                print ("Valid bit: " + str(valid))
                print("Tag: " + currTagDM)
                output.write("Direct Mapped Cache, 2 blocks with size of 4 words: \n")
                output.write("Block accessed: " + addr[12]+ "\n")
                output.write ("Valid bit: " + str(valid)+ "\n")
                output.write("Tag: " + currTagDM+ "\n")

                # B.)
                if (DMBlkI2W[int(addr[12:14], 2)] == ""):
                    valid = 0
                else:
                    valid = 1
                if (DMBlkI2W[int(addr[12:14], 2)] == currTagDM):
                    DMHit2W += 1
                else:
                    DMMiss2W += 1
                    DMBlkI2W[int(addr[12:14], 2)] = currTagDM

                print("Direct Mapped Cache, 4 block with size of 2 words: ")
                print("Block accessed: " + str(int(addr[12:14], 2)))
                print ("Valid bit: " + str(valid))
                print("Tag: " + currTagDM)

                output.write("Direct Mapped Cache, 4 block with size of 2 words: \n")
                output.write("Block accessed: " + str(int(addr[12:14], 2))+ "\n")
                output.write ("Valid bit: " + str(valid)+ "\n")
                output.write("Tag: " + currTagDM+ "\n")
                # C.)
                missed = True
                valid = 0
                block = -1
                for i in range(0, 4):
                    if (FABlkI2W[i] == currTagFA):
                        if (FABlkI2W[i] != ""):
                            FAHit2W += 1
                            missed = False
                            block = i
                        break
                if (missed):
                    while (i < 4 and FABlkI2W[i] != "" ):
                        i += 1
                    if (i < 4):
                        FABlkI2W[i] = currTagFA
                        FALRU.append(i)
                        valid = 0
                        block = i
                    else:
                        FABlkI2W[FALRU[0]] = currTagFA
                        block = FALRU[0]
                        i = FALRU.pop(0)
                        FALRU.append(i)
                        valid = 1
                print("Fully-Associated Cache, 4 blocks with size of 2 words: ")
                print("Block accessed: " + str(block))
                print("Valid bit: " + str(valid))
                print("Tag: " + currTagFA)

                output.write("Fully-Associated Cache, 4 blocks with size of 2 words: \n")
                output.write("Block accessed: " + str(block)+ "\n")
                output.write("Valid bit: " + str(valid)+ "\n")
                output.write("Tag: " + currTagFA+ "\n")

                # D.)
                missed = True
                valid = 1
                if (SASetI2W[2 * (int(addr[12:14], 2))] == currTagDM):
                    if (SASetI2W[int(addr[12:14], 2)] != ""):
                        SAHit2W += 1
                        missed = False
                elif (SASetI2W[2 * (int(addr[12:14], 2)) + 1] == currTagDM):
                    if (SASetI2W[2 * (int(addr[12:14],2)) + 1] != ""):
                        SAHit2W += 1
                        missed = False

                if (missed):
                    SAMiss2W += 1
                    if (SASetI2W[2 * (int(addr[12:14], 2))] == ""):
                        SASetI2W[2 * (int(addr[12:14], 2))] = currTagDM
                        valid = 0
                    elif (SASetI2W[2 * (int(addr[12:14], 2)) + 1] == ""):
                        SASetI2W[2 * (int(addr[12:14], 2)) + 1] = currTagDM
                        valid = 0
                    elif (SALRU[int(addr[12] + addr[13], 2)] == 0):
                        SASetI2W[2 * (int(addr[12] + addr[13], 2)) + 1] = currTagDM
                        SALRU[int(addr[12] + addr[13], 2)] = 1
                    else:
                        SASetI2W[2 * (int(addr[12] + addr[13], 2))] = currTagDM
                        SALRU[int(addr[12] + addr[13], 2)] = 0
                print("2-way Set-Associative Cache, 4 sets / 8 blocks with size of 2 words: ")
                print("Set accessed: " + str(int(addr[12:14], 2)))
                print("Block accessed: " + str(SALRU[int(addr[12] + addr[13], 2)]))
                print("Valid bit: " + str(valid))
                print("Tag: " + currTagDM)
                output.write("2-way Set-Associative Cache, 4 sets / 8 blocks with size of 2 words:\n")
                output.write("Set accessed: " + str(int(addr[12:14], 2))+ "\n")
                output.write("Block accessed: " + str(SALRU[int(addr[12] + addr[13], 2)])+ "\n")
                output.write("Valid bit: " + str(valid)+ "\n")
                output.write("Tag: " + currTagDM+ "\n")
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

                Mem[int(round(Reg[rs]*dummyA)+imm)]=Reg[rt]
                PC +=1
                print (str(function) + " $" + str(rs) + "," + str(imm) + "($" + str(rt) + ")")
                print ("Cycles in Multi-Cycle: 4")
                output.write (str(function) + " $" + str(rs) + "," + str(imm) + "($" + str(rt) + ")\n")
                output.write ("Cycles in Multi-Cycle: 4\n")
                if (forward_check == True):
                      print ("Forwarded?: $" + str (rt) + " was forwarded")
                      output.write ("Forwarded?: $" + str (rt) + " was forwarde\n")
                else:
                      print ("Forwarded?: No")
                      output.write ("Forwarded?: No\n")
            print ("")
            output.write("\n")
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
    print("Direct mapped cache, block size of 4 words, a total of 2 blocks:")
    print("HITS:     " + str(DMHit4W))
    print("MISS:     " + str(DMMiss4W))
    print("HIT Rate: " + str(float(DMHit4W) / float(DMHit4W + DMMiss4W)))
    print("\nDirect mapped cache, block size of 2 words, a total of 4 blocks:")
    print("HITS:     " + str(DMHit2W))
    print("MISS:     " + str(DMMiss2W))
    print("HIT Rate: " + str(float(DMHit2W) / float(DMHit2W + DMMiss2W)))
    print("\nFully-Associated Cache, 4 blocks with size of 2 words:")
    print("HITS:     " + str(FAHit2W))
    print("MISS:     " + str(FAMiss2W))
    print("HIT Rate: " + str(float(FAHit2W) / float(FAMiss2W + FAHit2W)))
    print("\n2-way Set-Associative Cache, 4 sets / 8 blocks with size of 2 words:")
    print("HITS:     " + str(SAHit2W))
    print("MISS:     " + str(SAMiss2W))
    print("HIT Rate: " + str(float(SAHit2W) / float(SAHit2W + SAMiss2W)))
    output.write("Reg: " + str(Reg))
    output.write("\nPC : " + str(PC+1))
    output.write("\nDIC: " + str(DIC))
    output.write("\nMulticycle Simulation Results: ")
    output.write("\n# Three Cycles: " + str(three_cyc))
    output.write("\n# Four Cycles: " + str(four_cyc))
    output.write("\n# Five Cycles: " + str(five_cyc))
    output.write("\nTotal Cycles: " + str(tot_cyc))
    output.write("\nPipeline Simulation Results: ")
    output.write("\nTotal Forwards: " + str(forward))
    output.write("\nlw-use: " + str(lw_use))
    output.write("\ncompute-branch compare: " + str(compute_branch_compare))
    output.write("\nbranch taken flush: " + str(branch_taken_flush))
    output.write("\nTotal Delays: " +str(tot_delay) + " Cycles")
    output.write("\nTotal Cycles: " + str(tot_cyc2))
    output.write("\n")
    output.write("\nDirect mapped cache, block size of 4 words, a total of 2 blocks:")
    output.write("\nHITS:     " + str(DMHit4W))
    output.write("\nMISS:     " + str(DMMiss4W))
    output.write("\nHIT Rate: " + str(float(DMHit4W) / float(DMHit4W + DMMiss4W)))
    output.write("\n\nDirect mapped cache, block size of 2 words, a total of 4 blocks:")
    output.write("\nHITS:     " + str(DMHit2W))
    output.write("\nMISS:     " + str(DMMiss2W))
    output.write("\nHIT Rate: " + str(float(DMHit2W) / float(DMHit2W + DMMiss2W)))
    output.write("\n\nFully-Associated Cache, 4 blocks with size of 2 words:")
    output.write("\nHITS:     " + str(FAHit2W))
    output.write("\nMISS:     " + str(FAMiss2W))
    output.write("\nHIT Rate: " + str(float(FAHit2W) / float(FAMiss2W + FAHit2W)))
    output.write("\n\n2-way Set-Associative Cache, 4 sets / 8 blocks with size of 2 words:")
    output.write("\nHITS:     " + str(SAHit2W))
    output.write("\nMISS:     " + str(SAMiss2W))
    output.write("\nHIT Rate: " + str(float(SAHit2W) / float(SAHit2W + SAMiss2W)))
    


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
    outFile = open("p4_output_imem_.txt", "w")

    outFile.write("ECE366 Fall 2018: MIPS Mini Assembler")
    outFile.write("\n\nMembers:")
    outFile.write("\nFrancis Paul Amadeo")
    outFile.write("\nSteven Mac\n\n")

    outFile.write("\nReading in instruction file...")
    for line in inFile:
        if (line == "\n"):
            continue
        line = line.replace("\n", "")
        line = line.replace("0x", "")
        instr.append(hexToBin(line))  # Copy all instruction into a list
        Nlines += 1

    print("...finished reading in instruction file")
    print("\nSimulating...")
    outFile.write("\n...finished reading in instruction file")
    outFile.write("\n\nSimulating...")
    simulate(instr, outFile)
    print("\nSimulation done")
    outFile.write("\n\nSimulation done")

    inFile.close()
    outFile.close()

    exit()


if __name__ == "__main__":
    main()
