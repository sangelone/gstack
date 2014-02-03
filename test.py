#!/usr/bin/env python

from stackmachine import Machine


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
                PUSH 1      ; count to 10 with a loop
                DUP
                DUP
                PUSH 10
                JE 3
                INC
                JMP -5
                POP
                """,
        'out': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    },    
)

vm = Machine(verbose)
for t in testdata:
    vm.stack = t['in']
    vm.code = t['code']
    vm.run()

    if vm.has_errors or vm.stack != t['out']:
        print "Error!"
        print "Excpected:", t['out']
        print "Result was:", vm.stack
        print "Code:"
        vm.code_listing()
    elif verbose:
        print "Test passed! Result:", vm.stack
