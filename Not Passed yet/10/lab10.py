#!/usr/bin/python2.7
from numpy import *


def assignment_problem(a, n):
	u = [0 for i in xrange(n + 1)]
	v = [0 for i in xrange(n + 1)]
	way = [0 for i in xrange(n + 1)]
	p = [0 for i in xrange(n + 1)]
	for i in xrange(1, n + 1):
		p[0] = i
		j0 = 0
		minv = [inf for i in xrange(n + 1)]
		used = [False for i in xrange(n + 1)]
		while (True):
			used[j0] = True
			i0 = p[j0]
			delta = inf
			j1 = -1
			for j in xrange(1, n + 1):
				if not used[j]:
					cur = a[i0][j] - u[i0] - v[j]
					if (cur < minv[j]):
						minv[j] = cur
						way[j] = j0

					if (minv[j] < delta):
						delta = minv[j]
						j1 = j

			for j in xrange(n + 1):
				if used[j]:
					u[p[j]] += delta
					v[j] -= delta
				else:
					minv[j] -= delta

			j0 = j1
			if p[j0] == 0:
				break

		while (True):
			j1 = way[j0]
			p[j0] = p[j1]
			j0 = j1
			if j0==0: 
				break

	ans = [0 for i in xrange(n + 1)]
	for j in xrange(1, n + 1):
		ans[p[j]] = j

	print -v[0]
	return ans


if __name__ == "__main__":
	a = [
		[0, 0, 0, 0, 0],
		[0, 2, -1 , 9, 4],
		[0, 3, 2, 5, 1],
		[0, 13, 0, -3, 4],
		[0, 5, 6, 1, 2]
	]
	n = 4
	res = assignment_problem(a, n)
	print res