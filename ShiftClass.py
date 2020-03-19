import datetime as dt
from datetime import timedelta

#Structured as 
# List Workweek (List of Workdays)
# contains list of Employees
# with each Employee containing the name and hours worked that day


# #shift class
# class calShift:
#     def __init__(self, name, start, end):
#         self.name = name
#         self.start = start
#         self.end = end
#     def __str__(self):
#         return(f'{self.name}: {(self.start).time()}-{(self.end).time()}')

#employee weekly class
class Employee:
    def __init__(self, name):
        self.name = name
        self.availability_today = 0

class Workday:
    def __init__(self, date):
        self.date = date
        self.employee_list = []
    
 