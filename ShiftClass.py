import datetime as dt
from datetime import timedelta

#shift class
class calShift:
    def __init__(self, name, start, end):
        self.name = name
        self.start = start
        self.end = end
    def __str__(self):
        return(f'{self.name}: {(self.start).time()}-{(self.end).time()}')

#employee weekly class
class Employee:
    def __init__(self, name, weekstart, weekend):
        self.name = name
        self.weekstart = weekstart
        self.weekend = weekend
