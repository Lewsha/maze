__author__ = 'Lewsha'


import math
import copy
import sys


#Object of class - square of our maze
class Square():
    def __init__(self, x_position, y_position, adjacency, north, south, east, west):
        self._y_position = y_position
        self._x_position = x_position
        self._adjacency = adjacency
        self._north = north
        self._south = south
        self._east = east
        self._west = west

    def set_north(self, north):
        self._north = north

    def set_south(self, south):
        self._south = south

    def set_east(self, east):
        self._east = east

    def set_west(self, west):
        self._west = west

    def get_x(self):
        return self._x_position

    def get_y(self):
        return self._y_position

    def get_adj(self):
        return self._adjacency

    def get_north(self):
        return self._north

    def get_south(self):
        return self._south

    def get_east(self):
        return self._east

    def get_west(self):
        return self._west


#function for building maze
def adjacency_table(string):
    string = string[0:string.find('end')]
    string = string.split('\n')
    adj_table = []
    for i in range(len(string) - 1):
        adj_table.append(list())
        adj_table[i] = string[i].split()
    for i in range(0, len(adj_table)):
        for j in range(0, len(adj_table[i])):
            adj_table[i][j] = int(adj_table[i][j])
    return adj_table


#function for searching of shortest way
def bfs_bomb(start, end, maze, bomb_count, adj_table):
    #usual bfs
    level = {start: 0}
    parent = {start: None}
    i = 1
    frontier = [start]
    heap = list()
    heap.append(start)
    while end not in heap and frontier:
        next = []
        for u in frontier:
            for v in maze[u].get_adj():
                if v not in level and v not in heap:
                    heap.append(v)
                    level[v] = i
                    parent[v] = u
                    next.append(v)
        frontier = next
        i += 1
    result = list()
    result.append(end)
    i = end
    while start not in result:
        result.append(parent[i])
        i = parent[i]
    result.reverse()

    x_distance = int(math.fabs(maze[start].get_x() - maze[end].get_x()))
    y_distance = int(math.fabs(maze[start].get_y() - maze[end].get_y()))
    min_lenght = x_distance + y_distance
    if len(result) < min_lenght:
        print('No way!')
    if len(result) == min_lenght:
        return result
    if bomb_count > 0:
        #modified bfs
        #algorithm enumerates all possible ways using bombs
        adj = copy.deepcopy(adj_table)
        level = {start: 0}
        bomb_parent = {start: None}
        ways_bomb_count = {start: bomb_count}
        i = 1
        frontier = [start]
        heap = list()
        heap.append(start)
        while end not in heap and frontier and bomb_count >= 0:
            next = []
            for u in frontier:
                for v in adj[u]:
                    ways_bomb_count[v] = ways_bomb_count[u]
                if (maze[u].get_north() is not None) and maze[u].get_north() not in adj[u] and ways_bomb_count[u] > 0:
                    adj[u].append(maze[u].get_north())
                    if adj[u][len(adj[u]) - 1] not in heap:
                        ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
                if (maze[u].get_south() is not None) and maze[u].get_south() not in adj[u] and ways_bomb_count[u] > 0:
                    adj[u].append(maze[u].get_south())
                    if adj[u][len(adj[u]) - 1] not in heap:
                        ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
                if (maze[u].get_east() is not None) and maze[u].get_east() not in adj[u] and ways_bomb_count[u] > 0:
                    adj[u].append(maze[u].get_east())
                    if adj[u][len(adj[u]) - 1] not in heap:
                        ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
                if (maze[u].get_west() is not None) and maze[u].get_west() not in adj[u] and ways_bomb_count[u] > 0:
                    adj[u].append(maze[u].get_west())
                    if adj[u][len(adj[u]) - 1] not in heap:
                        ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
                for v in adj[u]:
                    if v not in level and v not in heap:
                        heap.append(v)
                        level[v] = i
                        bomb_parent[v] = u
                        next.append(v)
            frontier = next
            i += 1
        bomb_result = list()
        bomb_result.append(end)
        i = end
        while start not in bomb_result:
            bomb_result.append(bomb_parent[i])
            i = bomb_parent[i]
        bomb_result.reverse()
        if len(bomb_result) < len(result):
            return bomb_result


#taking information about maze
try:
    file = open(sys.argv[1], 'r')
    string = file.read()
    file.close()
except FileNotFoundError:
    print('File not found')
    exit()
info = string[string.find('end') + 4:].split()
bomb_count = int(info[0])
start = int(info[1])
end = int(info[2])
#building of maze
adj_table = adjacency_table(string)
a = math.sqrt(len(adj_table))
maze = list()
for i in range(len(adj_table)):
    f = Square(int(i // a), int(i % a), adj_table[i], None, None, None, None)
    if i - a > 0:
        f.set_north(int(i - a))
    if (i // a) == (i - 1) // a:
        f.set_east(int(i - 1))
    if (i // a) == (i + 1) // a:
        f.set_west(int(i + 1))
    if (i + 10) < len(adj_table):
        f.set_south(int(i + 10))
    maze.append(f)
print(bfs_bomb(start, end, maze, bomb_count, adj_table))
