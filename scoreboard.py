# scoreboard.py - runs the scoreboard based on instructions
from fu import FunctionalUnit, FORMAT_HEADER
from decode import instructions as inst_funcs

ASM_FILE = 'scoreboard.asm'


""" The ScoreboardParser class is responsible for taking in an
assembly file as input and creating its respective Scoreboard object
which can then be used to simulate the scoreboarding algorithm. The
parser has one function in its API: scoreboard_for_asm()"""
class ScoreboardParser:

  def __init__(self, asm_file):
    self.sb = Scoreboard()
    self.asm = asm_file


  """ Parses a functional unit in the assembly file"""
  def __parse_fu(self, asm_tokens):
    f_unit = asm_tokens[0][1:]
    num_units = int(asm_tokens[1])
    clocks = int(asm_tokens[2])
    for unit in range(0, num_units):
      self.sb.units.append(FunctionalUnit(f_unit, clocks))


  """ Parses an instruction in the assembly file"""
  def __parse_inst(self, inst_tokens):
    key = inst_tokens[0]
    inst_func = inst_funcs[key]
    instruction = inst_func(' '.join(inst_tokens))
    self.sb.instructions.append(instruction)


  """ Parses a line of the assembly file"""
  def __parse_asm_line(self, line):
    tokens = line.split()

    # if the line starts with '.' it is a functional unit
    # instead of an instruction
    if tokens[0][0] == '.':
      f_units = self.__parse_fu(tokens)
    else:
      inst = self.__parse_inst(tokens)


  """ Creates a Scoreboard object based on a given asm file"""
  def scoreboard_for_asm(asm_file):
    parser = ScoreboardParser(asm_file)
    with open(parser.asm, 'r') as f:
      assembly = [line.strip() for line in f]
    for instruction in assembly:
      parser.__parse_asm_line(instruction)
    return parser.sb


""" The Scoreboard class is used to simulate the scoreboarding algorithm.
"""
class Scoreboard:

  def __init__(self):
    self.units = []           # array of FunctionalUnit
    self.instructions = []    # array of Instruction
    self.reg_status = {}      # register status table
    self.pc = 0               # program counter
    self.clock = 1            # processor clock


  def __str__(self):
    result = 'CLOCK: %d\n' % (self.clock)
    result += FORMAT_HEADER + '\n'
    for unit in self.units:
      result += str(unit) + '\n'
    return result


  """ Checks to see if the scoreboard is done executing. Returns True if so"""
  def done(self):
    done_executing = True
    out_of_insts = not self.has_remaining_insts()
    if out_of_insts:
      for fu in self.units:
        if fu.busy:
          done_executing = False
          break
    return out_of_insts and done_executing


  """ Checks to see if there are instructions left to issue to the
  scoreboard and returns True if so"""
  def has_remaining_insts(self):
    return self.pc < len(self.instructions)


  """ Determines if an instruction is able to be issued"""
  def can_issue(self, inst, fu):
    if inst is None:
      return False
    else:
      return inst.op == fu.type and not fu.busy and not (inst.fi in self.reg_status)


  """ Determines if an instruction is able to enter the read operands phase"""
  def can_read_operands(self, fu):
    return fu.busy and fu.rj and fu.rk


  """ Determines if an instruction is able to enter the execute phase"""
  def can_execute(self, fu):
    # check to make sure we've read operands, the functional unit
    # is actually in use, and has clocks remaining
    return (not fu.rj and not fu.rk) and fu.issued()


  """ Determines if an instruction is able to enter the writeback phase"""
  def can_write_back(self, fu):
    can_write_back = False
    for f in self.units:
      can_write_back = (f.fj != fu.fi or not f.rj) and (f.fk != fu.fi or not f.rk)
      if not can_write_back:
        break
    return can_write_back


  """ Issues an instruction to the scoreboard"""
  def issue(self, inst, fu):
    fu.issue(inst, self.reg_status)
    self.reg_status[inst.fi] = fu
    self.instructions[self.pc].issue = self.clock
    fu.inst_pc = self.pc


  """ Read operands stage of the scoreboard"""
  def read_operands(self, fu):
    fu.read_operands()
    self.instructions[fu.inst_pc].read_ops = self.clock


  """ Execute stage of the scoreboard"""
  def execute(self, fu):
    fu.execute()
    if fu.clocks == 0:
      self.instructions[fu.inst_pc].ex_cmplt = self.clock


  """ Writeback stage of the scoreboard"""
  def write_back(self, fu):
    fu.write_back(self.units)
    self.instructions[fu.inst_pc].write_res = self.clock
    # clear out the result register status
    del self.reg_status[fu.fi]
    fu.clear()


  """ Tick: simulates a clock cycle in the scoreboard"""
  def tick(self):
    # unlock all functional units
    for fu in self.units:
      fu.lock = False

    # Get the next instruction based on the PC
    next_instruction = self.instructions[self.pc] if self.has_remaining_insts() else None

    for fu in self.units:
      if self.can_issue(next_instruction, fu):
        self.issue(next_instruction, fu)
        self.pc += 1
        fu.lock = True
      elif self.can_read_operands(fu):
        self.read_operands(fu)
        fu.lock = True
      elif self.can_execute(fu):
        self.execute(fu)
        fu.lock = True
      elif fu.issued():
        # the functional unit is in use but can't do anything
        fu.lock = True

    for fu in self.units:
      if not fu.lock and self.can_write_back(fu):
        self.write_back(fu)

    self.clock += 1


if __name__ == '__main__':
  sb = ScoreboardParser.scoreboard_for_asm(ASM_FILE)

  while not sb.done():
    sb.tick()

  # display the final results
  print('                               Read      Execute   Write    ')
  print('                        Issue  Operands  Complete  Result   ')
  print('                    ----------------------------------------')
  for instruction in sb.instructions:
    print(str(instruction))
