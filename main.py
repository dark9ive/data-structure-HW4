# dijkstra source: https://github.com/blkrt/dijkstra-python/blob/3dfeaa789e013567cd1d55c9a4db659309dea7a5/dijkstra.py
import networkx as nx
import matplotlib.pyplot as plt
import random
import heapq

def dijkstra(graph, source, target):
    heap = []
    visited = {}
    distance = {}
    shortest_distance = {}
    parent = {}

    for node in range(len(graph)):
        distance[node] = None
        visited[node] = False
        parent[node] = None
        shortest_distance[node] = float("inf")

    heapq.heappush(heap, (0, source))
    distance[source] = 0
    shortest_distance[source] = 0
    while len(heap) != 0:
        #print(heap)
        current = heapq.heappop(heap)[1]
        if visited[current] == True:
            continue
        visited[current] = True
        if current == target:
            break
        for neighbor in graph[current]:
            if visited[neighbor] == False:
                try:
                    distance[neighbor] = shortest_distance[current] + graph[current][neighbor]['length']
                    #print("{curr}, {neighbor} with length 2".format(curr=current, neighbor=neighbor))
                except KeyError:
                    distance[neighbor] = shortest_distance[current] + 1
                    #print(shortest_distance[current])
                if distance[neighbor] < shortest_distance[neighbor]:
                    shortest_distance[neighbor] = distance[neighbor]
                    parent[neighbor] = current
                    heapq.heappush(heap, (shortest_distance[neighbor], neighbor))
    #print(distance)
    #print(shortest_distance)
    #print(parent)
    #print(target)
    return shortest_distance[target]

def init_world(Max, X, Y):
    G = nx.watts_strogatz_graph(n = Max, k = 2, p = 0)
    edgedict = dict()
    for i in range(0, X, 1):
        again = True
        while again:
            again = False
            x = random.randint(0, Max-1)
            y = random.randint(0, Max-1)
            while x == y or abs(x-y) == 1 or abs(x-y) == Max-1:
                x = random.randint(0, Max-1)
                y = random.randint(0, Max-1)
            try:
                edgedict[x*Max+y] += 1
                again = True
            except KeyError:
                edgedict[x*Max+y] = 1
                edgedict[y*Max+x] = 1
                G.add_edge(x, y, length=Y)
    return G

def print_world(G):
    pos=nx.circular_layout(G)
    plt.figure(3,figsize=(10,10))
    nx.draw(G, pos, with_labels=True, font_weight='bold', node_size=600, font_size=20)
    nx.draw_networkx_edge_labels(G, pos)

def avg_distance(G, Z):
    total = 0
    for i in range(0, Z, 1):
        x = random.randint(0, Max-1)
        y = random.randint(0, Max-1)
        while x == y:
            x = random.randint(0, Max-1)
            y = random.randint(0, Max-1)
        ans=dijkstra(G, x, y)
        #print("{x}, {y}, ans:{ans}".format(x=x, y=y, ans=ans))
        
        total += ans
    return total/Z

if __name__ == '__main__':
    Max = 1000
    X = 200
    Y = 100
    Z = 100
    Round = 20
    for Y in range(1, 501, 1):
        total = 0
        csv_file = open("./log.csv", "a")
        for i in range(0, Round, 1):
            G = init_world(Max, X, Y)
            #print_world(G)
            total += avg_distance(G, Z)
        print("Avg distaance for Y = {Y} is {ans}".format(Y=Y, ans=total/Round))
        csv_file.write(str(total/Round) + '\n')
        csv_file.close()
