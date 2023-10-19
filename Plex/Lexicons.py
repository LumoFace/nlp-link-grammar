
#=======================================================================
#
#   Python Lexical Analyser
#
#   Lexical Analyser Specification
#
#=======================================================================

import types

import Actions
import DFA
import Errors
import Machines
import Regexps

# debug_flags for Lexicon constructor
DUMP_NFA = 1
DUMP_DFA = 2

class State:
  """
  This class is used as part of a Plex.Lexicon specification to
  introduce a user-defined state.

  Constructor:

     State(name, token_specifications)
  """

  name = None
  tokens = None

  def __init__(self, name, tokens):
    self.name = name
    self.tokens = tokens

class Lexicon:
  """
  Lexicon(specification) builds a lexical analyser from the given
  |specification|. The specification consists of a list of
  specification items. Each specification item may be either:

     1) A token definition, which is a tuple:

           (pattern, action)

        The |pattern| is a regular axpression built using the
        constructors defined in the Plex module.

        The |action| is the action to be performed when this pattern
        is recognised (see below).

     2) A state definition:

           State(name, tokens)

        where |name| is a character string naming the state,
        and |tokens| is a list of token definitions as
        above. The meaning and usage of states is described
        below.

  Actions
  -------

  The |action| in a token specication may be one of three things:

     1) A function, which is called as follows:

           function(scanner, text)

        where |scanner| is the relevant Scanner instance, and |text|
        is the matched text. If the function returns anything
        other than None, that value is returned as the value of the
        token. If it returns None, scanning continues as if the IGNORE
        action were specified (see below).

      2) One of the following special actions:

         IGNORE means that the recognised characters will be treated as
                white space and ignored. Scanning will continue until
                the next non-ignored token is recognised before returning.

         TEXT   causes the scanned text itself to be returned as the
                value of the token.

      3) Any other value, which is returned as the value of the token.

  States
  ------

  At any given time, the scanner is in one of a number of states.
  Associated with each state is a set of possible tokens. When scanning,
  only tokens associated with the current state are recognised.

  There is a default state, whose name is the empty string. Token
  definitions which are not inside any State definition belong to