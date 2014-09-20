from nary_trees import LinkedNAryTree

class DecisionTree(LinkedNAryTree):
  """Abstraction to represent DecisionTree with binary splits"""

  class DecisionElement:
    __slots__ = '_conditionAttrIndex', '_branchSplitMap', '_classLabel'
    def __init__(self, conditionAttrIndex = None, branchSplitMap = {}, classLabel = None):
      self._conditionAttrIndex = conditionAttrIndex
      if type(branchSplitMap) is not dict:
        raise TypeError('branch splits should be a map')
      self._branchSplitMap = branchSplitMap
      self._classLabel = classLabel

    def addSplitEntry(self, key, value):
      self._branchSplitMap[key] = value

    def setConditionAttrIndex(self, index):
      self._conditionAttrIndex = index

    def setClassLabel(self, label):
      self._classLabel = label

  def __init__(self):
    super(DecisionTree, self).__init__()

  def add_child(self, p, e):
    if not isinstance(e, self.DecisionElement) or e._classLabel is None:
      raise TypeError('leaf node should have a classLabel associated')
    if len(p.element()._branchSplitMap) == 0 or p.element()._conditionAttrIndex is None:
      raise ValueError('parent should have condition parameters')
    return super(DecisionTree, self).add_child(p, e)

  def add_root(self, e):
    if not isinstance(e, self.DecisionElement) or None in (e._classLabel, e._conditionAttrIndex) or len(e._branchSplitMap) == 0:
      raise TypeError('Root node should have a complete DecisionElement')
    return super(DecisionTree, self).add_root(e)