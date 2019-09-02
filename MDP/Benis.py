# -*- coding: utf-8 -*-
"""
Created on Sat Jan 20 13:01:36 2018

@author: himmelreich, stegemann, kuehne
"""
import numpy

class Playing_field:
    
    # constructor
    def __init__(self, field, gamma = 0.5, ev_number = 1, error = 0.2):
        self._field = field
        self._policy = numpy.zeros((len(field), len(field[0])))
        self._values = numpy.zeros((len(field), len(field[0])))
        self._gamma = gamma
        self._ev_number = ev_number
        self._error = error
    
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
    iterates through whole playing field, evaluates worth of each possible
    policy entry, sets policy as best(maximal) one.
    '''    
    def update_policy(self):
        for y in range (len(self._field)):
            for x in range (len(self._field[0])):
                # evaluate different policy option
                up = evaluate(self, x, y, [0,-1])
                down = evaluate(self, x, y, [0,1]) 
                right = evaluate(self, x, y, [1,0])
                left = evaluate(self, x, y, [-1,0])
                # set new policy
                if (max(up, down, right, left) == up):
                    self._policy[x][y] = "up"
                elif (max(up, down, right, left) == down):
                    self._policy[x][y] = "down"
                elif (max(up, down, right, left) == right):
                    self._policy[x][y] = "right"
                elif (max(up, down, right, left) == left):
                    self._policy[x][Y] = "left" 
    
    '''
    evaluates a specific policy entry, gives back corresponding value
    '''                
    def evaluate(self, x, y, dir):
        forward = ((1 - self._error) * self._values[x + dir[0], y + dir[1]])
        left = (self._error/2 * self._values[x + neighbours(dir)[0][0], y + neighbours(dir)[0][1]])
        right = (self._error/2 * self._values[x + neighbours(dir)[1][0], y + neighbours(dir)[1][1]])
        r(x, y, dir) + self._gamma * (forward + left + right)
    
    '''
    iterates through playing field, adjusts values according to policy
    '''    
    def update_values(self):
     
    '''
    prints playing field
    '''    
    def print_field(self):
    
    '''
    performs one iteration of evaluating the current policy and choosing a new one
    '''    
    def step(self):
        for x in range(_ev_number):
            update_values(self)
        update_policy(self)
    
    '''
    Takes a direction as input and gives back the neighbours, represented as change
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
        
    
    
