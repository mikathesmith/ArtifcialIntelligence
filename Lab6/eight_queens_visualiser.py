import pylab as pl
import numpy as np
from numpy import ndarray
import time
import random

__author__ = "Lech Szymanski"
__email__ = "lechszym@cs.otago.ac.nz"


class chess_board:
    
    def __init__(self):
        #Create a new figure
        self.plfig=pl.figure(dpi=100)
        #Create a new subplot
        self.plax = self.plfig.add_subplot(111)
        #Create bitmap for the chessboard
        b = np.matrix('1 0 1 0 1 0 1 0; 0 1 0 1 0 1 0 1;1 0 1 0 1 0 1 0; 0 1 0 1 0 1 0 1;1 0 1 0 1 0 1 0; 0 1 0 1 0 1 0 1;1 0 1 0 1 0 1 0; 0 1 0 1 0 1 0 1');
        #Plot the chessboard
        self.plax.matshow(b, cmap=pl.cm.gray)
        pl.ion()
        pl.show()        
        self.scatter_handle = []

    #Show state of the b (encoded as an array of 8 queens with position
    #from the bottom of the board in oardeach column)
    def show_state(self,c):
        if self.scatter_handle:
            self.scatter_handle.remove()
        #The queens are shown as red dots on the chessboard
        self.scatter_handle = self.plax.scatter(x=[0,1,2,3,4,5,6,7],y=[8-i for i in c], s=40, c='r')
        self.plfig.canvas.draw()


  #  def crossover(self, parents):
   #     father, mother = parents
    #    index1 = random.randint(1, len(self.target)-2)
     #   index2 = random.randint(1, len(self.target)-2)
      #  if index1 > index2: index1, index2 = index2, index1
       # child1 = father[:index1] + mother[index1:index2] + father[index2:]
       # child2 = mother[:index1] + father[index1:index2] + mother[index2:]
       # return(child1)

    def crossover(self, parent1, parent2):
        r = random.Random()
        crossover_index = r.randint(0, 8)  # choose random crossover point

        left = parent1[0:crossover_index]
        right = parent2[crossover_index:8]
        left.extend(right)
        return left #returns new offspring chromosome


    def fitness(self, parent):
        #for loop to check that all the numbers in the parent are different to make sure none of the queens take each
        #other. (still can diagonal)
        fitness = len(np.unique(parent))
        return fitness





if __name__ == '__main__':
    #Close any open figures, and start a new one
    pl.close('all')
    #Create instance of chess board visualisation
    board = chess_board()
    parentList = ndarray((500,),int)

    #Show 5 different random queen distributions
    for i in range(0, 500):
        #Generate a random queen distribution - 8 integers in range 1-8
        c=np.random.randint(1, 8, 8)

        #Show the new state
        #print(c)
        parentList[i] = board.fitness(c) #returns number of unique elements
        board.show_state(c)

        print(board.crossover(c, c))

        #print(parentList[i])
            #board.show_state(c)
            #print("unique!")

          #  p= np.append(c)

         #choose two parents from p to crossover
        #Pause for 2 seconds
        time.sleep(0.005)
        pl.pause(0.005)

   # print(board.crossover(parentList[np.random.randint(1,500)], parentList[np.random.randint(1,500)]))
