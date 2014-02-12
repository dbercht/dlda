import nltk
from nltk.tree import Tree

class Result:
  """Container class to hold results"""
  def __init__(self, resultTuple):
    self.value = resultTuple
  
  def todict(self):
    return { "result" : self.value }

class Trackable:
    """Class to handle trackables"""
    def __init__(self, movement = "", results = [], typ = "", trackables = []):
      self.movement = movement
      self.results = results
      self.typ = typ
      self.trackables = trackables
      self.scheme = []

    def todict(self):
      return { "movement" : self.movement,
               "results" : [r.todict() for r in self.results],
               "type" : self.typ,
               "trackables" : [t.todict() for t in self.trackables],
               "scheme" : self.scheme }

class Builder:
  """Class to build a trackables from chunks"""


  @staticmethod
  def build(chunk):
    print "Building "
    trackable  = Trackable()
    nestedTrackables =  []
    results = []
    for subtree in chunk:
      if type(subtree) is Tree:
        node = subtree.node
        if node == 'TRACKABLE': nestedTrackables.append(Builder.build(subtree))
        if node == 'SCHEME': trackable.scheme = [w for (w, pos) in subtree]
        if node == 'MOVEMENT': trackable.movement = " ".join([w for (w, pos) in subtree])
        if node == 'RESULT':
          print subtree
          results.append(Result(" ".join([w for (w, pos) in subtree])))
      else:
        print "NO", subtree
    trackable.trackables = nestedTrackables
    trackable.results = results
    return trackable
