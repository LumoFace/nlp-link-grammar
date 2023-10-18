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
  ""