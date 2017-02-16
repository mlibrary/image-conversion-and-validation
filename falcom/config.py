# Copyright (c) 2017 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.

class Config:

    default_key = "default"
    default = ( )

    def __len__ (self):
        return 0

    def __getitem__ (self, key):
        return ( )

    def __contains__ (self, key):
        return True

    def __repr__ (self):
        return "<{}>".format(self.__class__.__name__)
