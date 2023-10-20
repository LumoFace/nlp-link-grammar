#=======================================================================
#
#	 Python Lexical Analyser
#
#	 Regular Expressions
#
#=======================================================================

import array
import string
import types
from sys import maxint

import Errors

#
#	 Constants
#

BOL = 'bol'
EOL = 'eol'
EOF = 'eof'

nl_code = ord('\n')

#
#	 Helper functions
#

def chars_to_ranges(s):
	"""
	Return a list of character codes consisting of pairs
	[code1a, code1b, code2a, code2b,...] which cover all
	the characters in |s|.
	"""
	char_list = list(s)
	char_list.sort()
	i = 0
	n = len(char_list)
	result = []
	whil