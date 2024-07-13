import numpy as np
from typing import Dict, Tuple

class Box:
  def __init__(self):
    self.entropy = 9
    self.isSubmited = False
    self.isWriten = False
    self.posibilities = {x : True for x in range(1,10)}
    self.number = "-"

  def reset(self):
    self.entropy = 9
    self.isSubmited = False
    self.isWriten = False
    self.posibilities = {x : True for x in range(1,10)}
    self.number = "-"
  
  def submit(self):
    self.isSubmited = True
    self.number = self.drawLots()
  
  def write(self, number):
    self.number = number
    self.isSubmited = True
    self.isWriten = True

  def isTaken(self):
    return self.isSubmited
  
  def getValue(self):
    return self.number
  
  def getEntropy(self):
    return self.entropy
  
  def eliminatePossibility(self, number):
    if self.posibilities[number]:
      self.entropy -= 1 
    self.posibilities[number] = False
  
  def drawLots(self):
    selection = np.random.randint(0, self.entropy)
    i = 0
    for k, v in self.posibilities.items():
      if v:
        if i == selection:
          return k
        i += 1


class Sudoku:
  def __init__(self, fields : Dict[Tuple[int, int], int]):
    self.matrix = [[Box() for x in range(9)] for y in range(9)]
    self.fields = fields
    self.initializeFields()

  def initializeFields(self):
    for coords, number in self.fields.items():
      y, x = coords
      self.initializeBox(x, y, number)

  def correctEntropies(self, x, y, val):
    for i in range(9):
      box = self.matrix[i][x]
      if not box.isTaken():
        box.eliminatePossibility(val)

    for i in range(9):
      box = self.matrix[y][i]
      if not box.isTaken():
        box.eliminatePossibility(val)

    for i in range((x // 3) * 3, (x // 3) * 3 + 3):
      for j in range((y // 3) * 3, (y // 3) * 3 + 3):
        box = self.matrix[j][i]
        if not box.isTaken():
          box.eliminatePossibility(val)

  def submitBox(self, x, y):
    self.matrix[y][x].submit()
    self.correctEntropies(x, y, self.matrix[y][x].getValue())

  def initializeBox(self, x, y, value):
    self.matrix[y][x].write(value)
    self.correctEntropies(x, y, value)

  def findNext(self):
    minEntr = 10
    resX = None
    resY = None
    allSubmited = True
    for y in range(9):
      for x in range(9):
        if not self.matrix[y][x].isTaken():
          allSubmited = False 
          if self.matrix[y][x].entropy < minEntr:
            resX = x
            resY = y
            minEntr = self.matrix[y][x].entropy

    return resY, resX, allSubmited
  
  def reset(self):
    for y in range(9):
      for x in range(9):
        self.matrix[y][x].reset()
    
    self.initializeFields()

  def giveSollution(self):
    allSubmited = False
    while not allSubmited:
      y, x, allSubmited = self.findNext()
      res = np.array([[self.matrix[y][x].getValue() for x in range(9)] for y in range(9)])

      if not allSubmited and (x is None or self.matrix[y][x].getEntropy() == 0):
          self.reset()
      if isinstance(x, int):
        self.submitBox(x, y)
    return res

  def __repr__(self):
    return np.array([[self.matrix[y][x].getValue().__str__() for x in range(9)] for y in range(9)]).__str__()
      


def main():
  # doneFields = {(2,0):3, (3,0):2,(4,0):8,(5,0):4,(3,1):3,(5,1):6,(7,1):4,(8,1):5,(0,2):9,(1,2):4,(2,2):6,(3,2):1,(4,2):5,(7,2):3, (1,3):6,(4,3):3,(5,3):1, (6,3):2, (7,3):5,(8,3):7,(1,4):5, (3,4):6,(6,4):9, (2,5):7,(5,5):9,(6,5):6,(7,5):1,(5,6):5,(7,6):7,(8,6):8,(1,7):1, (4,7):6, (7,7):2, (0, 8):7, (1,8):3, (6,8):5,(7,8):6,(8,8):1 }
  doneFields = {(2,0):1,(3,0):4,(4,0):6,(5,0):3,(3,1):8,(4,1):5,(7,1):3,(1,2):8,(2,2):4,(4,3):7, (7,3):8, (8,3):3, (6,4):6,(8,4):1,(1,5):6,(2,5):3,(5,5):2,(6,5):7,(7,5):4, (4,6):2,(5,6):6,(6,6):4,(7,6):5,(1,7):4,(2,7):8,(7,8):6,(8,8):7}
  sudoku = Sudoku(doneFields)
  print("\nbefore:\n", sudoku)
  sudoku.giveSollution()
  print("\nafter:\n",sudoku, "\n")

if __name__ == "__main__":
  main()
  

