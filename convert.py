import os
from xlsx2csv import Xlsx2csv
for file in os.listdir():
	if file.endswith(".xlsx"):
		Xlsx2csv(file, dateformat="%m/%d/%Y",outputencoding="utf-8").convert(file[:-5] + ".csv")