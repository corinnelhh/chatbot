import nltk
sentence = "Nathan ran all the way to the store"
tokens = nltk.tokenize.wordpunct_tokenize(sentence)
posTagged = nltk.pos_tag(tokens)

justTags = []
for word, tag in posTagged:
    justTags.append(tag)
print justTags


grammar1 = nltk.parse_cfg("""
  Sent  -> NP VP
  NP -> Det Nom | PropN
  Nom -> Adj Nom | N
  VP -> V Adj | V NP | V S | V NP PP | V P NP
  PP -> P NP
  PropN -> 'NNP' | 'NNPS'
  Det -> 'DT' | 'a'
  N -> 'NN' | 'NNS'
  Adj  -> 'JJ' | 'JJR' |  'JJS'
  V ->  'VB'  | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ'
  P -> 'TO'
  CC -> 'CC'
  PR -> 'PR'
  RB -> 'RB' | 'RBR' | 'RBS'
  """)

sent = "Mary saw chased angry Bob".split()
rd_parser = nltk.RecursiveDescentParser(grammar1)
for tree in rd_parser.nbest_parse(justTags):
    print tree

print len(rd_parser.nbest_parse(justTags)) > 0
