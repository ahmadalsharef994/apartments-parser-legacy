#This class is to parse the xml and get all the information in it
from lxml import etree
from General_Spider.attribute.multipleValuesAttribute import MultipleValuesAttribute
from General_Spider.attribute.selectorAtribute import SelectorAtribute
from General_Spider.attribute.metaAttribute import MetaAttribute
from General_Spider.attribute.responseAttribute import ResponseAttribute
from General_Spider.actions.actions import Actions
import os.path

class AttributesXMLParser():
    def __init__(self, attributesXMLFilePath):
        self.doc=etree.parse(attributesXMLFilePath)

    def getValueOfTag(self, tagName): #This function returns the value of a specific tag for exmaple, the tageName could be "FirstDate"
        return self.doc.find(tagName).text

    def getStartUrls(self): #This function returns the start urls 
        UrlsFromXML = self.doc.findall('start_urls/url')
        Urls = list()
        for oneUrl in UrlsFromXML:
            Urls.append(oneUrl.text)
        return Urls

    def getMastersAttributes(self): #This function returns the master attributes in a dictionary, the key is the attribute name and the value is the attribute object
        Attributes = dict()
        masterItemsFromXML = self.doc.findall('MasterPage/MasterAttributes/Attribute')
        for oneAttribute in masterItemsFromXML:
            selectorAttribute = SelectorAtribute(xpath = oneAttribute.find('xpath').text, name = oneAttribute.find('name').text,defaultValue = oneAttribute.find('defaultValue').text)
            Attributes[oneAttribute.find('name').text] = selectorAttribute
        return Attributes

    def getMasterContainers(self): #This function returns the container of the mater attributes
        containers=[]
        containersFromXML = self.doc.findall('MasterPage/Containers/xpath')
        for oneXpath in containersFromXML:
            containers.append(oneXpath.text)
        return containers

    def getNextPage(self, sel, currentMasterPageUrl): #This function returns the next page in the master attribute. the next page could have preffix, suffix, and actions
        nextPage = sel.xpath(str(self.getValueOfTag('MasterPage/NextPage/xpath'))).extract()[0]
        if len(nextPage)>0:
            doesHaveAction = self.doc.find('MasterPage/NextPage/action')
            if doesHaveAction is not None:
                nextPage = getattr(AttributesXMLParser, doesHaveAction.text)(nextPage, currentMasterPageUrl)
            doesHavePrefix = self.doc.find('MasterPage/NextPage/prefix')
            if doesHavePrefix is not None:
                nextPage = self.doc.find('MasterPage/NextPage/prefix').text+nextPage
            doesHaveSuffix = self.doc.find('MasterPage/NextPage/suffix')
            if doesHaveSuffix is not None:
                nextPage = nextPage + self.doc.find('MasterPage/NextPage/suffix').text
            return nextPage

    def getDateValue(self, value):#This function returns the date value. note that the date value could have actions
        doesHaveActions = self.doc.find('DateAttribute/action')
        if doesHaveActions is not None:
            value = getattr(Actions, self.doc.find('DateAttribute/action').text)(value)
        return value

    def getPageLink(self, value, sel): #This function returns the link value, note that the link could have preffix and suffix
        doesHavePrefix = self.doc.find('MasterPage/LinkAttribute/prefix')
        if doesHavePrefix is not None:
            value = self.doc.find('MasterPage/LinkAttribute/prefix').text + value
        doesHaveSuffix = self.doc.find('MasterPage/LinkAttribute/suffix')
        if doesHaveSuffix is not None:
            value = self.doc.find('MasterPage/LinkAttribute/suffix').text + value
        doesHaveAction = self.doc.find('MasterPage/LinkAttribute/action')
        if doesHaveAction is not None:
            value = getattr(Actions, doesHaveAction.text)(value)
        return value

    def getDetailsAttributes(self):#This function returns the details attribute in a dictionary, the key is the attribute name and the value is the attribute object
         Attributes = dict()
         detailsAtributesFromXML = self.doc.findall('DetailsAttributes/Attribute')
         for OneAttribute in detailsAtributesFromXML:
            attributeType = OneAttribute.find('type').text
            if attributeType == "Multiple":
                multipleValuesAttribute = MultipleValuesAttribute(name = OneAttribute.find('name').text, xpath = OneAttribute.find('xpath').text, defaultValue = OneAttribute.find('defaultValue').text)
                Attributes[OneAttribute.find('name').text] = multipleValuesAttribute
            elif attributeType == "Selector":
                selectorAttribute = SelectorAtribute(xpath = OneAttribute.find('xpath').text, name = OneAttribute.find('name').text, defaultValue = OneAttribute.find('defaultValue').text)
                Attributes[OneAttribute.find('name').text] = selectorAttribute
            elif attributeType == "Meta":
                metaAttribute = MetaAttribute(name = OneAttribute.find('name').text, defaultValue = OneAttribute.find('defaultValue').text)
                Attributes[OneAttribute.find('name').text] = metaAttribute
            elif attributeType == "Response":
                responseAttribute = ResponseAttribute(name = OneAttribute.find('name').text, defaultValue = OneAttribute.find('defaultValue').text)
                Attributes[OneAttribute.find('name').text] = responseAttribute
         return Attributes

    def getDefaultValues(self, detailsAttributesDictionary):
        defaultValues = dict()
        for oneDetailsAtribute in detailsAttributesDictionary:
            defaultValues[oneDetailsAtribute] = detailsAttributesDictionary[oneDetailsAtribute].defaultValue
        return defaultValues

    def getMaxMasterPageNumber(self):
        try:
            mp = self.doc.find("MaxMasterPage").text
            return int(mp)
        except:
            return 30

    def getHeaders(self):
        headers = dict()
        headersAttributes = self.doc.findall('Headers/Header')
        for header in headersAttributes:
            headers[header.find('key').text] = header.find('value').text
        return headers

    def getTemplateValues(self, templatePath):
        templateParser = etree.parse(templatePath)
        detailsAttributesDictionary = templateParser.findall('Attribute')
        defaultValues = list()
        for oneDetailsAtribute in detailsAttributesDictionary:
            defaultValues.append(oneDetailsAtribute.find('name').text)
        return defaultValues

    @staticmethod
    def autotraderNextPageAction(nextPage, currentMasterPageUrl): #This function will be used by the function "getNextPage" because the auto trader website is using java script on the next page so this function will extract the next page from that script.
        return str((int(nextPage)-1)*10)
    @staticmethod
    def carmudiNextPageAction(nextPageValue, currentMasterPageUrl):
        return str(int(nextPageValue) + 1)
    @staticmethod
    def ezestateParseNextPage(nextPageValue, currentMasterPageUrl):
        return nextPageValue.split(',')[1].split('))')[0].replace(" ","")
    @staticmethod
    def dubizzleGetNextPagePrefixAndSuffix(nextPageValue, currentMasterPageUrl):
        index = currentMasterPageUrl.find(r'&page=')
        if index > 0:
            result = currentMasterPageUrl[:index]
        else:
            result = currentMasterPageUrl
        return result+nextPageValue
    def loadFuzzySettings(self):
        modulesDict = list()
        modules = self.doc.findall('FuzzyComparison/Modules/Module')
        for module in modules:
            moduleDict = dict()
            moduleName = module.find('name').text
            moduleDict['name'] = moduleName
            moduleConfigurationLoader = module.find('configurationLoader').text
            moduleDict['configurationLoader'] = moduleConfigurationLoader
            moduleConfigurationFile = module.find('configurationFile').text
            moduleDict['moduleConfigurationFile'] = moduleConfigurationFile
            settings = module.find('settings')
            settingsDict = dict()
            for oneSetting in settings:
                settingsDict[oneSetting.tag] = oneSetting.text
            moduleDict['settings'] = settingsDict
            modulesDict.append(moduleDict)
        return modulesDict