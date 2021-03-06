# Task: Put N queens in a MxM triangle board
# such as each queen cannot be insight of another queen
# 
# Original wording:
# "13. Rasti N valdovių išdėstymą M trikampėje lentoje, kad jos viena kitos nekirstų."

import sys
import timeit

def triangular_numbers(n):
    i, t = 1, 0
    while i <= n:
        yield t
        t += i
        i += 1


def print_board(board, m):
    cell_count = sum(range(0, m + 1))
    if cell_count != len(board):
        raise Exception("This board is not a triangle", cell_count, len(board))

    ix = 0
    jx = 0
    for l in range(0, m):
        ix += l + 1
        print(board[jx:ix])
        jx += l + 1

# --- Bruteforce methods

# Checks if a board is valid
def check_board(board, m):
    
    # checks rows
    # Works by counting 1s in a sublists
    ix = 0
    jx = 0
    for row in range(0, m):
        ix += row + 1
        if board[jx:ix].count(1) > 1:
            return False
        jx += row + 1
    
    # checks columns
    
    # builds a list of all possitions in that column
    possitions = list(triangular_numbers(m))
    for col in range(0, m):
        count = 0
        for pos in possitions:
            if board[pos]:
                count += 1
            if count > 1:
                return False
        
        possitions = list(map(lambda x: x + 1, possitions[1:]))

    # Checks diagonals
    possitions = list(triangular_numbers(m))
    for diag in range(0, m):
        
        count = 0
        for ix, pos in enumerate(possitions):
            if board[ix + pos]:
                count += 1
            
        if count > 1:
            return False
        
        possitions = possitions[1:]
    
    return True

def place_all(boards, board, poz, left, m):

    # Switch the lines bellow for full list of valid boards
    # if left >= 0:
    if left >= 0 and len(boards) == 0:
        ran = range(poz + 1, len(board) - left)
        for p in ran:
            board_copy = board.copy()
            board_copy[p] = 1
            
            if left == 0 and check_board(board_copy, m):
                boards.append(board_copy)

                # Remove the line bellow for full list of valid boards
                break
            else:
                place_all(boards, board_copy, p, left - 1, m)
    
    return boards

# Matrixes are initialized with zeroes 
# 1 indicates a placed queen
# n is a number of queens
# m - m x m matrix dimension
def bruteforce(m, n):
    return place_all([], [0] * sum(range(0, m + 1)), -1, n - 1, m)

# --- Backtracking methods

# Checks if a queen doesn't collide with other
# True => is valid i.e. doesn't collide
# False => is NOT valid i.e. does collide
def check_cell(board, m, poz):

    # checks rows
    # Works by counting 1s in a sublists
    ix = 0
    jx = 0
    for row in range(0, m):
        ix += row + 1
        if poz < ix and poz >= jx:
            if board[jx:ix].count(1) > 0:
                return False
        jx += row + 1

    # checks columns
    # builds a list of all possitions in that column
    possitions = list(triangular_numbers(m))
    for col in range(0, m):
        if poz in possitions:
            count = 0
            for pos in possitions:
                if board[pos]:
                    count += 1
                if count > 0:
                    return False
            
            break

        possitions = list(map(lambda x: x + 1, possitions[1:]))

    # Checks diagonals
    triangular_nums = list(triangular_numbers(m))
    for diag in range(0, m):
        
        possitions = []
        for ix, pos in enumerate(triangular_nums):
            possitions.append(ix + pos)
            
        if poz in possitions:
            count = 0
            for pos in possitions:
                if board[pos] == 1:
                    count += 1
                if count > 0:
                    return False
        
        possitions = possitions[1:]

    return True

def place_incrementally(boards, board, poz, left, m):
    
    # Switch the lines bellow for full list of valid boards
    # if left >= 0:
    if left >= 0 and len(boards) == 0:
        ran = range(poz + 1, len(board) - left)
        for p in ran:
            board_copy = board.copy()
            
            if check_cell(board_copy, m, p):
                board_copy[p] = 1
                
                if left == 0:
                    boards.append(board_copy)
                    
                    # Remove the line bellow for full list of valid boards
                    break
            
                else:
                    place_incrementally(boards, board_copy, p, left - 1, m)

    return boards

def backtracking(m, n):
    return place_incrementally([], [0] * sum(range(0, m + 1)), -1, n - 1, m)

if __name__ == '__main__':
    # Command line option parsing
    if len(sys.argv) == 3:
        m = int(sys.argv[1])  # M
        n = int(sys.argv[2])  # N
        print("Dim: ", m, " N:", n)
    else:
        print("Missing arguments")
        exit()
        
    # The interesting part
    # boards = bruteforce(m, n)
    boards = []
    TRIES = 3
    for im in range(4, 11):
        
        # print_board( backtracking(im, int(im/2)), im)
        
        avg = timeit.Timer("backtracking({}, {})"
            .format(im, int(im/2)), 'from __main__ import backtracking')\
            .timeit(number=TRIES) / TRIES
        
        print("For m={} n={} on avg. it took {}"
            .format(im, int(im/2), avg))
        
        
    # prints valid boards
    # if len(boards) > 0:
    #     print("VALID BOARD FOUND: ")
    #     for board in boards:
    #         print_board(board, m)
            
    # benchmark
    # import numpy as np
    # from bokeh.plotting import figure, output_file, show
    # from bokeh.layouts import row
    # output_file("benchmark.html")

    # TRIES = 3
    # MAX_BRUTE = 8
    # graph = []
    # for ix in range(4, 11):

    #     graph.append(figure(title="N={}".format(ix), x_axis_label='N', y_axis_label='Time'))

    #     brute_time = []
    #     back_time = []
    #     time_graph = []

    #     for jx in range(1, ix):
    #         brute_avg = timeit.Timer("bruteforce({}, {})"
    #             .format(ix, jx), 'from __main__ import bruteforce')\
    #             .timeit(number=TRIES) / TRIES
    #         brute_time.append(brute_avg)

    #         back_avg = timeit.Timer("backtracking({}, {})"
    #             .format(ix, jx), 'from __main__ import backtracking')\
    #             .timeit(number=TRIES) / TRIES
    #         back_time.append(back_avg)
    #         time_graph.append(jx)
            
    #         print("For m={} n={} on avg. it took {} for brute and {} for back"
    #             .format(ix, jx, brute_avg, back_avg))
    #         # print("For m={} n={} on avg. it took {} for back"
    #         #     .format(ix, jx, back_avg))
            
    #     graph[-1].line(time_graph, brute_time, color="red", legend_label="bruteforce")
    #     graph[-1].line(time_graph, back_time, color="blue",legend_label="backtracking")
    
    # MAX_BACK = 40
    # for ix in range(MAX_BRUTE, MAX_BACK):
    #     graph.append(figure(title="N={}".format(ix), x_axis_label='N', y_axis_label='Time'))

    #     back_time = []
    #     time_graph = []

    #     for jx in range(1, ix):

    #         back_avg = timeit.Timer("backtracking({}, {})"
    #             .format(ix, jx), 'from __main__ import backtracking')\
    #             .timeit(number=TRIES) / TRIES
    #         back_time.append(back_avg)
    #         time_graph.append(jx)
            
    #         print("For m={} n={} on avg. it took {} for back"
    #             .format(ix, jx, back_avg))
            
    #     graph[-1].line(time_graph, back_time, color="blue",legend_label="backtracking")
    
    # show(row(graph))
    
    # import time
    # time.sleep(1000000)
    
            
