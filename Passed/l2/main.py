import json

from dual_simplex import DualSimplex
from helpers import *


class Task(object):
    def __init__(self, A, b, c, dl, dr):
        self.A = np.array(A, dtype=float)
        self.b = np.array(b, dtype=float)
        self.c = np.array(c, dtype=float)
        self.dl = np.array(dl, dtype=float)
        self.dr = np.array(dr, dtype=float)


def solve(A, b, c, dl, dr):
    tasks = list()
    tasks.append(Task(A, b, c, dl, dr))

    r = -np.inf

    while tasks:
        task = tasks[0]

        tasks.pop(0)

        dual_simplex_solver = DualSimplex(task.A, task.b, task.c, task.dl, task.dr)
        result = dual_simplex_solver.solve()

        if result.x is None:
            continue

        if isinstance(result.c_x, str) or result.c_x <= r:
            continue

        if all([is_int(val) for val in result.x]):
            r, x = result.c_x, result.x
            continue

        xj, j = next((x_j, j) for j, x_j in enumerate(result.x) if not is_int(x_j))

        lj = get_ceil(xj)

        new_dr = np.array(task.dr)
        new_dr[j] = lj
        tasks.append(Task(task.A, task.b, task.c, task.dl, new_dr))

        new_dl = np.array(task.dl)
        new_dl[j] = lj + 1
        tasks.append(Task(task.A, task.b, task.c, new_dl, task.dr))

    return {"x": x, "c_x": sum([ci * xi for ci, xi in zip(c, x)]) if x is not None else None}


if __name__ == '__main__':
    tasks = json.loads(open("input.txt").read()).values()

    for task in tasks:
        sln = solve(**task)
        print(get_str_result(task["A"], task["b"], task["c"], task["dl"], task["dr"], sln["x"], sln["c_x"]))
