#!/usr/bin/python2.7
# coding=utf-8
from numpy import *
import Queue
import code


def make_graf(S, n): #строим граф списками смежности
	g = dict()
	for i in xrange(n):
		g[i] = []

	for i in xrange(len(S)):
		g[S[i][0]].append([S[i][1], S[i][2], 0]) # для прямых из какой в какую, и поток = 0 изначально
		g[S[i][1]].append([S[i][0], 0]) # для обатных пропускная способность будет 0

	return g # вернули граф


def solve_shortest_way(g, n, s, t): # поиск в ширину
	q = Queue.Queue()
	q.put(s)
	used = [False for i in xrange(n)]
	used[s] = True
	parent = [-1 for i in xrange(n)]
	flag = False
	# code.interact(local=dict(globals(), **locals()))
	while not q.empty():
		u = q.get()
		for v in g[u]:
			if not used[v[0]] and v[1] != 0:
				used[v[0]] = True
				parent[v[0]] = u
				q.put(v[0])
				if v[0] == t:
					flag = True
					break

		if flag:
			break

	path = []
	i = t
	if flag:
		while(i != s):
			path.append(i)
			i = parent[i]

		path.append(s)
		path.reverse()

	return path


def fordFalkerson(S, n, s, t):
	g = make_graf(S, n) # строим граф
	path = solve_shortest_way(g, n, s, t) # ищем путь
	flow = 0 # сразу поток равен 0
	while (len(path) != 0): # если пути нет - то жопа, иначе работает
		c = [] # c - массив пропускных способностей для выбранного кратчайшего пути
		for i in xrange(len(path) - 1):
			for j in xrange(len(g[path[i]])):
				if g[path[i]][j][0] == path[i+1]:
					break

			c.append(g[path[i]][j][1])

		c_min = min(c) # нашли с мин
		for i in xrange(len(path) - 1): # some magic
			for j in xrange(len(g[path[i]])): # проходимся  <-- вспомнить всё
				if g[path[i]][j][0] == path[i+1]:
					break

			if (len(g[path[i]][j])) == 3: #для прямых либо добавляем либо убираем для прямых
				g[path[i]][j][1] -= c_min # уменьшаем пропускную способнуть
				g[path[i]][j][2] += c_min # увеличиваем поток
				for k in xrange(len(g[path[i + 1]])):
					if g[path[i + 1]][k][0] == path[i]:
						break

				g[path[i + 1]][k][1] += c_min
			else: # для обратных дуг
				g[path[i]][j][1] -= c_min
				for k in xrange(len(g[path[i + 1]])):
					if g[path[i + 1]][k][0] == path[i]:
						break

				g[path[i + 1]][k][1] += c_min
				g[path[i + 1]][k][2] -= c_min

		flow += c_min # увеличиваем поток
		path = solve_shortest_way(g, n, s, t) # снова ищем кратчайший путь

	return [flow, g] # поток и граф


if __name__ == '__main__':
	S = [
		[0, 1, 12],
		[0, 5, 6],
		[1, 2, 2],
		[2, 3, 1],
		[2, 4, 5],
		[4, 3, 15],
		[4, 6, 2],
		[5, 1, 10],
		[5, 6, 8],
		[5, 4, 5],
		[6, 1, 2],
		[6, 2, 6]
	]
	s = 0
	t = 3
	n = 7
	res = fordFalkerson(S, n, s, t)
	print res
	"""S = [
		[0, 1, 4],
		[0, 3, 9],
		[1, 3, 2],
		[1, 4, 4],
		[2, 4, 1],
		[2, 5, 10],
		[3, 2, 1],
		[3, 5, 6],
		[4, 5, 1],
		[4, 6, 2],
		[5, 6, 9]
	]
	s = 0
	t = 6
	n = 7"""
