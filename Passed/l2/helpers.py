import numpy as np


def get_pretty_matrix_str(A):
    return str(np.matrix(A)).replace('\n', '\n\t')


def get_str_result(A, b, c, dl, dr, x, c_x):
    return "A : {}\nb : {}\nc : {}\ndl : {}\ndr : {}\nx : {}\nc(x) : {}\n"\
        .format(get_pretty_matrix_str(A), b, c, dl, dr, x, c_x)


def is_int(val):
    return abs(val - (val + 0.000001) // 1) <= 0.000001


def get_ceil(val):
    return int(val) if val >= 0 else int(val - 1.0)