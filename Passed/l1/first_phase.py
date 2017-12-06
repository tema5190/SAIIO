from numpy import *

EPS = 0.000001


def is_zero(value):
    return abs(value) < EPS


def solve(A, b, c):
    m, n = A.shape

    if any([element < 0 for element in b]):
        indexes = b < 0
        b[indexes] *= -1
        A[indexes, :] *= -1

    new_A = append(A.transpose(), eye(m, dtype=float64), axis=0).T

    x = append(zeros(n, dtype=float64), b)

    c = append(zeros(n, dtype=float64), -ones(m, dtype=float64))

    Jn = list(range(n))
    Jb = list(range(n, n + m))

    J = set(Jn)
    Ju = set(Jb)

    result_x = second_phase(new_A, b, c, x, Jb, Jn)

    if not all(abs(el) < EPS for el in result_x[-m:]):
        raise Exception("No sln")

    B = linalg.inv(new_A[:, Jb])
    lost_indexes = list(J - set(Jb))

    while True:
        if not set(Jb) & set(Ju):
            lJ = list(J)
            A = new_A[:, lJ]
            c = c[lJ]
            x = result_x[lJ]
            Jb = [lJ.index(el) for el in Jb]
            return Jb

        jk = (set(Jb) & set(Ju)).pop()
        k = jk - n
        ek = eye(m)[:, k]

        tmp = dot(ek, B)
        alpha = dot(tmp, new_A[:, lost_indexes])

        if not all([abs(el) < EPS for el in alpha]):
            s = list([abs(el) > EPS for el in alpha]).index(1)

            js = lost_indexes[s]

            Jb[k] = js
        else:
            Jb.remove(Jb[Jb.index(k)])
            Ju.remove(jk)

            new_A = delete(new_A, k, axis=0)

            b = delete(b, k)
            B = delete(B, k, axis=0)
            B = delete(B, k, axis=1)

            m -= 1


def get_index(arr, ind):
    try:
        return arr.index(ind)
    except ValueError:
        return -1


def get_new_B(B, z, s, m):
    zk = z[s]
    z[s] = -1
    z /= -zk
    M = eye(m)
    M[:, s] = z
    return dot(M, B)


def second_phase(A, b, c, x, Jb, Jn):
    m, n = A.shape
    basic_a = A[:, Jb]
    B = linalg.inv(basic_a)

    while True:
        basic_c = array([c[i] for i in Jb])

        u = dot(basic_c, B)
        delta = array(subtract(dot(u, A), c))

        k = get_index([delta[j] < 0 and not is_zero(delta[j]) for j in Jn], True)

        if not ~k:
            return x

        j0 = Jn[k]

        z = dot(B, A[:, j0])

        if all(z <= EPS):
            raise Exception("No sln")

        basis_x = x[Jb]

        theta = [basis_x[j] / z[j] if z[j] > 0 and not is_zero(z[j]) else inf for j in range(m)]

        theta0 = min(theta)

        s = get_index(theta, theta0)
        index_tetta0 = Jb[s]

        for i, j in enumerate(Jb):
            x[j] = x[j] - theta0 * z[i]

        x[j0] = theta0

        Jb[s] = j0
        basic_a[:, s] = A[:, j0]

        B = get_new_B(B, z, s, m)

        Jn[k] = index_tetta0
