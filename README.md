gstack
======


A stack-based VM implementing a very small instruction set
meant for use in genetic programming. It is very forgiving
to lend flexibility to automatically generated input code.

Recommend using PyPy with JIT to reach a few thousand instructions
per second.



**Features include**
- Very forgiving input evaluation
- Useful debugging mode prints instructions, stack, and friendly error info
- Continues quickly on most errors
    - Example: trying to jump past end of program is just ignored
    - If stack doesn't contain what an instruction expects, continues silently
    - On error, stack is retained and flag is set so the managing app can
      decide to keep or kill the program itself
- Major errors that will stop execution: bad instruction or arity
- Simple type system
    - Type is implied when value is pushed onto stack
    - Strongly, statically typed (type can never change)
    - All numbers pushed on the stack are Python floats
- Relative conditional jumping makes code segments more likely to work
  after crossover or mutation operations
- Easy to add or remove instructions
- Program ends when there are no more lines, an error, reaches END,
  or user-adjustable number of instructions have been executed (no infinite loops)


**Example input**

    PUSH 1      ; count to 100 with a loop
    DUP
    DUP
    PUSH 100
    JE 3        ; if the current number = 100, jump to end
    INC
    JMP -5      ; not done, continue looping
    POP         ; end (remove trailing test number)

**Example output (with Debug on)**

    1 >  PUSH 1
    [1.0]

    2 >  DUP
    [1.0, 1.0]

    3 >  DUP
    [1.0, 1.0, 1.0]

    4 >  PUSH 100
    [1.0, 1.0, 1.0, 100.0]

    5 >  JE 3
    [1.0, 1.0]

    6 >  INC
    [1.0, 2.0]

    7 >  JMP -5
    [1.0, 2.0]

    2 >  DUP
    [1.0, 2.0, 2.0]

    3 >  DUP
    [1.0, 2.0, 2.0, 2.0]

    4 >  PUSH 100
    [1.0, 2.0, 2.0, 2.0, 100.0]

    5 >  JE 3
    [1.0, 2.0, 2.0]

    6 >  INC
    [1.0, 2.0, 3.0]
    .
    .
    . etc

**TODO**
- Add features to unroll, optimize, and pretty-print
