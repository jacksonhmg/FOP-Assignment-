# initialise variables to be later addressed
RMAX = 25
CMAX = 30
initialgoodthirst = 50
initialgoodhunger = 35
initialevilthirst = 40
initialevilhunger = 15
steps = 50
import random


#initialise classes
class GoodCat():
    states = ["child","adult","dead"]
    def __init__(self, pos, name, number):
        self.name = name
        self.pos = pos
        self.age = random.randint(0,7)
        self.initialage = self.age
        self.state = self.states[0]
        self.thirst = initialgoodthirst
        self.hunger = initialgoodhunger
        self.initialgoodhunger = initialgoodhunger
        self.alpha = 1
        self.maxage = 40
        self.number = number

    def __str__(self):
        return self.state + "@" + str(self.pos)

    def drink(self, catarray, waterlist):
        self.thirst -= 1
        if self.thirst == 0:
            self.state = self.states[2]
        if self.state == self.states[2]:
            for row in range(RMAX):
                for col in range(CMAX):
                    for g in range(self.pos[row,col]):
                        self.pos[row,col] -= 1 #"kills" cat by removing position
                        print(self.name, 'died of dehydration!')
        for row in range(RMAX):
            for col in range(CMAX):
                if (row,col) in waterlist and catarray[row,col] >0: #checks if on top of one another
                    if self.thirst < initialgoodthirst: #if thirsty
                        self.thirst = initialgoodthirst
                        print(self.name, 'drank!')

    def eat(self, catarray, foodlist):
        self.hunger -= 1
        if self.hunger == 0:
            self.state = self.states[2]
        if self.state == self.states[2]:
            for row in range(RMAX):
                for col in range(CMAX):
                    for g in range(self.pos[row,col]):
                        self.pos[row,col] -= 1
                        print(self.name, 'died of hunger!')
        for row in range(RMAX):
            for col in range(CMAX):
                if (row,col) in foodlist and catarray[row,col] > 0:
                    if self.hunger < initialgoodhunger:
                        self.hunger = initialgoodhunger
                        print(self.name, 'ate!')


    def stepChange(self):
        self.age += 1
        if self.age < 10:
            self.state = self.states[0]
        if self.age > self.maxage:
            self.state = self.states[2]
        else:
            self.state = self.states[1]

        if self.state == self.states[2]:
            for row in range(RMAX):
                for col in range(CMAX):
                    for g in range(self.pos[row,col]):
                        self.pos[row,col] -= 1
                        print(self.name, 'died of old age!')


class EvilCat():
    states = ["child","adult","dead"]
    def __init__(self, pos, name, number):
        self.name = name
        self.pos = pos
        self.age = random.randint(0,7)
        self.initialage = self.age
        self.state = self.states[0]
        self.thirst = initialevilthirst
        self.hunger = initialevilhunger
        self.alpha = 1
        self.maxage = 40
        self.number = number

    def __str__(self):
        return self.state + "@" + str(self.pos)

    def drink(self, catarray, waterlist):
        self.thirst -= 1
        if self.thirst == 0:
            self.state = self.states[2]
        if self.state == self.states[2]:
            for row in range(RMAX):
                for col in range(CMAX):
                    for g in range(self.pos[row,col]):
                        self.pos[row,col] -= 1
                        print(self.name, 'died of dehydration!')
        for row in range(RMAX):
            for col in range(CMAX):
                if (row,col) in waterlist and catarray[row,col] >0:
                    if self.thirst < initialevilthirst:
                        self.thirst = initialevilthirst
                        print(self.name, 'drank!')

    def eat(self, catarray, foodlist):
        self.hunger -= 1
        if self.hunger == 0:
            self.state = self.states[2]
        if self.state == self.states[2]:
            for row in range(RMAX):
                for col in range(CMAX):
                    for g in range(self.pos[row,col]):
                        self.pos[row,col] -= 1
                        print(self.name, 'died of hunger!')
        for row in range(RMAX):
            for col in range(CMAX):
                if (row,col) in foodlist and catarray[row,col] > 0:
                    if self.hunger < initialevilhunger:
                        self.hunger = initialevilhunger
                        print(self.name, 'ate!')

    def stepChange(self):
        self.age += 1
        if self.age < 10:
            self.state = self.states[0]
        if self.age > self.maxage:
            self.state = self.states[2]
        else:
            self.state = self.states[1]

        if self.state == self.states[2]:
            for row in range(RMAX):
                for col in range(CMAX):
                    for g in range(self.pos[row,col]):
                        self.pos[row,col] -= 1
                        print(self.name, 'died of old age!')

