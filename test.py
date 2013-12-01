#!/usr/bin/env python

from stackmachine import Machine


""" A series of simple tests. Specify the input stack and the code and the
    expected resulting stack. Not all features and instructions are covered
    yet. The vm it runs against does not have any parameters changed.
"""


# Flip this is a test fails or you are adding new tests to get useful debug output
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
    else:
        print "Test passed! Result:", t['out']
