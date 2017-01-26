# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

def rotate_digit (digit):
    if digit > 4:
        return (digit * 2) - 9

    else:
        return digit * 2

def get_check_digit (number = None):
    if number:
        return (9 * rotate_digit(int(number))) % 10

    else:
        return None
