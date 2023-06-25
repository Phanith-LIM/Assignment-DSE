import csv
from prettytable import PrettyTable
from simple_term_menu import TerminalMenu

class Course:
    def __init__(self):
        self._course_data = {}
        self._dept_data = []
        self._del_data = []
        self._course_path = 'course.csv'
        self._dept_path = 'department.csv'
        self._det_path = 'delete_course.csv'
        self._header_course = []

    # Read data from csv file
    def readData(self):
        with open(self._course_path, 'r') as fileCourse, open(self._dept_path, 'r') as fileDept, open(self._det_path, 'r') as fileDelete:
            course_reader = csv.reader(fileCourse)
            dept_reader = csv.reader(fileDept)
            del_reader = csv.reader(fileDelete)

            # Read header
            self._header_course = next(course_reader)
            next(dept_reader)
            next(fileDelete)
            for course_data in course_reader:
                self._course_data[int(course_data[0])] = {
                    'id': int(course_data[0]),
                    'name': course_data[1],
                    'credit': int(course_data[2]),
                    'type': course_data[3],
                    'deptId': int(course_data[4]),
                }
            self._course_data = dict(sorted(self._course_data.items()))

            # Read department data
            for dept_data in dept_reader:
                self._dept_data.append(int(dept_data[0]))
            self._dept_data = sorted(self._dept_data)

            # Read deleted data
            for del_data in del_reader:
                self._del_data.append(int(del_data[0]))
            self._del_data = sorted(self._del_data)

    # Update data to csv file
    def updateData(self, mode, list=None):
        with open(self._course_path, mode, newline='') as File:
            if mode == 'a':
                reader = csv.writer(File)
                reader.writerow(list)
            elif mode == 'w':
                reader = csv.writer(File)
                reader.writerow(self._header_course)
                for i in self._course_data.values():
                    reader.writerow(i.values())

    # add course
    def add_course(self):
        self.readData()
        print('+ Create Course')
        while True:
            course_id = input('ID: ')
            if not course_id.isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            if int(course_id) in self._course_data.keys() or int(course_id) in self._del_data:
                print('Course ID already exists!')
                continue
            break

        course_name = input('Name: ')

        while True:
            course_credit = input('Credit: ')
            if not course_credit.isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            break

        # Select menu course type
        list_type = ['Compulsory', 'Elective']
        course_type = list_type[TerminalMenu(list_type, title='Type: ').show()]
        print('Type: ' + course_type)

        while True:
            dept_id = input('DeptId: ')
            if int(dept_id) not in self._dept_data:
                print('Department ID does not exist!')
                continue
            break
        self.updateData('a', [course_id, course_name, course_credit, course_type, dept_id])
        print('Course created successfully!')

    # search course by id
    def search_course(self, courseId):
        self.readData()
        print('+ Search Course')
        if int(courseId) not in self._course_data.keys():
            print('Search not found!')
            return
        table = PrettyTable(border=True, padding_width=1, header=True)
        table.field_names = self._header_course
        table.add_row(self._course_data[int(courseId)].values())
        print(table)

    # update course by id
    def update_course(self, courseId):
        self.readData()
        print('+ Update Course')
        if int(courseId) not in self._course_data.keys():
            print('Course ID does not exist!')
            return
        self._course_data[int(courseId)]['name'] = input('Name: ')
        while True:
            self._course_data[int(courseId)]['credit'] = input('Credit: ')
            if not self._course_data[int(courseId)]['credit'].isdigit():
                print('Invalid Input! Please enter a number.')
                continue
            break

        list_type = ['Compulsory', 'Elective']
        self._course_data[int(courseId)]['type'] = list_type[TerminalMenu(list_type, title='Type: ').show()]
        print('Type: ' + self._course_data[int(courseId)]['type'])

        while True:
            self._course_data[int(courseId)]['deptId'] = input('DeptId: ')
            if int(self._course_data[int(courseId)]['deptId']) not in self._dept_data:
                print('Department ID does not exist!')
                continue
            break
        self.updateData('w')
        print('Course updated successfully!')

    # delete course by id
    def delete_course(self, course_id):
        self.readData()
        print('+ Delete Course')
        if int(course_id) not in self._course_data.keys():
            print('Course ID does not exist!')
            return

        # Select menu confirm delete
        status = ['Yes', 'No']
        confirm = status[TerminalMenu(status, title='Are you sure you want to delete this course?', menu_highlight_style=('fg_red', "fg_red", "bold")).show()]
        if confirm == 'Yes':
            # Write deleted data to csv file
            with open(self._det_path, 'a', newline='') as fileDelete:
                deleter = csv.writer(fileDelete)
                deleter.writerow(self._course_data[int(course_id)].values())
            # Delete course data
            del self._course_data[int(course_id)]
            self.updateData('w')
            print('Course deleted successfully!')
            return
        print('Course not deleted!')

    # display all course
    def printData(self):
        self.readData()
        table = PrettyTable(border=True, padding_width=1, header=True)
        # add field name
        table.field_names = self._header_course
        # add data to table
        for i in self._course_data.values():
            table.add_row(i.values())
        print(table)

if __name__ == '__main__':
    course = Course()
    while True:
        list_menu = ['[a] Add new a course', '[b]Search a course by id', '[c]Update a course', '[d]Delete a course', '[e]Display all course', '[f]Exit']
        menu = TerminalMenu(list_menu, title='[Course Management]', menu_highlight_style=('fg_blue', "fg_blue", "bold")).show()
        if menu == 0:
            course.add_course()
        elif menu == 1:
            id = input('Enter course id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
            course.search_course(id)
        elif menu == 2:
            id = input('Enter course id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
            course.update_course(id)
        elif menu == 3:
            id = input('Enter course id: ')
            if not id.isdigit():
                print('Invalid Input! Please enter a number.')
            course.delete_course(id)
        elif menu == 4:
            course.printData()
        elif menu == 5:
            print('Program terminated!')
            break