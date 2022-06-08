import matplotlib.pyplot as plt
import numpy as np
import random
from cats import *

RMAX = 25
CMAX = 30
steps = 50

#create user interactivity
steps = input('\n Enter amount of steps in this simulation (every step is an hour with a two day max cycle):\n')
initpop = input('\n Enter initial total population of cats (this will be split into good and evil cats randomly:\n')
foodnum = input('\n Enter amount of food drops in this simulation:\n')
boxnum = input('\n Enter amount of mysterious box drops in this simulation:\n')


#create feature locations
water = [(23,2),(22,2),(21,2),(23,3),(22,3),(21,3),(23,28),(22,28),(21,28),(23,27),(22,27),(21,27),(2,2),(3,2),(4,2),(2,3),(3,3),(4,3),(2,28),(3,28),(4,28),(2,27),(3,27),(4,27)]

food = []
for i in range(int(foodnum)):
    row = random.randint(0,RMAX-1)
    col = random.randint(0,CMAX-1)
    food.append((row,col))

boxes = []
for i in range(int(boxnum)):
    row = random.randint(0,RMAX-1)
    col = random.randint(0,CMAX-1)
    boxes.append((row,col))




#function to simplify plotting inanimate plots (features: water, food, boxes, etc)
def make_feature_scatter(itemlist, colour, alpha):
    xlist = []
    ylist = []
    for r,c in itemlist:
        ylist.append(RMAX - r - 1)
        xlist.append(c)
    plt.scatter(xlist,ylist,color=colour, alpha = alpha, marker='s')


#function to simplify plotting animated objects (cats)
def make_cat_scatter(pop, colour, alpha, symbol):
    xlist = []
    ylist = []
    slist = []
    for row in range(RMAX):
        for col in range(CMAX):
            if pop[row,col] > 0:
                ylist.append(RMAX - row - 1)
                xlist.append(col) #flip rows/columns to y/x
                slist.append(pop[row,col]*100) #size increased to see marker tag easier
    plt.scatter(xlist,ylist,s=slist,color=colour,alpha = alpha,marker = symbol)


def move_em_good(current, moves, avoidlist, chaselist):
    nextgrid = np.zeros((current.pos).shape, dtype="int16")

    for row in range(RMAX):
        for col in range(CMAX):
            for g in range(current.pos[row,col]):
                for x, y in (((row - 1), col), ((row + 1), col), (row, (col - 1)), (row, (col + 1)), ((row - 1), (col - 1)), ((row - 1), (col + 1)), ((row + 1), (col - 1)), ((row + 1), (col + 1))): #Moore Neighbourhood
                    if not ((0 <= x < len(current.pos)) and (0 <= y < len(current.pos[1]))): #check done to pass over any positions outside the boundaries of the graph
                        continue
                    if current.hunger <= ((current.initialgoodhunger)/2): #if hungry
                        if (row,col) in chaselist and [x, y] > 0: #needs to be fixed. (something to do with being in g in range of current.pos[row,col]???)
                            nextgrid[x, y] += 1
                            return nextgrid
                            break
                else:
                    nextrow = row + random.choice(moves)
                    nextcol = col + random.choice(moves)
                    if nextrow < 0:
                        nextrow = 0
                    if nextcol < 0:
                        nextcol = 0
                    if nextrow >= RMAX:
                        nextrow = RMAX - 1
                    if nextcol >= CMAX:
                        nextcol = CMAX - 1
                    if nextgrid[nextrow, nextcol] and avoidlist[row,col] > 0: #if next position would've been on top of what its trying to avoid
                        nextrow = 0 #then do not move there
                        nextcol = 0
                    nextgrid[nextrow, nextcol] += 1
    return nextgrid



