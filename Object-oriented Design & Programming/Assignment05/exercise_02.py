import os
class Account:
    def __init__(self, account_no=None, name=None, password=None, balance=None, path=None):
        self.account_no = account_no
        self.name = name
        self.password = password
        self.balance = balance
        self._path = path if path else 'account.txt'
        self._list = {}
        self.check_file_exist()

    # check file exist or not
    def check_file_exist(self):
        if not os.path.isfile(self._path):
            with open(self._path, 'w') as File:
                for i in range(1, 6):
                    File.write(str(i) + ', ' + 'user' + str(i) + ', ' + '1234' + ', ' + str(1000) + '\n')

    # read data from data.txt
    def read_data(self):
        with open(self._path, 'r') as File:
            # read data line by line
            for line in File:
                p = Account('', '', '', '')  # create model
                raw_data = line.strip('\n')  # remove every \n
                p.account_no, p.name, p.password, p.balance = raw_data.split(', ')  # split data by ', ' and assign to model
                self._list[int(p.account_no)] = p  # add to dictionary

    # login method
    def login(self):
        # check file does file exists or not
        self.check_file_exist()
        # read data from file
        self.read_data()
        print('-Login')
        while True:
            self.account_no = int(input("Account Number: "))
            if self.account_no in self._list.keys():  # check account does it exist in data
                break
            else:
                print("Account Number does not exist")
        while True:
            self.password = input("Password: ")
            if self.password == self._list[self.account_no].password:  # check password does it match the account
                break
            else:
                print("Password is incorrect")
        print("Login successful")

    def display_balance(self):
        print("Your balance is: ", self._list[self.account_no].balance, '$')

    # withdraw method
    def withdraw(self):
        # check file does file exists or not
        self.check_file_exist()
        # read data from file
        self.read_data()
        print("-Withdraw")
        while True:
            amount = float(input("Amount: "))
            if (amount <= float(self._list[self.account_no].balance)) and (amount > 0):  # if amount <= balance it's going break
                break
            else:
                print("Insufficient balance")
        # withdraw money
        self._list[self.account_no].balance = float(self._list[self.account_no].balance) - amount
        # display balance after withDraw
        self.display_balance()
        print("Withdraw successful")

        # display balance after transfer
        with open(self._path, 'w') as File:
            for j in self._list.values():
                File.write(str(j.account_no) + ', ' + j.name + ', ' + j.password + ', ' + str(j.balance) + '\n')
    # deposit method
    def deposit(self):
        # check file does file exists or not
        self.check_file_exist()
        # read data from file
        self.read_data()
        print("-Deposit")
        while True:
            amount = float(input("Amount: "))
            if amount > 0:
                break
            else:
                print("Invalid amount")
        # deposit money
        self._list[self.account_no].balance = float(self._list[self.account_no].balance) + amount
        # display balance after deposit
        self.display_balance()
        print("Deposit successful")
        # display balance after transfer
        with open(self._path, 'w') as File:
            for j in self._list.values():
                File.write(str(j.account_no) + ', ' + j.name + ', ' + j.password + ', ' + str(j.balance) + '\n')

    def transfer(self):
        # check file does file exists or not
        self.check_file_exist()
        # read data from file
        self.read_data()
        print("-Transfer")
        while True:
            account_no = int(input("Account Number: "))
            if account_no in self._list.keys():
                break
            else:
                print("Account Number does not exist")
        while True:
            amount = float(input("Amount: "))
            if (amount <= float(self._list[self.account_no].balance)) and (amount > 0):
                break
            else:
                print("Insufficient balance")
        # transfer money
        # subtract from sender
        self._list[self.account_no].balance = float(self._list[self.account_no].balance) - amount
        # add to receiver
        self._list[account_no].balance = float(self._list[account_no].balance) + amount
        # write data to file
        with open(self._path, 'w') as File:
            for j in self._list.values():
                File.write(str(j.account_no) + ', ' + j.name + ', ' + j.password + ', ' + str(j.balance) + '\n')
        # display balance after transfer
        print("Transfer successful")
        self.display_balance()

# main method to run the program
if __name__ == '__main__':
    account = Account()
    account.login()
    print("Welcome to the Phanith Bank")
    while True:
        print("a. Display Balance")
        print("b. Withdraw")
        print("c. Deposit")
        print("d. Transfer")
        print("e. Exit")
        choice = input("Enter your choice: ")
        if choice == 'a':
            account.display_balance()
        elif choice == 'b':
            account.withdraw()
        elif choice == 'c':
            account.deposit()
        elif choice == 'd':
            account.transfer()
        elif choice == 'e':
            break
        else:
            print("Invalid choice")