import numpy as np
from tangles.util.entropy import entropy, joint_entropy


def conditional_entropie_sep(data: np.ndarray, sep: np.ndarray) -> np.ndarray:
    """returns ndarray with H(q_i|s) at position i with the rows of data being q_i and seps being a column-vector"""
    e = entropy(sep)
    je = np.zeros((data.shape[1])) - e
    for i in range(data.shape[1]):
        je[i] += joint_entropy(np.c_[data[:, i], sep])
    return je


def conditional_entropies(data: np.ndarray) -> np.ndarray:
    """returns ndarray with H(i|j) at position [i,j]"""
    h = entropy(data)
    je_mat = np.zeros((data.shape[1], data.shape[1]))
    for i in range(data.shape[1] - 1):
        for j in range(i + 1, data.shape[1]):
            je_mat[j, i] = joint_entropy(data[:, [i, j]])
            je_mat[i, j] = je_mat[j, i]
    je_mat -= h
    np.fill_diagonal(je_mat, 0)
    return je_mat


def O12(data: np.ndarray, seps: np.ndarray = None) -> np.ndarray:
    """Implementation of O12 from the book.

    Args:
        data (np.ndarray): the underlying seperations system S as a matrix, where each colomn represents a seperation.
        seps (np.ndarray): Seperations to calculate order of, each colomn represents a seperation. If not set, the order of each seperation s \in S will be returned.

    Returns:
        np.ndarray: Array with orders[i] containing order of seperation in colomn i of seps(/data, if seps was not set).
    """
    if seps == None:
        ce = conditional_entropies(data)
        return np.sum(ce, axis=0)
    elif len(seps.shape) == 1:
        return np.sum(conditional_entropie_sep(data, seps), axis=0)
    else:
        orders = np.zeros(seps.shape[1])
        for i in range(seps.shape[1]):
            orders[i] = np.sum(conditional_entropie_sep(data, seps[:, i]), axis=0)
        return orders
