__author__ = 'Lewsha'


import math
import copy
import sys

#function for building maze
def building_maze(string):
    string = string[:string.find('end') - 1]
    tmp_maze = string.split('\n')
    maze = list()
    for i in range(0, len(tmp_maze)):
        maze.append(list())
        maze[i] = tmp_maze[i].split()
    for i in range(0, len(maze)):
        for j in range(0, len(maze[i])):
            maze[i][j] = int(maze[i][j])
    return maze


def adjacency_table(maze):
    squares_count = ((len(maze) + 1) // 2) ** 2
    a = (len(maze) + 1) // 2
    adj_table = list()
    k = 0
    while k < squares_count:
        for i in range(0, len(maze), 2):
            for j in range(0, len((maze[i])), 2):
                adj_table.append(list())
                if k - a > 0:
                    if maze[i - 1][j] == 0:
                        adj_table[k].append(k - a)
                if (k // a) == (k - 1) // a:
                    if maze[i][j - 1] == 0:
                        adj_table[k].append(k - 1)
                if (k // a) == (k + 1) // a:
                    if maze[i][j + 1] == 0:
                        adj_table[k].append(k + 1)
                if (k + 10) < squares_count:
                    if maze[i + 1][j] == 0:
                        adj_table[k].append(k + a)
                k += 1
    return adj_table


def bfs_bomb(start, end, maze, adj_table):
    min_lenght = math.fabs(start[1] - end[1]) + math.fabs(start[2] - end[2])
    #modified bfs
    #algorithm enumerates all possible ways using bombs
    a = (len(maze) + 1) // 2
    adj = copy.deepcopy(adj_table)
    level = {start[0]: 0}
    bomb_parent = {start[0]: None}
    ways_bomb_count = {start[0]: bomb_count}
    i = 1
    frontier = [start[0]]
    heap = list()
    heap.append(start[0])
    while end[0] not in heap and frontier and bomb_count >= 0:
        next = []
        for u in frontier:
            for v in adj[u]:
                ways_bomb_count[v] = ways_bomb_count[u]
            if u - a > 0 and u - a not in adj[u] and ways_bomb_count[u] > 0:
                adj[u].append(u - a)
                if adj[u][len(adj[u]) - 1] not in heap:
                    ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
            if (u // a) == (u - 1) // a and u - 1 not in adj[u] and ways_bomb_count[u] > 0:
                adj[u].append(u - 1)
                if adj[u][len(adj[u]) - 1] not in heap:
                    ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
            if (u // a) == (u + 1) // a and u + 1 not in adj[u] and ways_bomb_count[u] > 0:
                adj[u].append(u + 1)
                if adj[u][len(adj[u]) - 1] not in heap:
                    ways_bomb_count[adj[u][len(adj[u]) - 1]] = ways_bomb_count[u] - 1
            if (u + 10) < a ** 2 and u + 10 not in adj[u] and ways_bomb_count[u] > 0:
                adj[u].append(u + 10)
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
    bomb_result.append(end[0])
    i = end[0]
    while start[0] not in bomb_result:
        bomb_result.append(bomb_parent[i])
        i = bomb_parent[i]
    bomb_result.reverse()
    return bomb_result


#taking information about maze
try:
    file = open('maze.txt', 'r')
    string = file.read()
    file.close()
except FileNotFoundError:
    print('File not found')
    exit()
info = string[string.find('end') + 4:].split('\n')
bomb_count = int(info[0])
start = info[1].split()
end = info[2].split()
for i in range(0, len(start)):
    start[i] = int(start[i])
    end[i] = int(end[i])
maze = building_maze(string)
adj_table = adjacency_table(maze)
print(bfs_bomb(start, end, maze, adj_table))