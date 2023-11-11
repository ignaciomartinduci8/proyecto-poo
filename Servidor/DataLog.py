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

    def logServerStatus(self, hostIP, port, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'SERVER_START'

            else:

                process = 'SERVER_STOP'

            f.write(f"{self.getTime()} | S | {process} | {hostIP} | {port}| {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotEffector(self, onOff, RPC):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'EFFECTOR_ON'

            else:

                process = 'EFFECTOR_OFF'

            if RPC:

                RPCon = 'RPC | '

            else:

                RPCon = ''


            f.write(f"{self.getTime()} | R | {process} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotConnection(self, port,baudrate, onOff, RPC):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'ROBOT_CONNECT'

            else:

                process = 'ROBOT_DISCONNECT'

            if RPC:

                RPCon = 'RPC | '

            else:

                RPCon = ''

            f.write(f"{self.getTime()} | R | {process} | {port} | {baudrate} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotMove(self,x,y,z,RPC):

        if RPC:

            RPCon = 'RPC | '

        else:

            RPCon = ''

        with open(f'{self.path}/{self.file}', 'a') as f:

            f.write(f"{self.getTime()} | R | MOVE | {x} | {y} | {z} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logHome(self,x,y,z,RPC):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if RPC:

                RPCon = 'RPC | '

            else:

                RPCon = ''

            f.write(f"{self.getTime()} | R | HOME | {x} | {y} | {z} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logProgram(self, onOff):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'PROGRAM_ON'

            else:

                process = 'PROGRAM_OFF'

            f.write(f"{self.getTime()} | P | {process} | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotStatus(self,modo,x,y,z,efector,RPC):

            with open(f'{self.path}/{self.file}', 'a') as f:

                if RPC:

                    RPCon = 'RPC | '

                else:

                    RPCon = ''

                f.write(f"{self.getTime()} |R | STATUS | {modo} | {x} | {y} | {z} | {efector} | {RPCon}{self.user}\n")
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

                if lineData[2] == ' PROGRAM_ON ':

                    res.append(lineData[0])

                    res.reverse()
                    return res

                else:

                    res.append(line.replace("\n", ""))

    def logAutomatic(self, gcode):

        gcode = gcode.replace("\n", "")

        with open(f'{self.path}/{self.file}', 'a') as f:

            f.write(f"{self.getTime()} | A | {gcode}  | {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logMotors(self, onOff, RPC):

        if onOff:

            process = 'MOTORS_ON'

        else:

            process = 'MOTORS_OFF'

        if RPC:

            RPCon = 'RPC | '

        else:

            RPCon = ''

        with open(f'{self.path}/{self.file}', 'a') as f:

            f.write(f"{self.getTime()} | R | {process} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRobotMode(self, onOff, RPC):

        with open(f'{self.path}/{self.file}', 'a') as f:

            if onOff:

                process = 'ROBOT_MODE_AUTOMATIC'

            else:

                process = 'ROBOT_MODE_MANUAL'

            if RPC:

                RPCon = 'RPC | '

            else:

                RPCon = ''

            f.write(f" {self.getTime()} | R | {process} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRPCConnection(self, IP, PORT):

            with open(f'{self.path}/{self.file}', 'a') as f:

                f.write(f"{self.getTime()} | RPC | CONNECT | {IP} | {PORT} | {self.user}\n")
                f.flush()
                os.fsync(f.fileno())
                f.close()

    def getUser(self):
        return self.user

    def logToggleLearn(self,onff, RPC):
        with open(f'{self.path}/{self.file}', 'a') as f:

            if onff:

                process = 'LEARN_ON'

            else:

                process = 'LEARN_OFF'

            if RPC:

                RPCon = 'RPC | '

            else:

                RPCon = ''

            f.write(f"{self.getTime()} | R | {process} | {RPCon}{self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

    def logRPCClientConnection(self, clientIP, clientPort, onOff,username = None):

        if username is None:

            printUser = ''

        else:

            printUser = f' {username}(C ) |'

        if onOff:

            process = 'CONNECTED_CLIENT'

        else:

            process = 'DISCONNECTED_CLIENT'

        with open(f'{self.path}/{self.file}', 'a') as f:

            f.write(f"{self.getTime()} | RPC | {process} | {clientIP} | {clientPort} |{printUser} {self.user}\n")
            f.flush()
            os.fsync(f.fileno())
            f.close()

