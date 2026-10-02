from __future__ import division
from __future__ import print_function

import sys
import math
import time
import queue as Q
import resource


#### SKELETON CODE ####
## The Class that Represents the Puzzle
class PuzzleState(object):
    """
        The PuzzleState stores a board configuration and implements
        movement instructions to generate valid children.
    """
    def __init__(self, config, n, parent=None, action="Initial", cost=0):
        """
        :param config->List : Represents the n*n board, for e.g. [0,1,2,3,4,5,6,7,8] represents the goal state.
        :param n->int : Size of the board
        :param parent->PuzzleState
        :param action->string
        :param cost->int
        """
        if n*n != len(config) or n < 2:
            raise Exception("The length of config is not correct!")
        if set(config) != set(range(n*n)):
            raise Exception("Config contains invalid/duplicate entries : ", config)

        self.n        = n
        self.cost     = cost
        self.parent   = parent
        self.action   = action
        self.config   = config
        self.children = []

        # Get the index and (row, col) of empty block
        self.blank_index = self.config.index(0)

    def display(self):
        """ Display this Puzzle state as a n*n board """
        for i in range(self.n):
            print(self.config[self.n*i : self.n*(i+1)])

    def move_up(self):
        """ 
        Moves the blank tile one row up.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index < self.n:
            return None
        new = list(self.config)
        i = self.blank_index
        new[i], new[i - self.n] = new[i - self.n], new=[i]
        return PuzzleState(tuple(new), self.n, self, "Up", self.cost + 1)
    
    def move_down(self):
        """
        Moves the blank tile one row down.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index >= self.n * (self.n - 1):
            return None
        new = list(self.config)
        i = self.blank_index
        new[i], new[i + self.n] = new[i + self.n], new[i]
        return PuzzleState(tuple(new), self.n, self, "Down", self.cost + 1)pass
      
    def move_left(self):
        """
        Moves the blank tile one column to the left.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == 0:
            return None
        new= list(self.config)
        i = self.blank_index
        new[i], new[i - 1] = new[i - 1],new[i]
        return PuzzleState(tuple(new), self.n, self, "Left", self.cost + 1)

    def move_right(self):
        """
        Moves the blank tile one column to the right.
        :return a PuzzleState with the new configuration
        """
        if self.blank_index % self.n == self.n - 1:
            return None
        new = list(self.config)
        i = self.blank_index
        new[i], new[i + 1] = new[i + 1],new[i]
        return PuzzleState(tuple(new), self.n, self, "Right", self.cost + 1)
      
    def expand(self):
        """ Generate the child nodes of this node """
        
        # Node has already been expanded
        if len(self.children) != 0:
            return self.children
        
        # Add child nodes in order of UDLR
        children = [
            self.move_up(),
            self.move_down(),
            self.move_left(),
            self.move_right()]

        # Compose self.children of all non-None children states
        self.children = [state for state in children if state is not None]
        return self.children

# Function that Writes to output.txt

### Students need to change the method to have the corresponding parameters
def writeOutput():
    ### Student Code Goes here
    # walk back up to parents to get path
    path = []
    cur = goal
    while cur.parent != None:
        path.append(cur.action)
        cur = cur.parent
    path = path[::-1]
     
    with open("output.txt", "w") as f:
        f.write("path_to_goal: " + str(path) + "\n")
        f.write("cost_of_path: " + str(goal.cost) + "\n")
        f.write("nodes_expanded: " + str(nodes_expanded) + "\n")
        f.write("search_depth: " + str(goal.cost) + "\n")
        f.write("max_search_depth: " + str(max_depth) + "\n")
        f.write("running_time: " + "%.8f" % run_time + "\n")
        f.write("max_ram_usage: " + "%.8f" % ram + "\n")



def bfs_search(initial_state):
    """BFS search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 
    frontier = Q.Queue()
    frontier.put(initial_state)
    visited = set()
    visited.add(tuple(initial_state.config))
    nodes_expanded = 0
    max_d = 0
 
    while not frontier.empty():
        state = frontier.get()
        if test_goal(state):
            run_time = time.time()-start
            ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2**20)
            writeOutput(state, nodes_expanded, max_d, run_time, ram)
            return state
        nodes_expanded += 1
        for child in state.expand():
            if tuple(child.config) not in visited:
                visited.add(tuple(child.config))
                frontier.put(child)
                if child.cost > max_d:
                    max_d = child.cost
 
    return None

