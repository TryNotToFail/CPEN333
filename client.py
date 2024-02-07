# Group#: 1
# Student Names: Duc Thang Huynh (Dustin) and Andrey Abushakhamnov

#Content of client.py; to complete/implement

from tkinter import *
import socket
import threading
from multiprocessing import current_process

class ChatClient:
    """
    This class implements the chat client.
    It uses the socket module to create a TCP socket and to connect to the server.
    It uses the tkinter module to create the GUI for the chat client.
    """
    def __init__(self, window):
        #Setup connection
        while True: #Handling when the server is not ready
            try:    #Constantly trying to connect 
                self.clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.clientSocket.connect(('127.0.0.1', 55556))
                break #Connected then breakout
            except ConnectionRefusedError:
                print("Connecttion refused")  #not connected send message

        #Get the port number
        _,port = self.clientSocket.getsockname()
        #Generate receiving threads
        thread = threading.Thread(target=self.receive_messages)
        thread.start()

        self.window = window
        #setup GUI
        self.setup_GUI(port)

    def setup_GUI(self, port):
        self.window.title("Chat Client - {}".format(current_process().name))

        #Name of the process and Chat message sentence
        Label(self.window, text="{} @port #".format(current_process().name) + f"{port}").grid(row=0,columnspan=2, sticky=W)
        Label(self.window, text="Chat message").grid(row=1, column=0, sticky=W)

        #The user input text box
        self.message_entry = Entry(self.window)
        self.message_entry.grid(row=1, column=1)
        #Set the enter button as a send function
        self.message_entry.bind("<Return>", self.send)

        #Chat history
        Label(self.window, text="Chat History").grid(row=2, column=0, sticky=W)

        #Insert the chat frame for the chat history
        self.chat_frame = Frame(self.window)
        self.chat_frame.grid(row=3, column=0, columnspan= 10)

        # Add a Scrollbar to the Text widget
        scrollbar = Scrollbar(self.window, orient='vertical')
        scrollbar.grid(row=3, column=9, sticky=NS)

        #Stop user from editing the chat history
        self.chat_text = Text(self.chat_frame, height=10, width=50, state='disabled', yscrollcommand=scrollbar.set)
        self.chat_text.grid(row=3,column=0, columnspan=10)

        #Add the function to scroll veritcally
        scrollbar.config(command=self.chat_text.yview)

    def send(self, event):
        #get the message 
        message = self.message_entry.get()
        #allow to change the chat history to insert the new sentence
        self.chat_text.config(state='normal')
        #send the message to the socket
        message_sent = '{}: '.format(current_process().name) + message
        self.chat_text.insert(END, '                            ' + message_sent + '\n')
        self.clientSocket.send(message_sent.encode('utf-8'))
        #delete the entered message, minimized the step to delete when user input new sentence
        self.message_entry.delete(0, END)
        #update the chat history to the new sent message
        self.chat_text.yview(END)
        #stop the user to edit the chat history
        self.chat_text.config(state='disabled')

    def receive_messages(self):
        try:
            while TRUE:
                message_rev = self.clientSocket.recv(1024).decode('utf-8') #decode the receive messsage
                self.chat_text.config(state='normal')                       #change state to modified th chat history
                self.chat_text.insert(END, message_rev + '\n')              #insert the new sentence to the chat history   
                self.chat_text.yview(END)                                   #view the last sentence
                self.chat_text.config(state='disabled')                     #change state not allowing user to modified the chat history
        except socket.error as e:
            print(e)

def main(): #Note that the main function is outside the ChatClient class
    window = Tk()
    c = ChatClient(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__':  # May be used ONLY for debugging
    main()
