import random
import copy
import nltk
from enum import Enum
from nltk.tree import Tree

class Type(Enum):
    #  TODO: Allow alias, e.g. 'load' should be 'weight'
    TIME = 'time'
    WEIGHT = 'weight'
    ENERGY = 'energy'
    DISTANCE = 'distance'
    CYCLE = 'cycle'

class Result:
  """Container class to hold results"""

  types = dict({
    'MAGT': Type.TIME,
    'MAGW': Type.WEIGHT,
    'MAGE': Type.ENERGY,
    'MAGD': Type.DISTANCE,
    'CD': Type.CYCLE,
    'MAGR': Type.CYCLE,
    })

  def __init__(self, resultTuple):
    self.id_ = random.getrandbits(128)
    self.chunk = resultTuple
    resType = resultTuple[-1][1]
    #  defaults to cycles
    self.typ = self.types.get(resType, 'cycle')
    self.value = chunkToString(resultTuple)
    self.values = [val for (val, pos) in resultTuple if pos == 'CD']
    self.unit = next((val for (val, pos) in resultTuple if pos.startswith('MAG')), "")

  def todict(self):
    return { "type"   : self.typ.value if self.typ else None,
             "values" : self.values,
             "unit" : self.unit,
             "id": self.id_,
             }

  def tostring(self, indent = 0):
    tab = "".join([" " for x in range(indent)])
    return tab + "- " + self.typ + ": " + ", ".join(self.values) + " " + self.unit


class Trackable:
    """Class to handle trackables"""
    def __init__(self, movement = "", results = None, typ = None, trackables = None, chunk=None):
      self.id_ = random.getrandbits(128)
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
               "type" : self.typ.value if self.typ else None,
               "fixmes" : self.fixmes,
               "trackables" : [t.todict() for t in self.trackables],
               "id": self.id_,
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
        elif node == 'TRACK': 
            tracking = [ele for ele in subtree if ele[1] == 'TRCK']
            if tracking:
                trackable.typ = Type(tracking[0][0])
        else:
            fixmes.append({'word': subtree[0], 'pos': subtree[1], 'id': random.getrandbits(128) })
      else:
        if type(subtree) is tuple:
          if subtree[1] == 'CD':
            results.append(Result([subtree]))
          else:
            fixmes.append({'word': subtree[0], 'pos': subtree[1], 'id': random.getrandbits(128) })

    #  distributing the multiple result values tot he child trackables
    distTrac = []
    for result in results:
      if len(result.values) > 1:
        for r in result.values:
          for t in nestedTrackables:
            res = copy.deepcopy(result)
            res.values = [r]
            track = copy.deepcopy(t)
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
