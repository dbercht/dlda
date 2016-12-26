import nltk
from utilsPickle import pickleDump, pickleLoad


def buildPOSChunker(verbose = False):
  grammar = """
MOVEMENT: }<MOVP><MOVP>+{ #Don't chunk multiple plural movements
MOVEMENT: {<PART>?<TO>?<MOD>*<MOV><MOD>*<MOV>?} #Movement must be refined
MOVEMENT: {<MOD>?<MOD>?<PART>?<TO>?<MOD|PART>+<MOV>?} #Movement must be refined
MOVEMENT: {<MOVEMENT><AND><MOVP>}
MOVEMENT: {<MOVEMENT>*<MOVP>}

RESULT: }<CD><CD>+<MAG.*><MOV.*>{ #not scheming series if sequence after
RESULT: {<CD>+<AND><CD><MAG.*>} #not scheming series if sequence after
RESULT: {<CD><MAG.*>} #x, y, z MAG
RESULT: {<FOR>?<CD><CD><CD>+<MAG.*>} #x, y, z MAG
RESULT: {<RESULT><AND><RESULT>}

TRACK: {<FOR><TRCK>} # for time/load/weight/distance
SCHEME: {<CD><CD><CD>+} #x,y,z

TRACKABLE: }<MOVEMENT|TRACKABLE><MOVEMENT>+<AT><RESULT>{
TRACKABLE: {<CD>?<MOVEMENT><AT><RESULT>}
TRACKABLE: {<CD><RESULT>?<MOVEMENT>} #21 pullups
TRACKABLE: }<RESULT><MOVEMENT><RESULT><MOVEMENT>{
TRACKABLE: {<RESULT>?<MOVEMENT><RESULT>?} #135 pound thruster
"""
  
  print "---------Building Regex POS Chunker"
  if verbose: print grammar
  cp = nltk.RegexpParser(grammar, loop=3)
  pickleDump(cp, 'POS_chunker')
  return cp

def chunkTags(sentence):
  return chunk(pickleLoad('POS_chunker'), sentence)

def chunk(chunker, sentence):
  return chunker.parse(sentence)
