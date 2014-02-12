import nltk
from utilsPickle import pickleDump, pickleLoad


def buildPOSChunker(verbose = False):
  grammar = """
MOVEMENT: }<MOVP><MOVP>+{ #Don't chunk multiple plural movements
MOVEMENT: {<PART>?<TO>?<MOD>*<MOV><MOD>*<MOV>?} #Movement must be refined
MOVEMENT: {<MOD>?<MOD>?<PART>?<TO>?<MOD|PART>+<MOV>?} #Movement must be refined
MOVEMENT: {<MOVEMENT><AND><MOVP>}
MOVEMENT: {<MOVEMENT>*<MOVP>}

RESULT: {<CD>+<MAG(R|T)><AND><CD>+<MAG(R|T)>} #x minutes/rounds and y seconds/reps
RESULT: }<CD><CD>+<MAG.*><MOV.*>{ #not scheming series if sequence after
RESULT: {<FOR>?<CD>+<MAG.*>} #x, y, z MAG

TRACK: {<FOR><TRCK>} # for time/load/weight/distance

SCHEME: {<CD><CD>+} #x,y,z

TRACKABLE: }<MOVEMENT|TRACKABLE><MOVEMENT>+<AT><RESULT>{
TRACKABLE: {<CD>?<MOVEMENT><AT><RESULT>}
TRACKABLE: {<CD><MOVEMENT>} #21 pullups
TRACKABLE: {<RESULT>?<MOVEMENT><RESULT>?} #135 pound thruster
"""
  
  print "---------Building Regex POS Chunker"
  if verbose: print grammar
  cp = nltk.RegexpParser(grammar, loop=3)
  pickleDump(cp, 'POS_chunker')
  return cp

def chunkTags(sentence):
  return chunk(pickleLoad('POS_chunker'), sentence)

def chunkChunks(chunks):
  return chunk(pickleLoad('chunk_chunker'), chunks)

def chunk(chunker, sentence):
  return chunker.parse(sentence)
