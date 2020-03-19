import csv
import datetime as dt
from dateutil.parser import parse
from ShiftClass import Employee, Workday


input_file = "21 Oct - Oct 25.csv"
year_number = "2019"

datetimes_of_week = []
Workweek = []
temp_employees = ['Adrian Cantu','Alec Schultz','John Luetzelschwab','Zachary Keller']

with open(input_file) as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    csv_file.seek(0) #resets to top of file
    avcol = -1
    avrow = -1
    for rownum, row in enumerate(csv_reader):
        try:
            colnum = row.index("Availability") #colnum gets daily availability column
            avrow = rownum #sets the col and row number of availability
            break
        except:
            pass
    
    print("ROW: "+str(avrow))
    print("COL: "+str(colnum))

    csv_file.seek(0) 

    #get all the dates of the week's schedule
    for row in csv_reader:
        try:
            if year_number in row[0]:
                Workweek.append(Workday((parse(row[0]).replace(year = int(year_number))))) #adds a Workday to the Workweek

        except:
            print("UwU")

    csv_file.seek(0) 
    
    for day in Workweek:
        for person in temp_employees:
            day.employee_list.append(Employee(person)) #adds the employees to look for to the list in Workday

    #set the hours for each person per day
    for day in Workweek:
        startSearch = False
        csv_file.seek(0) 
        for rownum, row in enumerate(csv_reader):
            if startSearch and row[0] == 'EER Employees': #hit the end of the employee list, go onto next day
                break

            try:
                possible_date = parse(row[0]).replace(year = int(year_number))            
                if day.date == possible_date: #we found the start of the next day's schedule
                    startSearch = True
            except: #row[0] is not a date
                pass

            for person in day.employee_list:
                if person.name == row[0]: #if a person in employee_list matches, set their daily hours
                    person.availability_today = row[29]
        pass
    
    for day in Workweek: #print all days and employee hours
        print(f"\n{day.date}:")
        for employee in day.employee_list:
            print(f"{employee.name} : {employee.availability_today}")



