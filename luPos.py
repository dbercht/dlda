from parse import saveTaggedSent, printFreqDist, getFreqDist, file2array, findNoMov, files2POS
import utilsPickle

def buildTagger():
  print "---------Building Unigrammer"
  data = buildUnigrammer()
  print "---------Fixing initial tokenization"
  data['tokens'][4] = [('bar', 'MOD'), ('muscle', 'MOD'), ('up', 'MOV')]
  data['tokens'][29] = [('knees', 'PART'), ('to', 'TO'), ('elbows', 'PART')]
  data['tokens'][32] = [('muscle', 'MOD'), ('up', 'MOV')]
  data['tokens'][41] = [('ring', 'MOD'), ('muscle', 'MOD'), ('up', 'MOV')]
  data['tokens'][50] = [('toes', 'PART'), ('to', 'TO'), ('bar', 'MOD')]
  data['tokens'][65] = [('strict', 'MOD'), ('muscle', 'MOD'), ('ups', 'MOV')]
  data['tokens'][82] = [('muscle', 'MOD'), ('ups', 'MOV')]
 # data['tokens'][10] = [('muscle', 'MOV'), ('up', 'MOD')]
 # data['tokens'][11] =  [('bar', 'MOD'), ('muscle', 'MOV'), ('up', 'MOD')]
 # data['tokens'][12] =  [('ring', 'MOD'), ('muscle', 'MOV'), ('up', 'MOD')]
  print "---------Building Bigrammer"
  data = buildBigrammer(data['tokens'], data['tagger'])
  utilsPickle.pickleDump(data['tagger'], 'tagger')
  saveTaggedSent(data['tokens'], 'data/tagged_movements.csv')

  printFreqDist(getFreqDist(data['tokens']))
  return data

def buildUnigrammer():
  import nltk, re
  movements = file2array('data/movements.csv')
  POS = getPOS()
  default_tagger = nltk.DefaultTagger("FIXME")
  number_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD')], backoff=default_tagger)
  unigram_tagger = nltk.UnigramTagger(model=POS, backoff=number_tagger)
  tokens = tag_sentences(unigram_tagger, movements)
  findNoMov(tokens) 
  return { 'tagger' : unigram_tagger, 'POS' : POS, 'tokens' : tokens , 'movements' : movements}

def buildBigrammer(tokens, backoff_tagger):
  import nltk
  movements = file2array('data/movements.csv')
  bigram_tagger = nltk.BigramTagger(tokens, backoff=backoff_tagger)
  tokens = tag_sentences(bigram_tagger, movements)
  findNoMov(tokens)
  return {'tagger' : bigram_tagger, 'tokens' : tokens , 'movements' : movements}

def buildTrigrammer(tokens, backoff_tagger):
  import nltk
  movements = file2array('data/movements.csv')
  trigram_tagger = nltk.TrigramTagger(tokens, backoff=backoff_tagger)
  tokens = tag_sentences(trigram_tagger, movements)
  findNoMov(tokens)
  return {'trigram_tagger' : trigram_tagger, 'tokens' : tokens , 'movements' : movements}

def prepare(word):
  import re
  return re.sub(r'[^a-z0-9#@&%]', ' ', word.lower()).strip()

#Gets the POS of all the necessary files
def getPOS():
  return files2POS('POS/parts.csv', 'POS/movements.csv', 'POS/modifiers.csv', 'POS/magnitudes.csv', 'POS/prepositions.csv', 'POS/completions.csv', 'POS/trackables.csv')

def tag_sentences(tagger, sentences):
  return [tag(tagger, sentence) for sentence in sentences]

def getTagger():
  return utilsPickle.pickleLoad('tagger.pkl')

def tag(tagger, sentence):
  return tagger.tag(prepare(sentence).split(" "))

def tag_sentence(sentence):
  return tag(getTagger(), sentence)
