from lxml import etree
import os.path
class ActionsXMLParser():
    def __init__(self, actionsXMLFilePath):
        self.doc=etree.parse(actionsXMLFilePath)
        self.actionsXMLFilePath=actionsXMLFilePath
        self.sourceNode = etree.parse(actionsXMLFilePath)
        self.actionsDictionary = dict()
        attributes = self.sourceNode.findall('DetailsAttributes/Attribute')
        for oneAttribute in attributes:
            hasAction = oneAttribute.find('actions')
            if hasAction is not None:
            #    self.actionsDictionary(oneAttribute.find('name').text) = None
            #else:
                allActionsForOneAttribute = oneAttribute.find('actions').findall('action')
                actionsList = list()
                for oneAction in allActionsForOneAttribute:
                    actionsList.append(oneAction.text)
                self.actionsDictionary[oneAttribute.find('name').text] = actionsList
        #import pdb; pdb.set_trace()
    def getActionsForAttribute(self, name): #This function is to get the actions for a specific attribute, the attribute is the parameter "name"
        attributeNode = self.sourceNode.find('DetailsAttributes/Attribute/')
        attributeNode = self.sourceNode.find(name)
        if attributeNode is None:
            return None
        else:
            actions = list()
            actionsNodes = attributeNode.findall('action')
            for oneAction in actionsNodes:
                actions.append(oneAction.text)
            return actions