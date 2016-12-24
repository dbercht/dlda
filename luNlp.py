from __future__ import division
import nltk, luPos, luChunker, parse

def analyze_sentence(sentence):
    #  Double process for recursive purposes
    return process(process(sentence))

def process(result):
  import luChunker, luPos
  if type(result) is str:
    return luChunker.chunkTags(luPos.tag_sentence(result))
  else:
    return luChunker.chunkChunks(result)

def processDump():
  import parse
  for (result, t) in parse.loadDump():
    print process(result)

def recreate(verbose = False):
  import luChunker, luPos, parse
  print "LimbrUp NLP process commence :)"
  print "-------------------------------\n"
  reload(parse)
  reload(luPos)
  reload(luChunker)
  luPos.buildTagger(verbose)
  luChunker.buildPOSChunker(verbose)

  tests = []
  tests.append(testMovements())
  tests.append(testDump())

  print "%10s %4s %4s" % ("Test", "Len", "Exp")
  for test in tests:
    print "%10s: %6d|%6d|%6.2f%%" % test

def testPOSChunks():
  tests = parse.loadDump()
  for (result, x, y) in tests:
    els = []
    for t in process(process(result)):
      if type(t) is nltk.Tree:
        els.append(t.label())
      else:
        els.append(t[1])
    print result
    print " ".join(els) + "\n"




def testDump():
  tests = parse.loadDump()
  return testChunker(tests, "Dump")

def testMovements():
  movements = [(movement, 1, "") for movement in parse.file2array('data/movements.csv')]
  return testChunker(movements, "Movements") 

def testChunker(tests, title = ""):
  #(string, number_movements)
  print "\n------------------------Start test " + title
  errors = 0
  for (result, numMovements, rType) in tests:
    numMovements = int(numMovements)
    chunk = process(result)
    mov = movements(chunk)
    if len(mov) != numMovements: 
      errors += 1
      print "- %4d movements found, expected %d" % (len(mov), numMovements)
      print result
      print mov
      print chunk
      print
  print "\n------------------------End test " + title
  return (title, len(tests), errors, 100*(len(tests)-errors)/len(tests)) 

def movements(chunk):
  arr = []
  for subtree in chunk:
    if type(subtree) is nltk.Tree and subtree.label() == 'MOVEMENT':
      arr.append(stringify(subtree))
    else:
      arr +=  [stringify(p) for p in subtree if type(p) is nltk.Tree and p.label() == 'MOVEMENT']
  return arr

def stringify(chunk):
  return " ".join([word for (word, pos) in chunk.leaves()])

