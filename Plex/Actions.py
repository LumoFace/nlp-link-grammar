#=======================================================================
#
#   Python Lexical Analyser
#
#   Actions for use in token specifications
#
#=======================================================================

class Action:

  def same_as(self, other):
    return self is other


class Return(Action):
  """
  Internal Plex action which causes |value| to
  be returned as the value of the associated token
  """

  value = None

  def __init__(self, value):
    self.value = value

  def perform(self, token_stream, text):
    return self.value

  def same_as(self, other):
    return isinstance(other, Return) and self.value == other.value

  def __repr__(self):
    return "Return(%s)" % repr(self.value)


class Call(Action):
  """
  Internal Plex action which causes a function to be called.
  """

  function = None

  def __init__(self, function):
    self.function = function

  def perform(self, token_stream, text):
    return self.function(token_stream, text)

  def __repr__(self):
    return "Call(%s)" % self.function.__name__

  def same_as(self, other):
    return isinstance(other, Call) and self.function is other.function


class Begin(Action):
  """
  Begin(state_name) is a Plex action which causes the Scanner to
  enter the state |state_name|. See the docstring of Plex.Lexicon 
  for more in