from dateutil.parser import *
from datetime import *
import re

class DateActions(object):
    @staticmethod
    def solve(s): #This function is to remove the th, st, nd, rd from the date
        return re.sub(r'(\d)(st|nd|rd|th)', r'\1', s)
    @staticmethod
    def standardDateDayFirst(value): #This function return the value from dates that have day as the first value for example, 3 january 2013, or 3 2014 janauray
        return str(parse(value, dayfirst=True).date())
    @staticmethod
    def standardDateYearFirst(value):#This function returns the value from dates that have year as the first value for exmaple, 2014 janauray 3, or 2013 3 janauary
        return str(parse(value, yearfirst=True).date())
    @staticmethod
    def standardDateMonthFirst(value): #This function returns the value from dates that have month as the first value for example january 2014 3 or january 3 2013
        return str(parse(value, dayfirst=False, yearfirst=False).date())
    @staticmethod
    def adDateInsideRange(FirstDateString, LastDateString, DateString): #This function check wether the entered date is between the first and last date
        FirstDate = datetime.strptime(DateActions.solve(FirstDateString), "%d %b %Y").date()
        LastDate = datetime.strptime(DateActions.solve(LastDateString), "%d %b %Y").date()
        Date = datetime.strptime(DateString, "%Y-%m-%d").date()
        if FirstDate >= Date >= LastDate:
            return True 
        else:
            return False