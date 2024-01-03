from structures.atoms import Atoms
import math

class linkgrammar_tree:
    def load_into_atoms(self):
        pass
    

class Print:
    def _has(self, has, sentence):
        if has in sentence:
            has = sentence.index(has)
            return (True, has)
        else:
            return (False, 0)
        
    def print_sentence(self, sentence):
        left_wall  = self._has('LEFT-WALL',  sentence)
        right_wall = self._has('RIGHT-WALL', sentence)
        ## start the indexer at 0 if we dont have the left wall
        ## or with 1 if we do, overloaded logic bec