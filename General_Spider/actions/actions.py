from __builtin__ import staticmethod

from dateutil.parser import *
import re
from datetime import *
import datetime
import json
class Actions():
    @staticmethod
    def changeToInteger(value): #This function is to change the string input to an integer value
        return int(value)
    @staticmethod
    def changeToFloat(value): #This function is to change the string input to a float value
        return float(value.replace(',',''))
    @staticmethod
    def standardDateDayFirst(value): #This function is to get the standard date from a given date, which its format starts with the day
        return str(parse(value, dayfirst=True).date())
    def standardDateYearFirst(value):#This funtion is to get the standard date from a given date, which its format starts with the year
        return str(parse(value, yearfirst=True).date()) 
    def standardDateMonthFirst(value):#This function is to get the standard date from a given date, which its format starts with the month
        return str(parse(value, dayfirst=False, yearfirst=False).date())
    @staticmethod
    def nextPageForAutotraderuaeCars(value): #This function is to get the next page for auto trader website
        intValue = int(value)
        intValue = (intValue -1)*10
        return "http://www.autotraderuae.com/cars/?page="+str(intValue)+"&view=&sort_by=edit_dt-desc&limit=10&car_make=&car_version=&color=&car_model=&makeYear=&city="
    @staticmethod
    def extractNumbersFromStringForDubaiMoto(value):
        return [i.replace(' ','') for i in re.findall(r'\d+(?:[\s,.]\d+)*', value)][0]
    @staticmethod
    def extractNumbersFromString(value): #This function is to get the numbers froma string
        return re.search('(\d+(?:[.,]\d*)*)', value).group(1)
    @staticmethod
    def changeEncodingToASCII(value): #This function is to get the encoding ascii value of a string
        return value.encode('ascii')
    @staticmethod
    def dubizzleGetLongitude(value): #This function is to get the longitude value from dubizzle website
        return re.search('GOOGLE_MAPS_LONGITUDE:\s*(\d+\.\d+),', value).group(1)
    @staticmethod
    def dubizzleGetLatitude(value): #This function is to get the latitude value from dubizzle website
        return re.search('GOOGLE_MAPS_LATITUDE:\s*(\d+\.\d+)', value).group(1)
    @staticmethod
    def propertyFinderGetLongitude(value): #This function is to get the longitude value from property finder website
        return re.search('gmap_longitude/(\d+\.\d+)', value).group(1)
    @staticmethod
    def propertyFinderGetLatitude(value): #This function is to get the latitude value from property finder website
        return re.search('gmap_latitude/(\d+\.\d+)', value).group(1)
    @staticmethod
    def justpropertyCorrectDate(value): #This function is to get the date value from just property website
        return re.search('Last Update:\s*(.*)', value).group(1)
    @staticmethod
    def yallamotorCorrectDate(value):
        try:
            value = re.search('Posted on \s*(.*)',value).group(1)
            return value.replace(",", "")
        except:
            return str(datetime.today().strftime("%d %b %Y"))
    @staticmethod
    def justpropertyDateAction(value):
        return value[:10]
    @staticmethod
    def dubizzleExtractCountryFromLocation(value):
        return value.split(">")[0]
    @staticmethod
    def dubizzleExtractCityFromLocation(value):
        return value.split(">")[1]
    @staticmethod
    def justRentalGetCity(x):
        return x.split(',')[len(x.split(','))-1]
    @staticmethod
    def drivearabiaDateExtracting(x):
        return 
    @staticmethod
    def extractCurrentFromStringForAutosouk(value):
        return re.search('\S*', value).group(0)
    @staticmethod
    def autosoukExtratModelMake(value):
        modelMakeYear = value.split("|")[1] #the result is like this Mitsubishi Galant AED 10,500
        return modelMakeYear.split('AED')[0]
    @staticmethod
    def propertyOnlineExtractReraFromDescription(value):
        for oneValue in value:
            if (oneValue.startswith('RERA')):
                return oneValue.split(':')[1]
    @staticmethod
    def getCordinatesFromAddress(value):
        import urllib2
        return urllib2.urlopen("https://maps.googleapis.com/maps/api/geocode/json?address={0}&key=AIzaSyCQ6D6PCyOzoit9qadoJln4WHbInirtfJs".format(value)).read()
    @staticmethod
    def getDatePropertyFinder(value):
        if value.strip() == "":
            value = str(datetime.date.today().strftime("%Y-%m-%d"))
            print ("The date was empty and now it is {0}".format(value))
            return value
        print("value inside = {0}".format(value))
        value = re.search('Last update: \s*(.*)',value).group(1)
        return value
    @staticmethod
    def propertyOnlineGetCityFromLocation(value):
        return value.split(",")[0]
    @staticmethod
    def propertyOnlineGetAreaFromLocation(value):
        return value.split(",")[1]
    @staticmethod
    def propertyOnlineGetBuildingFromLocation(value):
        return value.split(",")[2]
    @staticmethod
    def propertyFinderGetArea(value):
        return value.split('for rent in')[1]
    @staticmethod
    def justRentalGetBuilding(value):
        return value.split(',')[0]
    @staticmethod
    def justRentalGetArea(value):
        return value.split(',')[1]
    @staticmethod
    def propsearchextractlocation(value):
        return value.split('Location Map')[0]
    @staticmethod
    def checkIfStudioBedroom(value):
        if str(value).lower().strip() == "studio":
            return 0
        else:
            return value
    @staticmethod
    def checkIfStudioBedroomOrNumberSpecialCaseForPropSearch(value):
        if str(value).lower().strip() == "studio":
            return 0
        value = re.search('(\d+(?:[.,]\d*)*)', value).group(1)
        return int(value)
    @staticmethod
    def propsearchExtractTypeFromTitle(value):
        if re.search("villa", value, re.IGNORECASE):
            return "villa"
        elif re.search("apartment", value, re.IGNORECASE):
            return "apartment"
        elif re.search("studio", value, re.IGNORECASE):
            return "apartment"
        else:
            return "NA"

    @staticmethod
    def propsearchExtractAreaFromTitle(value):
        areaAndBuilding = re.match(".* Rent In (.*)" , value).group(1)
        return areaAndBuilding.split(',')[1]

    @staticmethod
    def propsearchExtractBuildingFromTitle(value):
        areaAndBuilding = re.match(".* Rent In (.*)", value).group(1)
        return areaAndBuilding.split(',')[0]
    @staticmethod
    def propsearchExtractPaymentType(value):
        return re.match("(.*) Rent", value).group(1)
    @staticmethod
    def yzepropertyExtractType(value):
        return re.match("Property type: (.*)", value).group(1)
    @staticmethod
    def yzerpropertyExtractPhone(value):
        d = json.loads(value)
        return d["phone"]
    @staticmethod
    def changeToSmallLetters(value):
        value = value.strip()
        return value.lower()
    @staticmethod
    def dubizzleExtractType(value):
        return re.match("(.*) for Rent", value).group(1)
    @staticmethod
    def cleanCity(value):
        value = value.strip()
        return value.lower()
    @staticmethod
    def CorrectLink(value):
        import urlparse
        url = urlparse.urlparse(value).geturl()
        fp = urlparse.urljoin(url, urlparse.urlparse(url).path)
        return fp
    @staticmethod
    def removeNonASCII(value):
        value = value.encode('ascii',errors='ignore')

    @staticmethod
    def dubizzleExtractTypeForSale(value):
        return re.match("(.*) for Sale", value).group(1)

    @staticmethod
    def propsearchExtractAreaFromTitleForSale(value):
        areaAndBuilding = re.match(".* Sale In (.*), (.*)", value)
        return areaAndBuilding.group(2)

    @staticmethod
    def propsearchExtractBuildingFromTitleForSale(value):
        areaAndBuilding = re.match(".* Sale In (.*), (.*)", value)
        return areaAndBuilding.group(1)

    @staticmethod
    def propertyFinderGetAreaForSale(value):
        return value.split('for sale in')[1]

    @staticmethod
    def justPropertyPaymentType(value):
        return value.split('per')[-1]
    @staticmethod
    def ezestateGetLongitude(value):
        isExist = value.find("map_exist = true")
        if isExist != "-1":
            coordinate = re.findall('(\d+\.\d+)', value)
            return coordinate[1]

    @staticmethod
    def ezestateGetLatitude(value):
        isExist = value.find("map_exist = true")
        if isExist != "-1":
            coordinate = re.findall('(\d+\.\d+)', value)
            return coordinate[0]
    @staticmethod
    def extractBuildingForYzerproperty(value):
        if len(value)> 2:
            last = value[-1]
            return Actions.changeToSmallLetters(last)
        else:
            return "na"

    @staticmethod
    def CorrectLinkYzerProperty(value):
        import urlparse
        url = urlparse.urlparse(value).geturl()
        fp = urlparse.urljoin(url, urlparse.urlparse(url).path)
        fp  = ''.join([i if ord(i) < 128 else '' for i in fp])
        return fp

    @staticmethod
    def convertListToString(value):
        return ','.join(value)

    @staticmethod
    def extractDateYzerProperty(value):
        updateDate = value.split(',')
        result = re.search('updated \s*(.*)', value).group(1)
        return result