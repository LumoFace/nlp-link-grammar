from csc.util.persist import get_picklecached_thing
from csc.nl import get_nl
from csc.nl.euro import LemmatizedEuroNL
from csc.conceptnet4.models import *
from csc.conceptnet4.analogyspace import conceptnet_2d_from_db
#from csc.divisi.flavors import ConceptByFeatureMatrix

from debug import *

weighted_triples = [
    (('baseball', 'IsA', 'sport'), 3.6),

]
#matrix = ConceptByFeatureMatrix.from_triples(weighted_triples)

class Analogies:
    def __init__(self):
        #self.tensor = get_picklecached_thing('tensor.gz')
        #self.svd = self.tensor.svd(k=50)
        self.en_nl = get_nl('en')
        self.normalizer = LemmatizedEuroNL('en')
        self.cnet = conceptnet_2d_from_db('en')
        self.analogyspace = self.cnet.svd(k=100)

    def similar(self, word_container):
        untagged = []
        last = []
        for words in word_container.tagged_words:
            normal = self.normalizer.normalize(words[0])
            untagged.append(norm