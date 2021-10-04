'''
Brill Tagger

The Brill Tagger is a transformational rule-based tagger.
It starts by running an initial tagger, and then
improves the tagging by applying a list of transformation rules.
These transformation rules are automatically learned from the training
corpus, based on one or more "rule templates."
https://www.nltk.org/api/nltk.tag.html?highlight=brill%20tag#module-nltk.tag.brill
from nltk.corpus import brown
from nltk.tag import UnigramTagger
from nltk.tag.brill import nltkdemo18

************************************************************************************************'''
import nltk
from nltk.corpus import treebank
from nltk.tag.brill import BrillTaggerTrainer, Word, Pos, Template, Tag


training_data = treebank.tagged_sents()[:100]
baseline_data = treebank.tagged_sents()[100:200]
gold_data = treebank.tagged_sents()[200:300]
testing_data = [nltk.untag(s) for s in gold_data]
Template._cleartemplates()
templates = [Template(Pos([-1])), Template(Pos([-1]), Word([0]))]
templates = [                  # or start, end args (as in nltk2):
    Template(Word([-3,-2,-1])), # Template(Word(-3, -1))
    Template(Word([1,2,3])),    # Template(Word(1, 3))
    Template(Tag([-1]), Tag([1])),
    Template(Tag([-1]), Word([1,2]))
]
backoff = nltk.RegexpTagger([
    (r'^-?[0-9]+(.[0-9]+)?$', 'CD'),   # cardinal numbers
    (r'(The|the|A|a|An|an)$', 'AT'),   # articles
    (r'.*able$', 'JJ'),                # adjectives
    (r'.*ness$', 'NN'),                # nouns formed from adjectives
    (r'.*ly$', 'RB'),                  # adverbs
    (r'.*s$', 'NNS'),                  # plural nouns
    (r'.*ing$', 'VBG'),                # gerunds
    (r'.*ed$', 'VBD'),                 # past tense verbs
    (r'.*', 'NN')                      # nouns (default)
])
baseline = backoff
print(baseline.evaluate(gold_data))
tt = BrillTaggerTrainer(baseline, templates, trace=3)
tagger1 = tt.train(training_data, max_rules=10)
