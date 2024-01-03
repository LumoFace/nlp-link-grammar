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
        ## or with 1 if we do, overloaded logic because of no
        ## ternary operator
        i = (left_wall[0] != True and 0 or 1)
        while(i < len(sentence) and i < right_wall[1]):
            print sentence[i],
            i += 1
        print

    def _sentence_len(self, sentence):
        self.sentence_len = len(' '.join(sentence))
        
    def _center_of_word(self, word):
        center = int(math.floor(len(word)/2.0))
        return center
    
    def _words_before_and_after(self, sentence, word):
        if word in sentence:
            idx = sentence.index(word)
            before = sentence[:idx]
            after = sentence[idx+1:]
            return (before, after)
        else:
            print '%s not in %s' % (word, sentence)
            return False
    
    def _before_and_after_lengths(self, before_after):
        before = len(' '.join(before_after[0]))
        after  = len(' '.join(before_after[1]))
        return (before, after)
    
    def _get_tag_placement(self, sentence, word, other_word):
        sentence = self._truncate_walls(sentence)
        self._sentence_len(sentence)
        
        before_after = self._words_before_and_after(sentence, word)
        lengths = self._before_and_after_lengths(before_after)
        left = lengths[0] + self._center_of_word(word)
        left_total = lengths[0] + len(word)
 