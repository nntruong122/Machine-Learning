from random import randint
from math import ceil

class EnumerationDistribution(object):
    """Maintains a map of objects and their probabilities.
    This map is then used to generate objects that match their distribution"""

    def __init__(self, map):
        super(EnumerationDistribution, self).__init__()
        if type(map) != type({}):
            raise ValueError("Map input expected")
        self._map = map
        total = 0
        self._ranges = {}
        range_start = 0

        for element in map:
            total += map[element]
        if total == 0:
            
        if total != 100:
            subTotal = 0
            for index, element in enumerate(map):
                map[element] *= (100/total)
                if index < len(map)-1:
                    map[element] = round(map[element])
                    subTotal += map[element]
                else:
                    map[element] = 100 - subTotal

        for index, element in enumerate(map):
            range_end = range_start + map[element] - 1
            self._ranges[(range_start, range_end)] = element
            range_start += map[element]

    def get_object(self):
        random_int = randint(0, 99)
        for element in self._ranges:
            if random_int >= element[0] and random_int <= element[1]:
                return self._ranges[element]
        return None
