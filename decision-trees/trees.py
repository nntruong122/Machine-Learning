class Tree(object):
  """Abstract base class representing a tree structure."""
  class Position:
    """An abstraction representing the placement of a single element."""

    def element(self):
      """Return the element stored at this Position."""
      raise NotImplementedError('must be implemented by subclass')

    def __eq__(self, other):
      """Return true if other position represents the same location."""
      raise NotImplementedError('must be implemented by subclass')

    def __ne__(self, other):
      return not (other == self)

  def root(self):
    """Docstring TBD."""
    raise NotImplementedError('must be implemented by subclass')

  def parent(self):
    """Docstring TBD."""
    raise NotImplementedError('must be implemented by subclass')

  def num_children(self, p):
    """Docstring TBD."""
    raise NotImplementedError('must be implemented by subclass')

  def children(self, p):
    """Docstring TBD."""
    raise NotImplementedError('must be implemented by subclass')

  def __len__(self):
    """Docstring TBD."""
    raise NotImplementedError('must be implemented by subclass')

  def is_root(self, p):
    """Docstring TBD."""
    return self.root == p

  def is_leaf(self, p):
    """Docstring TBD."""
    return self.num_children(p) == 0

  def is_empty(self):
    """Docstring TBD."""
    return len(self) == 0

  def depth(self, p):
    """Docstring TBD."""
    if self.is_root(p):
      return 0
    else:
      return 1 + self.depth(self.parent(p))

  def _sub_tree_height(self, p):
    """Docstring TBD."""
    if self.is_leaf(p):
      return 0
    else:
      return 1 + max(self._sub_tree_height(child) for child in self.children(p))

  def height(self, p = None):
    """Docstring TBD."""
    if p is None:
      p = self.root()
      return self._sub_tree_height(p)
