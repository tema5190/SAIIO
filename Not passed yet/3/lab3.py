#!/usr/bin/python2.7
from numpy import *
from simplex_method import SimplexMethodSolver
from math import floor
import code


class IntegerLinearProgrammingSolver(object):
    def __init__(self, A, b, c, d_low=None, d_high=None):
        self.A = A
        self.b = b
        self.c = c
        self.d_low = d_low
        self.d_high = d_high
        self.m, self.n = A.shape
        self.has_solution = False
        self.optimal_cost = -inf
        self.eps = 0.000001

    def is_integer(self, val):
        return abs(round(val) - val) < self.eps

    def is_integers(self, x):
        round_x = array([round(el) for el in x])
        return all(abs(round_x - x) < self.eps)

    def get_index_of_first_float(self, x):
        round_x = array([round(el) for el in x])
        return list(abs(round_x - x) < self.eps).index(False)

    def change_params(self, res):
        self.A = res.A
        self.B = res.B
        self.b = res.b
        self.c = res.c
        self.basic_indexes = res.basic_indexes
        self.nonbasic_indexes = res.nonbasic_indexes
        self.n = res.n
        self.m = res.m
        self.x = res.x

    def create_y(self):  # y - вспомоигательный вектор
        i0 = self.get_index_of_first_float(self.x)
        ji0 = self.basic_indexes.index(i0)  # Находим первую не целочисленную переменную
        return dot(eye(self.m)[:, ji0], self.B)  # возвращаем единичный вектор(где лежит не целая) умноженную на B => y

    def change_A(self, y):  # Добавляем ограничения в А
        alpha = dot(y, self.A)  # Сложная магия (математика) из методы
        alpha = array([round(el) if self.is_integer(el) else el for el in alpha])
        alpha = array([el - floor(el) for el in alpha])
        self.A = vstack([self.A, alpha])
        column = -eye(self.m + 1)[:, self.m]
        self.A = hstack([self.A, column.reshape(self.m + 1, 1)])

    def change_b(self, y):  # Умножаем y на B, б
        betta = dot(y, self.b)  # получаем число betta
        betta = betta - floor(betta)  # берём его дробную часть
        self.b = append(self.b, [betta])  # добавляем Дробную betta в наш вектор b

    def change_c(self):  # добавляем 0 для этой переменной в C
        self.c = append(self.c, [0])

    def change_restrictions(self, y):  # меняем ограничения
        self.change_A(y)
        self.change_b(y)
        self.change_c()
        self.m += 1
        self.n += 1

    def the_gomori_method(self):
        while True:
            res = SimplexMethodSolver(self.A, self.b, self.c).solve()  # решаем первый раз
            self.change_params(res)  # меняем параметры
            if (self.is_integers(self.x)):  # проверка на целочисленность
                return self
            y = self.create_y()  # пошла жара
            self.change_restrictions(y)  # меняем и погнали заного


if __name__ == "__main__":
    with open('test2.txt') as file:
        m, n = [int(elem) for elem in file.readline().split() if elem != ""]
        A = zeros((m, n))
        for i in xrange(m):
            A[i] = [float(elem) for elem in file.readline().split() if elem != ""]

        b = array([float(elem) for elem in file.readline().split() if elem != ""])
        c = array([float(elem) for elem in file.readline().split() if elem != ""])

    x0 = IntegerLinearProgrammingSolver(A, b, c).the_gomori_method()
    print map(lambda x: int(x), x0.x)
    print dot(x0.c, x0.x)
