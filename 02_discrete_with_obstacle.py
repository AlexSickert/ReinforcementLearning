#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Nov  6 11:19:12 2019

@author: alex
"""

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Nov 13 10:45:23 2018

@author: alex
"""

"""
↖
↗
↘
↙
←
↑
→
↓
©
®
×
<
>
"""
import math
import random
import time 
import sys

import numpy as np
import pandas as pd

actions = []
actions.append("↑")
actions.append("↗")
actions.append("→")
actions.append("↘")
actions.append("↓")
actions.append("↙")
actions.append("←")
actions.append("↖")

move_dic = {}
move_dic[actions[0]] = [-1, 0]
move_dic[actions[1]] = [-1, 1]
move_dic[actions[2]] = [0, 1]
move_dic[actions[3]] = [1, 1]
move_dic[actions[4]] = [1, 0]
move_dic[actions[5]] = [1, -1]
move_dic[actions[6]] = [0, -1]
move_dic[actions[7]] = [-1, -1]

board = []

y_board = 20
x_board = 80

y_goal = 18
x_goal = 78


def build_q_table(y_range, x_range, actions):
    
    table = {}
    
    for y in range(y_range):
        for x in range(x_range):
            a_arr = []
            for a in range(actions):
                a_arr.append(0)
            table[str(y) + "-" + str(x)] = a_arr
   
    return table

q_table = build_q_table(20, 80, 8)
    


    


def initialize_board(y_range, x_range):
    global board
    
    x_mid = int(x_range * 0.5)
    
    board = []
    
    for y in range(y_range):
        
        row = []
        for x in range(x_range):
            if y == 0 or y == y_range-1:
                c = "_"
            else:
                
                if x == 0 or x == x_range-1:
                    c = "|"
                else:
                    # generate some barriers where robot needs to go around
                    if x == x_mid and y > 5:
                        c = "|"
                    else:                    
                        c = " "
                    #c = " "
                        
            row.append(c)
        board.append(row)
        

    
    
                    
                
def show_board():
    global board
    s = ""
    for row in board:
        s += "\n"
        for col in row:
            s += col
    s += "\n"
    print(s)
        
    
def set_in_board(y, x, val):
    global board
    
    board[y][x] = val
    
    

   
#set_in_board(10, 40, actions[3])    


def crash_check(y, x):
    
    obstacle = board[y][x]
    #print(obstacle)
    
    if "|" in obstacle or "_" in obstacle:
        #print("crash")
        return True
    return False
    
        
def look_ahead_for_objects(y, x, dy, dx, steps):
    
    global board
    
    y_now = y
    x_now = x
    ret = -1

    for i in range(steps):
        
        y_now = y_now + dy
        x_now = x_now + dx
        v = board[y_now][x_now]
        
        if "_" in v or "|" in v :
            ret = i
            return ret

    return ret
        

def obejcts_in_sight(y, x, steps, sign):
    
    global actions
    
    i = actions.index(sign)
    
    li = i-1
    
    if li < 0:
        li = len(actions) -1
        
    ri = i + 1
    
    if ri >  len(actions) -1:
        ri = 0
    

    
    #if actions[0] in sign:
    l = look_ahead_for_objects(y, x, move_dic[actions[li]][0] , move_dic[actions[li]][1] , steps)
    m = look_ahead_for_objects(y, x, move_dic[actions[i]][0] , move_dic[actions[i]][1] , steps)
    r = look_ahead_for_objects(y, x, move_dic[actions[ri]][0] , move_dic[actions[ri]][1] , steps)
        
    return l, m, r
            
        
def gps_distance(y, x, y_goal, x_goal):

    dx = x_goal - x
    dy = y_goal - y
    
    dx = dx * dx
    dy = dy * dy
    
    d = math.sqrt(dx + dy)
    
    #print("distance: ", int(d) )
    return str(d)
    

def choose_best_action(current_state):
    
    global q_table
    
    arr = q_table[current_state]
    
    m = max(arr)
    
    if m == 0:
        action = random.randint(0, 7)
        #print("random action")
    else:    
        action = arr.index(m)
        
    return action, m
    
    

def get_reward(y_now, x_now, action, previous_distance):

    global y_goal
    global x_goal
    
    y_now += move_dic[actions[action]][0]
    x_now += move_dic[actions[action]][1]
    
    if crash_check(y_now, x_now ):
        reward = -100
        terminated = True
        
    else:
        
        reward = previous_distance - float(gps_distance(y_now, x_now, y_goal, x_goal))
        terminated = False
        
    return reward, terminated


def update_q_table(current_state, new_state, q, reward, terminated):
    
    global q_table
    
    a, m = choose_best_action(new_state)
    
    if terminated:
        q_t = reward
    else:
        q_t = reward + 0.95 * m
        
    a, m = choose_best_action(current_state)
        
    q_table[current_state][a] += 0.95 * (q_t - q) 
    #print("setting state ", current_state, " action ", a, " to value ", q_table[current_state][a])
    
    

for episode in range(300):
    
    
    
    initialize_board(y_board, x_board) 
    
    terminated = False
    y_now = 5
    x_now = 5
    
    show_interval_max = 100
    show_interval = 0
    
    show_board()
    
    
    #current_state = gps_distance(y_now, x_now, y_goal, x_goal)
    
    while not terminated:       
        
              
        
        distance_to_goal = float(gps_distance(y_now, x_now, y_goal, x_goal))
        
        current_state = str(y_now) + "-" + str(x_now)
        
        action, q = choose_best_action(current_state)
        
        # clear pervious
        set_in_board(y_now, x_now, ".") 
        
        #print("action: ", action)
        
        y_now += move_dic[actions[action]][0]
        x_now += move_dic[actions[action]][1]
    
        # calc new position based on action
    
        reward, terminated =  get_reward(y_now, x_now, action, distance_to_goal)
        
        new_state = str(y_now) + "-" + str(x_now)
        
        if not terminated:
            
            sign = actions[action]       
           
            set_in_board(y_now, x_now, sign) 
        
        
            gps_distance(y_now, x_now, y_goal, x_goal)
            
            set_in_board(y_now, x_now, sign) 
            
            l , m, r = obejcts_in_sight(y_now, x_now, 100, sign)
            #print("objects left: ", l)
            #print("objects middle: ", m)
            #print("objects right: ", r)
         
        #else:
            #print("terminated")
            
        
        update_q_table(current_state, new_state, q, reward, terminated)
        
        show_interval += 1
        if show_interval > show_interval_max:
            show_interval = 0
            print("episode ", episode)  
            show_board()
            time.sleep(0.5)
            

print("episode ", episode)              
show_board()        

    



    