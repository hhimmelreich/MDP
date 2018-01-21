# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:01:36 2018

@author: himmelreich, stegemann, kuehne
"""
import numpy
import random

class Playing_field:
    
    # constructor
    def __init__(self, field, gamma = 1, ev_number = 20, error = 0.2):
        self._field = field
        self._policy = Playing_field.generate_random_policy(len(field), len(field[0]))
        self._values = numpy.zeros((len(field), len(field[0])))
        self._gamma = gamma
        self._ev_number = ev_number
        self._error = error
        self._goal_reward = 1
        self._pitfall_reward = -1
        self._standard_reward = -0.04
    
    # getters
    def get_field(self):
        return self._field
    
    def get_policy(self):
        return self._policy
    
    def get_values(self):
        return self._values
    
    def get_gamma(self):
        return self.gamma
    
    def get_ev_number(self):
        return self.ev_number
    
    def get_error(self):
        return self.error
    
    # setters
    def set_field(self, field):
        self._field = field
        
    def set_policy(self, policy):
        self._policy = policy
        
    def set_values(self, values):
        self._values = values
        
    def set_gamma(self, gamma):
        self._gamma = gamma
        
    def set_ev_number(self, ev_number):
        self._ev_number = ev_number
        
    def set_error(self, error):
        self._error = error
        
    '''
    generates an array of length x, y, containing random policy
    '''
    def generate_random_policy(x_length, y_length):
        # up, down, right, left
        directions = [[0,-1], [0,1], [1,0], [-1,0]]
        rand_policy = numpy.empty([x_length, y_length], dtype=object)
        
        for y in range(y_length):
            for x in range(x_length):
                rand_policy[x][y] = random.choice(directions)
        return rand_policy
        
    
    '''
    iterates through whole playing field, evaluates worth of each possible
    policy entry, sets policy as best(maximal) one.
    '''    
    def update_policy(self):
        for x in range(len(self._field)):
            for y in range(len(self._field[0])):
                # evaluate different policy option
                up = self.evaluate(x, y, [0,-1])
                down = self.evaluate(x, y, [0,1]) 
                right = self.evaluate(x, y, [1,0])
                left = self.evaluate(x, y, [-1,0])
                # set new policy
                if (max(up, down, right, left) == up):
                    self._policy[x][y] = [0,-1]
                elif (max(up, down, right, left) == down):
                    self._policy[x][y] = [0,1]
                elif (max(up, down, right, left) == right):
                    self._policy[x][y] = [1,0]
                elif (max(up, down, right, left) == left):
                    self._policy[x][y] = [-1,0] 
    
    '''
    evaluates a specific policy entry, gives back corresponding value
    '''                
    def evaluate(self, x, y, dir):
        # if the policy tells us to move out of the field or on an obstacle, stay in place instead.
        # for moving correctly:
        if 0 <= (x + dir[0]) < len(self._field) and 0 <= (y + dir[1]) < len(self._field[0]) \
        and self._field[x + dir[0], y + dir[1]] != "O":
            forward = ((1 - self._error) * self._values[x + dir[0], y + dir[1]])
        else:
            forward = ((1 - self._error) * self._values[x, y])
        # for moving left:
        if 0 <= (x + Playing_field.neighbours(dir)[0][0]) < len(self._field) and 0 <= (y + Playing_field.neighbours(dir)[0][1]) < len(self._field[0]) \
        and self._field[x + Playing_field.neighbours(dir)[0][0], y + Playing_field.neighbours(dir)[0][1]] != "O":
            left = (self._error/2 * self._values[x + Playing_field.neighbours(dir)[0][0], y + Playing_field.neighbours(dir)[0][1]])
        else:
            left = (self._error/2 * self._values[x, y])
        # for moving right:
        if 0 <= (x + Playing_field.neighbours(dir)[1][0]) < len(self._field) and 0 <= (y + Playing_field.neighbours(dir)[1][1]) < len(self._field[0]) \
        and self._field[x + Playing_field.neighbours(dir)[1][0], y + Playing_field.neighbours(dir)[1][1]] != "O":
            right = (self._error/2 * self._values[x + Playing_field.neighbours(dir)[1][0], y + Playing_field.neighbours(dir)[1][1]])
        else:
            right = (self._error/2 * self._values[x, y])
            
        return self.reward_funct(x, y) + self._gamma * (forward + left + right)
    
    '''
    gives back the reward for moving on a specific field
    '''
    def reward_funct(self, x, y):
        if self._field[x][y] == "E":
            return self._goal_reward
        elif self._field[x][y] == "P":
            return self._pitfall_reward
        elif self._field[x][y] == "F":
            return self._standard_reward
        else:
            return 0
        
    
    '''
    iterates through playing field, adjusts values according to policy
    '''    
    def update_values(self):
        new_values = numpy.zeros([len(self._field), len(self._field[0])])
        for x in range(len(self._field)):
            for y in range(len(self._field[0])):
                if self._field[x][y] == "F":
                    
                    new_values[x][y] = self.evaluate(x, y, self._policy[x][y])
                elif self._field[x][y] == "E":
                    new_values[x][y] = self._goal_reward
                elif self._field[x][y] == "P":
                    new_values[x][y] = self._pitfall_reward
        self._values = new_values
     
    '''
    prints playing field
    '''    
    def print_field(self):
        policy = numpy.empty([len(self._field), len(self._field[0])], dtype=object)
        for x in range (len(self._field)):
            for y in range (len(self._field[0])):
                if self._field[x][y] == "E":
                    policy[x][y] = "E    "
                elif self._field[x][y] == "P":
                    policy[x][y] = "P    "
                elif self._field[x][y] == "O":
                    policy[x][y] = "O    "
                elif self._policy[x][y] == [-1, 0]:
                    policy[x][y] = "up   "
                elif self._policy[x][y] == [1, 0]:
                    policy[x][y] = "down "
                elif self._policy[x][y] == [0, 1]:
                    policy[x][y] = "right"
                elif self._policy[x][y] == [0, -1]:
                    policy[x][y] = "left "
        
        # printing policy
        print("Policy:")
        for y in range (len(policy)):
            print(policy[y])
        print("")
        
        values = numpy.empty([len(self._field), len(self._field[0])], dtype=object)
        for x in range (len(self._field)):
            for y in range (len(self._field[0])):
                if self._field[x][y] == "O":
                   values[x][y] = "O"
                else:
                    #values[x][y] = round(float(self._values[x][y]), 3)
                    values[x][y] = self._values[x][y]
        
        # printing values
        print("Values:")
        for x in range (len(self._values)):
            print("[", end="")
            for y in range (len(self._values[0])):
                #print(values[y])
                if self._field[x][y] == "O":
                    print(" X    ", end=" ")
                else:
                    print("%6.3f"% (values[x][y]), end=" ")
            print("]")
        print("")

    
    '''
    performs one iteration of evaluating the current policy and choosing a new one
    '''    
    def step(self):
        self._values = numpy.zeros([len(self._values), len(self._values[0])])
        for x in range(self._ev_number):
            Playing_field.update_values(self)
        self.update_policy()
    
    '''
    takes a direction as input and gives back the neighbours, represented as change
    in coordinates
    '''    
    def neighbours(dir):
        # dir = up
        if dir == [0,-1]:
            # left, right
            return [[-1,0], [1,0]]
        # dir = right
        elif dir == [1,0]:
            # up, down
            return [[0,-1], [0,1]]
        # dir = down
        elif dir == [0,1]:
            # right, left
            return [[1,0], [-1,0]]
        # dir = left
        elif dir == [-1,0]:
            # down, up
            return [[0,1], [0,-1]]
        
# open specified file
with open(input("Enter Filename: ")) as input_file:
    input_grid = input_file.readlines()
    line_length = len(input_grid[0].split())
    field = numpy.empty([len(input_grid), line_length], dtype=object)
    # write each entry of the grid world in a 2x2 array
    for i in range (len(input_grid)):
        line = input_grid[i].split()
        for j in range(len(line)):
            field[i][j] = line[j]
new_field = Playing_field(field)
new_field.print_field() 
new_field.step()
new_field.print_field()
for x in range (50):
    new_field.step()
new_field.print_field()   
    