import os
import sys
import fnmatch
import getopt

def main(argv):
  setpath()
  try:
    opts, args = getopt.getopt(argv,"ht:e:",["train=","test="])
    if(len(sys.argv) < 5):
      raise getopt.GetoptError(None)

  except getopt.GetoptError:
    print('\nusage: run.py -t <trainfile> -e <testfile>\n')
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print('run.py -t <trainfile> -e <testfile>')
      sys.exit()
    elif opt in ("-t", "--train"):
       trainfile = arg
    elif opt in ("-e", "--test"):
       testfile = arg

  from file_reader import FileReader
  fr = FileReader(testfile)
  from naive_bayes import NaiveBayes
  nb = NaiveBayes(trainfile)

  test_file_reader = FileReader(testfile)
  testData = test_file_reader.getRows()

  num_errors = 0
  true_positive = 0
  false_positive = 0
  true_negative = 0
  false_negative = 0

  #Testing phase
  for idx, row in enumerate(testData):
    prediction = nb.binary_classify(row)
    if row[-1] != prediction:
      num_errors += 1.0
      print("Error on row: %s" % str(idx+1))
      if row[-1] == '1':
        false_negative += 1
      else:
        false_positive += 1
    elif row[-1] == '0':
      true_negative += 1
    else:
      true_positive += 1

  print('\n\n--------------Error Count----------------')
  print(num_errors)
  print('\n\n--------------Accuracy----------------')

  print("\n\nThe Accuracy is " +str((len(testData) - num_errors)*100/len(testData)) + "%")
  print("\n===========The confusion matrix===========")
  print("\t No \t Yes")
  print("No \t", str(true_negative) + "\t", str(false_positive))
  print("Yes \t", str(false_negative) +"\t", str(true_positive))

def setpath():
  for root, dirs, files in os.walk('src'):
    for file in fnmatch.filter(files, '*.py'):
      sys.path.append(root)
    for file in fnmatch.filter(files, '*.pyc'):
      os.remove(os.path.join(root,file))

if __name__ == '__main__':
  main(sys.argv[1:])
{}