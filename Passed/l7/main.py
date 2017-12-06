import json

INF = float('-inf')


def ford_bellman(graph, begin):
    m = len(graph)
    n = max([x[0] for x in graph] + [x[1] for x in graph]) + 1
    d = [float('-inf')] * n
    d[begin] = 0
    f = [0] * n

    for i in range(n - 1):
        for j in range(m):
            if d[graph[j][0]] > INF:
                if d[graph[j][1]] < d[graph[j][0]] + graph[j][2]:
                    d[graph[j][1]] = d[graph[j][0]] + graph[j][2]

                    f[graph[j][1]] = graph[j][0]

    max_path_length = max(d)
    end = d.index(max_path_length)
    path = [end]
    # print(max_path_length)
    print(f)
    while f[end] != begin:
        path.append(f[end])
        end = f[end]

    path.append(0)
    path.reverse()

    return d, path


if __name__ == '__main__':
    data = json.loads(open('input.txt').read())

    print(ford_bellman(data, 0))
