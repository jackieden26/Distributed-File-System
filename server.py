import socket, sys, thread, os

############ Start - server functions ############
def serveClient(client):
    # File dictionary for current connection so that file pointers can be stored
    # for every individual client, so opened files don't need to be reopened and
    # file points aren't lost.
    #
    # filePtrs:
    #   key = fileName
    #   value = file pointer
    # ex:
    #   fileName : <filePointer>
    #
    filePtrs = {}
    while 1:
        filePtrs.update(filePtrs) # might not needed.

        # clnt sends function name
        fnName = client.recv(512)
        # confirmation
        client.send('x')
        # clnt sends file name
        fileName = client.recv(512)
        # confirmation
        client.send('x')
        # clnt sends option
        option = client.recv(512)

        if fnName == 'open':
            try:
                x = open('/tmp/'+fileName, option)
                filePtrs[fileName] = x
                client.send('File opened successfully.')
            except Exception, e:
                client.send(str(e))

        elif fnName == 'Server, please call read()':
            try:
                if fileName in filePtrs:
                    if option == 'None':
                        client.send( (filePtrs[fileName]).read() )
                    else:
                        client.send( (filePtrs[fileName]).read(int(option)) )
                else:
                    client.send(fileName + ' is not opened. Please open it first.')
            except Exception, e:
                client.send(str(e))

        elif fnName == 'write':
            try:
                if fileName in filePtrs:
                    (filePtrs[fileName]).write(option)
                    client.send(fileName + ' written successfully.')
                else:
                    client.send(fileName + ' is not opened. Please open it first.')
            except Exception, e:
                client.send(str(e))
        elif fnName == 'close':
            try:
                if fileName in filePtrs:
                    (filePtrs[fileName]).close()
                    client.send(fileName + ' closed.')
                else:
                    client.send(fileName + ' is not opened. Please open it first.')
            except Exception, e:
                client.send(str(e))
        elif fnName == 'closeConnection':
            client.send('Connection closed.')
            break
        else:
            break # print fnName, ' This line printed imples clnt sent unknown cmd. debug.'

    client.close()



#def server():
nclnt = 128
lstn = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
port = int(sys.argv[1])
lstn.bind(('',port))
lstn.listen(nclnt)

while 1:
    (clnt,ap) = lstn.accept()
    thread.start_new_thread(serveClient, (clnt,))
#----------- End - server functions -----------#
