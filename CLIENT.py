from PyQt5.QtWidgets import *

#imports all widgets from the pyqt5 module(used for gui)

import tkinter

#imports the tkinter module

import socket

#imports the socket module(used for actual server/client communication)

import _thread

#imports the threading module(used for multiprocessing within the same program)

import time

#imports the time module(used to prevent rapid spam of connections to the server upon the first failed one)

import random

#imports the random module(used for window color assignment)

window_color = random.randint(1, 4)

#Assigns a random color scheme for the background window out of four possible options.

SCREEN = tkinter.Tk()

#Creates a tkinter window ad the screen of the device.

SCREEN_WIDTH, SCREEN_HEIGHT = (SCREEN.winfo_screenwidth(), SCREEN.winfo_screenheight())

#This packs the two vaiables of "SCREEN_WIDTH" and "SCREEN_HEIGHT" and assigns them to the width of the tkinter
#screen window and the height of the tkinter screen window.

connection_loop = 0

#This establishes a connection loop for the client so if the first attempt fails a new one can be established.

while connection_loop == 0:

    #While the client isn't connected.

    try:

        #Attempts to run the main code.

        class MAIN_WINDOW(QMainWindow):

            #The class "MAIN_WINDOW" extends the QMainWindow class of the pyqt5 module.

            def __init__(self):

                #Initialization of the class.

                super().__init__()

                #Initializes the class object as a QMainWindow widget using the super method.

                if window_color == 1:
                    self.setObjectName('Background_Window_1')
                elif window_color == 2:
                    self.setObjectName('Background_Window_2')
                elif window_color == 3:
                    self.setObjectName('Background_Window_3')
                else:
                    self.setObjectName('Background_Window_4')

                #The if statements assign the previously mentioned color scheme.

                #The "setObjectName" method sets an ID for the items for later interpretation in the QSS file.

                self.setStyleSheet(open('STYLES.qss').read())

                #This sets the style sheet of this specific item to the sheet "STYLE.qss"

                self.setWindowTitle("Chat App")

                #Titles the window as "Chat App"

                self.setGeometry(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT)

                #The "setGeometry" method is similar to what is done in javascript with the positioning of items.
                #The start position of the window is at the top left (0, 0), and spans the "SCREEN_WIDTH", and "SCREEN_HEIGHT"

                self.FIRST_NAME = QLineEdit(self)

                #Estalishes an entry field for the first name of the client.

                self.FIRST_NAME.setToolTip("Enter your first name!")

                #Makes a handy little tooltip that will tell the user what to do when they hover over the widget.

                self.FIRST_NAME.setToolTipDuration(5000)

                #Sets the duration of the tooltip to be roughly 5 seconds.

                self.FIRST_NAME.setObjectName('FIRST_NAME')

                #This establishes the object ID as "FIRST_NAME"

                self.FIRST_NAME.setStyleSheet(open('STYLES.qss').read())

                #This sets the styling sheet of this object to STYLES.qss.

                self.FIRST_NAME.setGeometry(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 - 45, 300, 45)

                #The widget was now just positioned at 150 pixels to the left of the center of the screen, as well as
                #45 pixels above the center of the screen, and is 300 by 45 pixels large.

                self.LAST_NAME = QLineEdit(self)

                #Establishes a widget for the last name entry field of the user.

                self.LAST_NAME.setToolTip("Enter your last name!")

                #Creates a tooltip for the user to know what to input upon hovering.

                self.LAST_NAME.setToolTipDuration(5000)

                #Sets the tooltip duration to be roughly 5 seconds long.

                self.LAST_NAME.setObjectName('LAST_NAME')

                #Sets the object ID to "LAST_NAME".

                self.LAST_NAME.setStyleSheet(open('STYLES.qss').read())

                #This assigns the object to the style sheet of "STYLES.qss".

                self.LAST_NAME.setGeometry(SCREEN_WIDTH // 2 - 150, SCREEN_HEIGHT // 2 + 15, 300, 45)

                #Positions the widget in the same spot as the first name, but only 60 or so pixels lower.

                self.SIGN_IN_BUTTON = QPushButton("Sign In", self)

                #Creates a widget that functions as a sign in button of sorts for the user. The text entered in the
                #parameters is what shows up on the button.

                self.SIGN_IN_BUTTON.setToolTip("Click to sign in!")

                #This sets a Tooltip for the user to sign into their account, if the button wasnt already clear enough.

                self.SIGN_IN_BUTTON.setToolTipDuration(5000)

                #Tooltip duration of five seconds set to this button.

                self.SIGN_IN_BUTTON.setGeometry(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 75, 150, 50)

                #Sets the position of the button to be an additional 60 pixels lower than the last name field,
                #while also being in the center. The width of this widget is 150 pixels, and the height is 50.

                self.SIGN_IN_BUTTON.setObjectName('SIGN_IN_BUTTON')

                #This sets the item ID of this widget to "SIGN_IN_BUTTON".

                self.SIGN_IN_BUTTON.setStyleSheet(open('STYLES.qss').read())

                #This assigns the sing in button the style sheet of "STYLES.qss".

                self.SIGN_IN_BUTTON.clicked.connect(self.SIGN_IN)

                #This commands gives the button that we spent all this time on an actual function, which is called through
                #the connect function, which leads us into the chat portion of this application.

                self.ERROR = QLabel(self)

                #This widget is used to tell the user if the username they entered is currently being used or not.

                self.ERROR.setGeometry(SCREEN_WIDTH // 2 - 75, SCREEN_HEIGHT // 2 + 120, 150, 50)

                #This positions the error message right below the sign in button.

            def SIGN_IN(self):

                (CLIENT.Get_Socket()).send((self.FIRST_NAME.text().encode()) + ("_".encode()) + (self.LAST_NAME.text().encode()))

                #This line of code sends the server the clients name to check if it is being used or not.

                innit_data = (CLIENT.Get_Socket().recv(1024)).decode()

                #The variable "innit_data" decodes the recieved message to see if the server sent back approval for the name.

                if innit_data == "true":

                    #This if statement checks what the data decoded in tehe establishment of "innit_data" said.

                    CLIENT.Set_Name(self.FIRST_NAME.text() + "_" + self.LAST_NAME.text())

                    #Uppon approval the clients name will be set to the name sent to the server.

                    _thread.start_new_thread(CLIENT.getmsg, ())

                    #This is where things get fun. This function right here makes a new thread which allows us to listen for
                    #messages while also being able to send them out at the same time. The beauties of multiprocessing.

                    self.LAST_NAME.hide()

                    #Hides the last name widget

                    self.FIRST_NAME.hide()

                    #Hides the first name widget.

                    self.SIGN_IN_BUTTON.hide()

                    #Hides the sign in button widget.

                    self.ERROR.setText("")

                    #Hides the widget through the means of setting the text blank.

                    self.DISPLAY_BOX = QTextEdit(self)

                    #Creates the window that the client sees the messages in.

                    self.DISPLAY_BOX.setReadOnly(True)

                    #Makes it so the display cannot be altered in any manner, shape, or form.

                    self.DISPLAY_BOX.setGeometry(10, 10, SCREEN_WIDTH - 20, SCREEN_HEIGHT - 150)

                    #Sets the width of the message box to be the width of the screen minus 20 pixels, the height to be
                    #the height of the screen minus 150 pixels, and for it to start on the top left corner, 10 pixels out.

                    self.DISPLAY_BOX.setObjectName('DISPLAY_BOX')

                    #Sets the items ID to be "DISPLAT_BOX"

                    self.DISPLAY_BOX.setStyleSheet(open('STYLES.qss').read())

                    #Sets the style sheet of this object to be "STYLES.qss"

                    self.DISPLAY_BOX.show()

                    #Shows the display box on the screen in its position.

                    self.TYPE_BOX = QLineEdit(self)

                    #This creates a widget that the user would be able to type things into, allowing them to send messages.

                    self.TYPE_BOX.setGeometry(10, SCREEN_HEIGHT - 125, SCREEN_WIDTH - 200, SCREEN_HEIGHT - (SCREEN_HEIGHT - 75))

                    #Sets the starting position 10 pixels from the left of the screen, 125 from the bottom, and sets the height
                    #to be the height of the screen minus the desired padding, and leaves a space on the right for the send button.

                    self.TYPE_BOX.setObjectName('TYPE_BOX')

                    #Sets the objects ID as "TYPE_BOX".

                    self.TYPE_BOX.setToolTip("Say something nice!")

                    #Sets a tool tip encouraging conversation.

                    self.TYPE_BOX.setToolTipDuration(5000)

                    #Sets that tool tip duration to be 5 seconds long.

                    self.TYPE_BOX.setStyleSheet(open('STYLES.qss').read())

                    #Sets the style sheet as "STYLES.qss".

                    self.TYPE_BOX.show()

                    #Openly displays the typing box to the screen.

                    self.SEND_BUTTON = QPushButton("SEND", self)

                    #This creates the send button for the application.

                    self.SEND_BUTTON.setToolTip("Send your message!")

                    #This creates a tool tip telling the user that this button will send their message.

                    self.SEND_BUTTON.setToolTipDuration(5000)

                    #Sets this tool tip duration to be about 5 seconds long.

                    self.SEND_BUTTON.setGeometry(SCREEN_WIDTH - 175, SCREEN_HEIGHT - 125, 150, 75)

                    #Sets the position of this send button to be the screen width minus 175, and the height minus 125
                    #to allow for propper spacing of the elements, and it is 150 by 75 pixels large.

                    self.SEND_BUTTON.clicked.connect(self.Send_Msg)

                    #This assigns the button the command of "Send_Msg", which sends whatever is in the text box upon clicking.

                    self.SEND_BUTTON.setObjectName('SEND_BUTTON')

                    #This sets the items ID to "SEND_BUTTON".

                    self.SEND_BUTTON.setStyleSheet(open('STYLES.qss').read())

                    #Sets the style sheet oof this object to "STYLES.qss".

                    self.SEND_BUTTON.show()

                    #Shows the button to the screen of the client.

                else:

                    self.ERROR.setText("Name taken!")

                    #This end segment here just lets the user know that the name they chose is taken through turning the
                    #previous label into the message "Name taken!".

            def Add_Msg(self, message):

                #The parameter message is whatever was decoded and recieved by the client.

                self.DISPLAY_BOX.append(message)

                #This just adds the decoded message to the users display box.

            def Send_Msg(self):
                (CLIENT.Get_Socket()).send((str(CLIENT.Get_Name() + ": " + self.TYPE_BOX.text()).encode()))

                #This just sends the clients name plus their message to the server, which is then echoed back out to every
                #client that is connected to the server.

                self.TYPE_BOX.clear()

                #This clears the type box so that data can't be spam clicked.

        class Client():

            #Creates a client class for the program.

            def __init__(self):

                #Initializaion of all of the client data begins.

                global connection_loop

                #Allows the global variable of the connection loop to be altered.

                self.IP = socket.gethostname()

                #This retrieves the IP of the clients connection.

                self.PORT = 44444

                #For simplicity purposes we are going to use a comletely unused port on our network.

                #(This will all be greatly expanded on in the server documentation.

                self.name = ''

                #This sets the default name to be nothing.

                self.SOCKET = socket.socket()

                #This makes an actual socket for the client.

                self.SOCKET.connect((self.IP, self.PORT))

                #This connects the client to the server using their port number and IP address.

                connection_loop = 1

                #This sets the connection loop to one, as in true.

            def Set_Name(self, NAME):
                self.name = NAME

                #The parameter name is whatever the user enters for their first and last.

            def Get_Name(self):
                return self.name

                #This just returns the user's full name.

            def Get_Socket(self):
                return self.SOCKET

                #This returns the users socker ID for manipulation purposes.

            def getmsg(self):

                #This is the part of the code that allows us to recieve messages while sending data.

                self.x = CLIENT.Get_Socket()

                #Establishes X as a the clients socket through the class method of "Get_Socket".

                while True:

                    #There is a while true loop to allow constant flow of data.

                    data = self.x.recv(1024)

                    #Defines data as the raw, encoded utf-8 chunks, which are received in 1024 bite sizes.

                    print(data.decode())

                    #Prints the message to the console for debugging and potential logging and analysis purposes.

                    window.Add_Msg(data.decode())

                    #Adds the message received from the server to the message box.

        CLIENT = Client()

        #Establishes "CLIENT" as a instance of the "Client" class.

        app = QApplication([])

        #Creates an application through pyqt5. There is an empty list field left in the parameters for this method as there
        #are layers and different functions than can be added to the app.

        window = MAIN_WINDOW()

        #Establishes "window" as a instance of the "MAIN_WINDOW" class.

        window.show()

        #Shows the window to the screen.

        app.exec()

        #Executes the apps main loop.

    except:

        print("connection error")
        time.sleep(1)

        #Notifies the user that there was a connection error at one second intervals as to not cause spam.