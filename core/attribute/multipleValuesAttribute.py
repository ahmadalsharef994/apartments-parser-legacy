#This class is to get the value of multi value attribute for example, the image links attribute could have many images, so this class will take care of that
from core.attribute.genericAttribute import GenericAttribute

class MultipleValuesAttribute(GenericAttribute):
    def __init__(self, name, xpath, defaultValue='NA'):
        self.name = name
        self.xpath = xpath
        self.defaultValue = defaultValue

    def getResult(self, oneAd, response, flexibleItem):#oneAdd is the xpath container, response is the dom of the page
        results = list()
        objects = oneAd.xpath(self.xpath).extract()
        return objects
