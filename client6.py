from socket import *
from tkinter import *
import threading
from tkinter import font

HOST = 'localhost'
PORT = 50002
BUFSIZ = 1024
ADDR = (HOST, PORT)
tcpCliSock = socket(AF_INET, SOCK_STREAM)
tcpCliSock.connect(ADDR)

#this while loop is responsible for switching ports
while True:
    new_port = tcpCliSock.recv(BUFSIZ)
    if new_port:
        print(f"RECEIVED: {new_port.decode('utf-8')}")
        break
tcpCliSock.close()

#connecting to the new port
NEW_PORT = int(new_port.decode())
NEW_ADDR = (HOST, NEW_PORT)
newsock = socket(AF_INET, SOCK_STREAM)
newsock.connect(NEW_ADDR)

#lines 28 - 53 are creating the tkinter list window
#creates the tkinter window
root = Tk()
root.title('My Chat')
root.geometry('400x300')

#creates the label
label_font = font.Font(size=16)
label = Label(root, text="Enter text here:", font=label_font)
label.grid(row=0, column=0, padx=5, pady=5)

#creates the entry box
entry_font = font.Font(size=14)
entry = Entry(root, font=entry_font, width=30)
entry.grid(row=1, column=0, padx=5, pady=5)

frame = Frame(root)
frame.grid(row=2, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")


#creates the listbox and the scroll bar
scrollbar = Scrollbar(frame)
scrollbar.pack(side=RIGHT, fill=Y)
listbox_font = font.Font(size=14)
listbox = Listbox(frame, yscrollcommand=scrollbar.set)
listbox.pack(side=LEFT, fill=BOTH, expand=True)
scrollbar.config(command=listbox.yview)

#responsible for sending data to the server and printing it in the listbox
def insert_data():
    data = entry.get()
    if data:
        listbox.insert(END, 'SENT: ' + data)
        listbox.yview_moveto(1.0)
        data = data.encode('utf-8')
        newsock.send(data)
        entry.delete(0, END)

#creates the button for sending and printing data
button = Button(root, text="Send", command=insert_data)
button.grid(row=1, column=1, padx=5, pady=5)

#the conversetion between the client and the server
def chat():
    while True:

        data = newsock.recv(BUFSIZ)
        if not data:
            break
        print(f"RECEIVED: {data.decode('utf-8')}")
        #inserts the data from the server into the listbox
        listbox.insert(END, 'RECEIVED: ' + data.decode('utf-8'))
    newsock.close()
    root.destroy()

#responsible for creating the chat thread
threading.Thread(target=chat).start()

root.mainloop()
