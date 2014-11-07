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
                if (k + a) < squares_count:
                    if maze[i + 1][j] == 0:
                        adj_table[k].append(k + a)
                k += 1
    return adj_table


def bfs_bomb(start, end, bomb_count, maze, adj_table):
    #modified bfs
    #algorithm enumerates all possible ways using bombs
    min_lenght = int(math.fabs(start[1] - end[1]) + math.fabs(start[2] - end[2]))
    a = (len(maze) + 1) // 2
    bomb_result = list()
    for k in range(0, bomb_count + 1):
        bombs = k
        adj = copy.deepcopy(adj_table)
        level = {start[0]: 0}
        bomb_parent = {start[0]: None}
        ways_bomb_count = {start[0]: bombs}
        i = 1
        frontier = [start[0]]
        heap = list()
        heap.append(start[0])
        while end[0] not in heap and frontier and bombs >= 0:
            next = []
            for u in frontier:
                for v in adj[u]:
                    ways_bomb_count[v] = ways_bomb_count[u]
                for v in adj[u]:
                    if v not in level and v not in heap:
                        heap.append(v)
                        level[v] = i
                        bomb_parent[v] = u
                        next.append(v)
            for u in frontier:
                if (u - a > 0) and ((u - a) not in adj[u]) and (ways_bomb_count[u] > 0):
                    #print(u, u - a)
                    if u - a not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u - a]:
                        #print(u, 'north')
                        adj[u].append(u - a)
                        ways_bomb_count[u - a] = ways_bomb_count[u] - 1
                        level[u - a] = i
                        bomb_parent[u - a] = u
                        next.append(u - a)
                        heap.append(u - a)
                if ((u // a) == (u - 1) // a) and ((u - 1) not in adj[u]) and (ways_bomb_count[u] > 0):
                    #print(u, u // a)
                    if u - 1 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u - 1]:
                        #print(u, 'west')
                        adj[u].append(u - 1)
                        ways_bomb_count[u - 1] = ways_bomb_count[u] - 1
                        level[u - 1] = i
                        bomb_parent[u - 1] = u
                        next.append(u - 1)
                        heap.append(u - 1)
                if ((u // a) == (u + 1) // a) and (u + 1 not in adj[u]) and (ways_bomb_count[u] > 0):
                    #print(u, u // a)
                    if u + 1 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u + 1]:
                        #print(u, 'east')
                        adj[u].append(u + 1)
                        ways_bomb_count[u + 1] = ways_bomb_count[u] - 1
                        level[u + 1] = i
                        bomb_parent[u + 1] = u
                        next.append(u + 1)
                        heap.append(u + 1)
                if ((u + a) < a ** 2) and (u + a not in adj[u]) and (ways_bomb_count[u] > 0):
                    #print(u, u + a)
                    if u + 10 not in heap or (ways_bomb_count[u] - 1) > ways_bomb_count[u + a]:
                        #print(u, 'south')
                        adj[u].append(u + 10)
                        ways_bomb_count[u + a] = ways_bomb_count[u] - 1
                        level[u + a] = i
                        bomb_parent[u + a] = u
                        next.append(u + a)
                        heap.append(u + a)
            frontier = next
            i += 1
        bomb_result.append(list())
        bomb_result[k].append(end[0])
        j = end[0]
        if end[0] in heap:
            while start[0] not in bomb_result[k]:
                bomb_result[k].append(bomb_parent[j])
                j = bomb_parent[j]
            bomb_result[k].reverse()
        else:
            bomb_result[k].append('No way!')
    return bomb_result


#taking information about maze
try:
    file = open('test01.txt', 'r')
    text_string = file.read()
    file.close()
except FileNotFoundError:
    print('File not found')
    exit()
info = text_string[text_string.find('end') + 4:].split('\n')
bomb_count = int(info[0])
start = info[1].split()
end = info[2].split()
#print(info)
#print(bomb_count)
for i in range(0, len(start)):
    start[i] = int(start[i])
    end[i] = int(end[i])
maze = building_maze(text_string)
adj_table = adjacency_table(maze)
res = bfs_bomb(start, end, bomb_count, maze, adj_table)
min_length_result = [0, maze]
min_bomb_result = [bomb_count, maze]
min_combination_result = [bomb_count, maze]
for i in range(0, len(res)):
    if res[i][1] == 'No way!':
        continue
    if len(res[i]) - 1 < len(min_length_result[1]):
        min_length_result = [i, res[i]]
    if i < min_bomb_result[0]:
        min_bomb_result = [i, res[i]]
    if (i + len(res[i])) / 2 < (min_combination_result[0] + len(min_combination_result[1])) / 2:
        min_combination_result = [i, res[i]]
print(res)
print(min_length_result, min_bomb_result, min_combination_result)
