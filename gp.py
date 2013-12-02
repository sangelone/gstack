from stackmachine import Machine
from random import randint, random, choice


def random_integer():
    return str(randint(-5, 5))

def random_float():
    return str((random() * 2.0) - 1.0)

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
    f = 0
    for i in range(100):
        try:
            if result[i] == i*2:
                f += 1
        except: pass
    return f

def find_fitness(vm, code):
    vm.code = code
    vm.stack = []
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
vm._max_runlines = 500
instr = vm.instructions.keys()  # Full set
instr = ['INC', 'ADD', 'PUSH', 'JZ', 'JE', 'JMP', 'JGT', 'JLT', 'SUB', 'POP', 'SWP', 'DUP'] # Custom set
print instr


code = random_code(7)
best_fitness = find_fitness(vm, code)
i = 0

while best_fitness < 100:
    i += 1
    trial_code = modify_mutate(code, randint(1, 5))
    if randint(1,5) == 1:
        trial_code = random_code(7)
    trial_fitness = find_fitness(vm, trial_code)

    # Apply pressure to not have infinite loops or other 'errors'
    if (best_fitness > 2 or trial_fitness > 2) and vm.has_errors:
        continue

    if trial_fitness > best_fitness:
        code = trial_code
        best_fitness = trial_fitness
    if i % 100 == 0: print i, best_fitness, '\n', code, '\n'

print best_fitness
vm.code_listing()
print vm.stack
print vm.has_errors