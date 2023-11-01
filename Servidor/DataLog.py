import os
import datetime
import csv

class DataLog:

    def __init__(self):
        self.path = './Logs'
        self.file = self.fileSet()

    def fileSet(self):

        files = os.listdir(self.path)

        if len(files) == 0:

            return self.createFile(0)

        for file in files:

            with open(f'{self.path}/{file}', 'r') as f:

                id, date = f.readline().strip().split('-')

            if date == f'{self.getDate()}\n':

                return file

        return self.createFile(int(id)+1)

    def getDate(self):

        now = datetime.datetime.now()

        day = now.day
        month = now.month
        year = now.year

        return f'{year}_{month}_{day}'

    def createFile(self, id):

        date = self.getDate()

        file = f'{date}-DataLog.txt'

        with open(f'{self.path}/{file}', 'w') as f:

            f.write(f'{id}-{date}\n')

        return file

