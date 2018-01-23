#This class is an abstract class so all the other attribute calsses will inhert from it. it has the getRestul function will all its childern must implement in order
#to have a dynamic extracting attributes
from abc import ABCMeta, abstractmethod

class GenericAttribute(object):
    __metaclass__=ABCMeta
    @abstractmethod
    def getResult(self, sel, response, flexibleItem):#sel is the xpath container, response is the dom of the page
        pass 