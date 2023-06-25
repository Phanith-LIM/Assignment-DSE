import os.path
class Employees:
    def __init__(self, id=None, name=None, gender=None, salary=None, _list=None, path=None):
        self.id = id
        self.name = name
        self.gender = gender
        self.salary = salary
        self._path = path if path else 'employees.txt'
        self._list = {}
        self.check_file_exist()

    # check file exist or not
    def check_file_exist(self):
        if not os.path.isfile(self._path):
            with open(self._path, 'w') as File:
                for i in range(1, 6):
                    File.write(str(i) + ', ' + 'phanith' + str(i) + ', ' + 'M' + ', ' + str(i * 36) + '\n')

    # read data from data.txt
    def read_data(self):
        with open(self._path, 'r') as File:
            # read data line by line
            for line in File:
                e = Employees('', '', '', '')  # create model
                raw_data = line.strip('\n')  # remove every \n
                e.id, e.name, e.gender, e.salary = raw_data.split(', ')  # split data by ', ' and assign to model
                self._list[int(e.id)] = e  # add to dictionary

    def read_employee(self):
        self.check_file_exist()
        self.read_data()  # read data from to get date to _list
        while True:
            self.id = int(input("Id: "))
            if str(self.id) not in self._list.keys():  # if id from input not equal to keys. loop is going to break
                break
            else:
                print("Id already exists")
        self.name = input("Name: ")
        while True:
            self.gender = input("Gender: ")
            # if gender from input not equal to keys. loop is going to break
            if self.gender in ['M', 'F', 'Male', 'Female', 'male', 'female']:
                break
            else:
                print('gender must be M or F')
        self.salary = float(input("Salary: "))

    def add_employee(self):
        # check file exist or not
        self.check_file_exist()
        print('-Add Employee')
        self.read_employee()
        # write data to data.txt
        print('Employee added successfully')
        with open(self._path, 'a') as File:
            File.write(str(self.id) + ', ' + str(self.name) + ', ' + str(self.gender) + ', ' + str(self.salary) + '\n')
        # read data and write again to make data in data.text recognize by order
        self.read_data()
        with open(self._path, 'w') as File:
            for j in self._list.values():
                File.write(str(j.id) + ', ' + j.name + ', ' + j.gender + ', ' + str(j.salary) + '\n')

    def delete(self):
        # check file exist or not
        self.check_file_exist()
        print('-Remove Employee')
        self.read_data()
        while True:
            id = input("Id: ")
            if id in self._list.keys():  # if id from input not equal to keys. loop is going to break
                self._list.pop(id)  # remove by key dictionary
                with open(self._path, 'w') as File:
                    for j in self._list.values():
                        File.write(str(j.id) + ', ' + j.name + ', ' + j.gender + ', ' + str(j.salary) + '\n')
                print("deleted successfully}")
                break
            else:
                print("Id not found")

    def search_by_id(self, id=None):
        # check file exist or not
        self.check_file_exist()
        print('-Search Employee')
        # read data to get data from file
        self.read_data()
        print("--------------------------------------------")
        print("{:<5} {:<15} {:<10} {:<10}".format('ID', 'Name', 'Gender', 'Salary'))
        print("--------------------------------------------")
        # if id exist in self._list it's going to return that data
        if id in self._list.keys():
            print("{:<5} {:<15} {:<10} {:<10}".format(self._list[id].id, self._list[id].name, self._list[id].gender, self._list[id].salary))
        else:
            print("Search Not Found")  # if id doesn't exist display not found
        print("--------------------------------------------")

    def show(self):
        # check file exist or not
        self.check_file_exist()
        # read data to get data from file
        self.read_data()
        # display data
        print("--------------------------------------------")
        print("{:<5} {:<15} {:<10} {:<10}".format('ID', 'Name', 'Gender', 'Salary'))
        print("--------------------------------------------")
        for i in self._list.values():
            print("{:<5} {:<15} {:<10} {:<10}".format(i.id, i.name, i.gender, i.salary))
        print("--------------------------------------------")

# main program start here
if __name__ == '__main__':
    employees = Employees()
    while True:
        print("Employee Management System")
        print("a. Add a new employee")
        print("b. Delete employee by id")
        print("c. Search employee by id")
        print("d. Display all employee")
        print("e. Exit the program")
        menu = input("menu: ")
        if menu == 'a':
            employees.add_employee()
        elif menu == 'b':
            employees.delete()
        elif menu == 'c':
            id_employee = input("ID: ")
            employees.search_by_id(id_employee)
        elif menu == 'd':
            employees.show()
        elif menu == 'e':
            break
        else:
            print("Invalid choice")