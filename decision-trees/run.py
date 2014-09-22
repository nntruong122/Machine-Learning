import os
import sys
import fnmatch
import getopt

def main(argv):
  setpath()
  try:
    opts, args = getopt.getopt(argv,"ht:e:d:",["train=","test=","maxDepth="])
    if(len(sys.argv) < 7):
      raise getopt.GetoptError(None)

  except getopt.GetoptError:
    print '\nusage: run.py -t <trainfile> -e <testfile> -d <maxDepth>\n'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'run.py -t <trainfile> -e <testfile> -d <maxDepth>'
      sys.exit()
    elif opt in ("-t", "--train"):
       trainfile = arg
    elif opt in ("-e", "--test"):
       testfile = arg
    elif opt in ("-d", "--maxDepth"):
       maxDepth = int(arg)

  from file_reader import FileReader
  fr = FileReader(trainfile, True)

  from decision_tree_builder import DecisionTreeBuilder
  # getRows() returns a dataMatrix;
  dtb = DecisionTreeBuilder(fr.getRows())
  print ('Features: {}'.format(fr.featureNames))
  root = dtb.build(maxDepth)

  print('Height of the tree is {}'.format(dtb.decisionTree.height()))

  # Some debugging print statements for tennis dataset:

  # print(dtb.decisionTree.is_leaf(root))
  # print(dtb.decisionTree.num_children(root))
  # y = dtb.decisionTree.iThChild(root, 0)
  # z = dtb.decisionTree.iThChild(root, 1)
  # t = dtb.decisionTree.iThChild(root, 2)
  # print(dtb.decisionTree.is_leaf(y))
  # print(dtb.decisionTree.is_leaf(z))
  # print(dtb.decisionTree.is_leaf(t))

  # TBD: Code to test the testing rows and reporting accuracy etc.
  # Sample code for predicting classLabel for an unknown record.
  # Hard coded for playTennis record.
  print 'Sample test:'
  arr = ['Mild', 'Overcast', 'High', 'Weak']
  print ('\tClass label for {} is {}'.format(arr, dtb.predict(arr)))

def setpath():
  for root, dirs, files in os.walk('src'):
    for file in fnmatch.filter(files, '*.py'):
      sys.path.append(root)
    for file in fnmatch.filter(files, '*.pyc'):
      os.remove(os.path.join(root,file))

if __name__ == '__main__':
  main(sys.argv[1:])