def move_em_evil(current, moves, chaselist):
    nextgrid = np.zeros(current.shape, dtype="int16")

    for row in range(RMAX):
        for col in range(CMAX):
            for g in range (current[row, col]):
                for x, y in (((row - 1), col), ((row + 1), col), (row, (col - 1)), (row, (col + 1)), ((row - 1), (col - 1)), ((row - 1), (col + 1)), ((row + 1), (col - 1)), ((row + 1), (col + 1))): #Moore Neighbourhood   
                    if not ((0 <= x < len(current)) and (0 <= y < len(current[1]))): #check done to pass over any positions outside the boundaries of the graph
                        continue
                    if (chaselist[x, y] == 1).any():
                        nextgrid[x, y] += 1
                        return nextgrid
                        break
                else:
                    nextrow = row + random.choice(moves)
                    nextcol = col + random.choice(moves)
                    if nextrow < 0:
                        nextrow = 0
                    if nextcol < 0:
                        nextcol = 0
                    if nextrow >= RMAX:
                        nextrow = RMAX - 1
                    if nextcol >= CMAX:
                        nextcol = CMAX - 1
                    nextgrid[nextrow, nextcol] += 1
    return nextgrid



def main():
    
    moves  = [-1,0,1]
    moves2 = [-2,0,2]

    listofgoodcats = []
    listofgoodcatspos = []

    listofevilcats = []
    listofevilcatspos = []
    

    # Starting population
    
    for i in range(int(initpop)):  # randomize adding good or evil cats to grid
        xga = random.randint(0,RMAX-1)
        yga = random.randint(0,CMAX-1)

        toss = random.choice([0,1])
        if toss == 0:
            globals()['GoodCats%s' % i] = GoodCat(np.zeros((RMAX,CMAX), dtype="int16"), 'GoodCat%s' % i, 'N%s' % i) #global variable name given for testing purposes. Name and tag given based on loop number
            ((globals()['GoodCats%s' % i]).pos)[xga,yga] += 1
            listofgoodcatspos.append(((globals()['GoodCats%s' % i].pos))) #added to list of all good cats positions
            listofgoodcats.append(((globals()['GoodCats%s' % i]))) #added to list of all good cats


        elif toss == 1:
            globals()['EvilCats%s' % i] = EvilCat(np.zeros((RMAX,CMAX), dtype="int16"), 'EvilCat%s' % i, 'N%s' % i) #global variable name given for testing purposes. Name and tag given based on loop number
            ((globals()['EvilCats%s' % i]).pos)[xga,yga] += 1
            listofevilcatspos.append(((globals()['EvilCats%s' % i].pos))) #added to list of all evil cats positions
            listofevilcats.append(((globals()['EvilCats%s' % i]))) #added to list of all evil cats


    #totals made to have one array off all good cats positions and one array of all evil cats positions. makes tracking simpler
    listofgoodcatspostotal = sum(listofgoodcatspos)
    listofevilcatspostotal = sum(listofevilcatspos)





    # Simulation
    for t in range(int(steps)):    
        print("### Timestep ", t, "###")
        print("### Number of good cats: ", (listofgoodcatspostotal).sum(), "###")
        print("### Number of evil cats: ", (listofevilcatspostotal).sum(), "###")
        cattotal = np.add((listofgoodcatspostotal),(listofevilcatspostotal))
        print("### Number of total cats: ", cattotal.sum(), "###")
        
    
        for obj in listofgoodcats:
            if (sum(obj.pos) > 0).any(): #essentially checking to only do this to cats that are "alive" (still have a positions)
                print("Name: ", obj.name, "\t Hunger: ", obj.hunger, "\t Thirst: ", obj.thirst, "\t Age: ", obj.age)

        for x in listofevilcats:
            if (sum(x.pos) > 0).any():
                print("Name: ", x.name, "\t Hunger: ", x.hunger, "\t Thirst: ", x.thirst, "\t Age: ", x.age)



        [obj.stepChange() for obj in listofgoodcats] #applying stepChange method every step. makes them age every step       
        [x.stepChange() for x in listofevilcats]
        

        for x in listofevilcats:
            alphacalc = 1/(x.maxage - x.initialage) #calculation is done to see how much the alpha is needed to drop per step to have it fade away until death
            if (x.alpha - alphacalc) > 0: #alpha cant be below zero so check is done
                x.alpha -= alphacalc #alpha is reduced by that much every step

        for obj in listofgoodcats:
            alphacalc = 1/(obj.maxage - obj.initialage)
            if (obj.alpha - alphacalc) > 0:
                obj.alpha -= alphacalc




        #movement for each step
        #good movement
        goodnext = []

        for obj in listofgoodcats:
            if 5 < t < 24 or 29 < t < 48:
                goodnextspot = ((move_em_good(obj,moves,listofevilcatspostotal, food)))
                obj.pos = goodnextspot
            goodnext.append(obj.pos)

        listofgoodcatspostotal = sum(goodnext)  #recorded for evil cats to use. just makes it easier. could probably be simplified but this works for now



        #evil movement
        for x in listofevilcats:
            if 5 < t < 24 or 29 < t < 48:
                evilnextspot = ((move_em_evil(x.pos,moves2,listofgoodcatspostotal)))
                x.pos = evilnextspot



        
        #goodcat turn bad when on box
        for obj in listofgoodcats:
            for row in range(RMAX):
                for col in range(CMAX):
                    if (row,col) in boxes and obj.pos[row,col] > 0: #if goodcat on box
                        NewEvilCat = EvilCat(np.zeros((RMAX,CMAX), dtype="int16"), 'NewEvilCat born at timestep: %s' % t, 'B%s' % t) #new evil cat created
                        NewEvilCat.pos[row,col] += obj.pos[row,col] #new evil cat is given good cat's position
                        listofevilcats.append(NewEvilCat) #added to list of evil cats
                        obj.pos[row,col] = 0  #good cat "killed", gives illusion of good cat transforming to evil cat
                        print(obj.name, "turned evil!")

        

        #evil cat eating good cat
        for x in listofevilcats:
            for obj in listofgoodcats:
                for row in range(RMAX):
                    for col in range(CMAX):
                        if x.pos[row,col] and obj.pos[row,col] > 0: #if evil cat on top of good cat
                            obj.pos[row,col] = 0 #good cat "dies"
                            x.hunger = initialevilhunger #evil cat hunger increases to max
                            print(x.name, "ate", obj.name)



        #drink methods for both cats
        [obj.drink(obj.pos,water) for obj in listofgoodcats]
        [x.drink(x.pos,water) for x in listofevilcats]

        #eat methods for both cats
        [obj.eat(obj.pos,food) for obj in listofgoodcats]
        [x.eat(x.pos,food) for x in listofevilcats]

        
        

        #this loop is done again to now have an updated list of the good cats after theyve died of hunger or thirst or age or transformed or been eaten etc. just a final updated list to use that the start of the next loop when printing the "total number of good cats" in the log updates of each step
        goodnext = []
        for obj in listofgoodcats:
            goodnext.append(obj.pos)
        listofgoodcatspostotal = sum(goodnext)


        #same reason
        evilnext = []
        for x in listofevilcats:
            evilnext.append(x.pos)
        listofevilcatspostotal = sum(evilnext)
        



        #final creation of graph/simulation space/plot
        make_feature_scatter(water, "c", 0.8)
        make_feature_scatter(food, "g", 0.6)
        make_feature_scatter(boxes,"darkgoldenrod", 0.5) #brown colour
        for obj in listofgoodcats:
            make_cat_scatter(obj.pos,"b", obj.alpha, r"$ {} $".format(obj.number)) #weird notation done for marker that makes it more visible on graph. reference to how i found this given in references on report
        for x in listofevilcats:
            make_cat_scatter(x.pos, "r", x.alpha, r"$ {} $".format(x.number))
        if 0 <= t < 5 or 24 <= t < 29:
            plt.title("Cat Simulation (time = " + str(t) + ":00): Cats are asleep")
        else:
            plt.title("Cat Simulation (time = " + str(t) + ":00): Cats are awake")
        plt.xlabel("Columns")
        plt.ylabel("Rows")
        plt.xlim(-1,CMAX)
        plt.ylim(-1,RMAX)
        plt.pause(1)
        plt.clf()

if __name__ == "__main__":
    main()

