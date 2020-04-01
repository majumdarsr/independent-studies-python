
# coding: utf-8

# In[4]:


"""
Ai Club meet 03.24.2020

1. Write a function to give the sum of all the numbers in list?

2. Write a function to test whether the number is in the defined range or not?

3. Write a function to calculate number of upper case letters and number of lower case letters?
"""
import unittest

#1. This function returns sum of all numbers in the array
def summ(array):
    total = 0
    for num in array:
        total += num
    return total


#2. This function tells if num falls within (range1, range2)
def is_inrange(num, range1, range2):
    if range1 > range2:
        range1, range2 = range2, range1
    if range1 == range2:
        return num == range1
    return True if num in range(range1, range2+1, 1) else False



#3. This function returns the total numbers of upper and lowercase letters
def count_UpperLower(str1):
    count_upper = 0
    count_lower = 0
    for char in str1:
        if char.isalpha() and char.islower():
            count_lower += 1
        elif char.isalpha() and char.isupper():
            count_upper += 1
        else:
            pass
    return count_upper, count_lower


import unittest
# This class tests all the above functions
class test_week3Funct(unittest.TestCase):

    # Setting up the setup function that will stop widget from testing further

    #1. This function tests summ(array)
    def test_summ(self):
        array1 = [1, 4, 6, 2, 6, 26]
        array2 = [7909, 379, 2790, 11, 480]
        self.assertEqual(summ(array1), sum(array1))
        self.assertEqual(summ(array2), sum(array2))


    #2. This function tests is_inrange(num, range1, range2)
    def test_isinrange(self):
        num1, num2, num3, num4 = 38, 43709, 479, 8
        self.assertEqual(True, is_inrange(num1, 1, 40))
        self.assertEqual(False, is_inrange(num2, 1, 40))
        self.assertEqual(True, is_inrange(num3, 500, 40))
        self.assertEqual(True, is_inrange(num4, 8, 8))

    #3. This function tests count_UpperLower(str1)
    def test_count_UpLo(self):
        self.assertNotEqual((3, 4), count_UpperLower('Unit Test'))
        self.assertEqual((1, 4), count_UpperLower('Gates'))

    # This tears down all tests at the end


# Run main unittest function
if __name__ == '__main__':
    unittest.main(verbosity = 2)

