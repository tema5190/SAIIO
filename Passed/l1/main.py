from functools import reduce
import json
import numpy as np

from first_phase import solve as get_basis_ind

EPS = 0.0000001


class DualSimplex(object):
    def __init__(self, A, b, c, dl, dr):
        self.steps = 100
        self.A = np.array(A)
        self.m, self.n = self.A.shape
        self.b = np.array([b]).T
        self.c = np.array([c])
        self.dl = np.array([dl])
        self.dr = np.array([dr])
        self.Jb = get_basis_ind(self.A, self.b, self.c)

        self.x = None
        self.c_x = None

        self.solve()

    def solve(self):
        Ab = self.A[:, self.Jb]
        B = np.linalg.inv(Ab)
        cb = self.c[:, self.Jb]

        delta = np.dot(cb * B, self.A) - self.c

        J = [ind for ind in range(0, self.n)]

        Jn = [ind for ind in J if ind not in self.Jb]

        Jn_pos = [ind for ind in Jn if delta[0][ind] >= EPS]
        Jn_neg = [ind for ind in Jn if ind not in Jn_pos]

        while self.steps:
            self.steps -= 1

            def hi_func_non_base(ind):
                if ind in Jn_pos:
                    return self.dl[0][ind]
                elif ind in Jn_neg:
                    return self.dr[0][ind]
                else:
                    return None
                
            plan = np.array([hi_func_non_base(ind) for ind in J])

            prods = [np.dot(np.array([self.A[:, ind]]).T, plan[ind]) for ind in Jn]
            hib = np.dot(B, self.b - sum(prods)).T
            for ind, val in enumerate(self.Jb):
                plan[val] = hib[0][ind]

            is_optimal = all([self.dr[0][ind] + EPS >= plan[ind] >= self.dl[0][ind] - EPS for ind in self.Jb])

            if is_optimal:
                self.x, self.c_x = plan, np.dot(self.c, plan)[0]
                return self

            jk, k = np.inf, -1
            for ind, val in enumerate(self.Jb):
                if self.dr[0][val] < plan[val] + EPS or plan[val] < self.dl[0][val] - EPS:
                    if val < jk:
                        jk, k = val, ind

            e = np.zeros(len(self.Jb))
            e[k] = 1.0
            ujk = 1.0 if plan[jk] < self.dl[0][jk] else -1.0
            delta_y = np.dot(ujk, np.dot(np.eye(self.m, self.m)[:,k], B))
            mu = [np.dot(delta_y, self.A[:, ind]) for ind in Jn]

            def ok(ind, val):
                return (val in Jn_pos and mu[ind] < 0.0) or (val in Jn_neg and mu[ind] > 0.0)
            sigma = [[val, -delta[0][val] / mu[ind] if ok(ind, val) else np.inf] for ind, val in enumerate(Jn)]

            def min_sigma(x, y):
                if x[1] > y[1]:
                    return y
                else:
                    return x

            sigma0 = reduce(min_sigma, sigma, [-1, np.inf])
            # sigma0 = min(sigma)
            if sigma0[1] == np.inf:
                return self

            new_coplan = [self.new_delta(ind, jk, delta, ujk, Jn, sigma0, mu) for ind in J]
            delta[0] = new_coplan

            self.Jb[k] = sigma0[0]
            Ab = self.A[:, self.Jb]
            B = np.linalg.inv(Ab)

            Jn = [ind for ind in J if ind not in self.Jb]

            if ujk == 1.0:
                if sigma0[0] in Jn_pos:
                    Jn_pos[Jn_pos.index(sigma0[0])] = jk
                else:
                    Jn_pos.append(jk)

            if ujk == -1.0:
                if sigma0[0] in Jn_pos:
                    Jn_pos.pop(Jn_pos.index(sigma0[0]))

            Jn_neg = [ind for ind in Jn if ind not in Jn_pos]
            self.B, self.Ab = B, Ab

        self.x, self.c_x = None, None
        return self

    def new_delta(self, j, jk, delta, ujk, Jn, sigma0, mu):
        if j in Jn:
            return delta[0][j] + sigma0[1] * mu[Jn.index(j)]

        if j == jk:
            return delta[0][j] + sigma0[1] * ujk

        if j in self.Jb:
            return 0.0


if __name__ == '__main__':
    data = json.loads(open('input.txt').read())

    for task in data.values():
        simplex = DualSimplex(**task)
        # simplex.solve();
        print(simplex.x)
        print(simplex.c_x)
