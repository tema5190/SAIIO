import json

inf = float('inf')

if __name__ == '__main__':
    g = json.loads(open('input.txt').read())
    n = len(g)

    s = 0
    d = [inf] * n
    p = [0] * n

    d[s] = 0
    u = [False] * n

    for i in range(n):
        v = -1
        for j in range(n):
            if not u[j] and (v == -1 or d[j] < d[v]):
                v = j

        if d[v] == inf:
            break
        u[v] = True

        for j in range(len(g[v])):
            to = g[v][j][0]
            l = g[v][j][1]

            if d[v] + l < d[to]:
                d[to] = d[v] + l
                p[to] = v

    print(d)

    for i in range(1, n):
        v = i
        path = []
        while v != s:
            v = p[v]
            path.insert(0, v)

        path.append(i)

        print("Path from {} to {} : {}".format(s, i, path))
