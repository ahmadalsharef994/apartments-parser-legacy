#This class is to get the value of attributes using xpath
from core.attribute.genericAttribute import GenericAttribute

class SelectorAtribute(GenericAttribute, BaseException):
    def __init__(self, xpath, name, defaultValue):
        self.xpath = xpath
        self.defaultValue = defaultValue
        self.name = name

    def getResult(self, oneAd, response, flexibleItem): #oneAdd is the xpath container, response is the dom of the page
        try:
            #import pdb;pdb.set_trace()
            return oneAd.xpath(self.xpath).extract()[0].encode('utf-8', 'ignore')
        except:
            flexibleItem['didExceptionHappenDuringExtractingItems'] = True
            return self.defaultValue