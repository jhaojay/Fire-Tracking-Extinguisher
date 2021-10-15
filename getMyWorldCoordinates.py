import numpy as np

def getMyWorldCoordinates(map_from_array, map_to_array):
    x_mean = 0
    for x in map_from_array:
        x_mean = x_mean + x
    x_mean = x_mean / len(map_from_array)

    A = map_from_array[0] - x_mean
    for i in range(1, len(map_from_array)):
        A = np.column_stack((A, map_from_array[i] - x_mean))

    y_mean = 0
    for y in map_to_array:
        y_mean = y_mean + y
    y_mean = y_mean / len(map_to_array)

    B = map_to_array[0] - y_mean
    for i in range(1, len(map_to_array)):
        B = np.column_stack((B, map_to_array[i] - y_mean))

    C = np.matmul(B, A.T)

    u, s, vh = np.linalg.svd(C, full_matrices=True)

    diagonal_matrix = np.diag([1, 1, np.linalg.det(np.matmul(u, vh))])

    R = np.matmul(u,np.matmul(diagonal_matrix,vh))

    d = y_mean - np.matmul(R, x_mean)



    return R, d