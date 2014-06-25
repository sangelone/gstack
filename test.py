#!/usr/bin/env python

from stackmachine import Machine
from timeit import timeit
from random import choice


""" A series of simple tests. Specify the input stack and the code and the
    expected resulting stack. Not all features and instructions are covered
    yet. The vm it runs against does not have any parameters changed.

    TODO: convert this to PyUnit or Nose when packaging/installing is added
"""


# Flip this if a test fails or you are adding new tests to get useful debug output
verbose = False

testdata = (
    {   'in': [],
        'code': "",
        'out': []
    },
    {   'in': [1, 2, 3],
        'code': "",
        'out': [1, 2, 3]
    },
    {   'in': [1, 2, 3],
        'code': """
                ROT
                ROT
                PUSH -1
                """,
        'out': [3, 1, 2, -1]
    },
    {   'in': [],
        'code': """
                PUSH 11111
                """,
        'out': [11111]
    },
    {   'in': [],
        'code': """
                PUSH 5
                PUSH 1
                PUSH 100
                MUL
                ADD
                PUSH 2
                DIV
                PUSH 100
                EXP
                TRUNC
                """,
        'out': [1]
    },
    {   'in': [1],
        'code': """
                PUSH 10
                MUL
                PUSH 10
                DIV         ; result should still be 1.0
                LOG         ; natural log
                """,
        'out': [0.0]
    },
    {   'in': [1, 5],
        'code': """
                MIN
                PUSH 1
                PUSH 10
                MAX
                DUP
                INC
                """,
        'out': [1, 10, 11]
    },
    {   'in': [],
        'code': """
                PUSH 1      ; count to 100 with a loop
                DUP
                DUP
                PUSH 100
                JE 3
                INC
                JMP -5
                POP
                """,
        'out': range(1, 101)
    },
)

def calc_speed(iters, instructions=20):
    instr = ['POP','SWP','ROT','DUP','MUL','DIV','ADD','SUB','EXP','LOG','TRUNC']
    code = '\n'.join([choice(instr) for i in xrange(instructions)])
    setup = '''
from stackmachine import Machine
vm = Machine()
vm.code = """
    ''' + code + '''
    """
    '''
    return 1/(timeit('vm.stack=[5]*20;vm.run()', setup, number=iters) / iters * instructions)


if __name__ == '__main__':
    vm = Machine(verbose)
    for t in testdata:
        vm.stack = t['in']
        vm.code = t['code']
        vm.run()

        if vm.has_errors or vm.stack != t['out']:
            print "Test failed!\nExcpected:", t['out']
            print "Result was:", vm.stack
            print "Code:"
            vm.code_listing()
            print
        elif verbose:
            print "Test passed! Result:", vm.stack

    ips = calc_speed(iters=20000)
    if ips < 400:
        print "Warning: this machine may be too slow for this VM at", ips, "instructions per second"
    if verbose:
        print "Speed test results:\n", ips, "instructions per second =", ips / 1000000, "BogoMips"
