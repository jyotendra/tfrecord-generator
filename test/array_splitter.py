import math
import random

tot_element = 633
main_array = list(range(tot_element))

random.shuffle(main_array)

test_p = 0.1
train_p = 0.6
val_p = 0.3

test_a = main_array[0:math.floor(0.1 * tot_element)]
test_b = main_array[math.floor(0.1 * tot_element): math.floor(0.3 * tot_element)]
test_c = main_array[math.floor(0.3 * tot_element):]

len_a = len(test_a)
len_b = len(test_b)
len_c = len(test_c)

print(len_a + len_b + len_c)
