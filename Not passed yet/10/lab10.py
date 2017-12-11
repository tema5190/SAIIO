#!/usr/bin/python2.7
# coding=utf-8
from numpy import *


def assignment_problem(a, n):
    u = [0 for i in xrange(n + 1)]  # компонент потенциала
    v = [0 for i in xrange(n + 1)]  # второй компонент потенциала (изначально потенциал нулевой)
    way = [0 for i in xrange(n + 1)]  # храним минимумы (где они достигаются) для удобства восстановления
    # увеличивающей цепочки
    p = [0 for i in xrange(n + 1)]  # храним паросочетания

    for i in xrange(1, n + 1):  # цикл по строка матрицы
        p[0] = i  # (в р0 номер текущей рассматриваемой строки
        j0 = 0  # свободный столбец p[jo]
        minv = [inf for i in xrange(n + 1)]  # вспомогательные минимумы для пересчёта потенциала
        used = [False for i in xrange(n + 1)]

        while True:
            used[j0] = True
            i0 = p[j0]
            delta = inf  # ####минимум в столбце изначально inf
            j1 = -1
            # где этот минимум был достигнут (изначально нигде, это ведь и так ясно, зачем ты это пишешь,
            # я уже плавлюсь)

            for j in xrange(1, n + 1):
                if not used[j]:
                    cur = a[i0][j] - u[i0] - v[j]  # перемчитываем если не посещена
                    #
                    if cur < minv[j]:  # если меньше чем minv то меняем и Minv и минимум устанавливаем
                        minv[j] = cur
                        way[j] = j0
                    #
                    if minv[j] < delta:  # если minvj стал меньше delta то ее следует перезаписать
                        delta = minv[j]
                        j1 = j  # как и jl
                        #

            for j in xrange(n + 1):  # пересчёт потенциала
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta

            j0 = j1  # перезаписываем минимум где он был записан
            if p[j0] == 0:  # алгоритм работает пока не найдено
                break

        while True:
            j1 = way[j0] # перезаписываем где был достигнут минимум
            p[j0] = p[j1] # и меняем номер рассматриавемой строки
            j0 = j1
            if j0 == 0: # выходим если
                break

    ans = [0 for i in xrange(n + 1)]
    for j in xrange(1, n + 1):
        ans[p[j]] = j #перезаписываем для ответа

    print -v[0]
    return ans


if __name__ == "__main__":
    a = [
        [0, 0, 0, 0, 0], # дополнительные строки и столбцы
        [0, 2, -1, 9, 4],
        [0, 3, 2, 5, 1],
        [0, 13, 0, -3, 4],
        [0, 5, 6, 1, 2]
    ]
    n = 4
    res = assignment_problem(a, n)
    print res
