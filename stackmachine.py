import math

class Machine():    
    """ Simple stack based machine designed for genetic programming (GP) experiments.
        Easy to use and forgiving with nonfatal errors.
        
        See README and tests for examples. Reference implementation, use a faster VM for
        production.
    """

    def __init__(self, debug=False):
        self.stack = []
        self.debug = debug
        self.code = ""
        self.has_errors = False
        self._max_runlines = 100

        self.instructions = {
            'CLR':  self._clr,
            'PUSH': self._push, # takes 1 value
            'POP':  self._pop,
            'SWP':  self._swp,
            'ROT':  self._rot,
            'DUP':  self._dup,

            'MUL':  self._mul,
            'DIV':  self._div,
            'MOD':  self._mod,
            'ADD':  self._add,
            'SUB':  self._sub,
            'EXP':  self._exp,
            'LOG':  self._log,
            'TRUNC':self._trunc,
            'MIN':  self._min,
            'MAX':  self._max,
            'INC':  self._inc,

            'JMP':  self._jmp, # all jumps take an offset value
            'JZ':   self._jz,
            'JE':   self._je,
            'JNE':  self._jne,
            'JLT':  self._jlt,
            'JGT':  self._jgt,

            'END':  None
        }
    

    def _clr(self):
        self.stack = []

    def _push(self, a):
        try:
            a = float(a)
        except:
            a = a.strip('\'"`')
        self.stack.append(a)
    
    def _pop(self):
        if self.stack:
            self.stack.pop()

    # TODO: generalize. The arity=2 instructions below follow the same pattern.

    def _mul(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = self.stack[-1] * self.stack[-2]
            self.stack = self.stack[:-2]
            self.stack.append(val)
    
    def _div(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = self.stack[-1] / self.stack[-2]
            self.stack = self.stack[:-2]
            self.stack.append(val)
    
    def _mod(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = self.stack[-1] % self.stack[-2]
            self.stack = self.stack[:-2]
            self.stack.append(val)
    
    def _add(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = self.stack[-1] + self.stack[-2]
            self.stack = self.stack[:-2]
            self.stack.append(val)
    
    def _sub(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = self.stack[-1] - self.stack[-2]
            self.stack = self.stack[:-2]
            self.stack.append(val)

    def _exp(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = math.pow(self.stack[-1], self.stack[-2])
            self.stack = self.stack[:-2]
            self.stack.append(val)

    def _log(self):
        if self.stack:
            self.stack.append(math.log(self.stack.pop()))

    def _trunc(self):
        if self.stack:
            self.stack.append(math.trunc(self.stack.pop()))

    def _min(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = min(self.stack.pop(), self.stack.pop())
            self.stack.append(val)

    def _max(self):
        if len(self.stack) < 2:
            self.stack = [0]
        else:
            val = max(self.stack.pop(), self.stack.pop())
            self.stack.append(val)

    def _inc(self):
        if self.stack:
            self.stack[-1] += 1

    def _swp(self):
        if len(self.stack) > 1:
            self.stack[-2], self.stack[-1] = self.stack[-1], self.stack[-2]
    
    def _rot(self):
        if len(self.stack) > 1:
            self.stack = self.stack[1:] + self.stack[:1]

    def _dup(self):
        if self.stack:
            self.stack.append(self.stack[-1])

    def _jmp(self, a):
        try:
            n = self._curline + int(a)
        except:
            return
        if n == self._curline: return
        if n < 0: return
        if n > len(self.lines) - 1: return
        # offset being incremented after returning when calculating IP
        self._curline = n-1

    def _jz(self, a):
        if self.stack:
            if self.stack.pop() == 0:
                self._jmp(a)

    def _je(self, a):
        if len(self.stack) > 1:
            if self.stack.pop() == self.stack.pop():
                self._jmp(a)

    def _jne(self, a):
        if len(self.stack) > 1:
            if self.stack.pop() != self.stack.pop():
                self._jmp(a)

    def _jlt(self, a):
        if len(self.stack) > 1:
            if self.stack.pop() < self.stack.pop():
                self._jmp(a)

    def _jgt(self, a):
        if len(self.stack) > 1:
            if self.stack.pop() > self.stack.pop():
                self._jmp(a)
    
    def code_listing(self):
        self.lines = self.code.split('\n')
        for num, line in enumerate(self.lines):
            line = line.strip().upper()
            print num, '\t', line
        
    def evaluate(self, line):
        line = line.split(';')[0]
        line = line.strip().upper()
        if line:
            if self.debug: print self._curline, '> ', line
    
            tokens = line.split()
            instr = tokens[0]
            if instr == 'END': return False
            
            if len(tokens) > 1:
                values = tokens [1:]
            else: values = []
            
            try:
                self.instructions[instr](*values)
            except Exception as e:
                if self.debug: print "Error:", e
                self.has_errors = True
    
            if self.debug: print self.stack, '\n'
            
        self._curline += 1
        return True
    
    def run(self):
        self._curline = 0
        self._lines_executed = 0
        self.has_errors = False
        self.lines = self.code.split('\n')

        while(self.evaluate(self.lines[self._curline])):
            self._lines_executed += 1
            if self._lines_executed > self._max_runlines:
                if self.debug: print "Reached maximum runlines:", self._max_runlines
                self.has_errors = True
                break
            if self._curline >= len(self.lines):
                break
            
        return self.has_errors
