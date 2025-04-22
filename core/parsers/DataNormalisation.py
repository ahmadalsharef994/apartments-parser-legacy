from lxml import etree
import json
class DataNormalisation(object):
    def __init__(self):
        "pass"

class PaymentXMLParser(object):
    def __init__(self,xmlFile):
        self.doc = etree.parse(xmlFile)
        self.paymentTypes = {}
        self.paymentValueToMultiply = {}
        for key in self.doc.findall('master'):
            values = key.findall('synonyms')
            multiplier = key.findall('valueToMultiply')
            self.paymentTypes[key]=values
            self.paymentValueToMultiply = multiplier

    def getMasterValue(self,value):
        for key in self.paymentTypes:
            for synonyms in key:
                if synonyms.text == value:
                    result = {}
                    result['valueToMultiply'] = key.find('valueToMultiply').text
                    result['master_type'] =  key.find('key').text
                    return result


class PropertyXMLParser(object):
    def __init__(self, xmlFile):
        self.doc = etree.parse(xmlFile)
        self.propertyTypes = {}
        for key in self.doc.findall('master'):
            values = key.findall('synonyms')
            self.propertyTypes[key] = values


    def getMasterValue(self,value):
        for key in self.propertyTypes:
            for synonyms in key:
                if synonyms.text == value:
                    return key.find('key').text



class FurnishingXMLParser(object):
    def __init__(self, xmlFile):
        self.doc = etree.parse(xmlFile)
        self.furnishings = {}
        for key in self.doc.findall('master'):
            values = key.findall('synonyms')
            self.furnishings[key] = values

    def getMasterValue(self,value):
        for key in self.furnishings:
            for synonyms in key:
                if synonyms.text == value:
                    return key.find('key').text


class LoadJsonObject(object):
    def __init__(self,objectName):
        with open(objectName) as json_file:
            self.jsonObject = json.load(json_file)

    def getMasterValue(self,value):
        for key in list(self.jsonObject.keys()):
            for area in self.jsonObject[key]:
                if area == value:
                    return key
        return value