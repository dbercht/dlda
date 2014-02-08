def process(sentence):
  import luChunker, luPos
  return luChunker.chunk(luPos.tag_sentence(sentence))

def recreate():
  import luChunker, luPos
  reload(luPos)
  reload(luChunker)
  luPos.buildTagger()
