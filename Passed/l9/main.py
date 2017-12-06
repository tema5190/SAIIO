import json
import numpy as np


def prepare_d_matrix(graph):
    for u in range(len(graph)):
        for v in range(len(graph)):
            if (graph[u][v] == 0):
                if u != v:
                    graph[u][v] = float("inf")

    return graph


def prepare_r_matrix(n):
    next = [[] for i in range(n)]

    for arr in next:
        for i in range(n):
            arr.append(i + 1)

    return next


def floyd(graph):
    n = len(graph)

    next = prepare_r_matrix(n)
    graph = prepare_d_matrix(graph)

    for i in range(n):
        for u in range(n):
            for v in range(n):
                if graph[u][i] + graph[i][v] < graph[u][v]:
                    graph[u][v] = graph[u][i] + graph[i][v]
                    next[u][v] = next[u][i]

    return graph, next


def findPath(u, v, pathM, distanceM):
    if distanceM[u][v] == float('inf'):
        return "No path"

    c = u
    path = [u + 1]
    while c != v:
        c = pathM[c - 1][v - 1]
        path.append(c + 1)

    return path


if __name__ == "__main__":
    graph = json.loads(open("input.txt").read())

    print("D0:")
    print(np.matrix(graph))

    minPath, pathMatrix = floyd(graph)

    print("\nD:")
    print(np.matrix(minPath))

    print("\nR")
    print(np.matrix(pathMatrix))

    for u in range(len(graph)):
        for v in range(len(graph)):
            if v != u:
                print("Shortest path from {} to {} : {}".format(u + 1, v + 1, findPath(u, v, pathMatrix, minPath)))
