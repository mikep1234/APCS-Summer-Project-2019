import socket

#Import the socket module.

import _thread

#Import the threading module.

import tkinter

#Imports the tkinter module.

import sys

#imports the system module.

IP_ADDRESS = socket.gethostname()

#Gets the IP address of the host machine.

PORT = 44444

#Sets the port for the server to port 44444.

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

#Creates a socket for the server to be set up on.
#The protocol is AF_INET which is IPV4.
#The socket type is a stream socket, which transmits data smoother over a continuous connection.

s.bind((IP_ADDRESS, PORT))

#Binds the IP address and the port to the socket we just set up.

s.listen()

#Tells the socket server to listen for incoming connections.

name_list = []

#A list of names of the clients.

client_names = {}

#The clients names associeted with their sockets as well.

def getmsg(client):

    #Sets up a definition taking in the client information as the parameters.

    good_to_send = 0

    #Sentinel for the users username occupancy.

    while True:

        #Main loop for message reception and distribution.

        try:

            #Attempts to receive data from the user.

            data = client.recv(1024)

            #Assigns the variable data to the reception of a 1024 bite package.

            print(data.decode())

            #Prints the decoded data for monitoring and debugging purposes.

            if good_to_send == 1:

                #Checks the sentinel that tells if the user is good to send something.

                for C in client_names:

                    #Iterates through each client in the servers memory.

                    C.send(("\n".encode() + data + "\n".encode()))

                    #Sends the data that was received to the client in encoded text.

                    print("data sent to " + str(C))

                    #Tells the monitor of this program the data was sent to a user.
                    #This is for debugging purposes.

            elif client not in client_names:

                #Checks to see if the client is in the servers active memory.

                if data.decode() not in name_list:

                    #Check to see if the data received is a name available.

                    client_names[(client)] = str(data.decode())

                    #Adds the clients name as well a their client info to the dictionary for safe keeping.

                    client.send("true".encode())

                    #Sends back a string telling the clients program that it is good to swap GUIs.

                    name_list.append(data.decode())

                    #Appends the name to the list of names.

                    for C in client_names:

                        #For every client in the "client_names" dictionary.

                        C.send(("\n" + str(data.decode()) + " HAS JOINED THE CHAT\n").encode())

                        #Sends a message telling everyone in the room who joined the chat.

                    good_to_send = 1

                    #Sets the good to send sentinel to one instead of zero.

                else:

                    #If the name isn't available or if there are other issues, it sends back a "false" message.
                    #This tells the clients program to halt the transition of GUIs.

                    client.send("false".encode())
        except:

            #If data could not be received.

            for C in client_names:

                #For every client in the dictionary of clients.

                if C != client:

                    #If the client is not equal to the one with the messy connection.

                    C.send((str(client_names[client]) + " HAS DISCONNECTED").encode())

                    #Sends a disconnection message to everyone in the chat room.

            name_list.remove(client_names[client])

            #Removes the clients name from the list of clients.

            del client_names[client]

            #Deletes the clients name, as well as their client information from the dictionary.

            break

            #Exits the loop as to avoid any stress on the code having to process a dead connection.

while True:

    #Main loop for accepting new coonections.

    conn, addr = s.accept()

    #The connection and the address are passed in as variales to be unpacked by the accept function.

    _thread.start_new_thread(getmsg, (conn,))

    #Starts a new thread with the connection received as a parameter for out definition.
    #There really was no viable place to put the address information in this project, so I just kept it in there
    #For functionality of the code, and that's that.