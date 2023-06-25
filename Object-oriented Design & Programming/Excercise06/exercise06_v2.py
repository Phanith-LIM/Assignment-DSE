import csv
from prettytable import PrettyTable


from datetime import datetime
def validateDate(date):
    today = datetime.today()
    try:
        date = datetime.strptime(date, '%d/%m/%Y')
        if today.year - date.year >= 18:
            return True
        print('Your age must be greater than or equal to 18')
        return False
    except ValueError:
        print('Date must be in the format dd/mm/yyyy')
        return False

def validatePhone(phone):
    try:
        if not phone.startswith('0'):
            print('Phone must start with 0')
            return False
        if not phone.isdigit():
            print('Phone must be a number')
            return False
        if not 8 <= len(phone) <= 11:
            print('Phone must be 8-11 digits')
            return False
        return True
    except ValueError:
        return False

class Teacher:
    def __init__(self):
        self.teacher_data = {}
        self.course_data = {}
        self.del_data = []
        self.teacher_course = {}
        self.teacher_path = 'teacher.csv'
        self.course_path = 'course.csv'
        self.det_path = 'deleted_teacher.csv'
        self.teacher_course_path = 'teacher_course.csv'
        self.header_teacher = []
        self.header_course = []

    # Read data from csv file
    def readData(self):
        with open(self.teacher_path, 'r',) as fileTeacher, open(self.course_path, 'r') as fileCourse, open(self.teacher_course_path, 'r') as fileTC, open(self.det_path, 'r') as fileDelete:
            t_reader = csv.reader(fileTeacher)
            c_reader = csv.reader(fileCourse)
            tc_reader = csv.reader(fileTC)
            del_reader = csv.reader(fileDelete)

            # Read header
            self.header_teacher = next(t_reader)
            self.header_course = next(c_reader)
            next(tc_reader)
            next(del_reader)
            # Read Teacher data from teacher.csv
            for data in t_reader:
                self.teacher_data[int(data[0])] = {
                    'id': int(data[0]),
                    'name': data[1],
                    'gender': data[2],
                    'birth': data[3],
                    'phone': data[4],
                    'address': data[5],
                }
            self.teacher_data = dict(sorted(self.teacher_data.items()))
            # Read teacherId and courseId from teacher_course.csv
            for data in c_reader:
                self.course_data[int(data[0])] = {
                    'id': int(data[0]),
                    'name': data[1],
                    'credit': int(data[2]),
                }
            self.course_data = dict(sorted(self.course_data.items()))

            # Read teacherId and courseId from teacher_course.csv
            self.teacher_course.clear()
            for data in tc_reader:
                if int(data[0]) in self.teacher_course.keys():
                    self.teacher_course[int(data[0])].append(int(data[1]))
                    continue
                self.teacher_course[int(data[0])] = [int(data[1])]
            self.teacher_course = dict(sorted(self.teacher_course.items()))

            # read deleted id from deleted_teacher.csv
            for data in del_reader:
                self.del_data.append(int(data[0]))
            self.del_data = sorted(self.del_data)

    # Update data to csv file
    def updateDate(self, mode, data=None):
        with open(self.teacher_path, mode, newline='') as File:
            writer = csv.writer(File)
            if mode == 'a':
                writer.writerow(data)
                return
            if mode == 'w':
                writer.writerow(self.header_teacher)
                for data in self.teacher_data.values():
                    writer.writerow(data.values())

    # add teacher method
    def add_teacher(self):
        self.readData()
        while True:
            teacherId = input('Enter teacherId: ')
            if not teacherId.isdigit():
                print('Id must be a number')
                continue
            if not int(teacherId) > 0:
                print('Id must be a positive integer')
                continue
            if int(teacherId) in self.teacher_data.keys():
                print('Id already exists')
                continue
            if int(teacherId) in self.del_data:
                print('Id already exists')
                continue
            break

        name = input('Enter name: ')

        while True:
            gender = input('Gender: ')
            if gender in ['M', 'F']:
                break

        while True:
            birth = input('Enter birth: ')
            if validateDate(birth):
                break

        while True:
            phone = input('Enter phone: ')
            if validatePhone(phone):
                break

        address = input('Enter address: ')
        data = [teacherId, name, gender, birth, phone, address]
        self.updateDate('a', data)
        print('Add teacher successfully!')

    def search_teacher(self, teacherId):
        self.readData()
        teacherId = int(teacherId)
        if teacherId not in self.teacher_data.keys():
            print('Teacher Id does not exist!')
            return
        print('+ Search Teacher')
        table = PrettyTable()
        table.field_names = self.header_teacher
        table.add_row(self.teacher_data[teacherId].values())
        print(table)

    # update information of teacher
    def update_teacher(self, teacherId):
        self.readData()
        teacherId = int(teacherId)
        self.teacher_data[teacherId]['name'] = input('Enter name: ')

        while True:
            self.teacher_data[teacherId]['gender'] = input('Gender: ')
            if self.teacher_data[teacherId]['gender'] in ['M', 'F']:
                break

        while True:
            self.teacher_data[teacherId]['birth'] = input('Enter birth: ')
            if validateDate(self.teacher_data[teacherId]['birth']):
                break

        while True:
            self.teacher_data[teacherId]['phone'] = input('Enter phone: ')
            if validatePhone(self.teacher_data[teacherId]['phone']):
                break

        self.teacher_data[teacherId]['address'] = input('Enter address: ')
        self.updateDate('w')
        print('Update successfully!')

    # delete information of teacher
    def delete_teacher(self, teacherId):
        self.readData()
        teacherId = int(teacherId)
        print('+ Delete Teacher')
        if teacherId not in self.teacher_data.keys():
            print('Teacher Id does not exist!')
            return

        confirm = input('Are you sure you want to delete this course? (Yes/No): ')
        if confirm == 'Yes':
            with open(self.det_path, 'a', newline='') as fileDelete, open(self.teacher_course_path, 'w',
                                                                          newline='') as fileTC:
                # teacherId exists in teacher_course.csv
                if teacherId in self.teacher_course.keys():
                    del self.teacher_course[teacherId]
                    tc_writer = csv.writer(fileTC)
                    tc_writer.writerow(['TeacherId', 'CourseId'])
                    for key in self.teacher_course.keys():
                        for value in self.teacher_course[key]:
                            tc_writer.writerow([key, value])

                # writes deleted teacherId to deleted_teacher.csv
                del_writer = csv.writer(fileDelete)
                del_writer.writerow(self.teacher_data[teacherId].values())
                del self.teacher_data[teacherId]
                self.updateDate('w')
            print('Delete successfully!')
            return
        print('Delete canceled!')
        return

    # teacher teaches course by teacherId
    def course_taught_by(self, teacherId):
        self.readData()
        if int(teacherId) not in self.teacher_data.keys():
            print('Teacher Id does not exist!')
            return
        if int(teacherId) not in self.teacher_course.keys():
            print('Teacher does not teach any course!')
            return
        table = PrettyTable()
        table.clear()
        print('Lecturer: ' + self.teacher_data[int(teacherId)]['name'])
        table.field_names = self.header_course[:3]
        for index in self.teacher_course[int(teacherId)]:
            table.add_row([self.course_data[index]['id'], self.course_data[index]['name'], self.course_data[index]['credit']])
        print(table)

if __name__ == '__main__':
    teacher = Teacher()
    while True:
        print('[a] Add new a Teacher')
        print('[b] Search a Teacher by ID ')
        print('[c] Update a Teacher')
        print('[d] Delete a Teacher')
        print('[e] Display all courses taught by a teacher.')
        print('[f] Exit')
        menu = input('Enter your choice: ')
        if menu == 'a':
            teacher.add_teacher()
        elif menu == 'b':
            id = input('Enter teacher id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            teacher.search_teacher(id)
        elif menu == 'c':
            id = input('Enter teacher id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            teacher.update_teacher(id)
        elif menu == 'd':
            id = input('Enter teacher id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            teacher.delete_teacher(id)
        elif menu == 'e':
            id = input('Enter teacher id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            teacher.course_taught_by(id)
        elif menu == 'f':
            print('Program terminated!')
            break
        else:
            print('Invalid Input! Please enter again.')