# import student's functions
from solution import *
from sokoban import sokoban_goal_state, PROBLEMS
import os

# Select what to test
test_time_astar = True
test_time_gbfs = True
test_manhattan = True
test_fval_function = True
test_iterative_gbfs = True
test_alternate = True
test_iterative_astar = True
test_weighted_astar = True

def test_time_astar_fun():

    timebound = 5
    s0 = PROBLEMS[19]  # Problems get harder as i gets bigger
    time = os.times()[0]
    weight = 2
    final = iterative_astar(s0, heur_fn=heur_alternate, weight=weight, timebound=timebound)
    difference = os.times()[0] - time
    print('This amount of time was given: {}'.format(timebound))
    print('Your iterative_astar used this amoung of time: {}'.format(difference))

    if heur_alternate(s0) == 0:
        print('Please complete implementations before testing timekeeping')
        return

    if difference - timebound < 0.1:
        print('Time keeping was acceptable on this problem')
    if difference - timebound >= 0.1:
        print('Time keeping was not acceptable on this problem')

def test_time_gbfs_fun():

    timebound = 5
    s0 = PROBLEMS[19]  # Problems get harder as i gets bigger
    time = os.times()[0]
    final = iterative_gbfs(s0, heur_fn=heur_alternate, timebound=timebound)
    difference = os.times()[0] - time
    print('This amount of time was given: {}'.format(timebound))
    print('Your iterative_gbfs used this amoung of time: {}'.format(difference))

    if heur_alternate(s0) == 0:
        print('Please complete implementations before testing timekeeping')
        return
        
    if difference - timebound < 0.1:
        print('Time keeping was acceptable on this problem')
    if difference - timebound >= 0.1:
        print('Time keeping was not acceptable on this problem')

def test_manhattan_fun():
    ##############################################################
    # TEST MANHATTAN DISTANCE
    print('Testing Manhattan Distance')

    # Correct Manhattan distances for the initial states of the provided problem set
    correct_man_dist = [4, 8, 8, 3, 3, 11, 7, 11, 10, 12, 12, 13, 10, 13, 10, 35, 28, 41, 43, 36, 2, 2]

    solved = 0;
    unsolved = [];

    for i in range(0, len(PROBLEMS)):
        # print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]

        man_dist = heur_manhattan_distance(s0)
        print('calculated man_dist:', str(man_dist))
        # To see state
        # print(s0.state_string())
        if man_dist == correct_man_dist[i]:
            solved += 1
        else:
            unsolved.append(i)

    print("*************************************")
    print("In the problem set provided, you calculated the correct Manhattan distance for {} states out of 22.".format(
        solved))
    print("States that were incorrect: {}".format(unsolved))
    print("*************************************\n")
    ##############################################################

def test_alternate_fun():

    ##############################################################
    # TEST ALTERNATE HEURISTIC
    print('Testing alternate heuristic with best_first search')

    solved = 0;
    unsolved = [];
    benchmark1 = 9;
    benchmark2 = 16;
    timebound = 2  # time limit

    #for reference, solution lengths are here
    man_dist_solns = [29, 24, 23, 24, 12, -99, -99, 41, 20, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 30, 21]
    better_solns = [-99, 24, 23, 20, 12, -99, -99, 41, 20, -99, 73, 52, 64, 39, 40, 160, 139, -99, -99, 207, 30, 19]

    for i in range(0, len(PROBLEMS)):

        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        se = SearchEngine('best_first', 'full')
        se.init_search(s0, goal_fn=sokoban_goal_state, heur_fn=heur_alternate)
        final, stats = se.search(timebound)

        if final:
            # final.print_path()
            solved += 1
        else:
            unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("The manhattan distance implementation solved {} out of {} practice problems given {} seconds.".format(
        benchmark1, len(PROBLEMS), timebound))
    print("The better implementation solved {} out of {} practice problems given {} seconds.".format(benchmark2,
                                                                                                     len(PROBLEMS),
                                                                                                     timebound))
    print("*************************************\n")
    ##############################################################

def test_fval_function_fun():

    test_state = SokobanState("START", 6, None, None, None, None, None, None, None)

    correct_fvals1 = [6, 11, 16]

    ##############################################################
    # TEST fval_function
    print("*************************************")
    print('Testing fval_function')

    solved1 = 0
    weights = [0.01, .5, 1.]
    for i in range(len(weights)):

        test_node = sNode(test_state, hval=10, fval_function=fval_function)

        fval = round(fval_function(test_node, weights[i]), 0)
        print('Test', str(i), 'calculated fval:', str(fval), 'correct:', str(correct_fvals1[i]))

        if fval == correct_fvals1[i]:
            solved1 += 1

    print("\n*************************************")
    print("Your fval_function calculated the correct fval for {} out of {} tests.".format(solved1, len(correct_fvals1)))
    print("*************************************\n")

    ##############################################################

