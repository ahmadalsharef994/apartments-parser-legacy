from Constants import Constants
class ADDocumentModel(object):
    def clean(self, value):
        value = value.lower()
        value = value.strip()
        return value

    def __init__(self, item):
        self.ad = dict()
        attributes = [Constants.building, Constants.area, Constants.city, Constants.longitude, Constants.latitude]
        for attribute in attributes:
            if attribute in item:
                attributeValue = item[attribute]
                attributeValue = attributeValue.strip()
                attributeValue = attributeValue.lower()
                if (attributeValue != Constants.defaultValue and attributeValue != Constants.exceptionValue.lower()):
                    self.ad[attribute] = self.clean(attributeValue)
                    item[attribute] = self.clean(attributeValue)

class MDDocumentModel(object):
    def __init__(self, item):
        source = item[Constants._source]
        self.doc = dict()
        self.doc[Constants.id] = item[Constants._id]
        attributes  = [Constants.building, Constants.area, Constants.city, Constants.coordinates]
        for attribute in attributes:
            if attribute in source:
                attributeValue = source[attribute]
                attributeValue = attributeValue.strip()
                attributeValue = attributeValue.lower()
                if (attributeValue != Constants.defaultValue and attributeValue != Constants.exceptionValue.lower()):
                    self.doc[attribute] = attributeValue
    #you must check if coordinates field exists before calling this function
    def getLongitude(self):
        return self.doc[Constants.coordinates].split(",")[1]
    #you must check if coordinates field exists before calling this function
    def getLatitude(self):
        return self.doc[Constants.coordinates].split(",")[0]

#Google Maps document model
class GMDocumentModel(object):

    def clean(self, value):
        value = value.lower()
        value = value.strip()
        return value

    def __init__(self, googleMapsResponse):
        self.doc = dict()
        building = self.getBuildingName(googleMapsResponse)
        if building is not None:
            self.doc[Constants.building] = building
        area = self.getArea(googleMapsResponse)
        if area is not None:
            self.doc[Constants.area] = area
        coordinates = self.getCoordinates(googleMapsResponse)
        if coordinates is not None:
            self.doc[Constants.coordinates] = "{0},{1}".format(coordinates["lat"], coordinates["lng"])

    def getBuildingName(self, googleMapsResponse):
        for result in googleMapsResponse:
            for address in  result["address_components"]:
                for types in address["types"]:
                    if types == 'premise':
                        return self.clean(address["long_name"])
        return None

    def getArea(self, googleMapsResponse):
        for result in googleMapsResponse:
            for address in  result["address_components"]:
                for types in address["types"]:
                    if types == 'sublocality_level_1':
                        return self.clean(address["long_name"])
        return None

    def getCoordinates(self, googleMapsResponse):
        return googleMapsResponse[0]['geometry']['location']
