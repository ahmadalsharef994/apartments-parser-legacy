
from General_Spider.attribute.genericAttribute import GenericAttribute

class ResponseAttribute(GenericAttribute):
    def __init__(self, name, defaultValue='NA'):
        self.name = name
        self.defaultValue = defaultValue
    
    def getResult(self, oneAd, response, flexibleItem):#oneAdd is the xpath container, response is the dom of the page
        try:
            return oneAd.xpath(self.xpath).extract()[0].encode('utf-8')
        except:
            flexibleItem['didExceptionHappenDuringExtractingItems'] = True
            return self.defaultValue