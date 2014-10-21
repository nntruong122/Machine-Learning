import os
import sys
import fnmatch
import getopt
import math
import numpy
import decimal

def logistic_Regression(training_Set_Matrix):
  weight_Vector = [0.0 for i in range(len(training_Set_Matrix[0]))]
  learning_Rate=0.01
  for x in range(0,100):
    gradient_Vector = [0.0 for i in range(len(training_Set_Matrix[0]))]
    print "The number of times this loop runs "+str(x)
    for example in training_Set_Matrix:
      probability=0.0
      result =0.0
      error=0.0
      for i in range(len(weight_Vector)):
        result+= round(weight_Vector[i],2)*float(example[i])  
        
      probability= 1.0/(1.0+math.exp(-1*round(result,2)))
      
      error=int(example[len(training_Set_Matrix[0])-1]) - probability
      
      for position in range(len(gradient_Vector)):
        gradient_Vector[position] += error*float(example[position])  
      for position in range(len(gradient_Vector)):
        weight_Vector[position] += (learning_Rate*gradient_Vector[position])
      
  print "==================Calulation for weight vector is complete=========="
  print "\n\n The weight vector"
  print weight_Vector     
  return weight_Vector     

def test_Result(weight_Vector, testing_Set_Matrix):
  count_zero=0
  count_ones=0
  for example in testing_Set_Matrix:
    multiplication_Result=0.0
    for i in range(len(weight_Vector)):
      #print round(weight_Vector[i],2)*int(example[i])
      multiplication_Result+= round(weight_Vector[i],2)*float(example[i])
    prediction =  1.0/(1.0+math.exp(-1*round(multiplication_Result,2)))
    print str(prediction) +" is the predicted value and the true value is "+example[len(testing_Set_Matrix[0])-1]
    if prediction<0.5:
      if "0"==example[len(testing_Set_Matrix[0])-1]:
        count_zero+=1          
    else:
      print "One is detected \n\n\n"
      count_ones+=1

  print "The number of ones "+str(count_ones)
  print "The number of zeros "+str(count_zero)  
    
def LR(input, target):
  (row,col) = input.shape 
  learning_Rate=0.1
  weight_Vector = numpy.zeros((col,1))
  gradient_Vector = numpy.zeros((col,1))
  iteration = 0
  max_iteration = 10
  while(True):
    iteration +=1
    pred = numpy.dot(input, weight_Vector)
    #print "prediction", pred
    error= target-pred
    print numpy.dot(numpy.transpose(error),error)
    gradient_Vector= gradient_Vector + numpy.dot(numpy.transpose(error),target)
    weight_Vector+=  learning_Rate*gradient_Vector
    #print weight_Vector

    if iteration > max_iteration:
      break


def main(argv):
  setpath()
  try:
    opts, args = getopt.getopt(argv,"ht:e:",["train=","test="])
    if(len(sys.argv) < 5):
      raise getopt.GetoptError(None)

  except getopt.GetoptError:
    print '\nusage: run.py -t <trainfile> -e <testfile> \n'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'run.py -t <trainfile> -e <testfile>'
      sys.exit()
    elif opt in ("-t", "--train"):
       trainfile = arg
    elif opt in ("-e", "--test"):
       testfile = arg


  from file_reader import FileReader
  fr = FileReader(trainfile)
  training_Set= fr.getRows()

  #Readin the test file and creating the matrix
  from file_reader import FileReader
  test_File_Reader = FileReader(testfile)

  testing_Set= test_File_Reader.getRows()
  test_Result(logistic_Regression(training_Set),testing_Set)
  
def setpath():
  for root, dirs, files in os.walk('src'):
    for file in fnmatch.filter(files, '*.py'):
      sys.path.append(root)
    for file in fnmatch.filter(files, '*.pyc'):
      os.remove(os.path.join(root,file))

if __name__ == '__main__':
  main(sys.argv[1:])
{}