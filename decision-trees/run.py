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
  fr = FileReader(trainfile)

  from decision_tree_builder import DecisionTreeBuilder
  # getRows() returns a dataMatrix;
  dtb = DecisionTreeBuilder(fr.getRows())
  print ('Features: {}'.format(fr.featureNames))
  root = dtb.build(maxDepth)
  print('Tree Building Complete and Successful')
  print('Height of the tree is {}'.format(dtb.decisionTree.height()))

  # Some debugging print statements for tennis dataset:
  #dtb.print_Tree()
  #print(dtb.decisionTree.is_leaf(root))
  #print(dtb.decisionTree.num_children(root))
  #y = dtb.decisionTree.iThChild(root, 0)
  #z = dtb.decisionTree.iThChild(root, 1)
  #t = dtb.decisionTree.iThChild(root, 2)
  #print(dtb.decisionTree.is_leaf(y))
  #print(dtb.decisionTree.is_leaf(z))
  #print(dtb.decisionTree.is_leaf(t))

  #Testing section  

  #create a zero initialized confusion matrix
  confusion_matrix=[[0 for j in range(len(fr.getClassLabels()))] for j in range(len(fr.getClassLabels()))]
  #read the test file
  testFile_Reader = FileReader(testfile)
  dataMatrix_testFile = testFile_Reader.getRows()
  Error_Count =0
  No =0
  Yes=0
  No_Error= 0
  Yes_error=0
  Total_records = len(dataMatrix_testFile)+0.0
  #Testing phase
  for row in dataMatrix_testFile:
    predicted_classLabel = dtb.predict(row)
    print ('\tActual Label is {}, and Predicted Label is {}'.format(row[len(row)-1], predicted_classLabel))
    #confusion_matrix[int(row[len(row)-1])-1][int(predicted_classLabel)-1]+= 1
    if not row[len(row)-1]==predicted_classLabel:    
      Error_Count += 1.0
  #To print confusion matrix for zoo data set uncomment line 66          
  print ('\n\n------------------Confusion Matrix----------')
  for row in confusion_matrix:
    print row

  print('\n\n--------------Error Count----------------')
  print Error_Count  
  print('\n\n--------------Accuracy----------------')
  print (Total_records-Error_Count)/Total_records

def setpath():
  for root, dirs, files in os.walk('src'):
    for file in fnmatch.filter(files, '*.py'):
      sys.path.append(root)
    for file in fnmatch.filter(files, '*.pyc'):
      os.remove(os.path.join(root,file))

if __name__ == '__main__':
  main(sys.argv[1:])