def dfs_search(initial_state):
    """DFS search"""
    ### STUDENT CODE GOES HERE ###
    start = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
 
    frontier = [initial_state]  # using a list as the stack
    visited = set()
    visited.add(tuple(initial_state.config))
    nodes_expanded = 0
    max_d = 0
 
    while len(frontier) > 0:
        state = frontier.pop()
 
        if test_goal(state):
            run_time = time.time() - start
            ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2**20)
            writeOutput(state, nodes_expanded, max_d, run_time, ram)
            return state
 
        nodes_expanded += 1
        children = state.expand()
        # push in revrse so Up popped 1st
        for c in reversed(children):
            if tuple(c.config) not in visited:
                visited.add(tuple(c.config))
                frontier.append(c)
                if c.cost > max_d:
                    max_d = c.cost

def A_star_search(initial_state):
    """A * search"""
    ### STUDENT CODE GOES HERE ###
     start = time.time()
    start_ram = resource.getrusage(resource.RUSAGE_SELF).ru_maxrss
    # nodegot added, so ties on f get broken by who was pushed first UDLR
    count = 0
    frontier = Q.PriorityQueue()
    frontier.put((calculate_total_cost(initial_state), count, initial_state))
    visited = set()
    visited.add(tuple(initial_state.config))
    nodes_expanded = 0
    max_depth = 0
 
    while not frontier.empty():
        f, c, state = frontier.get()
        if test_goal(state):
            run_time = time.time() - start
            ram = (resource.getrusage(resource.RUSAGE_SELF).ru_maxrss - start_ram) / (2**20)
            writeOutput(state, nodes_expanded, max_depth, run_time, ram)
            return state
        nodes_expanded += 1
        for c in state.expand():
            if tuple(c.config) not in visited:
                visited.add(tuple(c.config))
                count += 1
                frontier.put((calculate_total_cost(c), count, c))
                if c.cost > max_depth:
                    max_depth = c.cost
 
    return None

def calculate_total_cost(state):
    """calculate the total estimated cost of a state"""
    ### STUDENT CODE GOES HERE ###
    h = 0
    for i in range(len(state.config)):
        tile = state.config[i]
        if tile == 0:
            continue  # blank -it does not count
        h += calculate_manhattan_dist(i, tile, state.n)
    return state.cost + h
 

def calculate_manhattan_dist(idx, value, n):
    """calculate the manhattan distance of a tile"""
    row, col = idx // n, idx % n
    goal_r = value // n
    goal_c = value % n
    return abs(row - goal_r) + abs(col - goal_c)

def test_goal(puzzle_state):
    """test the state is the goal state or not"""
    if tuple(puzzle_state.config) == tuple(range(puzzle_state.n * puzzle_state.n)):
        return True
    return False

# Main Function that reads in Input and Runs corresponding Algorithm
def main():
    search_mode = sys.argv[1].lower()
    begin_state = sys.argv[2].split(",")
    begin_state = list(map(int, begin_state))
    board_size  = int(math.sqrt(len(begin_state)))
    hard_state  = PuzzleState(begin_state, board_size)
    start_time  = time.time()
    
    if   search_mode == "bfs": bfs_search(hard_state)
    elif search_mode == "dfs": dfs_search(hard_state)
    elif search_mode == "ast": A_star_search(hard_state)
    else: 
        print("Enter valid command arguments !")
        
    end_time = time.time()
    print("Program completed in %.3f second(s)"%(end_time-start_time))

if __name__ == '__main__':
    main()
