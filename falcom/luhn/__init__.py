# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

from .check_digit_number import CheckDigitNumber

class LuhnNumber (CheckDigitNumber):

    def generate_from_int (self, n):
        total = 0

        while n > 0:
            total += self.__add_two_digits(n % 100)
            n //= 100

        return (9 * total) % 10

    def __add_two_digits (self, n):
        return (n // 10) + self.__rotate_digit(n % 10)

    def __rotate_digit (self, n):
        result = n * 2
        return result if result < 10 else result - 9

def get_check_digit (number = None):
    n = LuhnNumber(number)
    return n.get_check_digit()

def verify_check_digit (number = None):
    n = LuhnNumber(number)
    return n.has_valid_check_digit()
