
#Dumps a pickle
def pickleDump(tagger, filename):
    from cPickle import dump
    output = open(filename+'.pkl', 'wb')
    dump(tagger, output, -1)
    output.close()

#Eats a pickle
def pickleLoad(filename):
  from cPickle import load
  input = open(filename, 'rb')
  var = load(input)
  input.close()
  return var
