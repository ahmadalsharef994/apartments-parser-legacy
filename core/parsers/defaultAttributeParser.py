from lxml import etree
from pprint import pprint
class defaultAttributeParser():
    def __init__(self, defaultAttributeFile):
        self.doc=etree.parse(defaultAttributeFile)

    def getDefaultAttributes(self):
        attributesDict = list()
        attributes = self.doc.findall('Attribute')
        for attribute in attributes:
            attributesDict.append(attribute.find('name').text)
        return attributesDict

#a = defaultAttributeParser('Apartments.xml')
#pprint(a.getDefaultAttributes())