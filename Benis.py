# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:01:36 2018

@author: himmelreich, stegemann, kuehne
"""
import numpy
import random

class Playing_field:
    
    # constructor
    def __init__(self, field, gamma = 0.5, ev_number = 1, error = 0.2):
        self._field = field
        self._policy = Playing_field.generate_random_policy(len(field), len(field[0]))
        self._values = numpy.zeros((len(field), len(field[0])))
        self._gamma = gamma
        self._ev_number = ev_number
        self._error = error
        self._goal_reward = 1
        self._pitfall_reward = -1
        self._standard_reward = 0.042
    
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
        for y in range(len(self._field)):
            for x in range(len(self._field[0])):
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
        if self._field[x][y] == "G":
            return self._goal_reward
        elif self._field[x][y] == "P":
            return self._pitfall_reward
        elif self._field[x][y] == "E":
            return self._standard_reward
        else:
            return 0
        
    
    '''
    iterates through playing field, adjusts values according to policy
    '''    
    def update_values(self):
        new_values = numpy.empty([len(self._field), len(self._field[0])])
        for y in range(len(self._field)):
            for x in range(len(self._field[0])):
                new_values[x][y] = self.evaluate(x, y, self._policy[x][y])
        self._values = new_values
     
    '''
    prints playing field
    '''    
    def print_field(self):
        # printing playing field
        for y in range (len(self._field)):
            print(self._field[y])
        # printing values
        for y in range (len(self._values)):
            print(self._values[y])
        # printing policy
        for y in range (len(self._policy)):
            print(self._policy[y])
    
    '''
    performs one iteration of evaluating the current policy and choosing a new one
    '''    
    def step(self):
        for x in range(self._ev_number):
            Playing_field.update_values(self)
        self.update_policy()
        
    def test(self):
        print("test successfull")
    
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
        
new_field = Playing_field(numpy.array([['E','E', 'E', 'G'],\
                                       ['E','O', 'E', 'P'],\
                                       ['E','E', 'E', 'E']], dtype=object))
new_field.print_field() 
new_field.step()
new_field.print_field() 
new_field.step()
new_field.print_field()   
    