import nltk

def buildChunker():
  grammar = """
MOVEMENT: {<PART>?<TO>?<MOD|MOV>+} #Movement must be refined
RESULT: {<CD>+<MAG.*><AND><CD>+<MAG.*>} #x minutes/rounds and y seconds/reps
RESULT: {<CD>+<MAG.*>} #x, y, z MAG
SCHEME: {<CD>+} #x,y,z

"""
  cp = nltk.RegexpParser(grammar)
  return cp

def chunk(sentences):
  return buildChunker().parse(sentences)
