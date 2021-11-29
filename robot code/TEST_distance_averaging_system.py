from Camera import get_average_of_subarray
import numpy

zeroArray = numpy.zeros((20,40),dtype=int)
print("TEST 1 - basic functionality")
if get_average_of_subarray(zeroArray,5,5,1) == 0:
    print("TEST 1 - pass")
else:
    print("TEST 1 - FAIL")

print("TEST 2 - correct coordinates")

zeroArray[15][30] = 1

if get_average_of_subarray(zeroArray,15,30,0) == 1:
    print("TEST 2 - pass")
else:
    print("TEST 2 - FAIL")