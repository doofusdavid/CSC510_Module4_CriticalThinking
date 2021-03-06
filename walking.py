#!/usr/bin/env python
# coding: utf-8

from __future__ import print_function

import math
from simpleai.search import SearchProblem, astar, greedy

MAP = """
##############################
#         M              #   #
# MMMM    MMMMMMMM       #   #
#  o M    M              #   #
#    MMM     MMMM   MMMMMM   #
#         MMMM      M        #
#            M  MMMMMMMMMMMM #
#     MMMMMMMM  M       M x  #
#        M      M            #
##############################
"""
MAP = [list(x) for x in MAP.split("\n") if x]

COSTS = {
    "up": 1.0,
    "down": 1.0,
    "left": 1.0,
    "right": 1.0,
    "up left": 1.4,
    "up right": 1.4,
    "down left": 1.4,
    "down right": 1.4,
    "up mountain": 2.0,
    "down mountain": 2.0,
    "left mountain": 2.0,
    "right mountain": 2.0,
    "right mountain": 2.0,
    "up left mountain": 2.8,
    "up right mountain": 2.8,
    "down left mountain": 2.8,
    "down right mountain": 2.8
}


class GameWalkPuzzle(SearchProblem):

    def __init__(self, board):
        self.board = board
        self.goal = (0, 0)
        for y in range(len(self.board)):
            for x in range(len(self.board[y])):
                if self.board[y][x].lower() == "o":
                    self.initial = (x, y)
                elif self.board[y][x].lower() == "x":
                    self.goal = (x, y)

        super(GameWalkPuzzle, self).__init__(initial_state=self.initial)

    def actions(self, state):
        actions = []
        for action in list(COSTS.keys()):
            newx, newy = self.result(state, action)
            if self.board[newy][newx] != "#":
                if self.board[newy][newx] != "M" and action.count("mountain") == 0:
                    actions.append(action)
                if self.board[newy][newx] == "M" and action.count("mountain") > 0:
                    actions.append(action)
        return actions

    def result(self, state, action):
        x, y = state

        if action.count("up"):
            y -= 1
        if action.count("down"):
            y += 1
        if action.count("left"):
            x -= 1
        if action.count("right"):
            x += 1

        new_state = (x, y)
        return new_state

    def is_goal(self, state):
        return state == self.goal

    def cost(self, state, action, state2):
        return COSTS[action]

    def heuristic(self, state):
        x, y = state
        gx, gy = self.goal
        # return abs(x-gx) + abs(y-gy)
        return math.sqrt((x - gx) ** 2 + (y - gy) ** 2)


def main():
    problem = GameWalkPuzzle(MAP)
    result = astar(problem, graph_search=True)
    print("A*")
    displayResults(problem, result)
    result = greedy(problem, graph_search=True)
    print("Greedy")
    displayResults(problem, result)


def displayResults(problem, result):
    fullpath = result.path()
    path = [x[1] for x in fullpath]
    for y in range(len(MAP)):
        for x in range(len(MAP[y])):
            if (x, y) == problem.initial:
                print("o", end='')
            elif (x, y) == problem.goal:
                print("x", end='')
            elif (x, y) in path:
                if MAP[y][x] == "M":
                    print("!", end='')
                else:
                    print("??", end='')
            else:
                print(MAP[y][x], end='')
        print()
    cost = sum(COSTS[x[0]] for x in fullpath[1:])
    mountain_moves = 0
    for x in fullpath[1:]:
        if x[0].count("mountain"):
            mountain_moves += 1

    print("Total Cost: ", cost)
    print("Mountain Moves: ", mountain_moves)
    print("")


if __name__ == "__main__":
    main()
