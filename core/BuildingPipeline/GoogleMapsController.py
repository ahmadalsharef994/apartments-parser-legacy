import  googlemaps
import json
from core.BuildingPipeline.models import GMDocumentModel
from core.BuildingPipeline.Constants import Constants
class google_map(object):
    def __init__(self):
        "google map api  extract longitude and latitude"
        self.set_api_key("AIzaSyD-lKFWnWzOSalK4xEUU6QeG6eW1Lm-o3s")

    def set_addresss(self,adrs):
        self.name=adrs
        self.address=self.maps.geocode(adrs)

    def set_api_key(self,client_key):
        "set the  google client API"
        self.maps=googlemaps.Client(key=client_key)


class GoogleMapsController(object):

    @staticmethod
    def GetAddressResult(adrs):
        map = google_map()
        map.set_addresss(adrs)
        return map.address

    def getModel(self, searchTerms):
        map = google_map()
        map.set_addresss(searchTerms)
        results = map.address
        self.model = GMDocumentModel(googleMapsResponse = results)
        return self.model

    def getBuildingName(self, latitude, longitude):
        latlng=str(latitude) + "," + str(longitude)
        model = self.getModel(searchTerms = latlng)
        if Constants.building in model.doc:
            return model.doc[Constants.building]
        else:
            return None

    def getAreaFromLatLong(self, latitude,longitude):
        latlng = str(latitude) + "," + str(longitude)
        model = self.getModel(searchTerms = latlng)
        if Constants.area in model.doc:
            return model.doc[Constants.area]
        else:
            return None

    def getAreaFromBuildingCity(self, building, city):
        buildingAndCity = str(city) + " " + str(building)
        model = self.getModel(searchTerms = buildingAndCity)
        if Constants.area in model.doc:
            return model.doc[Constants.area]
        else:
            return None

    def getCoordinates(self,building,city):
        buildingAndCity = str(city) + " " + str(building) 
        model = self.getModel(searchTerms = buildingAndCity)
        if Constants.coordinates in model.doc:
            return model.doc[Constants.coordinates]
        else:
            return None

# print  GoogleMapFullResult.getAreaFromLatLong(25.1950,55.2784)
#print  GoogleMapFullResult.getAreaFromBuildingCity("Downtown Dubai","dubai")