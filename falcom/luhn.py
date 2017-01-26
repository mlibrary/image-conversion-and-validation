# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class LuhnNumber:

    def __init__ (self, number = None):
        self.__set_number(number)

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

def is_luhn_checkable (number):
    if isinstance(number, str):
        return bool(number)

    else:
        return isinstance(number, int)

def rotate_digit (digit):
    result = digit * 2
    return result if result < 10 else result - 9

def add_two_digits (two_digits):
    first_digit = two_digits // 10
    second_digit = two_digits % 10

    return first_digit + rotate_digit(second_digit)

def get_check_digit_from_checkable_int (number):
    total = 0

    while number > 0:
        total += add_two_digits(number % 100)
        number //= 100

    return (9 * total) % 10

def get_check_digit_if_convertable_to_int (number):
    try:
        return get_check_digit_from_checkable_int(int(number))

    except ValueError:
        return None

def get_check_digit (number = None):
    if is_luhn_checkable(number):
        return get_check_digit_if_convertable_to_int(number)

    else:
        return None

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
