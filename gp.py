from stackmachine import Machine
from random import randint, random, choice


def random_integer():
    return str(randint(-50, 50))

def random_float():
    return str((random() * 200.0) - 100.0)

def random_instruction():
    needs_int = ('JMP', 'JZ', 'JE', 'JNE', 'JLT', 'JGT')
    needs_float = ('PUSH',)
    line = ''
    
    instruction = choice(instr)
    line += instruction
    if instruction in needs_int:
        line += ' ' + random_integer()
    if instruction in needs_float:
        line += ' ' + random_float()
    line += '\n'
    return line

def random_code(length):
    code = ""
    for i in range(length):
        code += random_instruction()
    return code

def fitness(result):
    return len(result)  # Dumb one, just go for the longest stack

def find_fitness(vm, code):
    vm.code = code
    vm.run()
    return fitness(vm.stack)

def modify_append(a, b):
    return a + b

def modify_mutate(code, count):
    selection = []
    lines = code.split('\n')

    for i in range(count):
        selection.append(randint(0, len(lines)-1))

    for i in selection:
        lines[i] = random_instruction().strip()

    return '\n'.join(lines)

vm = Machine()
instr = vm.instructions.keys()

code = random_code(10)

for i in range(20):
    print find_fitness(vm, code)
    code = modify_mutate(code, 5)
    print find_fitness(vm, code)

