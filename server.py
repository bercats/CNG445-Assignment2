from socket import *
from threading import *

class ClientThread(Thread):
    def __init__(self, clientAddress, clientSocket):
        Thread.__init__(self)
        self.cSocket = clientSocket
        self.cAddress = clientAddress
        print ("New connection added: ", clientAddress)

    def run(self):
        print ("Connection from : ", self.cAddress)
        self.cSocket.send("Welcome to the library! Connection Successful".encode())
        while True:
            clientMsg = self.cSocket.recv(1024).decode()
            #login message: login;username;password
            if clientMsg.startswith("login"):
                self.login(clientMsg)
            elif clientMsg.startswith("requestbooks"):
                self.sendbooks(clientMsg)
            elif clientMsg == "exit":
                self.exit()
            else:
                self.cSocket.send("Invalid command!".encode())

    def login(self, clientMsg):
        clientMsg = clientMsg.split(";")
        user, book, operations = load_data()
        for i in range(len(user)):
            if user[i][0] == clientMsg[1] and user[i][1] == clientMsg[2]:
                if user[i][2] == "librarian" or user[i][2] == "manager":
                    #loginsuccess;username;role
                    self.cSocket.send(f"loginsuccess;{user[i][0]};{user[i][2]}".encode())
                return
        self.cSocket.send("loginfailure".encode())
    
    def sendbooks(self, clientMsg):
        clientMsg = clientMsg.split(";")
        users, books, operations = load_data()
        books_string = ";".join(str(book) for book in books)
        self.cSocket.send(books_string.encode())
        return
        


    def exit(self):
        print ("Client at ", self.cAddress, " disconnected...")
        self.cSocket.close()
        exit()

    
            
        

def load_data():
    #users file read
    usersfile = open("users.txt", "r")
    user = usersfile.readlines()
    usersfile.close()
    for i in range(len(user)):
        user[i] = user[i].strip().split(";")
    #books file read
    booksfile = open("books.txt", "r")
    book = booksfile.readlines()
    booksfile.close()
    for i in range(len(book)):
        book[i] = book[i].strip().split(";")
    #operations file read
    operationsfile = open("operations.txt", "r")
    operations = operationsfile.readlines()
    operationsfile.close()
    for i in range(len(operations)):
        operations[i] = operations[i].strip().split(";")
    return user, book, operations


if __name__ == "__main__":
    serverSocket = socket(AF_INET, SOCK_STREAM)
    serverSocket.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
    serverSocket.bind(('', 8080))
    print ("Server started...")
    while True:
        print ("Waiting for connections...")
        serverSocket.listen()
        clientSocket, clientAddress = serverSocket.accept()
        newClient = ClientThread(clientAddress, clientSocket)
        newClient.start()
