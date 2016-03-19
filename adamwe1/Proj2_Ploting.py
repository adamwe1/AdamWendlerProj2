#Proj2_Ploting.py
#Adam Wendler
#CMSC471
#Description: Optimizes a 2D problem and graphs. I created a 
#seperate set of code with a larger step size to graph.  
#I found that using too small a step size lead to the 
#graph takeing too long to complete.  However, I wanted 
#my graph to search with a small step size to make sure 
#it would find the optimum. Therefore, I created this 
#code to create the plots and the other code for general testing.  
#This Code will run much faster then that in Proj2.py. 
#Requires packages from Anaconda.

import math
import random
import sys
import matplotlib
import matplotlib.pyplot as plt
import numpy as np
from mpl_toolkits.mplot3d import Axes3D



#Class used to hold the current position and it's neighbors.
#2D problems only
class ProblemArray:
    #initalization
    def __init__(self, xInti, yInti, equation, stepSize, places):
        self.x = xInti
        self.y = yInti
        self.step = stepSize
        self.prob = equation
        self.places = places
        self.neighbors = []
        self.neighSolu = []

    #sets the bounds of the data space 
    def SetBounds(self, minx, maxx, miny, maxy):
        self.minx = minx
        self.maxx = maxx
        self.miny = miny
        self.maxy = maxx
        
    #Sets the values to offset the neighbors by
    def GetNeighborValues(self):
        #x value decreases
        self.lessx = round(self.x - self.step, self.places)
        self.lessx = max(self.lessx, self.minx)
        
        #x increaces
        self.morex = round(self.x + self.step, self.places)
        self.morex = min(self.morex, self.maxx)

        #y decreaces
        self.lessy = round(self.y - self.step, self.places)
        self.lessy = max(self.lessy, self.miny)

        #y increaces
        self.morey = round(self.y + self.step, self.places)
        self.morey = min(self.morey, self.maxy)



    #Finds all neighboring coordinates and their Solution and places in two arrays
    def GetArray(self):
        #coordinates
        self.neighbors.append((self.x, self.y))
        self.neighbors.append((self.x, self.lessy))
        self.neighbors.append((self.x, self.morey))
        self.neighbors.append((self.lessx, self.y))
        self.neighbors.append((self.lessx, self.lessy))
        self.neighbors.append((self.lessx, self.morey))
        self.neighbors.append((self.morex, self.y))
        self.neighbors.append((self.morex, self.lessy))
        self.neighbors.append((self.morex, self.morey))

        #solutions
        self.neighSolu.append(self.prob(self.x, self.y))
        self.neighSolu.append(self.prob(self.x, self.lessy))
        self.neighSolu.append(self.prob(self.x, self.morey))
        self.neighSolu.append(self.prob(self.lessx, self.y))
        self.neighSolu.append(self.prob(self.lessx, self.lessy))
        self.neighSolu.append(self.prob(self.lessx, self.morey))
        self.neighSolu.append(self.prob(self.morex, self.y))
        self.neighSolu.append(self.prob(self.morex, self.lessy))
        self.neighSolu.append(self.prob(self.morex, self.morey))

    
    #recives the solution of the current xy coordinate pair
    def GetSolution(self):
        return self.neighSolu[0]
        
    #checks array for the optimum(minimum) solution
    def CheckArray(self):
        if not self.neighbors:
            print ("List not generated")
        else:
            hold = min(self.neighSolu)
            self.holdIndex = self.neighSolu.index(hold)
            optX, optY = self.neighbors[self.holdIndex]
            return  self.neighbors[self.holdIndex]
        
    #returns random position in the value space with solution
    def BadMove(self):
            optX = random.randrange(int(self.minx), int(self.maxx))
            optY = random.randrange(int(self.miny), int(self.maxy))
            solution = self.prob(optX, optY)
            return optX, optY, solution
        
        
    #redifines the current position and clears neighbor arrays
    def RedefineValues(self, newX, newY):
        self.x = newX
        self.y = newY
        self.neighbors[:] = []
        self.neighSolu[:] = []




def ToOptimize(x, y):
    r =  np.sqrt(x**2 + y**2)
    f =  np.sin(x**2 + y**3)/(.1 + r**2)
    g =  x**2 + 5*y**2
    h =  np.exp(1 - r**2)/2
    z =  f + g + h
    return z



def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
    x = random.randrange(int(xmin), int(xmax))
    y = random.randrange(int(ymin), int(ymax))
    xxs = []
    yys = []
    zzs = []

    fig = plt.figure()
    ax = fig.gca(projection = '3d')

    ax.set_xlim3d(-2.5, 2.5)
    ax.set_ylim3d(-2.5, 2.5)
    ax.set_zlim3d(0, 40)
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    xs = np.arange(-2.5, 2.5, .25)
    ys = np.arange(-2.5, 2.5, .25)
    xs, ys = np.meshgrid(xs,ys)
    zs = function_to_optimize(xs,ys)
    
    ax.plot_wireframe(xs, ys, zs, color = 'b')
    plt.title("Hill Climb")

    xxs.append(x)
    yys.append(y)
    zzs.append(function_to_optimize(x,y))
    
    probspace = ProblemArray(x, y, function_to_optimize, step_size, 2)
    probspace.SetBounds(xmin, xmax, ymin, ymax)
    step = 0
    escape = 0
    free = 100
    while True:
        step = step+1
        probspace.GetNeighborValues()
        probspace.GetArray()
            
        newX, newY = probspace.CheckArray()
        solution = probspace.GetSolution()
            
        if newX == x and newY == y:
            if escape > free:
                ax.scatter(xxs, yys, zzs, color = 'r')
                plt.show()
                return (float(x), float(y))
            else:
                escape = escape + 1
            
        else:
            
            escape = 0
            x = newX
            y = newY
            
            xxs.append(x)
            yys.append(y)
            zzs.append(function_to_optimize(x,y))
            
            probspace.RedefineValues(x, y)
                
    return (float(x), float(y))

        
        
        