def test_iterative_gbfs_fun():

    man_dist_solns = [20, 19, 21, 20, 8, -99, -99, 41, 15, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 30, 19]
    len_benchmark = [-99, 19, 21, 20, 9, -99, -99, 41, 15, -99, 73, 49, 62, 39, 38, 160, 139, -99, -99, 207, 30, 19]
    
    
    ##############################################################
    # TEST iterative GBFS
    print('Testing iterative GBFS')

    solved = 0;
    unsolved = [];
    benchmark = 0;
    timebound = 2  # 2 second time limit
    for i in range(0, len(PROBLEMS)):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        final, stats = iterative_gbfs(s0, heur_fn=heur_alternate, timebound=timebound)

        if final:
            # final.print_path() #if you want to see the path
            if final.gval <= len_benchmark[i] or len_benchmark[
                i] == -99:  # replace len_benchmark with man_dist_solns to compare with manhattan dist.
                benchmark += 1
            solved += 1
        else:
            unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved,
                                                                                                              benchmark))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("The manhattan distance implementation solved 9 out of the 22 practice problems given 2 seconds.")
    print("The better implementation solved 16 out of the 22 practice problems given 2 seconds.")
    print("*************************************\n")

def test_iterative_astar_fun():

    man_dist_solns = [17, 18, 21, 10, 8, -99, -99, 41, 14, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, -99, 30, 19]
    len_benchmark = [-99, 18, 21, 10, 8, -99, -99, 41, 14, -99, 36, 30, 28, 27, 27, -99, -99, -99, -99, -99, 30, 19]
    

    ##############################################################
    # TEST iterative WEIGHTED A STAR
    print('Testing iterative Weighted A Star')

    solved = 0;
    unsolved = [];
    benchmark = 0;
    timebound = 2 # 2 second time limit
    for i in range(0, len(PROBLEMS)):
        print("*************************************")
        print("PROBLEM {}".format(i))

        s0 = PROBLEMS[i]  # Problems get harder as i gets bigger
        weight = 10  # note that if you want to over-ride this initial weight in your implementation, you are welcome to!
        final, stats = iterative_astar(s0, heur_fn=heur_alternate, weight=weight, timebound=timebound)

        if final:
            # final.print_path()
            if final.gval <= len_benchmark[i] or len_benchmark[i] == -99:
                benchmark += 1
            solved += 1
        else:
            unsolved.append(i)

    print("\n*************************************")
    print("Of {} initial problems, {} were solved in less than {} seconds by this solver.".format(len(PROBLEMS), solved,
                                                                                                  timebound))
    print("Of the {} problems that were solved, the cost of {} matched or outperformed the benchmark.".format(solved,
                                                                                                              benchmark))
    print("Problems that remain unsolved in the set are Problems: {}".format(unsolved))
    print("The manhattan distance implementation solved 9 out of the 22 practice problems given 2 seconds.")
    print("The better implementation solved 13 out of the 22 practice problems given 2 seconds.")
    print("*************************************\n")
    ##############################################################

def test_weighted_astar_fun():
    solved, score1, score2 = 0, 0, 0
    weights = [10, 5, 2, 1]

    for j in range(0, 5):  # tiny problems only!
        m = PROBLEMS[j]  # Problems get harder as j gets bigger
        state_counts = []
        gvals = []
        for weight in weights:
            final, stats = weighted_astar(m, heur_fn=heur_manhattan_distance, weight=weight,
                                          timebound=5)  # nice liberal timebound here :)
            if final:
                solved += 1 #must solve one
                state_counts.append(stats.states_expanded)
                gvals.append(final.gval)
            else:
                state_counts.append(-99)
                gvals.append(-99)

        # now test the state_counts and gvals
        if solved == 0:
            flag = False  # solved nothing!
        else:
            flag = True

        for i in range(0, len(state_counts) - 2):  # forward check
            if state_counts[i + 1] != -99 and gvals[i + 1] == -99:  # no solution, means no comparison to be made
                if state_counts[i] > state_counts[i + 1] or gvals[i] < gvals[
                    i + 1]:  # state counts should be increasing and gvals decreasing
                    flag = False
        if flag: score1 += 1  # did we pass?

        if solved == 0:
            flag = False  # solved nothing!
        else:
            flag = True

        for i in range(len(state_counts) - 1, 0, -1):  # backward check
            if state_counts[i - 1] != -99 and gvals[i - 1] == -99:  # no solution, means no comparison to be made
                if gvals[i - 1] == -99 and gvals[
                    i] != -99:  # no solution with a lower weight, but a solution with a higher one
                    flag = False
        if flag: score2 += 1  # did we pass?

    summary_score = score1 + score2
    print("\n*************************************")
    print("Of the 20 runs over 5 problems, {} solutions were found with weighted a star in the time allotted.".format(
        solved))
    print("Weighted a-star expanded more nodes as weights decreased {} of 5 times".format(score1))
    print("Estimated score is {} of 10.".format(summary_score))
    print("*************************************\n")

def test_all():
    if test_time_astar: test_time_astar_fun()
    if test_time_gbfs: test_time_gbfs_fun()
    if test_manhattan: test_manhattan_fun()
    if test_fval_function: test_fval_function_fun()
    if test_iterative_gbfs: test_iterative_gbfs_fun()
    if test_alternate: test_alternate_fun()
    if test_iterative_astar: test_iterative_astar_fun()
    if test_weighted_astar: test_weighted_astar_fun()

if __name__=='__main__':
    test_all()

