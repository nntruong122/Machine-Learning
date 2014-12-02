import os
import sys
import fnmatch
import getopt
import math
import numpy
import decimal

def copyMatrix(input_Matrix,row_length,col_length):
  row_count=0
  col_count =0
  newMatrix= [[0 for x in range(col_length)] for x in range(row_length)]

  for row in input_Matrix:
    col_count =0
    for col in row:
       newMatrix[row_count][col_count] = col
       col_count += 1
    row_count +=1 


  return newMatrix

def convergence(firstMatrix, secondMatrix, row_length,col_length):
  subtractMatrix= [[0 for x in range(col_length)] for x in range(row_length)]
  row_count =0
  col_count =0
  zero_count =0
  for row in range(row_length):
    col_count =0
    for col in range(col_length):
       subtractMatrix[row_count][col_count] = firstMatrix[row_count][col_count] - secondMatrix[row_count][col_count]
       if subtractMatrix[row_count][col_count] == 0.0:
        zero_count +=1
       col_count += 1
    row_count +=1 

  return zero_count == col_length* row_length

def valueIteration(defaultReward):
  discountedValue = 0.9
  from World import World
  instance = World()
  instance.default_Reward = defaultReward
  #print instance.isWalls(3,2)
 
  # old actions ={'right':[0.8,0.2],'left':[1.0],'up':[0.8,0.2],'down':[1.0]}

  actions = {'right':{'right':0.8,'down':0.2},'left':{'left':1.0},'up':{'up':0.8,'left':0.2},'down':{'down':1.0}}
  #initialize the value
  valueGrid =[[0 for x in range(instance.world_Column)] for x in range(instance.world_Row)] 

  previousValueGrid =[[0 for x in range(instance.world_Column)] for x in range(instance.world_Row)] 

  iterations = 0
  stop = False


  while not stop :
    iterations +=1
    previousValueGrid = copyMatrix(valueGrid,instance.world_Row,instance.world_Column)
    for row in range(instance.world_Row):
      for col in range(instance.world_Column):
        #for all states

        #for all actions

        valueActions=[0,0,0,0]
        count = 0
        if not instance.isWalls(row,col):
          for key,pairs in actions.iteritems():
            
            total  =0.0
            for action,value in pairs.iteritems():
             
              if instance.isWithinWorld(action,row,col):
                newCoordinates = instance.newPosition(action,row,col)
                total += (value*valueGrid[newCoordinates[0]][newCoordinates[1]])
            
            valueActions[count] = instance.getRewards(row,col) + (discountedValue * total)
            count +=1


        valueGrid[row][col] = max(valueActions)

    #print valueGrid
    stop = convergence(valueGrid,previousValueGrid,instance.world_Row,instance.world_Column)
            
  print valueGrid 
  print "The number of iterations is "+str(iterations)



def main(argv):
  setpath()
  try:
    opts, args = getopt.getopt(argv,"hd:",["default="])
    if(len(sys.argv) < 3):
      raise getopt.GetoptError(None)

  except getopt.GetoptError:
    print '\nusage: run.py -d <default reward> \n'
    sys.exit(2)
  for opt, arg in opts:
    if opt == '-h':
      print 'run.py -d <default reward>'
      sys.exit()
    elif opt in ("-d", "--default"):
       defaultReward = arg


  valueIteration(int(defaultReward))

  

  
def setpath():
  for root, dirs, files in os.walk('src'):
    for file in fnmatch.filter(files, '*.py'):
      sys.path.append(root)
    for file in fnmatch.filter(files, '*.pyc'):
      os.remove(os.path.join(root,file))

if __name__ == '__main__':
  main(sys.argv[1:])
{}