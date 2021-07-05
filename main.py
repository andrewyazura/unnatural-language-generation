import tokenize_uk as tn
from text_generation import tokens_to_graph

with open('tmp/text.txt', 'r') as f:
    t = f.read()

tokens = tn.tokenize_words(t)
graph = tokens_to_graph(tokens)
