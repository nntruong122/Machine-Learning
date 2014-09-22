from linked_binary_trees import LinkedBinaryTree

class DecisionTree(LinkedBinaryTree):
  """Abstraction to represent DecisionTree with binary splits"""

  class DecisionElement:
    __slots__ = '_conditionAttrIndex', '_leftSplitValue', '_classLabel'
    def __init__(self, conditionAttrIndex = None, leftSplitValue = None, classLabel = None):
      self._conditionAttrIndex = conditionAttrIndex
      self._leftSplitValue = leftSplitValue
      self._classLabel = classLabel

  def __init__(self):
    super(DecisionTree, self).__init__()

  def add_left(self, p, e):
    if not isinstance(e, self.DecisionElement) or e._classLabel is None:
      raise TypeError('leaf node should have a classLabel associated')
    if None in (p.element()._leftSplitValue, p.element()._conditionAttrIndex):
      raise ValueError('parent should have condition parameters')
    return super(DecisionTree, self).add_left(p, e)

  def add_right(self, p, e):
    if not isinstance(e, self.DecisionElement) or e._classLabel is None:
      raise TypeError('leaf node should have a classLabel associated')
    if None in (p.element()._leftSplitValue, p.element()._conditionAttrIndex):
      raise ValueError('parent should have condition parameters')
    return super(DecisionTree, self).add_right(p, e)

  def add_root(self, e):
    if not isinstance(e, self.DecisionElement) or None in (e._classLabel, e._conditionAttrIndex, e._leftSplitValue):
      raise TypeError('Root node should have a complete DecisionElement')
    return super(DecisionTree, self).add_root(e)
