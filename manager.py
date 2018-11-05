import socket, sys, thread, os

global fileName
fileName = 'server.py'

def sysStart(hostList, portNum):


    for host in hostList:
        # ex: scp srvr.py jackied@pc12.cs.ucdavis.edu:/tmp
        addr = 'scp '+ fileName + ' '+ host + ':/tmp'
        print addr
        os.system(addr)

    for host in hostList:
        # ex: ssh jackied@pc12.cs.ucdavis.edu python /tmp/srvr.py 2373 &
        uploadCmd = 'ssh ' + host + ' python /tmp/' + fileName + ' ' + str(portNum)+ ' &'
        print uploadCmd
        os.system(uploadCmd)


    # todo: look for 'sysStop'. ssh rm then end function
    userInput = raw_input('Servers started. Type sysStop() to shut all servers.\n')
    while not userInput == 'sysStop()':
        userInput = raw_input('Unknown command. Type sysStop() to shut all servers.\n')

    print '\nsysStop() starts. \n'
    sysStop(hostList)
    print '\nsysStart() ends. All hosts closed.'
    # threads end since function ends.







def sysStop(hostList):
    # ssh mtimzh@pc12.cs.ucdavis.edu rm -f /tmp/fileName
    for host in hostList:
        delCmd = 'ssh ' + host + ' rm -f /tmp/' + fileName
        os.system(delCmd)
        print delCmd
