#   Look for #IMPLEMENT tags in this file. These tags indicate what has
#   to be implemented to complete the warehouse domain.

#   You may add only standard python imports
#   You may not remove any imports.
#   You may not import or otherwise source any of your own files

import os  # for time functions
import math  # for infinity
from search import *  # for search engines
from sokoban import sokoban_goal_state, SokobanState, Direction, PROBLEMS  # for Sokoban specific classes and problems

heur_table = {}


def box_in_corner(box, state):
    (x, y) = box
    if x == 0:
        if y == 0 or y == state.height - 1:
            return True

    if x == state.width - 1:
        if y == 0 or y == state.height - 1:
            return True
    return False


def box_in_pseudo_corner(box, state):
    # Blockers contains original obstacles, other boxes, and the walls
    blockers = state.boxes.union(state.obstacles)
    (x, y) = box
    up = (x, y + 1)
    down = (x, y - 1)
    left = (x - 1, y)
    right = (x + 1, y)

    # Case 1: Form pseudo corner with walls and blockers
    if (up in blockers) or (down in blockers):
        if x == 0 or x == state.width - 1:
            return True

    if (left in blockers) or (right in blockers):
        if y == 0 or y == state.height - 1:
            return True

    # Case 2: Form pseudo corner with obstacles
    # did not consider boxes as other boxes can be moved and it is not a deadlock
    if up in state.obstacles and ((left in state.obstacles) or (right in state.obstacles)):
        return True
    if down in state.obstacles and ((left in state.obstacles) or (right in state.obstacles)):
        return True

    return False


def edge_without_storage(box, state):
    # If the box is along the wall and there is no storage along that wall -> deadlock
    (x, y) = box

    # Find possible storage positions first.
    possible_storages = []
    for store in state.storage:
        possible_storages.append(store)
    for box in state.boxes:
        if box in possible_storages:
            possible_storages.remove(box)

    # populate x_list and y_list with possible storage position
    (x_list, y_list) = ([], [])
    for storage_pos in possible_storages:
        x_list.append(storage_pos[0])
        y_list.append(storage_pos[1])

    if x == 0 and (0 not in x_list):
        return True
    elif x == (state.width - 1) and ((state.width - 1) not in x_list):
        return True

    elif y == 0 and (0 not in y_list):
        return True
    elif y == (state.height - 1) and ((state.width - 1) not in y_list):
        return True

    return False


def checkDeadLock(state):
    # for each box, check whether it's yet to be stored
    # if it is not stored in storage position, check whether current box position is deadlock
    for box in state.boxes:
        if box not in state.storage:
            if box_in_corner(box, state) or box_in_pseudo_corner(box, state) or edge_without_storage(box, state):
                return True
    return False


