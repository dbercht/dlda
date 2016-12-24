import nltk
from nltk.tree import Tree
import copy

class Result:
  """Container class to hold results"""
  types = dict({
    'MAGT' : 'time',
    'MAGW' : 'weight',
    'MAGE' : 'energy',
    'MAGD' : 'distance',
    'CD' : 'cycle',
    'MAGR' : 'cycle'
    })
  def __init__(self, resultTuple):
    self.chunk = resultTuple
    resType = resultTuple[-1][1]
    #defaults to cycles
    self.typ = self.types.get(resType, 'cycle')
    self.value = chunkToString(resultTuple)
    self.values = [val for (val, pos) in resultTuple if pos == 'CD']
    self.unit = next((val for (val, pos) in resultTuple if pos.startswith('MAG')), "")
     
  def todict(self):
    return { "type"   : self.typ,
             "value" : self.values,
             "unit" : self.unit
             }

  def tostring(self, indent = 0):
    tab = "".join([" " for x in range(indent)])
    return tab + "- " + self.typ + ": " + ", ".join(self.values) + " " + self.unit


class Trackable:
    """Class to handle trackables"""
    def __init__(self, movement = "", results = None, typ = None, trackables = None, chunk=None):
      self.chunk = chunk
      self.movement = movement
      self.results = results
      self.typ = typ
      self.trackables = trackables
      self.fixmes = [],
      self.certainty = 0

    def todict(self):
      return { "movement" : self.movement,
               "certainty" : self.certainty,
               "results" : [r.todict() for r in self.results],
               "type" : self.typ,
               "fixmes" : self.fixmes,
               "trackables" : [t.todict() for t in self.trackables]
               }
    def tostring(self, indent = 0):
      tab = "".join([" " for x in range(indent)])
      r = "\n".join([r.tostring(indent + 2) for r in self.results])
      t = "\n".join([t.tostring(indent + 4) for t in self.trackables])
      return "%s- %s\n%s\n%s" % (tab, self.movement, r, t)

class Builder:
  """Class to build a trackables from chunks"""


  @staticmethod
  def build(chunk):
    trackable  = Trackable(chunk=chunk)
    nestedTrackables =  []
    fixmes = []
    results = []
    for subtree in chunk:
      if type(subtree) is Tree:
        node = subtree.label()
        if node == 'TRACKABLE': nestedTrackables.append(Builder.build(subtree))
        elif node == 'MOVEMENT': trackable.movement = chunkToString(subtree) 
        elif node == 'RESULT' or node == 'SCHEME': results += buildResults(subtree)
        else:
          fixmes.append(subtree)
      else:
        if type(subtree) is tuple:
          if subtree[1] == 'CD':
            results.append(Result([subtree]))
          else:
            fixmes.append(subtree)

    distTrac = []
    for result in results:
      print "Results"
      print type(result.value)
      if len(result.values) > 1:
        print "List"
        for r in result.values:
          print r
          for t in nestedTrackables:
            print t
            res = copy.deepcopy(result)
            res.values = [r]
            track = copy.deepcopy(t)
            print res.tostring()
            track.results.append(res)
            distTrac.append(track)

    trackable.trackables = nestedTrackables #distTrac
    trackable.results = results
    trackable.fixmes = fixmes
    return trackable

def buildResults(tree):
  isSubTree = False
  results = []
  for t in tree:
    if type(t) is Tree and t.label() == 'RESULT':
      isSubTree = True
      results.append(Result(t))
  if not isSubTree:
    results.append(Result(tree))
  return results

def chunkToString(movChunk):
  mov = []
  for w in movChunk:
    if type(w) is Tree:
      mov.append(chunkToString(w))
    else:
      mov.append(w[0])
  return " ".join(mov)
