# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

def rotate_digit (digit):
    if digit > 4:
        return (digit * 2) - 9

    else:
        return digit * 2

def add_two_digits (two_digits):
    first_digit = two_digits // 10
    second_digit = two_digits % 10

    return first_digit + rotate_digit(second_digit)

def get_check_digit_from_checkable_int (number):
    return (9 * add_two_digits(number)) % 10

def get_check_digit (number = None):
    if number:
        return get_check_digit_from_checkable_int(int(number))

    else:
        return None
