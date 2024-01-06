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
        
        if other_word:
            next_word = self._words_before_and_after(sentence, other_word)
            next_length = self._before_and_after_lengths(before_after)[0]
            right = left_total + next_length + self._center_of_word(other_word)
        else:
            right = 0
            
        return (left, right)

    def _truncate_walls(self, sentence):
        new_w = []

        left_wall  = self._has('LEFT-WALL',  sentence)
        right_wall = self._has('RIGHT-WALL', sentence)
        
        current = (left_wall[0] != True and 0 or 1)
        while(current < len(sentence) and current < right_wall[1]):
            #self._get_tag_placement(words, words[current], right_word)
            new_w.append(sentence[current])
            current += 1
            
        return new_w
    
    def _draw_tag_placement(self, tag_locations, tag):
        output = []
        i      = 0
        
        if tag == 'RW':
            return

        left = tag_locations[0]
        idx = self.centers.index(left)
        
        if len(self.rows) >= 1 and len(self.last_length) >= 1:
            if self.centers[idx]+2 == self.last_length[-1]:
                add_to_last_row = True
                i = self.last_length[-1]
            else:
                add_to_last_row = False
        else:
            add_to_last_row = False
            
        if len(self.centers) <= 1 or len(self.centers) <= (idx+1):
            while(i < self.centers[idx]):
                output.append(' ')
                i += 1
                
            output.append('+')
            output.append(tag)
            output.append('+')
            self.rows.append(output)
            return
        
        if not add_to_last_row:
            if idx == 0:
                while(i < self.centers[idx]):
                    output.append(' ')
                    i += 1

            else:
                while(i <= self.centers[idx]):
                    output.append(' ')
                    i += 1

            i += 1
            output.append('+')

        tag_len = len(tag)
        tag_center = self._center_of_word(tag)
        tag_diff = self.centers[idx+1] - self.centers[idx]
        tag_draw_center = (tag_diff - tag_len)/2
        tag_distance = tag_draw_center + i

        while(i >= self.centers[idx] and i < tag_distance):
            if add_to_last_row:
                self.rows[-1].append('-')
            else:
                output.append('-')
            i += 1

        i = i + tag_len
        if add_to_last_row:
            self.rows[-1].append(tag)
        else:
            output.append(tag)
