import csv
import datetime as dt
import os, sys
from dateutil.parser import parse
from ShiftClass import Employee, Workday


year_number = "2019"
end_words = ['EER EMPLOYEES', 'EERC EMPLOYEES'] #word that comes after the last person of the day. It changes >.>

datetimes_of_week = []
Workyear = [] #list of Workweeks

searched_employees = [] 

with open('employees.csv') as csv_file:
    csv_reader = csv.reader(csv_file, delimiter=',')
    for row in csv_reader:
        searched_employees.append(row[0].upper())

for file in os.listdir(os.path.realpath("")+"/csv2019"):
    if file.endswith(".csv"):
        print(f"Running for {file}")
        
        Workweek = [] #list of Workdays
        with open(os.path.realpath("")+"/csv2019/"+file) as csv_file:
            csv_reader = csv.reader(csv_file, delimiter=',')
            csv_file.seek(0) #resets to top of file
            avcol = -1
            avrow = -1
            for rownum, row in enumerate(csv_reader):
                try:
                    avcol = row.index("Availability") #colnum gets daily availability column
                    avrow = rownum #sets the col and row number of availability
                    break
                except:
                    pass
            
            print("ROW: "+str(avrow))
            print("COL: "+str(avcol))
            if(avcol == -1 or avrow == -1): #safeguard against an incorrectly formatted input
                exit(-1)

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
                for person in searched_employees:
                    day.employee_list.append(Employee(person)) #adds the employees to look for to the list in Workday

            #set the hours for each person per day
            for day in Workweek:
                startSearch = False
                csv_file.seek(0) 
                for rownum, row in enumerate(csv_reader):
                    csvname = row[0].upper()
                    if startSearch and csvname in end_words: #hit the end of the employee list, go onto next day
                        break

                    try:
                        possible_date = parse(csvname).replace(year = int(year_number))            
                        if day.date == possible_date: #we found the start of the next day's schedule
                            startSearch = True
                    except: #csvname is not a date
                        pass

                    for person in day.employee_list:
                        if person.name == csvname: #if a person in employee_list matches, set their daily hours
                            person.availability_today = row[avcol]
                pass
            
            for day in Workweek: #print all days and employee hours
                print(f"\n{day.date}:")
                for employee in day.employee_list:
                    print(f"{employee.name} : {employee.availability_today}")
        Workyear.append(Workweek)

Workyear.sort(key=lambda x: x[0].date) #sorts the list of Workweeks into chronological order

searchname = "John Luetzelschwab".upper()

#now for the output
# with open(searchname+'.csv', mode='w') as csv_file:
#     employee_writer = csv.writer(csv_file, delimiter=',')
#     for week in Workyear:
#         for day in week:
#             for person in day.employee_list:
#                 if person.name == searchname:
#                     employee_writer.writerow([(day.date).strftime("%Y/%m/%d"),person.availability_today])
with open(searchname+'.csv', mode='w') as csv_file:
    employee_writer = csv.writer(csv_file, delimiter=',')

    dtweeks = []
    for week in Workyear:
        for day in week:
            dtweeks.append((day.date).strftime("%Y/%m/%d")) #first row is all dates
    employee_writer.writerow(dtweeks)

    for week in Workyear:
        for day in week:
            for person in day.employee_list:
                    


#finds the searchname's highest input availability

# maxhours = 0
# maxdate = dt.datetime.now()
# searchname = "Shawn Victor".upper() #note - needs to be in temp_employees for now
# for week in Workyear:
#     weekhours = 0
#     for day in week:
#         for john in day.employee_list:
#             if john.name == searchname:
#                 weekhours += float(john.availability_today)
#     if weekhours != 0.0:
#         print(f"Week of {week[0].date} : {weekhours} hours put in ")
#     if weekhours > maxhours:
#         maxhours = weekhours
#         maxdate = week[0].date
# print(f"The most availability for {searchname} was {maxhours} hours the week of {maxdate}")


