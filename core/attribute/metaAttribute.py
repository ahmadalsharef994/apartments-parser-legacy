#This class is to get the data which has been sent from master page to details page using meta
from core.attribute.genericAttribute import GenericAttribute

class MetaAttribute(GenericAttribute):
    def __init__(self, name, defaultValue='NA'):
        self.name = name
        self.defaultValue = defaultValue

    def getResult(self, sel, response, flexibleItem):#sel is the xpath container, response is the dom of the page
        return response.meta[self.name]