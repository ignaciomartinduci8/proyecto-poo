import os
import datetime
import csv

class DataLog:

    def __init__(self, user):
        self.user = user
        self.path = './Logs'
        self.file = self.fileSet()

    def fileSet(self):

        if not os.path.exists(self.path):
            os.mkdir(self.path)

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

    def logRobotEffector(self, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'EFFECTOR_ON'

            else:

                process = 'EFFECTOR_OFF'

            f.write(f"R | {process} | {self.getTime()} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotConnection(self, port,baudrate, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'ROBOT_CONNECT'

            else:

                process = 'ROBOT:DISCONNECT'

            f.write(f"R | {process} | {port} | {baudrate} | {self.getTime()} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotMove(self,x,y,z):

        with open(f'{self.path}/{self.file}', 'a') as f:

            f.write(f"R | MOVE | {x} | {y} | {z} | {self.getTime()} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logHome(self,x,y,z):

        with open(f'{self.path}/{self.file}', 'a') as f:

            f.write(f"R | HOME | {x} | {y} | {z} | {self.getTime()} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logProgram(self, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'PROGRAM_ON'

            else:

                process = 'PROGRAM_OFF'

            f.write(f"P | {process} | {self.getTime()} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotStatus(self,modo,x,y,z,efector):

            with open(f'{self.path}/{self.file}', 'a') as f:

                f.write(f"R | STATUS | {modo} | {x} | {y} | {z} | {efector} | {self.getTime()} | {self.user}\n")
                f.flush()
                os.fsync(f.fileno())
                f.close()







    def getLastSession(self):

        res = []

        with open(f'{self.path}/{self.file}', 'r') as f:

            lines = f.readlines()
            lines.reverse()

            for line in lines:

                lineData = line.split('|')

                if lineData[1] == ' PROGRAM_ON ':

                    res.append(lineData[-2])

                    res.reverse()
                    return res

                else:

                    res.append(line.replace("\n", ""))
