# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

def get_check_digit (number = None):
    if number:
        return (8 * int(number)) % 10

    else:
        return None
