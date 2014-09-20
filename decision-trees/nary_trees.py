from trees import Tree

class LinkedNAryTree(Tree):
  """N-aryTree made of nodes related via links"""

  class _Node:
    __slots__ = '_element', '_parent', '_children'
    def __init__(self, element, children, parent = None):
      self._element = element
      self._parent = parent
      if type(children) is not list:
        raise TypeError('children should be a list')
      self._children = children

  class Position(Tree.Position):
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

  def iThChild(self, p, i):
    node = self._validate(p)
    if i >= len(node._children) or i < 0:
      raise ValueError('Invalid index for child')
    return self._make_position(node._children[i])

  def num_children(self, p):
    node = self._validate(p)
    return len(node._children)

  def add_root(self, e):
    if self._root is not None: raise ValueError('Root exists')
    self._size = 1
    # Validate that element e is not null
    self._root = self._Node(e, [])
    return self._make_position(self._root)

  def add_child(self, p, e):
    node = self._validate(p)
    self._size +=1
    child = self._Node(e, [], node)
    node._children.append(child)
    return self._make_position(child)

  def _replace(self, p, e):
    node = self._validate(p)
    old = node._element
    node._element = e
    return old

  def children(self, p):
    node = self._validate(p)
    for child in node._children:
      yield self._make_position(child)
