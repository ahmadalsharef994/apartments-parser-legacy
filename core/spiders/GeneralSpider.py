from scrapy.spiders import Spider
from scrapy.selector import Selector
from scrapy.loader import ItemLoader
from scrapy.http import Request
from scrapy.http import Response
from core.parsers.attributesXMLParser import AttributesXMLParser
from core.parsers.actionsXMLParser import ActionsXMLParser
from core.items import FlexibleItem
from core.actions.dateActions import DateActions
from core.attribute.multipleValuesAttribute import MultipleValuesAttribute
from core.attribute.metaAttribute import MetaAttribute
from core.pipelines import ActionsPipeline
from core.FuzzyComparisonPipeline import FuzzyComparisonPipeline
from core.defaultAttributesPipeline import defaultAttributesPipeline
from core.email.EmailComponent import EmailComponent
from core.pipelines import DataNormalisation
from core.parsers.DataNormalisation import LoadJsonObject
from core.BuildingPipeline.Constants import Constants
from core.parsers.DataNormalisation import FurnishingXMLParser
#from scrapy import log
from datetime import *
import logging
#import MySQLdb
import time
import datetime
from pydispatch import dispatcher
from scrapy import signals

class GeneralSpider(Spider):

    name = 'GeneralSpider'
    start_urls = []
    def __init__(self, attributesXMLFilePath):
        self.masterPagesNumbers= 0
        self.detailsPagesNumbers = 0
        dispatcher.connect(self.spider_closed, signals.spider_closed)
        dispatcher.connect(self.spider_error, signals.spider_error)
        self.attributesXMLFilePath = attributesXMLFilePath
        self.attributesXMLParser = AttributesXMLParser(self.attributesXMLFilePath)
        self.actionsXMLParser = ActionsXMLParser(self.attributesXMLFilePath)
        ActionsPipeline.setActionsXMLParser(self.actionsXMLParser)
        self.dataNormalisation ={}
        self.dataNormalisation[Constants.payment_type]  = LoadJsonObject("General_Spider/mapping/paymentType.json")
        self.dataNormalisation[Constants.type]  = LoadJsonObject('General_Spider/mapping/propertyType.json')
        self.dataNormalisation[Constants.furnished] = LoadJsonObject('General_Spider/mapping/furnishings.json')
        self.dataNormalisation[Constants.area] = LoadJsonObject('General_Spider/mapping/Area.json')
        DataNormalisation.setMapping(self.dataNormalisation)
        defaultAttributesPipeline.setDefaultAttributeParser(self.attributesXMLParser.getTemplateValues(self.attributesXMLParser.getValueOfTag('TemplateAttributes')))
        FuzzyComparisonPipeline.setFuzzyModules(self.attributesXMLParser.loadFuzzySettings())
        self.domain = self.attributesXMLParser.getValueOfTag('domain')
        self.logFile = self.attributesXMLParser.getValueOfTag('LogFile')
        logging.basicConfig(filename=self.logFile, level=logging.INFO)
        self.name = self.attributesXMLParser.getValueOfTag('SpiderName')
        from scrapy.utils.project import get_project_settings
        myS = get_project_settings()
        self.myLogger = logging.getLogger(self.name)
        # self.myLogger.setLevel(10)
        #myS.set(myS, 'JOBDIR', "SeenFolders/Apartment/Rent/seen_apartment_sale_ezestatedubai")
        self.myLogger.info('The spider {0} with xml file = {2} starts working on {1}'.format(self.name,  datetime.datetime.now(), attributesXMLFilePath))
        self.startTime=datetime.datetime.now()
        self.start_urls=self.attributesXMLParser.getStartUrls()
        self.dateAttributePlace = self.attributesXMLParser.getValueOfTag('DateAttribute/Place')
        self.dateAttributeName = self.attributesXMLParser.getValueOfTag('DateAttribute/Name')
        if (self.dateAttributePlace=="DetailsPage" or self.dateAttributePlace=="MasterPage"):
            self.FirstDateString=self.attributesXMLParser.getValueOfTag('FirstDate')
            #tomorrow = datetime.date.today() + datetime.timedelta(days=1)
            #self.FirstDateString = str(tomorrow.strftime("%d %b %Y"))
            self.LastDateString=self.attributesXMLParser.getValueOfTag('LastDate')
            #self.LastDateString = str(time.strftime("%d %b %Y"))
            self.dateFunction = self.attributesXMLParser.getValueOfTag('DateAttribute/DateFunction')
        self.mastersAttributes=self.attributesXMLParser.getMastersAttributes()
        self.linkAttributeName = 'ad_link'
        self.detailsAttributes=self.attributesXMLParser.getDetailsAttributes()
        ActionsPipeline.setDefaultValues(self.attributesXMLParser.getDefaultValues(self.detailsAttributes));
        self.containers=self.attributesXMLParser.getMasterContainers()
        self.Category= self.attributesXMLParser.getValueOfTag('Category')
        self.Source = self.attributesXMLParser.getValueOfTag('Source')
        self.Action = self.attributesXMLParser.getValueOfTag('Action')
        self.numberOfPagesForNoDateWebsites = 0
        self.myLogger.debug('the start url is {0}'.format(self.start_urls))
        self.myLogger.debug('the finish of the init')
        self.maxMasterPageNumber = self.attributesXMLParser.getMaxMasterPageNumber()
        self.headers = self.attributesXMLParser.getHeaders()
        #self.start_requests()


    def start_requests(self):
        self.myLogger.debug('in start requests method')
        for url in self.start_urls:
            yield Request(url, headers=self.headers, callback=self.parse, dont_filter=True)


    def parse(self,response):
            self.myLogger.debug('we are in the parse method')
            self.masterPagesNumbers+=1
            sel = Selector(response)
            nextPage = self.attributesXMLParser.getNextPage(sel, response.url)
            #import pdb; pdb.set_trace()
            if self.dateAttributePlace == "MasterPage":
                for container in self.containers:
                    containerSelector = sel.xpath(container)
                    stop = False 
                    for oneAd in containerSelector:
                        meta = dict()
                        flexibleItem = FlexibleItem()
                        flexibleItem['didExceptionHappenDuringExtractingItems'] = False
                        for key in self.mastersAttributes:
                            meta[key] = self.mastersAttributes[key].getResult(oneAd, response,flexibleItem )
                        meta[self.dateAttributeName] = self.attributesXMLParser.getDateValue(meta[self.dateAttributeName])
                        if (self.dateFunction == "DayFirst"):
                            meta[self.dateAttributeName] = DateActions.standardDateDayFirst(meta[self.dateAttributeName])
                        elif (self.dateFunction == "MonthFirst"):
                            meta[self.dateAttributeName] = DateActions.standardDateMonthFirst(meta[self.dateAttributeName])
                        elif (self.dateFunction == "YearFirst"):
                            meta[self.dateAttributeName] = DateActions.standardDateYearFirst(meta[self.dateAttributeName])
                        meta['flexibleItem'] = flexibleItem
                        if ((DateActions.adDateInsideRange(self.FirstDateString, self.LastDateString, meta[self.dateAttributeName])) ):
                            meta[self.linkAttributeName] =  self.attributesXMLParser.getPageLink(meta[self.linkAttributeName], sel)
                            yield Request(meta[self.linkAttributeName], meta = meta, callback=self.parseDetailsPage)
                        else:
                            stop = True
                    if stop == False and nextPage != None:
                        yield Request(nextPage, callback = self.parse, dont_filter=True)
            elif self.dateAttributePlace == "DetailsPage":
                for container in self.containers:
                    containerSelector = sel.xpath(container)
                    numberOfAds = 0
                    for oneAd in containerSelector:
                        numberOfAds +=1
                        meta = dict()
                        flexibleItem = FlexibleItem()
                        flexibleItem['didExceptionHappenDuringExtractingItems'] = False
                        for key in self.mastersAttributes:
                            meta[key] = self.mastersAttributes[key].getResult(oneAd, response, flexibleItem)
                        if numberOfAds == len(containerSelector):
                            meta['isLast'] = "True"
                        else:
                            meta['isLast'] = "False"
                        meta['flexibleItem'] = flexibleItem
                        if numberOfAds == len(containerSelector):
                            meta['nextPage'] = nextPage
                        meta[self.linkAttributeName] = self.attributesXMLParser.getPageLink(meta[self.linkAttributeName], sel)
                        yield Request(meta[self.linkAttributeName], meta = meta, callback = self.parseDetailsPage)
            elif self.dateAttributePlace=="No Place":
                print("the number of item is {0}".format(len(self.containers)))
                for container in self.containers:
                    containerSelector = sel.xpath(container)
                    for oneAd in containerSelector:
                        meta = dict()
                        flexibleItem = FlexibleItem()
                        flexibleItem['didExceptionHappenDuringExtractingItems'] = False
                        for key in self.mastersAttributes:
                            meta[key] = self.mastersAttributes[key].getResult(oneAd, response, flexibleItem)
                        meta[self.linkAttributeName] = self.attributesXMLParser.getPageLink(meta[self.linkAttributeName], sel)
                        meta['flexibleItem'] = flexibleItem
                        yield Request(meta[self.linkAttributeName], meta = meta, callback = self.parseDetailsPage)
                    self.numberOfPagesForNoDateWebsites+=1
                    if (self.numberOfPagesForNoDateWebsites <= self.maxMasterPageNumber):
                        yield Request(nextPage, callback = self.parse, dont_filter=True)
    
    def parseDetailsPage(self, response):
        #import pdb; pdb.set_trace()
        self.detailsPagesNumbers+=1
        sel = Selector(response)
        flexibleItem = response.meta['flexibleItem']
        if self.dateAttributePlace == "MasterPage":
            for attribute in self.detailsAttributes:
                flexibleItem[attribute] = self.detailsAttributes[attribute].getResult(sel, response, flexibleItem)
            flexibleItem['source'] = self.Source
            flexibleItem['action'] = self.Action
            flexibleItem['category'] = self.Category
            yield flexibleItem
        elif self.dateAttributePlace == "DetailsPage":
            for attribute in self.detailsAttributes:
                flexibleItem[attribute] = self.detailsAttributes[attribute].getResult(sel, response, flexibleItem)
            flexibleItem['source'] = self.Source
            flexibleItem['action'] = self.Action
            flexibleItem['category'] = self.Category
            flexibleItem[self.dateAttributeName] = self.attributesXMLParser.getDateValue(flexibleItem[self.dateAttributeName])
            if (self.dateFunction == "DayFirst"):
                flexibleItem[self.dateAttributeName] = DateActions.standardDateDayFirst(flexibleItem[self.dateAttributeName])
            elif (self.dateFunction == "MonthFirst"):
                flexibleItem[self.dateAttributeName] = DateActions.standardDateMonthFirst(flexibleItem[self.dateAttributeName])
            elif (self.dateFunction == "YearFirst"):
                flexibleItem[self.dateAttributeName] = DateActions.standardDateYearFirst(flexibleItem[self.dateAttributeName])
            isCorrectDate= True
            try:
                #it was item instead of flexibleItem
                isCorrectDate = DateActions.adDateInsideRange(self.FirstDateString, self.LastDateString, flexibleItem[self.dateAttributeName])
            except:
                isCorrectDate = True
            if (isCorrectDate):
                print ("the date is inside the range")
                yield flexibleItem
                if ((response.meta.get('isLast') is not None) and (response.meta.get('isLast') == "True")):
                    yield Request(url = response.meta.get('nextPage'), callback = self.parse, dont_filter=True)
            else:
                print ("the date is NOT insde the range")
        elif self.dateAttributePlace=="No Place":
            for attribute in self.detailsAttributes:
                flexibleItem[attribute] = self.detailsAttributes[attribute].getResult(sel, response, flexibleItem)
            flexibleItem['source'] = self.Source
            flexibleItem['action'] = self.Action
            flexibleItem['category'] = self.Category
            today = datetime.date.today()
            flexibleItem[self.dateAttributeName] = str(today.strftime("%Y-%m-%d"))
            yield flexibleItem

    def spider_error(self, failure, response, spider):
        errorMessage = "Error on {0}, traceback: {1}".format(response.url, failure.getTraceback())
        print(errorMessage)
        from time import gmtime, strftime
        EmailComponent.sendEmail(errorMessage, "Error {0}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime())))

    def spider_closed(self, spider):
        print(('The number of master pages in the spider {1} are {0}'.format(self.masterPagesNumbers, self.attributesXMLFilePath)))
        print(('The number of details pages in the spider {1} are {0}'.format(self.detailsPagesNumbers, self.attributesXMLFilePath)))
        print(('The spider {0} with xml {2} finished working on {1}'.format(self.name, str(datetime.datetime.now()), self.attributesXMLFilePath)))
        '''
        try:
            self.conn = MySQLdb.connect(user='william', passwd='Password@01', db='scrapy', host='localhost', charset="utf8", use_unicode=True)
            self.cursor = self.conn.cursor()
            self.cursor.execute("""INSERT INTO log_table (spider_name, master_numbers, details_numbers, start_time, end_time) VALUES (%s, %s, %s, %s, %s)""", (self.name, int(self.masterPagesNumbers), int(self.detailsPagesNumbers), str(self.startTime), str(datetime.datetime.now())))
            self.conn.commit()
        except MySQLdb.Error, e:
            print "Error %d: %s" % (e.args[0], e.args[1])
            errorMessage = "Error on {0} : {1}".format(e.args[0], e.args[1])
            EmailComponent.sendEmail(errorMessage, "MySQL Exception 1")
        except Exception as ee:
            errorMessage2 = "Error on {0}".format(str(ee))
            print errorMessage2
            EmailComponent.sendEmail(errorMessage2, "MySQL Exception 2")
        '''

