To generate a csv with each employee's daily availability:
    -Create a folder with all the weekly schedules to be checked in .csv format (see 'converting to csv' if your have .xlsx from Google Drive)
    -Create a .csv file 'employees.csv' containing the employees to check, formatted with one name per row in the first column
    -Run the command 'python3 analyze.py input_folder year_number output_filename'

To convert a folder of .xlsx files to .csv:
    -Create a folder containing all the .xlsx files you wish to convert
    -Move the program 'convert.py' into the created fodler
    -Run the command 'python3 convert.py'
    -The error potential invalid date format is usually OK - just check your output!