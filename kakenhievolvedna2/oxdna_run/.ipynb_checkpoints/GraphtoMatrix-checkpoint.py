import numpy as np
from numpy import linalg as LA

def get_matrix(myarray, nNodes):
    current_index = 0
    indexes = {}
    myarray_2d = myarray[nNodes: nNodes + nNodes * nNodes].reshape([nNodes, nNodes])

    for i in range(nNodes):
        for j in range(nNodes):
            if myarray_2d[i, j] != 0:
                indexes[(i, j)] = current_index
                current_index += 1
    matrix = np.zeros([current_index, current_index])

    for i in range(nNodes):
        for j in range(nNodes):
            for k in range(nNodes):
                # print(myarray_2d[i, j], myarray_2d[j, k])
                if myarray_2d[i, j] != 0.0 and myarray_2d[j, k] != 0.0:
                    matrix[indexes[(i, j)], indexes[(j, k)]] = 1

    myarray_3d = myarray[nNodes + nNodes*nNodes:].reshape([nNodes, nNodes, nNodes])
    for i in range(nNodes):
        for j in range(nNodes):
            for k in range(nNodes):
                for l in range(nNodes):
                    # print(myarray_3d[i, j, k], myarray_3d[j, k, l])
                    if myarray_3d[i, j, k] != 0.0 and myarray_2d[l, i]:
                        matrix[indexes[(l, i)], indexes[(j, k)]] = -1

    # w, v = LA.eig(matrix)
    return matrix

def get_matrix_new(myarray, nNodes):
    myarray_2d = myarray[nNodes: nNodes + nNodes * nNodes].reshape([nNodes, nNodes])

    matrix = np.zeros([nNodes, nNodes])
    for i in range(nNodes):
        matrix[i, i] -= 0.1

    for i in range(nNodes):
        for j in range(nNodes):
            #print(myarray_2d[i, j], myarray_2d[j, k])
            if myarray_2d[i, j] != 0.0:
                matrix[i, j] += 1

    myarray_3d = myarray[nNodes + nNodes*nNodes:].reshape([nNodes, nNodes, nNodes])
    for i in range(nNodes):
        for j in range(nNodes):
            for k in range(nNodes):
                # print(myarray_3d[i, j, k], myarray_3d[j, k, l])
                if myarray_3d[i, j, k] != 0.0:
                    matrix[i, k] += -1

    # w, v = LA.eig(matrix)
    return matrix