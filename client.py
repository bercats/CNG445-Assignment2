from socket import *
from tkinter import *
from tkinter import messagebox

class ClientScreen(Frame):
    def __init__(self, cSocket):
        self.cSocket = cSocket
        serverMsg = self.cSocket.recv(1024).decode()

        #pop up window
        messagebox.showinfo('Welcome', serverMsg)

        Frame.__init__(self)
        self.pack()
        self.master.title("Login")

        self.frame1 = Frame(self)
        self.frame1.pack(padx=5, pady=5)

        self.UserNameLabel = Label(self.frame1, text="Username")
        self.UserNameLabel.pack(side=LEFT, padx=5, pady=5)

        self.UserName = Entry(self.frame1)
        self.UserName.pack(side=LEFT, padx=5, pady=5)

        self.frame2 = Frame(self)
        self.frame2.pack(padx=5, pady=5)

        self.PasswordLabel = Label(self.frame2, text="Password")
        self.PasswordLabel.pack(side=LEFT, padx=5, pady=5)

        self.Password = Entry(self.frame2, show="*")
        self.Password.pack(side=LEFT, padx=5, pady=5)

        self.frame3 = Frame(self)
        self.frame3.pack(padx=5, pady=5)

        self.LoginButton = Button(self.frame3, text="Login", command=self.login)
        self.LoginButton.pack(padx=5, pady=5)

        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)


    def login(self):
        self.cSocket.send(f"login;{self.UserName.get()};{self.Password.get()}".encode())
        serverMsg = self.cSocket.recv(1024).decode()
        #loginsuccess;username;role
        #example: loginsuccess;greg;librarian
        #get role from serverMsg
        if serverMsg.split(';')[0] == "loginsuccess":
            if serverMsg.split(';')[2] == "librarian":
                self.master.destroy()
                self.librarianWindow = librarianWindow(self.cSocket)
                self.librarianWindow.mainloop()
            elif serverMsg.split(';')[2] == "manager":
                self.master.destroy()
                self.managerWindow = managerWindow(self.cSocket)
                self.managerWindow.mainloop()
        else:
            messagebox.showinfo('Error', serverMsg)

    def on_closing(self):
        self.cSocket.send("exit".encode())
        self.master.destroy()



class librarianWindow(Frame):
    def __init__(self, cSocket):
        self.cSocket = cSocket
        Frame.__init__(self)
        #TITLE
        self.grid(padx=5, pady=5)
        self.master.title("Librarian Panel")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame1 = Frame(self)
        self.frame1.grid(row=0, padx=5, pady=5)
        self.bookslabel = Label(self.frame1, text="Books")
        self.bookslabel.grid(row=0, padx=5, pady=5)
        #BOOKS
        self.frame2 = Frame(self)
        self.frame2.grid(row=1, column=0, padx=5, pady=5)
        self.frame3 = Frame(self)
        self.frame3.grid(row=1, column=1, padx=5, pady=5)
        #send request books
        self.cSocket.send("requestbooks".encode())
        #receive books
        books_data = self.cSocket.recv(1024).decode()
        #split books_data into individual books
        books = books_data.split(';')
        #list books with checkbuttons
        self.booklist = []
        self.labelList = []
        for book_data in books:
            book = book_data.strip('[]').split(', ')  # Split each book record into components
            if len(book) > 1:  # Check if the book record has at least two elements
                book_title = book[1].strip("'")  # Remove quotes around the title
                book_author = book[2].strip("'")  # Remove quotes around the author
                self.labelList.append(Label(self.frame2, text=f"{book_title} by {book_author}", anchor='w'))
                self.booklist.append(Checkbutton(self.frame2))
        for i, label in enumerate(self.labelList):
            label.grid(row=i, column=0, padx=5, pady=5)
        for i, book in enumerate(self.booklist):
            book.grid(row=i, column=1, padx=5, pady=4)

        #Date (dd.mm.yyyy)
        self.frame3 = Frame(self)
        self.frame3.grid(row=len(self.labelList), column=0, padx=5, pady=5)
        self.datelabel = Label(self.frame3, text="Date (dd.mm.yyyy):")
        self.datelabel.grid(row=0,column=0, padx=7, pady=5)
        self.date = Entry(self.frame3)
        self.date.grid(row=0,column=1, padx=7, pady=5)

        #Client's Name
        self.frame4 = Frame(self)
        self.frame4.grid(row=len(self.labelList) + 1, column=0, padx=5, pady=5)
        self.clientlabel = Label(self.frame4, text="Client's Name:")
        self.clientlabel.grid(row=0, column = 0, padx=5, pady=5)
        self.client = Entry(self.frame4)
        self.client.grid(row=0, column = 1, padx=5, pady=5)

        #rent, return, close buttons
        self.frame5 = Frame(self)
        self.frame5.grid(row=len(self.labelList) + 2, column=0, padx=5, pady=5)
        self.rentbutton = Button(self.frame5, text="Rent", command=self.rent)
        self.rentbutton.grid(row=0, column=0, padx=5, pady=5)
        self.returnbutton = Button(self.frame5, text="Return", command=self.returnbook)
        self.returnbutton.grid(row=0, column=1, padx=5, pady=5)
        self.closebutton = Button(self.frame5, text="Close", command=self.on_closing)
        self.closebutton.grid(row=0, column=2, padx=5, pady=5)

        


    def on_closing(self):
        self.cSocket.send("exit".encode())
        self.master.destroy()

    def rent(self):
        #rent;librarianName;clientsUsername;date;itemID;itemID...
        #example: rent;greg;bob;12.12.2020;1;2;3
        #get selected books
        selected_books = []
        for i, book in enumerate(self.booklist):
            if book.get() == 1:
                selected_books.append(i)
        print(selected_books)
    
    def returnbook(self):
        pass

class managerWindow(Frame):
    def __init__(self, cSocket):
        self.cSocket = cSocket
        Frame.__init__(self)
        self.grid(padx=5, pady=5)
        self.master.title("Manager Panel")
        self.master.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame1 = Frame(self)
        self.frame1.grid(row=0, padx=5, pady=5)

        report_options = [
            ("(1) Most rented book overall", "report1"),
            ("(2) Librarian with the highest number of operations", "report2"),
            ("(3) Total generated revenue by the library", "report3"),
            ("(4) Average rental period for 'Harry Potter'", "report4")
        ]

        self.reportslabel = Label(self.frame1, text="REPORTS")
        self.reportslabel.grid(row=0, padx=5, pady=5)
        # Create a StringVar to hold the value of the selected radio button
        self.selected_option = StringVar()
        # Create a radio button for each report option
        for i, (text, value) in enumerate(report_options):
            Radiobutton(self.frame1, text=text, variable=self.selected_option, value=value).grid(row=i+1, column=0, padx=5, pady=5)
        self.frame3 = Frame(self)
        self.frame3.grid(row=2, column=0, padx=5, pady=5)
        #create, close
        self.createbutton = Button(self.frame3, text="Create", command=self.create)
        self.createbutton.grid(row=0, column=0, padx=5, pady=5)
        self.closebutton = Button(self.frame3, text="Close", command=self.on_closing)
        self.closebutton.grid(row=0, column=1, padx=5, pady=5)


    def on_closing(self):
        self.cSocket.send("exit".encode())
        self.master.destroy()
    
    def create(self):
        pass


if __name__ == "__main__":
    HOST = ""
    PORT = 8080
    socket = socket(AF_INET, SOCK_STREAM)
    socket.connect((HOST, PORT))
    window = ClientScreen(socket)
    window.mainloop()