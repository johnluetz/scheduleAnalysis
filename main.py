import csv
import datetime as dt
from dateutil.parser import parse


input_file = "3 Feb - Feb 8.csv"

months_of_year = ['January', 'February', 'March', 'April', 'May', 'June', 'July', 'August', 'September', 'October', 'November', 'December']
datetimes_of_week = []

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
    list_dates = []
    for row in csv_reader:
        try:
            if any(month in row[0] for month in months_of_year):
                datetimes_of_week.append((parse(row[0]).replace(year = 2019)))
        except:
            print("UwU")

    csv_file.seek(0) 
    
    for rownum, row in enumerate(csv_reader):        
        if rownum > avrow:
            if row[0] == "EER Employees": #end of employee list
                break
            print(f"{row[0]} : {row[colnum]}")
            