# SOKOBAN HEURISTICS
def heur_alternate(state):
    # IMPLEMENT
    '''a better heuristic'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # heur_manhattan_distance has flaws.
    # Write a heuristic function that improves upon heur_manhattan_distance to estimate distance between the current state and the goal.
    # Your function should return a numeric value for the estimate of the distance to the goal.
    # EXPLAIN YOUR HEURISTIC IN THE COMMENTS. Please leave this function (and your explanation) at the top of your solution file, to facilitate marking.

    heur_alt = 0

    # construct key for heuristic table
    key = ""
    for box1 in state.boxes:
        key = key + " " + str(box1[0]) + " " + str(box1[1])
    for robot in state.robots:
        key = key + " " + str(robot[0]) + " " + str(robot[1])

    # check whether current state is in the hash table
    # if it does, simply returns it. No need to recompute
    if key in heur_table:
        return heur_table[key]

    # check whether current state has a deadlock that will not allow puzzle completion
    # if there is a deadlock, return infinite heuristic and populate given state in the heuristic table
    if checkDeadLock(state):
        heur_table[key] = float("inf")
        return float("inf")

    # Assign the closest box to each of the robot
    # remove the box after it is assigned
    possible_boxes = []
    for box in state.boxes:
        possible_boxes.append(box)

    for robot in state.robots:
        min_dist = float("inf")
        remove = None
        for box in possible_boxes:
            if man_dist(robot, box) < min_dist:
                min_dist = min(man_dist(robot, box), min_dist)
                remove = box

        if remove is not None:
            possible_boxes.remove(remove)

        heur_alt += min_dist

    # Assign the closest storage to each of the box
    # Find possible storage positions first.
    possible_storages = []
    for store in state.storage:
        possible_storages.append(store)
    for box in state.boxes:
        if box in possible_storages:
            possible_storages.remove(box)

    for box in state.boxes:
        if box in state.storage:
            continue

        min_dist = float("inf")
        for storage in possible_storages:
            min_dist = min(man_dist(storage, box), min_dist)

        heur_alt += min_dist

    # populate table current state with its heuristic
    heur_table[key] = heur_alt
    return heur_alt

def heur_zero(state):
    '''Zero Heuristic can be used to make A* search perform uniform cost search'''
    return 0

def man_dist (n1,n2):
    return abs(n1[0] - n2[0]) + abs(n1[1] - n2[1])

def heur_manhattan_distance(state):
    # IMPLEMENT
    '''admissible sokoban puzzle heuristic: manhattan distance'''
    '''INPUT: a sokoban state'''
    '''OUTPUT: a numeric value that serves as an estimate of the distance of the state to the goal.'''
    # We want an admissible heuristic, which is an optimistic heuristic.
    # It must never overestimate the cost to get from the current state to the goal.
    # The sum of the Manhattan distances between each box that has yet to be stored and the storage point nearest to it is such a heuristic.
    # When calculating distances, assume there are no obstacles on the grid.
    # You should implement this heuristic function exactly, even if it is tempting to improve it.
    # Your function should return a numeric value; this is the estimate of the distance to the goal.

    sum = 0
    for box in state.boxes:
        distances = list()
        for storage in state.storage:
            curr = man_dist(box, storage)
            distances.append(curr)
        if len(distances) > 0:
            sum += min(distances)
    return sum

def fval_function(sN, weight):
    # IMPLEMENT
    """
    Provide a custom formula for f-value computation for Anytime Weighted A star.
    Returns the fval of the state contained in the sNode.

    @param sNode sN: A search node (containing a SokobanState)
    @param float weight: Weight given by Anytime Weighted A star
    @rtype: float
    """
    return sN.gval + weight * sN.hval

# SEARCH ALGORITHMS
def weighted_astar(initial_state, heur_fn, weight, timebound):
    # IMPLEMENT
    '''Provides an implementation of weighted a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of weighted astar algorithm'''

    weight = 5
    se = SearchEngine('custom', 'full')
    wrapped_fval_function = (lambda sN: fval_function(sN, weight))
    se.init_search(initial_state, sokoban_goal_state, heur_fn, wrapped_fval_function)

    final_state, final_stats = se.search(timebound)
    return final_state, final_stats

def iterative_astar(initial_state, heur_fn, weight=1, timebound=10):  # uses f(n), see how autograder initializes a search line 88
    # IMPLEMENT
    '''Provides an implementation of realtime a-star, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False as well as a SearchStats object'''
    '''implementation of iterative astar algorithm'''

    # find end time
    end_time = os.times()[0] + timebound

    # initialize Multiplier
    multiplier = 0.6

    # initialize the search engine
    se = SearchEngine('custom', 'full')
    se.init_search(initial_state, sokoban_goal_state, heur_fn, (lambda sN: fval_function(sN, weight)))

    # initialize default values for result and costbound
    best_state = False
    best_stat = None
    best_cost = float("inf")

    # initialize the time bound
    time_remaining = end_time - os.times()[0]

    while time_remaining > 0:

        # perform search
        curr_state, curr_stat = se.search(time_remaining, (float("inf"), float("inf"), best_cost))

        # if more optimal solution found, update the result and the cost bound
        if curr_state and best_cost > curr_state.gval + heur_fn(curr_state):
            best_state = curr_state
            best_stat = curr_stat
            best_cost = curr_state.gval + heur_fn(curr_state)

        # decrease the weight within each iteration
        weight = weight * multiplier

        # Update the time bound
        time_remaining = end_time - os.times()[0]

    return best_state, best_stat

def iterative_gbfs(initial_state, heur_fn, timebound=5):  # only use h(n)
    # IMPLEMENT
    '''Provides an implementation of anytime greedy best-first search, as described in the HW1 handout'''
    '''INPUT: a sokoban state that represents the start state and a timebound (number of seconds)'''
    '''OUTPUT: A goal state (if a goal is found), else False'''
    '''implementation of iterative gbfs algorithm'''

    # find end time
    end_time = os.times()[0] + timebound

    # initialize default value for result and cost bound
    final_state = False
    final_stat = None
    best_cost = float("inf")

    # initialize the search engine
    se = SearchEngine("best_first", "full")
    se.init_search(initial_state, sokoban_goal_state, heur_fn)

    # initialize time bound
    time_remaining = end_time - os.times()[0]

    while time_remaining > 0:
        # perform search
        curr_state, curr_stat = se.search(time_remaining, (best_cost, float("inf"), float("inf")))

        # if more optimal solution found, update the result and the cost bound
        if curr_state and best_cost > curr_state.gval:
            final_state = curr_state
            final_stat = curr_stat
            best_cost = final_state.gval

        # Update the time bound
        time_remaining = end_time - os.times()[0]

    return final_state, final_stat

