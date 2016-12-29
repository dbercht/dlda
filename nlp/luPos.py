from parse import saveTaggedSent, printFreqDist, getFreqDist, file2array, findNoMov, files2POS
import utilsPickle

def buildTagger(verbose=False):
  movements = file2array('./nlp/data/movements.csv')
  print "---------Building Unigrammer"
  unigrammer = buildUnigrammer()
  tokens = tag_sentences(unigrammer, movements)
  if verbose: findNoMov(tokens) 
  print "---------Building Bigrammer"
  bigrammer = buildBigrammer(tokens, unigrammer)
  tokens = tag_sentences(bigrammer, movements)
  if verbose: findNoMov(tokens)
  utilsPickle.pickleDump(bigrammer, 'tagger')
  saveTaggedSent(tokens, './nlp/data/tagged_movements.csv')

  if verbose: printFreqDist(getFreqDist(tokens))
  return bigrammer

def buildUnigrammer():
  import nltk, re
  POS = getPOS()
  default_tagger = nltk.DefaultTagger("FIXME")
  number_tagger = nltk.RegexpTagger([(r'^-?[0-9]+(.[0-9]+)?$', 'CD')], backoff=default_tagger)
  unigram_tagger = nltk.UnigramTagger(model=POS, backoff=number_tagger)
  return unigram_tagger

def buildBigrammer(tokens, backoff_tagger):
  import nltk
  bigram_tagger = nltk.BigramTagger(tokens, backoff=backoff_tagger)
  return bigram_tagger

def buildTrigrammer(tokens, backoff_tagger):
  import nltk
  movements = file2array('./nlp/data/movements.csv')
  trigram_tagger = nltk.TrigramTagger(tokens, backoff=backoff_tagger)
  tokens = tag_sentences(trigram_tagger, movements)
  findNoMov(tokens)
  return {'trigram_tagger' : trigram_tagger, 'tokens' : tokens , 'movements' : movements}

def prepare(word):
  import re
  word = re.sub(r'[^a-z0-9#@&%]', ' ', word.replace('\\n', ' ').replace('\\r', '').lower()).strip()
  word = ' '.join(word.split())  # remove multiple whitespaces
  return word

#Gets the POS of all the necessary files
def getPOS():
  pos = files2POS(
    './nlp/POS/completions.csv',
    './nlp/POS/magnitudes.csv',
    './nlp/POS/modifiers.csv',
    './nlp/POS/movements.csv',
    './nlp/POS/parts.csv',
    './nlp/POS/prepositions.csv',
    './nlp/POS/trackables.csv',
  )
  return dict([(prepare(word), pos[word]) for word in pos.keys()])

def tag_sentences(tagger, sentences):
  return [tag(tagger, sentence) for sentence in sentences]

def getTagger():
  return utilsPickle.pickleLoad('tagger')

def tag(tagger, sentence):
  return tagger.tag(prepare(sentence).split(" "))

def tag_sentence(sentence):
  return tag(getTagger(), sentence)
