import json
import uuid
import re
class defaultAttributesPipeline(object):
    def process_item(self, item, spider):
        for attribute in defaultAttributesPipeline.defaultAttributesParser:
            #if not item.has_key(attribute):
            if not attribute in item:
                item = self.addAttributeToTheItem(attribute, item)
        return item

    def addAttributeToTheItem(self, attributeName, item):
        item[attributeName] = "does_not_exit_in_this_website"
        return item

    @staticmethod
    def setDefaultAttributeParser(defaultAttributesParser):
        defaultAttributesPipeline.defaultAttributesParser = defaultAttributesParser

#from parsers.defaultAttributeParser import defaultAttributeParser
#a = defaultAttributeParser('parsers/Apartments.xml')
#defaultAttributesPipeline.setDefaultAttributeParser(a.getDefaultAttributes())
#item = dict()
#item['william'] = 'william'
#item['city'] = 'city2'
#b = defaultAttributesPipeline()
#b.process_item(item, None)
