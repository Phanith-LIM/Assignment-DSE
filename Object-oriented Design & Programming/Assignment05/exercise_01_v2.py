class Employees:
    def __init__(self, id=None, name=None, gender=None, salary=None, _list=None,):
        self.id = id
        self.name = name
        self.gender = gender
        self.salary = salary
        self._path = 'employees.txt'
        self._dic = {}
    # read data from data.txt
    def read_data(self):
        list = {}
        with open(self._path, 'r') as File:
            # read data line by line
            for line in File:
                e = Employees('', '', '', '')  # create model
                raw_data = line.strip('\n')  # remove every \n
                e.id, e.name, e.gender, e.salary = raw_data.split(', ')  # split data by ', ' and assign to model
                list[int(e.id)] = e  # add to dictionary
        self._dic = dict(sorted(list.items()))  # sort dictionary by key
    def read_employee(self):
        self.read_data()  # read data from to get date to _list
        while True:
            self.id = int(input("Id: "))
            if self.id not in self._dic.keys():  # if id from input not equal to keys. loop is going to break
                break
            print("Id already exists")
        self.name = input("Name: ")
        while True:
            self.gender = input("Gender: ")
            # gender in list is going to break
            if self.gender in ['M', 'F', 'Male', 'Female', 'male', 'female']:
                break
            print('gender must be M or F')
        self.salary = float(input("Salary: "))
    def add_employee(self):
        print('-Add Employee')
        self.read_employee()
        # write data to data.txt
        print('Employee added successfully')
        with open(self._path, 'a') as File:
            File.write(str(self.id) + ', ' + str(self.name) + ', ' + str(self.gender) + ', ' + str(self.salary) + '\n')
        # read data to get data from file
        self.read_data()
        # write data again to make sure data is sorted
        with open(self._path, 'w') as File:
            for j in self._dic.values():
                File.write(str(j.id) + ', ' + str(j.name) + ', ' + str(j.gender) + ', ' + str(j.salary) + '\n')
    def delete(self):
        print('-Remove Employee')
        self.read_data()
        while True:
            id = int(input("Id: "))
            if id in self._dic.keys():  # if id exist in self._dic it's going to remove that data
                self._dic.pop(id)  # remove by key dictionary
                with open(self._path, 'w') as File:
                    for j in self._dic.values():
                        File.write(str(j.id) + ', ' + j.name + ', ' + j.gender + ', ' + str(j.salary) + '\n')
                print("deleted successfully")
                break
            print("Id not found")
    def search_by_id(self, id=None):
        print('-Search Employee')
        # read data to get data from file
        self.read_data()
        print("--------------------------------------------")
        print("{:<5} {:<15} {:<10} {:<10}".format('ID', 'Name', 'Gender', 'Salary'))
        print("--------------------------------------------")
        # if id exist in self._dic it's going to return that data
        if int(id) in self._dic.keys():
            print("{:<5} {:<15} {:<10} {:<10}".format(self._dic[id].id, self._dic[id].name, self._dic[id].gender, self._dic[id].salary))
            # if id doesn't exist display not found
        else:
            print("Search Not Found")
        print("--------------------------------------------")

    def show(self):
        # read data to get data from file
        self.read_data()
        # display data
        print("--------------------------------------------")
        print("{:<5} {:<15} {:<10} {:<10}".format('ID', 'Name', 'Gender', 'Salary'))
        print("--------------------------------------------")
        for p in self._dic.values():
            print("{:<5} {:<15} {:<10} {:<10}".format(p.id, p.name, p.gender, p.salary))
        print("--------------------------------------------")

# main program start here
if __name__ == '__main__':

    # generate data to file
    with open('employees.txt', 'w') as file:
        for i in range(1, 6):
            file.write(str(i) + ', ' + 'phanith' + str(i) + ', ' + 'M' + ', ' + str(i * 36) + '\n')

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
            id_employee = int(input("ID: "))
            employees.search_by_id(id_employee)
        elif menu == 'd':
            employees.show()
        elif menu == 'e':
            break
        else:
            print("Invalid choice")