import csv
import os

class FileReader(object):
  """FileReader is for abstracting reading of files for training and testing"""
  __slots__ = 'filepath', 'featureNames', 'containsHeader'
  def __init__(self, filepath, containsHeader = False):
    super(FileReader, self).__init__()
    self.filepath = filepath
    self.containsHeader = containsHeader
    self.featureNames = []

  def getRows(self):
    with open(self.filepath,'rb') as fileReader:
      csv_reader = csv.reader(fileReader)
      if self.containsHeader:
        self.featureNames = csv_reader.next()
      return [row for row in csv_reader]

  def getClassLabels(self):
    matrix= self.getRows()
    classLabelsMap={}
    for row in matrix:
       if not classLabelsMap.has_key(row[len(row)-1]):
        classLabelsMap[row[len(row)-1]]='true'
    return sorted(classLabelsMap)
