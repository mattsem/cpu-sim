#main memory
cols,rows = 16,16

mem = [[0]*cols]*rows
#print(mem)


#instr memory
global instrMem
global pc
global lr
global sp
pc = [0]*16
lr = [0]*16
sp = [0]*16


#registers
r0 = [0]*16
r1 = [1]*16
r2 = [0]*16
r3 = [0]*16
r4 = [0]*16
r5 = [0]*16
r6 = [0]*16
r7 = [0]*16
r8 = [0]*16
r9 = [0]*16
r10 = [0]*16
r11 = [0]*16
r12 = [0]*16
r13 = [0]*16
rr = [0]*16

regs = {'r0': r0,'r1': r1, 'r2': r2, 'r3': r3, 'r4': r4,'r5': r5, 'r6' : r6, 'r7' : r7, 'r8': r8, 'r9':r9, 'r10': r10, 'r11':r11, 'r12' : r12, 'r13':r13, 'rr':rr}

#r0 always zero
freeRegs = [1,1,0,0,0,0,0,0,0,0,0,0,0,0,1]

variables = {}


functions = {}

def readInst():
    inst = None
    while inst != 'end':
        inst = input('enter instruction:\n')
        #print(inst)
        if inst.split()[0] == 'add':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = add(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'addi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = add(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'sub':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = sub(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'subi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = sub(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'mul':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = naiveMul(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'print':
            printRegs()

        if inst.split()[0] == 'load':
            p1 = inst.split()[1]
            memory = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            regs[p1] = load(regs[p1],int(memory))
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'store':
            memory = inst.split()[1]
            p1 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            store(int(memory),regs[p1])

        if inst.split()[0] == 'read':
            readFile()

        if inst.split()[0] == 'run':
            runFile()

        if inst.split()[0] == 'jump':
            jump(inst.split()[1])

        if inst.split()[0] == 'beq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchEq(regs[p1],regs[p2],int(addr))

        if inst.split()[0] == 'bnq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchNeq(regs[p1],regs[p2],int(addr))
       
        

    printRegs()

def add(reg1, reg2):
    result = [0]*16
    #print('adding')
    #print(binToDec(reg1),' = ', binToDec(reg1) ,' + ' , binToDec(reg2))
    carry = 0
    sum = 0 
    #big endian so traverse in reverse
    for index in range(15,-1,-1):
        sum = reg1[index] + reg2[index] + carry
        if sum == 0:
            result[index] = 0
            carry = 0
        elif sum == 1:
            result[index] = 1
            carry = 0
        elif sum == 2:
            result[index] = 0
            carry = 1
        elif sum == 3:
            result[index] = 1
            carry = 1
    return result

def sub(reg1,reg2):
    result = [0]*16
    #print('subbing')
    #print(binToDec(reg1),' = ', binToDec(reg1) ,' - ' , binToDec(reg2))
    borrow = 0
    diff = 0

    for index in range(15,-1,-1):
        diff = reg1[index] - reg2[index] - borrow
        if diff == 0:
            result[index] = 0
            borrow = 0
        elif diff == 1:
            result[index] = 1
            borrow = 0
        elif diff == -1:
            result[index] = 1
            borrow = 1
        elif diff == -2:
            result[index] = 0
            borrow = 1
    return result


def naiveMul(reg1,reg2):
    print('multiplying')
    print(binToDec(reg1),' = ', binToDec(reg1) ,' * ' , binToDec(reg2))
    result = reg1
    if binToDec(reg2) == 0 or binToDec(reg1) == 0:
        result = decToBin(0)
        return result
    for addition in range(1,binToDec(reg2)):
            result = add(result,reg1)
    return result


def jump(address):
    global pc
    pc = decToBin(address)

def branchEq(reg1,reg2,address):
    if sub(reg1,reg2) == decToBin(0):
        jump(address)
        print('branching to ', address)
    else:
        print('not branching')


def branchNeq(reg1,reg2,address):
    if sub(reg1,reg2) != decToBin(0):
        jump(address)
        print('branching to ', address)
    else:
        print('not branching')

def load(reg, memory):
    print('loading')
    return mem[memory]


def store(memory, reg):
    print('storing')
    mem[memory] = reg
    print(mem)
    printRegs()


def readFile():
    global instrMem
    instructions = open('cpu-sim/instr.txt','r')
    instrMem = [line.strip() for line in instructions]
    line = 0
    for inst in instrMem:
        if inst.split()[0] == 'func:':
            functions.update({inst.split()[1] : line})
            print(functions)
        line +=1

    instructions.close()
    printInstr()

def binToDec(reg):
    dec = 0
    for num in reg:
        dec = (2*dec)+num
    return dec

def decToBin(dec):
    bin = [0]*16
    for index in range(15,-1,-1):
        bit = dec % 2
        bin[index] = bit
        dec//=2
    return bin


def printRegs():
    for reg in regs:
        print(reg,': ',regs[reg], binToDec(regs[reg]))

def printInstr():
    print(instrMem)


def runFile():
    global pc
    global lr
    pc = sub(pc,pc)
    while binToDec(pc) != 65535:
        inst = instrMem[binToDec(pc)]
        pc = add(pc,decToBin(1))
        print(inst)
        #print(binToDec(pc))
        if inst.split()[0] == 'end':
            printRegs()
            pc = decToBin(65535)
        
        if inst.split()[0] == 'add':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = add(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'addi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = add(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'sub':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = sub(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'subi':
            p1 = inst.split()[1]
            imm = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if imm is None:
                print('invalid instruction format')
                break

            binImm = decToBin(int(imm))
            regs[p1] = sub(regs[p1],binImm)
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'mul':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            regs[p1] = naiveMul(regs[p1],regs[p2])
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'print':
            printRegs()

        if inst.split()[0] == 'load':
            p1 = inst.split()[1]
            memory = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            regs[p1] = load(regs[p1],int(memory))
            print(regs[p1])
            print(binToDec(regs[p1]))

        if inst.split()[0] == 'store':
            memory = inst.split()[1]
            p1 = inst.split()[2]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if memory is None:
                print('invalid instruction format')
                break
            store(int(memory),regs[p1])

        if inst.split()[0] == 'jump':
            jump(inst.split()[1])
        
        if inst.split()[0] == 'beq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchEq(regs[p1],regs[p2],int(addr))

        if inst.split()[0] == 'bnq':
            p1 = inst.split()[1]
            p2 = inst.split()[2]
            addr = inst.split()[3]
            if p1 is None or p1 not in regs:
                print('invalid instruction format')
                break
            if p2 is None or p2 not in regs:
                print('invalid instruction format')
                break
            branchNeq(regs[p1],regs[p2],int(addr))

        #if inst.split()[0] == 'func:':
         #   functions.update({inst.split()[1] : binToDec(pc)})
          #  print(functions)


        if inst.split()[0] == 'ret':
            regs['rr'] = regs[inst.split()[1]]
            print(regs['rr'],binToDec(regs['rr']))
            pc = lr

        if inst.split()[0] in functions:
            print('jumping to func:',inst.split()[0])
            lr = pc
            jump(functions[inst.split()[0]]+1)

        if inst.split()[0] == 'int':
            for index in range(len(freeRegs)):
                if freeRegs[index] == 0:
                    variables.update({inst.split()[1] : index})
                    freeRegs[index] = 1
                    break
            print(freeRegs)
            print(variables)
            

        if inst.split()[0] in variables:
            suffix = variables[inst.split()[0]]
            print(inst.split()[0], ' : ', regs['r'+str(suffix)], binToDec(regs['r'+str(suffix)]))

        
        
            
    print('PROGRAM COMPLETED')


#printRegs()
#print(sub(decToBin(5),decToBin(4)))
#print(decToBin(1))
readInst()