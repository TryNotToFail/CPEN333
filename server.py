# Group#: 1
# Student Names: Duc Thang Huynh (Dustin) and Andrey Abushakhamnov

#Content of client.py; to complete/implement

from tkinter import *
import socket
import threading

class ChatServer:
    """
    This class implements the chat server.
    It uses the socket module to create a TCP socket and act as the chat server.
    Each chat client connects to the server and sends chat messages to it. When 
    the server receives a message, it displays it in its own GUI and also sends 
    the message to the other client.  
    It uses the tkinter module to create the GUI for the server client.
    """
    def __init__(self, window):
        #Setup GUI
        self.window = window
        self.setup_GUI()

        threading.Thread(target=self.setup_server).start()
    
    def setup_server(self):
        #Setup socket server
        self.serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        #Reuse the socket
        self.serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #Waiting for request 
        self.serverSocket.bind(('127.0.0.1', 55556))  # Change the port to a different one
        self.serverSocket.listen()

        print("Server is ready")

        self.clients = set()
        self.threads = set()

        #Accept the request
        while True:
            try:
                clientSocket, addr = self.serverSocket.accept()
                print("Connection from", addr)
                self.clients.add(clientSocket)
                cthread = threading.Thread(target=self.handling, args=(clientSocket,))
                cthread.daemon = TRUE
                self.threads.add(cthread)
                cthread.start()
            except socket.error:
                print(socket.error)
                break
        
        #Threading for the receive message
    def handling(self, csocket):
        while True:
            try:
                message = csocket.recv(1024).decode('utf-8')
                for i in self.clients:
                    if csocket != i:
                        i.send(message.encode('utf-8'))
                self.chat_text.config(state="normal")
                self.chat_text.insert(END, f"{message}" + '\n')
                self.chat_text.config(state="disabled")
            except socket.error:
                print(socket.error)
                self.clients.remove(csocket)
                break

    def setup_GUI(self):
        self.window.title("Chat Server")
        print("Setup GUI")

        #Label the chat history and server
        Label(self.window, text="Chat Server").grid(row=0, column=0, sticky=W)
        Label(self.window, text="Chat History").grid(row=1, column=0, sticky=W)

        #Add Scrollbar
        scrollbar = Scrollbar(self.window, orient='vertical')
        scrollbar.grid(row=2, column=7, sticky=NS)

        #Add the text box
        self.chat_text = Text(self.window, height=10, width=50, state='disabled', yscrollcommand=scrollbar.set)
        self.chat_text.grid(row=2, column=0, columnspan=7)

        #Configure allow scroll
        scrollbar.config(command=self.chat_text.yview)
        print("Done setup GUI")

def main(): #Note that the main function is outside the ChatServer class
    window = Tk()
    ChatServer(window)
    window.mainloop()
    #May add more or modify, if needed

if __name__ == '__main__': # May be used ONLY for debugging
    main()
