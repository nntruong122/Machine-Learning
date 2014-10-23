from file_reader import FileReader
from math import log

class NaiveBayes(object):
    """docstring for NaiveBayes
            1. ClassLabel is assumed to be last index
            2. All the rows are assumed to be of the same size
            3. The csv file is assumed to contain atleast one row
    """
    def __init__(self, trainfile, is_smoothed = True):
        __slots__ = '_prior', '_conditional', '_file', '_is_smoothed', '_num_features'
        super(NaiveBayes, self).__init__()
        self._file = trainfile
        self._prior = {}
        self._conditional = {}
        self._is_smoothed = is_smoothed
        self.generate()

    def calcCounts(self):
        # Missing labels not yet added.

        fr = FileReader(self._file)
        rows = fr.getRows()
        self._num_features = len(rows[0])-1

        feature_count = {}
        label_count = {}
        label_count['total'] = 0

        for row in rows:
            label_count['total'] += 1
            if label_count.get(row[-1]) is None:
                label_count[row[-1]] = 1
            else:
                label_count[row[-1]] += 1

            if feature_count.get(row[-1]) is None:
                feature_count[row[-1]] = {}
                for i in range(self._num_features):
                    feature_count[row[-1]][str(i)] = {}
                    feature_count[row[-1]][str(i)]['total'] = 0

            for i in range(self._num_features):
                feature_i = feature_count[row[-1]][str(i)]
                value = feature_i.get(row[i])
                feature_i[row[i]] = 1 if value is None else feature_i[row[i]]+1
                feature_count[row[-1]][str(i)]['total'] += 1

        for label in feature_count:
            for feature in feature_count[label]:
                feature_values = set()
                for l in filter(lambda x: x != 'total', feature_count):
                    for value in feature_count[l][feature]:
                        feature_values.add(value)

                for value in feature_values:
                    if feature_count[label][feature].get(value) is None:
                        feature_count[label][feature][value] = 0

        return(label_count, feature_count)

    def laplaceSmoothing(self):
        counts_result = self.calcCounts()
        label_count = counts_result[0]
        feature_count = counts_result[1]

        for label in feature_count:
            for feature in feature_count[label]:
                for value in filter(lambda x: x != 'total', feature_count[label][feature]):
                    feature_count[label][feature][value] += 1
                    feature_count[label][feature]['total'] += 1

        for label in filter(lambda x: x != 'total', label_count):
            label_count[label] += 1
            label_count['total'] += 1

        return (label_count, feature_count)

    def generate(self):
        counts_result = self.laplaceSmoothing() if self._is_smoothed else self.calcCounts()
        label_count = counts_result[0]
        feature_count = counts_result[1]

        for label in filter(lambda x: x != 'total', label_count):
            self._prior[label] = label_count[label] / label_count['total']

        for label in feature_count:
            self._conditional[label] = {}
            for feature in feature_count[label]:
                self._conditional[label][feature] = {}
                for value in filter(lambda x : x != 'total', feature_count[label][feature]):
                    self._conditional[label][feature][value] = feature_count[label][feature][value] / feature_count[label][feature]['total']


    def binary_classify(self, feature_array):
        # Check to see if the feature_array has enough dimensions.
        labels = list(self._prior)
        value = 0
        for i in range(self._num_features):
            try:
                l1 = self._conditional[labels[0]][str(i)][feature_array[i]] * self._prior[labels[0]]
                l2 = self._conditional[labels[1]][str(i)][feature_array[i]] * self._prior[labels[1]]
                value += log(l1/l2)
            except KeyError:
                raise ValueError( "Could not categorize this example: " + str(feature_array))
        return labels[0] if value >= 0 else labels[1]
