import sys
import os
import fnmatch

def main(argv):
  setpath()
  from q_learning import QLearning
  from grid_world import Grid

  # 5 rows, 4 cols, unreachables : [(1,1), (1,3)], pits : [(3,1)], goal : (4,3)
  g = Grid(5, 4, [(1,1),(1,3)], [(3,1)], (4,3))
  q = QLearning(g)
  q.learn()

def setpath():
  for root, dirs, files in os.walk('src'):
    for file in fnmatch.filter(files, '*.py'):
      sys.path.append(root)
    for file in fnmatch.filter(files, '*.pyc'):
      os.remove(os.path.join(root,file))

if __name__ == '__main__':
  main(sys.argv[1:])
{}