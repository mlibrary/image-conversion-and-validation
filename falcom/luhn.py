# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class LuhnNumber:

    def __init__ (self, number = None):
        self.__set_number(number)

    def get_check_digit (self):
        if self:
            return self.__get_check_digit_from_checkable_int()

        else:
            return None

    def __bool__ (self):
        return self.number is not None

    def __repr__ (self):
        return "<{} {}>".format(self.__class__.__name__,
                                repr(self.number))

    def __set_number (self, number):
        if isinstance(number, int):
            self.number = number

        elif isinstance(number, str):
            self.__try_to_extract_number_from_str(number)

        else:
            self.number = None

    def __try_to_extract_number_from_str (self, number):
        try:
            self.number = int(number)

        except ValueError:
            self.number = None

    def __get_check_digit_from_checkable_int (self):
        total = 0
        n = self.number

        while n > 0:
            total += self.__add_two_digits(n % 100)
            n //= 100

        return (9 * total) % 10

    def __add_two_digits (self, n):
        return (n // 10) + self.__rotate_digit(n % 10)

    def __rotate_digit (self, n):
        result = n * 2
        return result if result < 10 else result - 9

def is_luhn_checkable (number):
    if isinstance(number, str):
        return bool(number)

    else:
        return isinstance(number, int)

def get_check_digit (number = None):
    n = LuhnNumber(number)
    return n.get_check_digit()

def convert_to_int (number):
    try:
        return int(number)

    except ValueError:
        return 1

def verify_check_digit (number = None):
    if is_luhn_checkable(number):
        number = convert_to_int(number)

        return number % 10 == get_check_digit(number // 10)

    else:
        return False
