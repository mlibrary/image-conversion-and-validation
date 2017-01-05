# Copyright (c) 2016 The Regents of the University of Michigan.
# All Rights Reserved. Licensed according to the terms of the Revised
# BSD License. See LICENSE.txt for details.
from collections.abc import Mapping

class DecoyMapping (Mapping):
    """Pretends to be a mapping but tracks queries and returns 0.

    This is nice if you need to know exactly which keys are queried.
    """

    def __init__ (self, value = 0):
        """Init an empty decoy mapping."""

        # Start with an empty set.
        self.__keys = set()
        self.__value = value

    def get_keys (self):
        """Return the set of keys."""
        return self.__keys

    def __getitem__ (self, key):
        """Add key and return 0."""

        # A query! Add this to our set.
        self.__keys.add(key)

        # Return 0. Probably safe.
        return self.__value

    def __len__ (self):
        """Return 0."""
        return 0

    def __iter__ (self):
        """Return an empty iterator."""
        return iter(())

def get_keys_required_by_format_str (s):
    """Return the set of named keywords in the format string."""

    # Use a decoy mapping to track whatever we're asking for.
    mapping = DecoyMapping()

    # We use format map to stop the thing from trying to convert to a
    # dict or anything weird.
    junk = s.format_map(mapping)

    # Return the resulting set of keys.
    return mapping.get_keys()
