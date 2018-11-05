import socket, sys, thread, os

############ Start - User Functions ############
def hashSrvr(filename):
    theServerNum = hash(filename) % len(hostlist)
    return theServerNum


def dInit(hostList, portnum):
    # cdHosts: boolean list of hosts showing connected or not
    # sockList: corresponding sockets
    global hostlist, portnumber, cdHosts, sockList
    hostlist = hostList
    portnumber = portnum
    cdHosts = [0] * len(hostList)
    sockList = []

    for i in range(len(hostList)):
        x = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        sockList.append(x)


def dopen(filename,mode = 'r'):
    serverIndex = hashSrvr(filename)

    if cdHosts[serverIndex] == 0:
        host = hostlist[serverIndex]
        cdHosts[serverIndex] = 1
        (sockList[serverIndex]).connect((host,portnumber))

    s = sockList[serverIndex]

    # send steps for all functions:
    # - server waits for message
    # - client sends function name and waits for confirmation. Server receives,
    #   sends 'x' as confirmation, and starts to wait for message again.
    # - client receives confirmation, sends file name and waits for confirmation.
    #   Server receives, sends 'x' as confirmation, and starts to wait for
    #   message again.
    # - client receives confirmation, sends option and waits for result (error
    #   message or successful action confirmation)

    # All of above is to get around the issue of not being able to use string
    # using <socket>.send(). Could cause problems, but not required for error
    # checking

    s.send('open')
    s.recv(1)
    s.send(filename)
    s.recv(1)
    s.send(mode)

    result = s.recv(4096)

    if result == 'File opened successfully.':
        print result
        # returns a "fileObject"; see class declaration for details
        resultFilename = fileObject(filename)
        return resultFilename
    else:
        print result


# fileObject is created so that user can call function like "x.dwrite('')" .
class fileObject:
    def __init__(self,fileName):
        self.filename = fileName

    def dclose(self):
        serverIndex = hashSrvr(self.filename)
        s = sockList[serverIndex]
        s.send('close')
        s.recv(1)
        s.send(self.filename)
        s.recv(1)
        s.send(' ')

        # if error occurs, we need to have the error message,
        # so we put a lot of buffer here
        result = s.recv(4096)
        print result


    def dread(self,num = None):
        serverIndex = hashSrvr(self.filename)
        s = sockList[serverIndex]
        s.send('Server, please call read()')
        s.recv(1)
        s.send(self.filename)
        s.recv(1)
        s.send(str(num))
        result = s.recv(4096)
        print result

    def dwrite(self,content):
        serverIndex = hashSrvr(self.filename)
        s = sockList[serverIndex]
        s.send('write')
        s.recv(1)
        s.send(self.filename)
        s.recv(1)
        s.send(content)
        result = s.recv(4096)
        print result


def closeConnection():
    for i in range(len(hostlist)):
        if cdHosts[i] == 1:
            (sockList[i]).send('closeConnection')
            (sockList[i]).recv(1)
            (sockList[i]).send(str(None))
            (sockList[i]).recv(1)
            (sockList[i]).send(str(None))
            (sockList[i]).recv(4096) # this line should be commented if the
                                     # lines below (debug purpose) aren't
            # if (sockList[i]).recv(4096) == 'Connection closed.':
                # print hostlist[i] + ' closed.'
            # else:
               # print 'Something Happened while disconnecting.'
        (sockList[i]).close()
#----------- End - User Functions -----------#
