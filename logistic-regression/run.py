import os
import sys
import fnmatch
import getopt
import math
import numpy
import decimal


#This function creates a copy of the input array
def copy_Array(input_Array):
  new_Array = [0 for i in range(len(input_Array))]
  count=0;
  for x in input_Array:
    new_Array[count] = x
    count +=1
  return new_Array  


#This function takes in old value and new value of the weight vector after each iteration
# and returns True or False if there is convergence
def convergence(vector_One, vector_Two):
  result_Vector = [0 for i in range(len(vector_One))]
  total_Count = 0
  for position in range(len(vector_One)):
    result_Vector[position] = vector_One[position] - vector_Two[position]

  #check for convergence, if the difference between all the elements of both the input vectors
  #is less than 0.04, there is convergence  
  for x in result_Vector:
    if math.fabs(x) < 0.04:
      total_Count +=1
  
  if total_Count == len(vector_One):
    return False
  return True


#This function trains the logistic regression model and returns learnt weight vector
def logistic_Regression(training_Set_Matrix):
  weight_Vector = [0.0 for i in range(len(training_Set_Matrix[0]))]
  learning_Rate=0.001
  flag= True
  while flag:
    gradient_Vector = [0.0 for i in range(len(training_Set_Matrix[0]))]
    old_Weight_Vector = copy_Array(weight_Vector)
    for example in training_Set_Matrix:
      probability,scalar_value,error=0.0 ,0.0,0.0
      #Calculate weight vector * feature vector viz. w.x
      for i in range(len(weight_Vector)):
        scalar_value+= round(weight_Vector[i],2)*float(example[i])  
        
      probability= 1.0/(1.0+math.exp(-1*round(scalar_value,2)))
      
      error=int(example[len(training_Set_Matrix[0])-1]) - probability
      
      for position in range(len(gradient_Vector)):
        gradient_Vector[position] += error*float(example[position])  
      for position in range(len(gradient_Vector)):
        weight_Vector[position] += (learning_Rate*gradient_Vector[position])
    new_Weight_Vector =weight_Vector
    flag=convergence(old_Weight_Vector,new_Weight_Vector)
  #print "==================Calulation for weight vector is complete=========="
  #print "\n\n The weight vector"
  #print weight_Vector     
  return weight_Vector     

#This function takes input the learnt weight vectors and the training set and predicts the values
def test_Result(weight_Vector, testing_Set_Matrix):
  error_Count=0
  total_Count = len(weight_Vector)
  true_positive,true_negative,false_positive,false_negative=0,0,0,0
  for example in testing_Set_Matrix:
    multiplication_Result=0.0
    for i in range(len(weight_Vector)):
      multiplication_Result+= round(weight_Vector[i],2)*float(example[i])
    prediction =  1.0/(1.0+math.exp(-1*round(multiplication_Result,2)))

    if prediction<0.5:
      print "The predicted value is 0 and the true value is "+ example[len(testing_Set_Matrix[0])-1]
      if "0"==example[len(testing_Set_Matrix[0])-1]:
        true_negative+=1
      else:  
        error_Count+=1   
        false_negative +=1   
    else:
      print "The predicted value is 1 and the true value is "+ example[len(testing_Set_Matrix[0])-1]
      if "1"==example[len(testing_Set_Matrix[0])-1]:
        true_positive +=1
      else:
        false_positive +=1  
        error_Count+=1


  print  "\n\nThe accuracy measure is " +str((total_Count - error_Count)*100/total_Count) + "%"
  print "\n===========The confusion matrix==========="
  print "\t No \t Yes"
  print "No \t", str(true_negative) + "\t", str(false_positive)
  print "Yes \t", str(false_negative) +"\t", str(true_positive)

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