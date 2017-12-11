#!/usr/bin/python2.7
# coding=utf-8
from numpy import inf, copy
from lab10 import *


class TravellingSalesmanProblemSolver(object):
    def __init__(self, c):
        self.c = c
        self.n = len(c[0])
        self.r = reduce(lambda s, x: s + x, [c[i][i + 1] for i in xrange(self.n - 1)]) + c[self.n - 1][0]
        self.plan = range(self.n).append(0)

    def calculate_plan(self, res):  # проходимся по всем и считаем сумму рекорд
        return reduce(lambda s, x: s + x, [self.c[i][res[i]] for i in xrange(self.n)])

    def dfs(self, v):  # обход в глубину для ветвления
        self.used[v] = True
        self.components[self.comp_index].append((v, self.assigment_problem_res[v]))
        if not self.used[self.assigment_problem_res[v]]:
            self.dfs(self.assigment_problem_res[v])

    def create_components(self):  # вычисляем компоненты плана (подциклы считаем)
        self.used = [False for _ in xrange(self.n)]
        self.components = []
        self.comp_index = 0
        for i in xrange(self.n):
            if not self.used[i]:
                self.components.append([])
                self.dfs(i)
                self.comp_index += 1

    def branch_and_bound(self):  # основной метод
        try:
            self.assigment_problem_res = AssignmentProblemSolver(copy(self.c)).solve()  # решаем задачу о назначениях
            r = self.calculate_plan(self.assigment_problem_res)  # считаем план для нашей задачи (первоначальной)
            raised = False
        except ValueError:
            raised = True  # не имеет решений
        if raised or r >= self.r:
            return  # если рекорд больше старого тоже выходим
        self.create_components()  # иначе находим компоненты плана (их количество)

        if (len(self.components) == 1):  # если их количество равно 1 - значит это задача о назначениях
            self.plan = [c[0] for c in self.components[0]]
            self.plan.append(0)
            self.r = r  # пересчитываем план и перезаписываем рекорд
        else:
            for component in self.components:  # иначе ветвим и ставим бесконечности
                for i, j in component:
                    cij = self.c[i][j]
                    self.c[i][j] = inf
                    self.branch_and_bound()
                    self.c[i][j] = cij  # так пока не кончаться задачи (кончится рекурсия)

    def solve(self):  # просто вызываем метод
        self.branch_and_bound()
        return self


if __name__ == '__main__':
    c = [
        [inf, 10, 25, 25, 10],  # из первого города в первый и т.д.
        [1, inf, 10, 15, 2],
        [8, 9, inf, 20, 10],
        [14, 10, 24, inf, 15],
        [10, 8, 25, 27, inf]
    ]
    res = TravellingSalesmanProblemSolver(c).solve()
    print res.plan
    print res.r
