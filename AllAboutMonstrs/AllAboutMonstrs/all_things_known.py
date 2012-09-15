"""
  Gathered information about all things known
"""

import facilities, units, bestiary

ALL_THINGS = {}

for m in facilities, units, bestiary:
    classes = dict((c.__name__, c) for c in vars(m).values() if hasattr(c, "name"))
    ALL_THINGS.update(classes)

def find_by_name(short_name):
    return ALL_THINGS.get(short_name)
