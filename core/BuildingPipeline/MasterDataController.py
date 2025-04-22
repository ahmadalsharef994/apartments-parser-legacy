from .ElasticsearchController import MasterDataIndexController
from .ElasticsearchController import ADIndexController
from .Constants import Constants
from core.BuildingPipeline.GoogleMapsController import GoogleMapsController
class MasterDataController(object):
    #File matching master Data based on coordinates (handling Area case)
    def handleCoordinatesMatching(self, mdDoc, adDoc, rawAd, shouldInsertToAd = True):
        print ("handleCoordinatesMatching")
        if Constants.building in mdDoc.doc:
            rawAd[Constants.building] = mdDoc.doc[Constants.building]
            adDoc.ad[Constants.building] = mdDoc.doc[Constants.building]
        if Constants.coordinates in mdDoc.doc:
            rawAd[Constants.coordinates] = mdDoc.doc[Constants.coordinates]
            adDoc.ad[Constants.coordinates] = mdDoc.doc[Constants.coordinates]
        if Constants.area in adDoc.ad and Constants.area  not in mdDoc.doc:
            MasterDataIndexController().updateArea(id = mdDoc.doc[Constants.id],area = adDoc.ad[Constants.area])
            if shouldInsertToAd:
                rawAd = ADIndexController().insert(rawAd)
        elif Constants.area in mdDoc.doc and Constants.area not in adDoc.ad:
            rawAd[Constants.area] = mdDoc.doc[Constants.area]
            if shouldInsertToAd:
                rawAd = ADIndexController().insert(rawAd)
        elif Constants.area not in mdDoc.doc and Constants.area not in adDoc.ad:
            area = GoogleMapsController().getAreaFromLatLong(latitude = adDoc.ad[Constants.latitude], longitude = adDoc.ad[Constants.longitude])
            if area is not None:
                adDoc.ad[Constants.area] = area
                mdDoc.doc[Constants.area] = area
                MasterDataIndexController().updateArea(id = mdDoc.doc[Constants.id], area = area)
                rawAd[Constants.area] = area
                if shouldInsertToAd:
                    rawAd = ADIndexController().insert(rawAd)
            else:
                if shouldInsertToAd:
                    rawAd = ADIndexController().insert(rawAd)
        else:
            if shouldInsertToAd:
                rawAd = ADIndexController().insert(rawAd)
    #File matching master Data (handling Area case)
    def handleAreaInBuildingMatching(self, mdDoc, adDoc, rawAd, shouldInsertToAd = True):
        if Constants.building in mdDoc.doc:
            rawAd[Constants.building] = mdDoc.doc[Constants.building]
            adDoc.ad[Constants.building] = mdDoc.doc[Constants.building]
        if (Constants.coordinates in mdDoc.doc) and ((Constants.coordinates not in adDoc.ad) and (Constants.longitude not in adDoc.ad) and (Constants.latitude not in adDoc.ad)):
            rawAd[Constants.coordinates] = mdDoc.doc[Constants.coordinates]
            adDoc.ad[Constants.coordinates] = mdDoc.doc[Constants.coordinates]
        if Constants.area in adDoc.ad and Constants.area  not in mdDoc.doc:
            MasterDataIndexController().updateArea(id = mdDoc.doc[Constants.id],area = adDoc.ad[Constants.area])
            if shouldInsertToAd:
                rawAd = ADIndexController().insert(rawAd)
        elif Constants.area in mdDoc.doc and Constants.area not in adDoc.ad:
            rawAd[Constants.area] = mdDoc.doc[Constants.area]
            if shouldInsertToAd:
                rawAd = ADIndexController().insert(rawAd)
        elif Constants.area not in mdDoc.doc and Constants.area not in adDoc.ad:
            googleMapsController = GoogleMapsController()
            area = googleMapsController.getAreaFromBuildingCity(building = adDoc.ad[Constants.building], city = adDoc.ad[Constants.city])
            if area is not None:
                adDoc.ad[Constants.area] = area
                mdDoc.doc[Constants.area] = area
                MasterDataIndexController().updateArea(id = mdDoc.doc[Constants.id], area = area)
                rawAd[Constants.area] = area
                if shouldInsertToAd:
                    rawAd = ADIndexController().insert(rawAd)
            else:
                if shouldInsertToAd:
                    rawAd = ADIndexController().insert(rawAd)
        else:
            if shouldInsertToAd:
                rawAd = ADIndexController().insert(rawAd)

    #File matching master Data(handling coordinates case )
    def handleCoordinatesInBuildingMatching(self, mdDoc, adDoc, rawAd):
        print("handleCoordinatesInBuildingMatching")
        if (Constants.longitude in adDoc.ad) and (Constants.latitude in adDoc.ad) and (Constants.coordinates not in mdDoc.doc):
            print("Ad has coordinates but MD doesn't have")
            mdDoc.doc[Constants.coordinates] = "{0},{1}".format(adDoc.ad[Constants.latitude], adDoc.ad[Constants.longitude])
            MasterDataIndexController().updateCoordinates(id = mdDoc.doc[Constants.id],coordinates = "{0},{1}".format(adDoc.ad[Constants.latitude],adDoc.ad[Constants.longitude]))
            rawAd = ADIndexController().insert(rawAd)
        elif (Constants.longitude not in adDoc.ad) and (Constants.latitude not in adDoc.ad) and (Constants.coordinates in mdDoc.doc):
            print("Md has coordinates but Ad doesn't")
            rawAd[Constants.longitude] = mdDoc.getLongitude()
            rawAd[Constants.latitude] = mdDoc.getLatitude()
            rawAd = ADIndexController().insert(rawAd)
        elif (Constants.longitude not in adDoc.ad) and (Constants.latitude not in adDoc.ad) and (Constants.coordinates not in mdDoc.doc):
            print("Neither Ad nor Md has coordinates")
            coordinates = GoogleMapsController().getCoordinates(building = adDoc.ad[Constants.building], city=adDoc.ad[Constants.city])
            masterDataIndexController = MasterDataIndexController()
            mdDoc.doc[Constants.coordinates] = coordinates
            rawAd[Constants.longitude] = mdDoc.getLongitude()
            rawAd[Constants.latitude] = mdDoc.getLatitude()
            masterDataIndexController.updateCoordinates(id = mdDoc.doc[Constants.id], coordinates = mdDoc.doc[Constants.coordinates])
            rawAd = ADIndexController().insert(rawAd)
        else:
            print("Both Ad and Md has coordinates")
            rawAd = ADIndexController().insert(rawAd)
    #No matching file in Master Data based on Building name
    def handleNoMatchingFile(self, adDoc, rawAd):
        print("handleNoMatchingFile")
        if (Constants.longitude in adDoc.ad) and (Constants.latitude in adDoc.ad) and (Constants.area in adDoc.ad):
            print("Ad has coordinates and area")
            MasterDataIndexController().insert(building = adDoc.ad[Constants.building], area = adDoc.ad[Constants.area],city = adDoc.ad[Constants.city], coordinates = "{0},{1}".format(adDoc.ad[Constants.latitude], adDoc.ad[Constants.longitude]))
            rawAd = ADIndexController().insert(rawAd)
        elif (Constants.longitude in adDoc.ad) and (Constants.latitude in adDoc.ad) and (Constants.area not in adDoc.ad):
            print("Ad has coordinates without area")
            area = GoogleMapsController().getAreaFromLatLong(longitude = adDoc.ad[Constants.longitude], latitude=adDoc.ad[Constants.latitude])
            MasterDataIndexController().insert(building = adDoc.ad[Constants.building], area = area, city = adDoc.ad[Constants.city], coordinates = "{0},{1}".format(adDoc.ad[Constants.latitude], adDoc.ad[Constants.longitude]))
            adDoc.ad[Constants.area] = area
            rawAd[Constants.area] = area
            rawAd = ADIndexController().insert(rawAd)
        elif (Constants.longitude not in adDoc.ad) and (Constants.latitude not in adDoc.ad) and (Constants.area in adDoc.ad):
            print("Ad has area without coordinates")
            coordinates = GoogleMapsController().getCoordinates(building = adDoc.ad[Constants.building], city = adDoc.ad[Constants.city])
            rawAd[Constants.coordinates] = coordinates
            adDoc.ad[Constants.coordinates] = coordinates
            MasterDataIndexController().insert(building = adDoc.ad[Constants.building], area = adDoc.ad[Constants.area], city = adDoc.ad[Constants.city], coordinates = adDoc.ad[Constants.coordinates])
            rawAd = ADIndexController().insert(rawAd)
        else:
            print("Ad doesn't have neither are nor coordinates")
            googleMapsController = GoogleMapsController()
            area = googleMapsController.getAreaFromBuildingCity(building = adDoc.ad[Constants.building], city = adDoc.ad[Constants.city])
            if Constants.coordinates in googleMapsController.model.doc:
                coordinates = googleMapsController.model.doc[Constants.coordinates]
                adDoc.ad[Constants.coordinates] = coordinates
                rawAd[Constants.coordinates] = coordinates
            adDoc.ad[Constants.area] = area
            rawAd[Constants.area] = area
            MasterDataIndexController().insert(building = adDoc.ad[Constants.building], area = area, city = adDoc.ad[Constants.city], coordinates = adDoc.ad[Constants.coordinates])
            rawAd = ADIndexController().insert(rawAd)
