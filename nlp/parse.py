def saveTaggedSent(tagged_sent, file_name):
  arr = []
  for token in tagged_sent:
    string = []
    for (word,pos) in token:
      string.append("%s/%s" % (word, pos))
    arr.append(";".join(string))
  f = open(file_name, 'w')
  f.write("\n".join(arr))
  f.close()


def printFreqDist(fdist):
  print "%5s %s" % ("freq", "pos")
  for key in fdist.keys():
    print "%6.2f %s" % (fdist[key], key)

def getFreqDist(token_sents):
  import nltk
  arr = []
  for token_sent in token_sents:
    posA = []
    prev = 'N'
    accounted = False
    for (word, pos) in token_sent:
      if prev != pos and pos != 'AND':
        posA.append(pos)
      else:
        if not accounted:
          accounted = True
          posA.append('+')
      if pos != 'AND':
        prev = pos
    arr.append('-'.join(posA))
    accounted = False
  return nltk.FreqDist(arr)
    

#Reads a file and places its contents in an array
def file2array(file):
  with open(file, 'r') as f:
    return [line.strip() for line in f]

#Takes in a csv file as an array and voncerts it to a word/POS tuple array
def array2POS(csvArray):
  return dict((mod.split(";")[0], mod.split(";")[1]) for mod in csvArray)

#Aggregates files to their POS
#Takes in a csv file as an array and voncerts it to a word/POS tuple array
def array2ResType(csvArray):
  # (Result, num_movements, type)
  return [(resType.split(";")[0], resType.split(";")[1], resType.split(";")[2]) for resType in csvArray]

def files2POS(*files):
  arr = []
  for file in files:
    arr = arr + file2array(file)
  return array2POS(arr)

def loadDump():
  arr = []
  return array2ResType(file2array('./nlp/data/dump.csv'))


#Pretty print
def posAndWord(posTuples):
  for token in posTuples:
    poss = ''
    move = ''
    for (word, pos) in token:
      poss += ' ' + pos
      move += ' ' + word
    print "%44s :%s" % (poss, move)

def findNoMov(tokens):
  count = 0
  for (i, tokenA) in enumerate(tokens):
      movs = 0
      fixMe = False
      for (word, pos) in tokenA:
        if pos.startswith('MOV') : movs += 1
        if pos == 'FIXME' : fixMe = True
      if fixMe or movs != 1: 
        print i, movs, tokenA
        count += 1
  print "Total: %d" % (count)