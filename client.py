
import socket
import threading
import tkinter as tk
from tkinter import scrolledtext, Entry, Button, Label

HOST = '127.0.0.1'
PORT = 1234

class ChatClientGUI:
    def __init__(self, master):
        self.master = master
        master.title("Chat Client")

        master.minsize(width=600, height=400)


        master.columnconfigure(0, weight=1)
        master.columnconfigure(1, weight=0)
        master.columnconfigure(2, weight=2)
        master.rowconfigure(0, weight=0)
        master.rowconfigure(1, weight=1)
        master.rowconfigure(2, weight=0)

        self.username_label = Label(master, text="Username:", fg="black", font=("Helvetica", 12))
        self.username_label.grid(row=0, column=0, sticky="e")

        self.username_entry = Entry(master, width=20, font=("Helvetica", 12))
        self.username_entry.grid(row=0, column=1, sticky="we")

        self.connect_button = Button(master, text="Connect", command=self.connect_to_server, font=("Helvetica", 12))
        self.connect_button.grid(row=0, column=2, sticky="w")

        self.chat_display = scrolledtext.ScrolledText(master, state='disabled', height=15, width=50, font=("Helvetica", 12))
        self.chat_display.grid(row=1, column=0, columnspan=3, sticky="nsew")

        self.message_entry = Entry(master, width=40, font=("Helvetica", 12))
        self.message_entry.grid(row=2, column=0, columnspan=4, sticky="ew")

        self.send_button = Button(master, text="Send", command=self.send_message, state=tk.DISABLED,fg="black" ,font=("Helvetica", 12))
        self.send_button.grid(row=2, column=2, sticky="ew")

        self.message_entry.bind("<Return>", self.send_on_enter)

        self.username_entry.bind("<Return>", self.connect_on_enter)

        self.client = None
        self.username = None

    def send_on_enter(self, event):
        self.send_message()

    def connect_on_enter(self, event):
            self.connect_to_server()
    def connect_to_server(self):
        username = self.username_entry.get()
        if not username:
            print("Username cannot be empty")
            return

        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect((HOST, PORT))
            print("Successfully connected to server")
            self.username_entry.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.DISABLED)
            self.send_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f'Unable to connect to server: {e}')
            return

        self.client.sendall(username.encode())
        threading.Thread(target=self.receive_messages).start()



    def connect_to_server(self):
        username = self.username_entry.get()
        if not username:
            print("Username cannot be empty")
            return

        self.username = username
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        try:
            self.client.connect(('127.0.0.1', 1234))
            print("Successfully connected to server")
            self.username_entry.config(state=tk.DISABLED)
            self.connect_button.config(state=tk.DISABLED)
            self.send_button.config(state=tk.NORMAL)
        except Exception as e:
            print(f'Unable to connect to server: {e}')
            return

        self.client.sendall(username.encode())
        threading.Thread(target=self.receive_messages).start()

    def send_message(self):
        message = self.message_entry.get()
        if message:
            self.client.sendall(message.encode())
            self.message_entry.delete(0, 'end')
            self.display_local_message(f"{self.username}: {message}")
        else:
            print("Empty message")

    def display_local_message(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)



    def receive_messages(self):
        while True:
            try:
                message = self.client.recv(2048).decode('utf-8')
                self.display_message(message)
            except Exception as e:
                print(f"Error receiving message: {e}")
                break

    def display_message(self, message):
        self.chat_display.configure(state='normal')
        self.chat_display.insert(tk.END, message + '\n')
        self.chat_display.configure(state='disabled')
        self.chat_display.see(tk.END)

if __name__ == '__main__':
    root = tk.Tk()
    chat_client = ChatClientGUI(root)
    root.mainloop()