def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    x = random.randrange(int(xmin), int(xmax))
    y = random.randrange(int(ymin), int(ymax))

    xxs = []
    yys = []
    zzs = []

    fig = plt.figure()
    ax = fig.gca(projection = '3d')

    ax.set_xlim3d(-2.5, 2.5)
    ax.set_ylim3d(-2.5, 2.5)
    ax.set_zlim3d(0, 40)
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    xs = np.arange(-2.5, 2.5, .25)
    ys = np.arange(-2.5, 2.5, .25)
    xs, ys = np.meshgrid(xs,ys)
    zs = function_to_optimize(xs,ys)
    
    ax.plot_wireframe(xs, ys, zs, color = 'b')
    plt.title("Hill Climb With Restarts")

    xxs.append(x)
    yys.append(y)
    zzs.append(function_to_optimize(x,y))
    
    probspace = ProblemArray(x, y, function_to_optimize, step_size, 2)
    probspace.SetBounds(xmin, xmax, ymin, ymax)

    ii = 0
    answers = []
    coord = []
    
    step = 0
    escape = 0
    free = 100
    while True:
        step = step + 1

        #get the min back
        probspace.GetNeighborValues()
        probspace.GetArray()
        newX, newY = probspace.CheckArray()
            
        if newX == x and newY == y:
            if escape > free:
                solution = function_to_optimize(x,y)
                answers.append(solution)
                coord.append((float(newX), float(newY)))
            
                if ii < num_restarts:
                    ii = ii + 1
                    escape = 0
                    x = random.randrange(int(xmin), int(xmax))
                    y = random.randrange(int(ymin), int(ymax))
                    probspace.RedefineValues(x, y)

                else:
                    optimum=answers.index(min(answers))
                    ax.scatter(xxs, yys, zzs, color = 'r')
                    plt.show()
                    return coord[optimum]
            else:
                escape = escape + 1
                
        else:
            escape = 0
            xxs.append(x)
            yys.append(y)
            zzs.append(function_to_optimize(x,y))
            x = newX
            y = newY
            probspace.RedefineValues(x, y)

            
    return(float(x), float(y))


    
def simulated_annaeling(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
    x = random.randrange(int(xmin), int(xmax))
    y = random.randrange(int(ymin), int(ymax))
    probspace = ProblemArray(x, y, function_to_optimize, step_size, 2)
    stillLowering = True
    answer = 99999
    coord = [0,0]
    
    xxs = []
    yys = []
    zzs = []

    fig = plt.figure()
    ax = fig.gca(projection = '3d')

    ax.set_xlim3d(-2.5, 2.5)
    ax.set_ylim3d(-2.5, 2.5)
    ax.set_zlim3d(0, 40)
    
    ax.set_xlabel('X axis')
    ax.set_ylabel('Y axis')
    ax.set_zlabel('Z axis')

    xs = np.arange(-2.5, 2.5, .25)
    ys = np.arange(-2.5, 2.5, .25)
    xs, ys = np.meshgrid(xs,ys)
    zs = function_to_optimize(xs,ys)
    
    ax.plot_wireframe(xs, ys, zs, color = 'b')
    plt.title("Simulated Annaeling")

    xxs.append(x)
    yys.append(y)
    zzs.append(function_to_optimize(x,y))

    step = 1
    escape = 0
    free = 100
    measuredStep = step
    maxSteps = max_temp 
    probspace.SetBounds(xmin, xmax, ymin, ymax)
    
    while True:
            step = step + 1
            probspace.GetNeighborValues()
            probspace.GetArray()
            
            solution = probspace.GetSolution()
                        
            temperature = measuredStep/maxSteps
            newX, newY, newSolution= probspace.BadMove()
            skip = (newSolution - solution)/temperature
            
                
            if skip >= random.random() and stillLowering:
                escape = 0
                x = newX
                y = newY
                xxs.append(x)
                yys.append(y)
                zzs.append(function_to_optimize(x,y))
                probspace.RedefineValues(x, y)
            
            else:
                newX, newY = probspace.CheckArray()
            
                if newX == x and newY == y:
                    if escape > free:
                        ax.scatter(xxs, yys, zzs, color = 'r')
                        plt.show()
                        return (float(x), float(y))
                    
                    else:
                        escape = escape + 1
            
                else:
                    escape = 0
                    x = newX
                    y = newY
                    xxs.append(x)
                    yys.append(y)
                    zzs.append(function_to_optimize(x,y))
                    probspace.RedefineValues(x, y)
                    
                    
            if measuredStep == maxSteps and stillLowering:
                stillLowering = False
                if solution < answer:
                    solution = answer
                    x = coord[0]
                    y = coord[1]

            elif measuredStep < maxSteps:
                measuredStep = step
                
    return(x, y)

    
def main():
    domain = 2.5
    step = .01
    
    #hill climbing 
    hillResult = hill_climb(ToOptimize, step, -domain, domain, -domain, domain)
    print(hillResult)
    sys.stdout.flush()
    #hill climbing with random number restarts
    hillRandom = hill_climb_random_restart(ToOptimize, step, 20, -domain, domain, -domain, domain)
    print(hillRandom)
    sys.stdout.flush()
    #simulated annaeling
    saResult = simulated_annaeling(ToOptimize, step, 10000, -domain, domain, -domain, domain)
    print(saResult) 
    sys.stdout.flush()
    
main()