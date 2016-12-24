# NOTE: Unsafe assumption that all pickles are in current dir

#Dumps a pickle
def pickleDump(tagger, filename):
    from cPickle import dump
    output = open('./pickles/' + filename + '.pkl', 'wb')
    dump(tagger, output, -1)
    output.close()

#Eats a pickle
def pickleLoad(filename):
  from cPickle import load
  filename += '.pkl'
  input = open('./pickles/' + filename, 'rb')
  var = load(input)
  input.close()
  return var
