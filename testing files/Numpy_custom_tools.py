import numpy as np

def get_average_of_subarray(array, x, y, size):
    # get the rows and collumns to keep from the matrix
    lowcol = max(0, x-size)
    lowrow = max(0, y-size)
    
    highcol = min(array.shape[0], x+size+1)
    highrow = min(array.shape[1], y+size+1)

    # get the submatrix
    array = array[lowcol:highcol, lowrow:highrow]
    # if matrix has no values return 0
    if (array.size==0):
        return -1
    # return average of values in array
    # maybe it would be better to take the median value?
    return (np.average(array))


arr = np.array([
    [1,2,3,4],
    [5,6,7,8],
    [9,10,11,12],
    [13,14,15,16]
])

print(get_average_of_subarray(arr, 1, 1, 1))