import nltk
sentence = "They are fully rewarded for their treachery."
tokens = nltk.tokenize.wordpunct_tokenize(sentence)
posTagged = nltk.pos_tag(tokens)

justTags = []
for word, tag in posTagged:
    justTags.append(tag)
print justTags


grammar1 = nltk.parse_cfg("""
  Sent  -> NP VP | NP VP END
  NP -> Det Nom | PropN | Det NP | N | PR
  Nom -> Adj Nom | N
  VP -> V Adj | V NP | V S | V NP PP | V Prep NP | V
  PP -> Prep NP
  PropN -> 'NNP' | 'NNPS'
  Det -> 'DT' | 'a'
  N -> 'NN' | 'NNS'
  Adj  -> 'JJ' | 'JJR' |  'JJS'
  V ->  'VB'  | 'VBD' | 'VBG' | 'VBN' | 'VBP' | 'VBZ'
  Prep -> 'TO' | 'IN'
  CC -> 'CC'
  PR -> 'PRP' | 'PRP$'
  RB -> 'RB' | 'RBR' | 'RBS'
  END -> '.' | '?' | '!'
  """)

rd_parser = nltk.RecursiveDescentParser(grammar1)
try:
    for tree in rd_parser.nbest_parse(justTags):
        print tree
    print len(rd_parser.nbest_parse(justTags)) > 0
except ValueError:
    print "Unrecognized Character"
