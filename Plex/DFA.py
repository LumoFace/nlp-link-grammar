#=======================================================================
#
#   Python Lexical Analyser
#
#   Converting NFA to DFA
#
#=======================================================================

import Machines
from Machines import LOWEST_PRIORITY
from Transitions import TransitionMap

def nfa_to_dfa(old_machine, debug = None):
  """
  Given a nondeterministic Machine, return a new equivalent
  Machine which is deterministic.
  """
  # We build a new machine whose states correspond to sets of states
  # in the old machine. Initially we add a new state corresponding to
  # the epsilon-closure of each initial old state. Then we give transitions
  # to each new state which are the union of all transitions out of any
  # of the corresponding old states. The new state reached on a given
  # character is the one corresponding to the set of states reachable
  # on that character from any of the old states. As new combinations of
  # old states are created, new states are added as needed until closure
  # is reached.
  new_machine = Machines.FastMachine()
  state_map = StateMap(new_machine)
  # Seed the process using the initial states of the old machine.
  # Make the corresponding new states into initial states of the new
  # machine with the same names.
  for (key, old_state) in old_machine.initial_states.items():
    new_state = state_map.old_to_new(epsilon_closure(old_state))
    new_machine.make_initial_state(key, new_state)
  # Tricky bit here: we add things to the end of this list while we're
  # iterating over it. The iteration stops when closure is achieved.
  for new_state in new_machine.states:
    transitions = TransitionMap()
    for old_state in state_map.new_to_old(new_state).keys():
      for event, old_target_states in old_state.transitions.items():
        if event and old_target_states:
          transitions.add_set(event, set_epsilon_closure(old_target_states))
    for event, old_states in transitions.items():
      new_machine.add_transitions(new_state, event, state_map.old_to_new(old_states))
  if debug:
    debug.write("\n===== State Mapping =====\n")
    state_map.dump(debug)
  return new_machine

def set_epsilon_closure(state_set):
  """
  Given a set of states, return the union of the epsilon
  closures of its member states.
  """
  result = {}
  for state1 in state_set.keys():
    for state2 in epsilon_closure(state1).keys():
      result[state2] = 1
  return result

def epsilon_closure(state):
  """
  Return the set of states reachable from the given state
  by epsilon moves.
  """
  # Cache the result
  result = state.epsilon_closure
  if result is None:
    result = {}
    state.epsilon_closure = result
    add_to_epsilon_closure(result, state)
  return result

def add_to_epsilon_closure(state_set, state):
  """
  Recursively add to |state_set| states reachable from the given state
  by epsilon moves.
  """
  if not state_set.get(state, 0):
    state_set[state] = 1
    state_set_2 = state.transitions.get_epsilon()
    if state_set_2:
      for s