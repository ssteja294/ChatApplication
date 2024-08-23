# GUI

import socket
import threading
from tkinter import *
from tkinter import scrolledtext

def send():
    text = textEntry.get()
    if text:
        message = text.encode(FORMAT)
        msg_length = len(message)
        send_length = str(msg_length).encode(FORMAT)
        send_length += b' ' * (HEADER - len(send_length))
        client.send(send_length)
        client.send(message)
        uIChat(f"Sai: {text}")
        textEntry.delete(0, END) 

def uIChat(msg):
    chatDisplay.config(state = NORMAL)  
    chatDisplay.insert(END, msg + '\n')  
    chatDisplay.config(state = DISABLED)  
    chatDisplay.yview(END)


def receive():
    while True:
        try:
            msg_length = client.recv(HEADER).decode(FORMAT)
            if msg_length:
                msg_length = int(msg_length)
                msg = client.recv(msg_length).decode(FORMAT)
                window.after(0, lambda: uIChat(f"Server: {msg}"))
        except:
            print("An error occurred.")
            break

def userInterface():
	global window, chatDisplay, textEntry
	window = Tk()
	window.title("Client")
	window.geometry("1280x720")
	chatDisplay = scrolledtext.ScrolledText(window, state = DISABLED, width = 50, height = 20, wrap = WORD)
	chatDisplay.grid(row = 0, column = 0, padx = 10, pady = 10)
	textEntry = Entry(window, width = 40)
	textEntry.grid(row = 1, column=0, padx = 10, pady = 10)
	sendButton = Button(window, text = "Send", command = send)
	sendButton.grid(row = 1, column = 1, padx = 10, pady = 10)
	window.mainloop()

HEADER = 64-
PORT = 5123
FORMAT = 'UTF-8'
DISCONNECT_MESSAGE = "!DISCONNECT"
SERVER = "192.168.1.43"
ADDR = (SERVER, PORT)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(ADDR)
receive_thread = threading.Thread(target = receive)
receive_thread.start()
userInterface()