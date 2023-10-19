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
    file.write("Plex.Machine:\n")
    if self.initial_states is not None:
      file.write("   Initial states:\n")
      for (name, state) in self.initial_states.items():
        file.write("      '%s': %d\n" % (name, state.number))
    for s in self.states:
      s.dump(file)

class Node:
  """A state of an NFA or DFA."""
  transitions = None       # TransitionMap
  action = None            # Action
  action_priority = None   # integer
  number = 0               # for debug output
  epsilon_closure = None   # used by nfa_to_dfa()

  def __init__(self):
    # Preinitialise the list of empty transitions, because
    # the nfa-to-dfa algorithm needs it
    #self.transitions = {'':[]}
    self.transitions = TransitionMap()
    self.action_priority = LOWEST_PRIORITY

  def destroy(self):
    #print "Destroying", self ###
    self.transitions = None
    self.action = None
    self.epsilon_closure = None

  def add_transition(self, event, new_state):
    self.transitions.add(event, new_state)
  
  def link_to(self, state):
    """Add an epsilon-move from this state to another state."""
    self.add_transition('', state)

  def set_action(self, action, priority):
    """Make this an accepting state with the given action. If 
    there is already an action, choose the action with highest
    priority."""
    if priority > self.action_priority:
      self.action = action
      self.action_priority = priority

  def get_action(self):
    return self.action

  def get_action_priority(self):
    return self.action_priority

#	def merge_actions(self, other_state):
#		"""Merge actions of other state into this state according
#    to their priorities."""
#		action = other_state.get_action()
#		priority = other_state.get_action_priority()
#		self.set_action(action, priority)

  def is_accepting(self):
    return self.action is not None

  def __str__(self):
    return "State %d" % self.number

  def dump(self, file):
    import string
    # Header
    file.write("   State %d:\n" % self.number)
    # Transitions
#		self.dump_transitions(file)
    self.transitions.dump(file)
    # Action
    action = self.action
    priority = self.action_priority
    if action is not None:
      file.write("      %s [priority %d]\n" % (action, priority))
  

class FastMachine:
  """
  FastMachine is a deterministic machine represented in a way that
  allows fast scanning.
  """
  initial_states = None # {state_name:state}
  states = None         # [state]
                        # where state = {event:state, 'else':state, 'action':Action}
  next_number = 1       # for 