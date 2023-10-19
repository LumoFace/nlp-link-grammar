#=======================================================================
#
#   Python Lexical Analyser
#
#   Classes for building NFAs and DFAs
#
#=======================================================================

import string
import sys
from sys import maxint
from types import TupleType

from Transitions import TransitionMap

LOWEST_PRIORITY = -sys.maxint

class Machine:
  """A collection of Nodes representing an NFA or DFA."""
  states = None         # [Node]
  next_state_number = 1
  initial_states = None # {(name, bol): Node}

  def __init__(self):
    self.states = []
    self.initial_states = {}

  def __del__(self):
    #print "Destroying", self ###
    for state in self.states:
      state.destroy()

  def new_state(self):
    """Add a new state to the machine and return it."""
    s = Node()
    n = self.next_state_number
    self.next_state_number = n + 1
    s.number = n
    self.states.append(s)
    return s

  def new_initial_state(self, name):
    state = self.new_state()
    self.make_initial_state(name, state)
    return state

  def make_initial_state(self, name, state):
    self.initial_states[name] = state

  def get_initial_state(self, name):
    return self.initial_states[name]
  
  def dump(self, file):
    file.write(