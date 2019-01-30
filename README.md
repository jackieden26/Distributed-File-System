Files: manager.py, server.py,client.py

### Known CSIF Issues ###
  1. In order to use CSIF computers as hosts, a manager has to setup "passwordless login" for his/her account. See http://csifdocs.cs.ucdavis.edu/about-us/csif-general-faq#TOC-How-do-I-set-up-SSH-keys-to-allow-me-to-login-to-the-CSIF-computers-without-a-password-

  2. If the hosts are on CSIF, clients have to be on CSIF as well. See CSIF related socket problem stated in blogpost from Thursday, February 8, 10:25 am here: http://heather.cs.ucdavis.edu/~matloff/145/Blog.html



### Instructions ###
  Command size: 512 characters
  Maximum clients: 128

#### Manager ####
  1. Make sure manager.py and server.py are in the same directory, and the global variable 'fileName' in manager.py has to be identical to the name of server.py.

  2. To set up the hosts, run manager.py in interactive mode using command 'python -i manager.py'. In interactive mode, call sysStart(hostList, portNum) with the first argument to be a list of hosts (INCLUDES USERNAME IF IT'S REQUIRED TO GAIN ACCESS) and the second argument to be the port number.
  E.g.:
  sysStart(['jackied@pc18.cs.ucdavis.edu','jackied@pc19.cs.ucdavis.edu','jackied@pc26.cs.ucdavis.edu'],2339) 

  3. Now manager.py will upload server.py to every host in the list and run the script with the given port number, and servers are now discoverable by clients. To close the servers and remove the scripts from the hosts, simply type 'sysStop()'.

  4. Close the program by calling 'quit()' or using CTRL+D, or restart or start another list of servers using step 2.


#### Client ####
  1. Run client.py in interactive mode using command 'python -i client.py'.

  2. To initialize, call function dInit(hostList, portnum) with the list of hosts and port number given by the manager/host/person-who's-in-charge-of-the-servers.
  E.g.:
  dInit(['pc18.cs.ucdavis.edu','pc19.cs.ucdavis.edu','pc26.cs.ucdavis.edu'],2339)

  3. Call functions dclose(), dread(), dwrite(), and dopen() the same ways as calling the equivalent functions without the initial 'd''s.

  4. To close the connection, type 'closeConnection()'.

  5. Close the program by calling 'quit()  or using CTRL+D, or restart or start another connection using step 2.



##### Designs/How it works #####
  The role of server.py is simply to setup a socket on the host that it runs on for clients to connect and does what clients request. The role of manager.py is to upload server.py to every host using "scp", run the uploaded script in background using "ssh &", and wait for the disconnect signal ("sysStop()"). Once disconnect signal is received, manager.py removes the uploaded files from every host using "ssh rm" and end the connection by simply ends sysStart() to cause the threads to end. The role of client.py is to translate user inputs to server.py, so server.py can easily understand and respond to what users want.
