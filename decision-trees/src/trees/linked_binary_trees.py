from binary_trees import BinaryTree

class LinkedBinaryTree(BinaryTree):
  """BinaryTree made of nodes related via links"""

  class _Node:
    __slots__ = '_element', '_left', '_right', '_parent'
    def __init__(self, element, parent = None, left = None, right = None):
      self._element = element
      self._parent = parent
      self._left = left
      self._right = right

  class Position(BinaryTree.Position):
    """docstring for Position"""
    def __init__(self, container, node):
      self._container = container
      self._node = node

    def element(self):
      return self._node._element

    def __eq__(self, other):
      return type(other) is type(self) and other._node is self._node

  def _validate(self, p):
    if not isinstance(p, self.Position):
      raise TypeError('p must be proper Position type')
    if p._container is not self:
      raise ValueError('p does not belong to this container')
    if p._node._parent is p._node:      # Convention for deprecated nodes
      raise ValueError('p is no longer valid')
    return p._node

  def _make_position(self, node):
    return self.Position(self, node) if node is not None else None

  def __init__(self):
    self._root = None
    self._size = 0

  def __len__(self):
    return self._size

  def root(self):
    return self._make_position(self._root)

  def parent(self, p):
    node = self._validate(p)
    return self._make_position(node._parent)

  def left(self, p):
    node = self._validate(p)
    return self._make_position(node._left)

  def right(self, p):
    node = self._validate(p)
    return self._make_position(node._right)

  def num_children(self, p):
    node = self._validate(p)
    count = 0
    if node._left is not None:
      count += 1
    if node._right is not None:
      count += 1
    return count

  def add_root(self, e):
    if self._root is not None: raise ValueError('Root exists')
    self._size = 1
    # Validate that element e is not null
    self._root = self._Node(e)
    return self._make_position(self._root)

  def add_left(self, p, e):
    node = self._validate(p)
    if node._left is not None: raise ValueError('Left Child exists')
    self._size += 1
    # Validate that element e is not null
    node._left = self._Node(e, node)
    return self._make_position(node._left)

  def add_right(self, p, e):
    node = self._validate(p)
    if node._right is not None: raise ValueError('Right Child exists')
    self._size += 1
    # Validate that element e is not null
    node._right = self._Node(e, node)
    return self._make_position(node._right)

  def _replace(self, p, e):
    node = self._validate(p)
    old = node._element
    node._element = e
    return old
