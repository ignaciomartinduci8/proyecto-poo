import os
import datetime
import csv
if not os.path.exists('./Logs'):
    os.mkdir('./Logs')

class DataLog:

    def __init__(self, user):
        self.user = user
        self.path = './Logs'
        self.file = self.fileSet()

    def fileSet(self):

        files = os.listdir(self.path)

        if len(files) == 0:

            return self.createFile(0)

        for file in files:

            with open(f'{self.path}/{file}', 'r') as f:

                id, date = f.readline().strip().split('-')

            if date == self.getDate():

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
            f.flush()
            os.fsync(f.fileno())
            f.close()

        return file

    def getTime(self):

        now = datetime.datetime.now()

        hour = now.hour
        minute = now.minute
        second = now.second

        return f'{hour}:{minute}:{second}'

    def logClientConnection(self, clientName, ip, port, time, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'CLIENT_CONNECT'

            else:

                process = 'CLIENT_DISCONNECT'

            f.write(f"S | {process} | {clientName} | {ip} | {port} | {time}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logServerStatus(self, hostIP, port, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'SERVER_START'

            else:

                process = 'SERVER_STOP'

            f.write(f"S | {process} | {hostIP} | {port} | {self.getTime()} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()