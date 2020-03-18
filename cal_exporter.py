from collections import OrderedDict
import datetime as dt 
from dateutil.parser import parse
from datetime import timedelta
import csv
import re
from ShiftClass import calShift
from quickstart import createEvent
days_of_week = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
datetimes_of_week = []
shifts_export = []
workable_hours = []


#given a date and a string list of times, return a datetime list with that date plus the given times
def generateDatetimeList(date, times):
    daily_datetimes = []
    beforeNoon = True
    for time in times:
        if beforeNoon:
            temptime = (parse(time))
            actual = dt.datetime.combine(date,temptime.time())
            daily_datetimes.append(actual)
        if time == '12:30':
            beforeNoon = False
        elif not beforeNoon:
            temptime = (parse(time)) + timedelta(hours=12) #add 12 hours for afternoon!
            actual = dt.datetime.combine(date,temptime.time())
            daily_datetimes.append(actual)
    
    return daily_datetimes

#given a dict of shift strings and work dates, combine the two and export an array of shift objects
def shiftSupplier(shiftsdict, weekdates):
    shiftslist = []
    for todayshifts, validshifts in zip(shiftsdict, weekdates.items()):
        working = False
        start = dt.datetime.now()
        end = dt.datetime.now()
        name = "NONE"
        for strshift, dtshift in zip (todayshifts, validshifts[1]): #where the shifts are divided up
            if not working and strshift != '': #started working after not
                name = strshift
                start = dtshift
                working = True

            elif working and strshift != name: #finished a shift, may have started a new one OR stopped working
                    end = dtshift
                    worked_hours = calShift(name, start, end)
                    shiftslist.append(worked_hours)
                    if strshift == '': #off to another pasture...
                        working = False
                    else: #you're still working, start another shift!
                        start = dtshift
                        name = strshift
                        working = True
        #you can end the day still working, finalize that last shift!
        if working:
            end = (validshifts[1])[len(validshifts[1])-1] + timedelta(minutes=30)
            worked_hours = calShift(name, start, end)
            shiftslist.append(worked_hours)


        #debug only
        #print(f'DATE {validshifts[0].date()} OVER!')

    return shiftslist #list of shift objects

#finds the shifts and returns a list of shifts
def getShifts(employee_name, input_file):
    global workable_hours
    employee_shifts = []

    dictshifts = dict.fromkeys(datetimes_of_week, None) #dictafy the data
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        csv_file.seek(0) #resets to top of file
        for row in csv_reader:
            if row[0] == employee_name:
                shift_cleaner = row[:len(workable_hours)+1]
                shift_cleaner = [shift.upper() for shift in shift_cleaner]
                shift_cleaner = [re.sub(r"\b%s\b" % 'A', '', shift) for shift in shift_cleaner]
                shift_cleaner = [re.sub(r"\b%s\b" % 'F', '', shift) for shift in shift_cleaner]
                del shift_cleaner[0]
                employee_shifts.append(shift_cleaner)

        
        for dayshifts in employee_shifts: #where dayshift is a list of the day's shifts
            print(*dayshifts)
    return employee_shifts


def convert(person, person_email, input_file):
    
    global workable_hours

    print("Running for "+person+"...")
    with open(input_file) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0

        #find what dates are on the schedule, convert to datetime (just YYYY/MM/DD) and save in datetimes_of_week list
        list_dates = []
        for row in csv_reader:
            try:
                if any(day in row[0] for day in days_of_week):
                    datetimes_of_week.append(parse(row[0]))
            except:
                print("UwU")

        dictdates = OrderedDict.fromkeys(datetimes_of_week, None) #dictafy the data
        
        #find all times listed on the schedule, save in workable_hours list
        csv_file.seek(0) #resets to top of file
        for row in csv_reader: 
            workable_hours = row
            break
        
        workable_hours = list(filter(None, workable_hours))
        #workable_hours.remove(' ') #should have a clean list of times from (usually) 8am - 8pm

        #assign each date in dictdates a list of datetime objects with their corresponding dates AND times
        for day in dictdates:
            dictdates[day] = generateDatetimeList(day, workable_hours)

    weekshifts = getShifts(person, input_file)
    shift_export = shiftSupplier(weekshifts, dictdates)

    #write to output
    if len(shift_export) != 0:
        for shift in shift_export:
            createEvent(shift.name,person_email,shift.start,shift.end)
