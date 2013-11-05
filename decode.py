# decode.py - creates instructions from decoded text
# each function takes a tokenized instruction string
# and returns an instruction
import re

"""The instruction class defines an instruction in the scoreboard.
Each instruction is not only capable of holding its operands, destination,
and operation. It also holds the string representation of the instruction
as it was read in the assembly file as well as the cycles that it finishes
certain stages in"""
class Instruction:

  def __init__(self, repr, op, dst, src1, src2):
    self.issue = self.read_ops = self.ex_cmplt = self.write_res = -1
    self.op = op          # instruction operation
    self.fi = dst         # destination register
    self.fj = src1        # source register
    self.fk = src2        # source register
    self.repr = repr      # the string representation

  def __str__(self):
    return "%-24s%-7d%-10d%-10d%-8d" % \
        (self.repr, self.issue, self.read_ops, self.ex_cmplt, self.write_res)


"""Utility method to tokenize an instruction string"""
def tokenize_instruction(instruction):
  tokens = re.split(',| ', instruction)
  return list(filter(None, tokens))   # remove empty strings if any

"""Load immediate instruction"""
def __li(inst):
  inst_toks = tokenize_instruction(inst)
  op = 'integer'
  fi = inst_toks[1]
  return Instruction(inst, op, fi, None, None)

"""Generic load or store instruction"""
def __load_store(inst):
  inst_toks = tokenize_instruction(inst)
  op = 'integer'
  fi = inst_toks[1]
  fk = re.search('\((.*)\)', inst_toks[2]).group(1)    # extract register
  return Instruction(inst, op, fi, None, fk)

"""Generic add, subtract, multiply or divide instruction"""
def __arithmetic(inst):
  inst_toks = tokenize_instruction(inst)
  op = unit_for_instruction[inst_toks[0]]
  fi = inst_toks[1]
  fj = inst_toks[2]
  fk = inst_toks[3]
  return Instruction(inst, op, fi, fj, fk)

"""Generic arthmetic operation with immediate"""
def __arithmetici(inst):
  inst_toks = tokenize_instruction(inst)
  op = unit_for_instruction[inst_toks[0]]
  fi = inst_toks[1]
  fj = inst_toks[2]
  return Instruction(inst, op, fi, fj, None)

""" This dictionary has operations as keys and has values of functions
that correspond to those operations. The functions will parse and instruction
of a certain operation and return a representation that can be used within
the scoreboard itself"""
instructions = {
    'LI':     __li,               # INTEGER unit
    'LW':     __load_store,
    'SW':     __load_store,
    'LD':     __load_store,
    'SD':     __load_store,
    'ADD':    __arithmetic,
    'ADDI':   __arithmetici,
    'SUB':    __arithmetic,
    'SUBI':   __arithmetici,
    'ADDD':   __arithmetic,       # ADD unit
    'SUBD':   __arithmetic,
    'MULTD':  __arithmetic,       # MULT unit
    'DIVD':   __arithmetic,       # DIV unit
    }


unit_for_instruction = {
    'ADD':    'integer',
    'ADDI':   'integer',
    'SUB':    'integer',
    'SUBI':   'integer',
    'ADDD':   'add',       # ADD unit
    'SUBD':   'add',
    'MULTD':  'mult',       # MULT unit
    'DIVD':   'div',       # DIV unit
    }
