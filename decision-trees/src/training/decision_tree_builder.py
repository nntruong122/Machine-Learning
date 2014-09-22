from nary_decision_trees import DecisionTree
from math import log

class DecisionTreeBuilder(object):
  """Contains dataset used to train & build a decisiontree,
     Also contains the decision tree that is learnt"""

  __slots__ = '_dataMatrix', 'decisionTree', '_classLabelIndex', '_rowIndicesSet', '_colIndicesSet'

  def __init__(self, dataMatrix, classLabelIndex = None):
    if not dataMatrix:
      raise ValueError('The data should not be empty')
    self._dataMatrix = dataMatrix
    self.decisionTree = DecisionTree()

    if not classLabelIndex:
      self._classLabelIndex = len(dataMatrix[0]) - 1
    else:
      self._classLabelIndex = classLabelIndex

    self._rowIndicesSet = set(range(len(dataMatrix)))
    self._colIndicesSet = set(range(len(dataMatrix[0]))) - {self._classLabelIndex}

  def build(self, maxDepth = 1, rowIndicesSet = None, colIndicesSet = None, root = None):
    if not rowIndicesSet:
      rowIndicesSet = self._rowIndicesSet
    if not colIndicesSet:
      colIndicesSet = self._colIndicesSet
    if maxDepth < 1:
      raise ValueError('Depth should atleast be 1')

    bestAttrResult = self.getBestAttribute(rowIndicesSet, colIndicesSet)
    conditionAttrIndex = bestAttrResult[0]
    countMap = bestAttrResult[1]
    branchSplitMap = {}
    count = 0

    # To ensure proper order for children
    for attrValue in sorted(countMap[conditionAttrIndex]):
      branchSplitMap[attrValue] = count
      count += 1

    classLabel = self.getClassLabel(countMap[conditionAttrIndex])
    decisionElement = DecisionTree.DecisionElement(conditionAttrIndex, branchSplitMap, classLabel)

    if not root:
      new_root = self.decisionTree.add_root(decisionElement)
    else:
      new_root = self.decisionTree.add_child(root, decisionElement)

    hasZeroEntropy = True
    label = None
    for index in rowIndicesSet:
      if not label:
        label = self._dataMatrix[index][self._classLabelIndex]
      else:
        if label != self._dataMatrix[index][self._classLabelIndex]:
          hasZeroEntropy = False
          break

    # Check if the building the table should be continued
    # 1. Zero entropy
    # 2. has the maxDepth reached
    if hasZeroEntropy or self.decisionTree.height() >= maxDepth:
      return new_root

    # Inserting children in proper order
    for attrValue in sorted(countMap[conditionAttrIndex]):

      nextColIndicesSet = colIndicesSet - {conditionAttrIndex}
      nextRowIndicesSet = countMap[conditionAttrIndex][attrValue]['#']

      # 3. more features and rows remain to be processed
      if len(nextColIndicesSet) > 0 and len(nextRowIndicesSet) > 0:
        self.build(maxDepth, nextRowIndicesSet, nextColIndicesSet, new_root)

    return new_root

  def getBestAttribute(self, rowIndicesSet, colIndicesSet):
    if type(rowIndicesSet) is not set or type(colIndicesSet) is not set:
      raise TypeError('This function expects sets of row and column indices')
    if not rowIndicesSet or not colIndicesSet:
      raise ValueError('The sets should contains atleast one index')

    # If only one attribute is remaining
    if len(colIndicesSet) == 1:
      return list(colIndicesSet)[0]

    countMap = self.prepareCountMap(rowIndicesSet, colIndicesSet)
    entropy = 1.0
    for attribute in countMap:
      new_entropy = self.entropy(countMap[attribute])
      if entropy > new_entropy:
        entropy = new_entropy
        bestAttr = attribute
    return (bestAttr, countMap)

  def prepareCountMap(self, rowIndicesSet, colIndicesSet):
    countMap = {}
    for i in colIndicesSet:
      countMap[i]={}
    for rowNum in rowIndicesSet:
      for attrIndex in colIndicesSet:

        attrValue = self._dataMatrix[rowNum][attrIndex]
        classLabelValue = self._dataMatrix[rowNum][self._classLabelIndex]

        if countMap[attrIndex].has_key(attrValue):
          if countMap[attrIndex][attrValue].has_key(classLabelValue):
            countMap[attrIndex][attrValue][classLabelValue] += 1.0
          else:
            countMap[attrIndex][attrValue][classLabelValue] = 1.0
          countMap[attrIndex][attrValue]['#'].add(rowNum)
        else:
          countMap[attrIndex][attrValue] = {}
          countMap[attrIndex][attrValue][classLabelValue] = 1.0
          countMap[attrIndex][attrValue]['#'] = set([rowNum])
    return countMap

  def entropy(self, attrMap):
    entropy = 0.0
    countPerValue = 0.0
    for attrValueMap in attrMap:
      for classLabel in attrMap[attrValueMap]:
        if classLabel != '#':
          countPerValue += attrMap[attrValueMap][classLabel]

    for attrValueMap in attrMap:
      entropy += self.entropy_contribution(attrMap[attrValueMap], countPerValue)
    return entropy

  def entropy_contribution(self, attrValueMap, countPerAttr):
    valueEntropy = 0.0
    countPerAttrValue = 0.0
    #counts the countPerAttrValue
    for classLabel in attrValueMap:
      if classLabel != '#':
        countPerAttrValue += attrValueMap[classLabel]
    #calculating weighted average for entropy
    for classLabel in attrValueMap:
      if classLabel != '#':
        valueEntropy += -(attrValueMap[classLabel] / countPerAttrValue * \
                        log(attrValueMap[classLabel] / countPerAttrValue, 2)) * \
                        (countPerAttrValue/countPerAttr)
    return valueEntropy

  def getClassLabel(self, attrValueMap):
    classDistribution = {}
    for attrValue in attrValueMap:
      for classLabel in attrValueMap[attrValue]:
        if classLabel != '#':
          if classDistribution.has_key(classLabel):
            classDistribution[classLabel] += 1
          else:
            classDistribution[classLabel] = 1

    count = 0
    for label in classDistribution:
      if classDistribution[label] > count:
        count = classDistribution[label]
        bestClassLabel = label

    return bestClassLabel

  def predict(self, featureArray):
    root = self.decisionTree.root()
    while not self.decisionTree.is_leaf(root):
      conditionAttrIndex = root.element()._conditionAttrIndex
      # The feature values can turn out to be numbers
      branchSplitValue = str(featureArray[conditionAttrIndex])
      if not root.element()._branchSplitMap.has_key(branchSplitValue):
        raise ValueError('Could not predict the classLabel. Unknown feature value')
      childIndex = root.element()._branchSplitMap[branchSplitValue]
      root = self.decisionTree.iThChild(root, childIndex)
    return root.element()._classLabel
