import os

class World:
   #This class contains all the details related to the world.
  walls = [(3,1),(3,3)]
  pit =(1,1)
  start=(4,0)
  goal =(0,3)
  world_Row = 5
  world_Column = 4
  default_Reward =-1

  def __init__(self):
    pass

  def isWalls(self, x_position,y_position):
    for single_Wall in self.walls:
      if single_Wall[0]== x_position and single_Wall[1] == y_position:
        return True
    return False    

  def isGoal(self,x_position,y_position):
    if x_position == self.goal[0] and y_position == self.goal[1]:
      return True
    else:
      return False


  def isPit(self,x_position,y_position):
    if x_position == self.pit[0] and y_position == self.pit[1]:
      return True
    else:
      return False



  def isWithinWorld(self,direction,x_position,y_position):
    #check for values of left
    if direction =='up':
      if (x_position-1) >=0 and (not self.isWalls(x_position-1,y_position)):
        return True
      else:
        return False
    elif direction == 'down':
      if(x_position+1) <=4 and (not self.isWalls(x_position+1,y_position)):
        return True 
      else:
        return False
    elif direction == 'left':
      if(y_position-1)>=0 and (not self.isWalls(x_position,y_position-1)):
        return True
      else:
        return False              
    elif direction =='right':
      if(y_position+1)<=3 and (not self.isWalls(x_position,y_position+1)):
        return True
      else:
        return False


  def getRewards(self,x_position,y_position):
    if self.isGoal(x_position,y_position):
      return 10
    elif self.isPit(x_position,y_position):
      return -50
    elif x_position < self.world_Row and y_position < self.world_Column:
      return self.default_Reward

  def newPosition(self,direction,x_position,y_position):
    if direction == 'up':
      return x_position-1, y_position
    elif direction == 'down':
      return x_position+1,y_position
    elif direction == 'left':
      return x_position,y_position-1
    elif direction =='right':
      return x_position,y_position+1



 