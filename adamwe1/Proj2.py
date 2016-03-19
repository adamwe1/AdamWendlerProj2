#Proj2.py
#Adam Wendler
#CMSC471
#Description: Optimizes a 2D problem by placing it into a Problem Array then 
#using Hill Climbing, Hill Climbing with random restarts, and Simulated Annealing

  
import math
import random
import sys



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
        #self.places -> decimal places to round too
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



    
#function to optimize.  Returns solution
def ToOptimize(x, y):
    r =  math.sqrt(x**2 + y**2)
    f =  math.sin(x**2 + y**3)/(.1 + r**2)
    g =  x**2 + 5*y**2
    h =  math.exp(1 - r**2)/2
    z =  f + g + h
    return z


#hill cliimbing
def hill_climb(function_to_optimize, step_size, xmin, xmax, ymin, ymax):
    #random X/y value
    x = random.randrange(int(xmin), int(xmax))
    y = random.randrange(int(ymin), int(ymax))

    #create the problem Array
    probspace = ProblemArray(x, y, function_to_optimize, step_size, 5)
    probspace.SetBounds(xmin, xmax, ymin, ymax)
    
    escape = 0
    free = 100
    while True:
        #finds neighbots
        probspace.GetNeighborValues()
        probspace.GetArray()
        
        #finds best move
        newX, newY = probspace.CheckArray()
            
        #tests if move is not changing.
        #after 100 attempts, returns value
        if newX == x and newY == y:
            if escape > free:
                return (float(x), float(y))
            else:
                escape = escape + 1
                
        #makes move
        else:
            escape = 0
            x = newX
            y = newY
            probspace.RedefineValues(x, y)
            
    #returns in case loop ends
    return (float(x), float(y))

        
        
#hill climbing with a random amount of restarts
# largelly simular to hill climbing
def hill_climb_random_restart(function_to_optimize, step_size, num_restarts, xmin, xmax, ymin, ymax):
    x = random.randrange(int(xmin), int(xmax))
    y = random.randrange(int(ymin), int(ymax))

    probspace = ProblemArray(x, y, function_to_optimize, step_size, 5)
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
        
        #testing non-moves
        if newX == x and newY == y:
            if escape > free:
                solution = function_to_optimize(x, y)
                answers.append(solution)
                coord.append((float(x), float(y)))
        
                #if restarts necessary, restart
                if ii < num_restarts:
                    ii = ii + 1
                    escape = 0
                    x = random.randrange(int(xmin), int(xmax))
                    y = random.randrange(int(ymin), int(ymax))
                    probspace.RedefineValues(x, y)
                    
                #when all restarts finished, returns 
                #minimum based on minimum result
                else:
                    optimum=answers.index(min(answers))
                    return coord[optimum]
            else:
                escape = escape + 1
                
        else:
            escape = 0
            x = newX
            y = newY
            probspace.RedefineValues(x, y)

            
    return(float(x), float(y))


#Simulates Annaeling
def simulated_annaeling(function_to_optimize, step_size, max_temp, xmin, xmax, ymin, ymax):
    x = random.randrange(int(xmin), int(xmax))
    y = random.randrange(int(ymin), int(ymax))
    probspace = ProblemArray(x, y, function_to_optimize, step_size, 5)
    probspace.SetBounds(xmin, xmax, ymin, ymax)
    stillLowering = True
    answer = 99999
    coord = [x,y]

    step = 1
    escape = 0
    free = 100
    measuredStep = step
    maxSteps = max_temp 
    while True:
        step = step + 1
        probspace.GetNeighborValues()
        probspace.GetArray()
            
        solution = function_to_optimize(x,y)
        # T = steps taken / maximum steps allowed
        temperature = measuredStep/maxSteps
        #gets random move
        newX, newY, newSolution= probspace.BadMove()
        #f(B) - f(A)/T
        skip = (newSolution - solution)/temperature
        
        #Randomlly allows random move
        #chance decreaces as an inverse factor of time
        if skip >= random.random() and stillLowering:
            escape = 0
            x = newX
            y = newY
            probspace.RedefineValues(x, y)
        
        #if random chance fails, hill climbing
        else:
            newX, newY = probspace.CheckArray()
            
            if newX == x and newY == y:
                if escape > free:
                    return (float(x), float(y))
                else:
                    escape = escape + 1
            
            else:
                escape = 0
                x = newX
                y = newY
                probspace.RedefineValues(x, y)
                    
        #once steps taken reaches maximum steps allowed
        #forces hill climbing from lowest found point
        if measuredStep == maxSteps and stillLowering:
            stillLowering = False
            if solution < answer:
                solution = answer
                x = coord[0]
                y = coord[1]

        #increaces measuredStep untill maxSteps reached
        elif measuredStep < maxSteps:
            measuredStep = step
                
    return(float(x), float(y))

#driver    
def main():
    domain = 2.5
    step = .00001
                  
    hillResult = hill_climb(ToOptimize, step, -domain, domain, -domain, domain)
    print(hillResult)
    sys.stdout.flush()
    hillRandom = hill_climb_random_restart(ToOptimize, step, 20, -domain, domain, -domain, domain)
    print(hillRandom)
    sys.stdout.flush()
    saResult = simulated_annaeling(ToOptimize, step, 10000, -domain, domain, -domain, domain)
    print(saResult) 
    sys.stdout.flush()

    
main()