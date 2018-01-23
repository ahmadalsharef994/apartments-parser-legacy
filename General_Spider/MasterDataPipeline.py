from General_Spider.BuildingPipeline.models import ADDocumentModel
from General_Spider.BuildingPipeline.models import MDDocumentModel
from General_Spider.BuildingPipeline.Constants import Constants
from General_Spider.BuildingPipeline.MasterDataController import MasterDataController
from General_Spider.BuildingPipeline.ElasticsearchController import ADIndexController
from General_Spider.BuildingPipeline.ElasticsearchController import ACIndexController
from General_Spider.BuildingPipeline.ElasticsearchController import MasterDataIndexController
from General_Spider.BuildingPipeline.GoogleMapsController import GoogleMapsController
class MasterDataPipeline(object):
     def process_item(self, item, spider):
         adModel = ADDocumentModel(item)
         masterDataController = MasterDataController()
         masterDataIndexController = MasterDataIndexController()
         acIndexController = ACIndexController()
         if Constants.building not in adModel.ad:
             #Building doesn't exist in the ad
             if (Constants.longitude in adModel.ad and Constants.latitude in adModel.ad):
                 #The ad contains longitude and latitude
                 result = masterDataIndexController.isBuildingExistsInMasterDataIndex(longitude = adModel.ad[Constants.longitude], latitude = adModel.ad[Constants.latitude])
                 if result is not None:
                     #There is a MD document with the same longitude and latitude
                     mdDoc = MDDocumentModel(result)
                     adModel.ad[Constants.building] = mdDoc.doc[Constants.building]
                     masterDataController.handleCoordinatesMatching(mdDoc = mdDoc, adDoc = adModel, rawAd = item)
                 else:
                     #MD doesn't contain a document with the same longitude and latitude
                     googleMapsController = GoogleMapsController()
                     building = googleMapsController.getBuildingName(latitude = adModel.ad[Constants.latitude], longitude = adModel.ad[Constants.longitude])
                     if (building is None):
                         #Google Maps doesn't have building value according to the giving longitude and latitude
                         item = ADIndexController().insert(rawAd = item)
                     else:
                         #Google Maps has a building name according to the giving longitude and latitude
                         adModel.ad[Constants.building] = building
                         item[Constants.building] = building
                         result = masterDataIndexController.isBuildingExistsInMasterDataIndex2(building = adModel.ad[Constants.building], city = adModel.ad[Constants.city])
                         if result is not None:
                             #There is MD document with the same building and city
                             mdDoc = MDDocumentModel(result)
                             masterDataController.handleAreaInBuildingMatching(mdDoc = mdDoc, adDoc = adModel, rawAd = item, shouldInsertToAd = False)
                             masterDataController.handleCoordinatesInBuildingMatching(mdDoc = mdDoc, adDoc = adModel, rawAd = item)
                         else:
                             #MD doesn't have a document with the same building and city
                             if (Constants.area in googleMapsController.model.doc) and (Constants.area not in adModel.ad):
                                adModel.ad[Constants.area] = googleMapsController.model.doc[Constants.area]
                                item[Constants.area] = googleMapsController.model.doc[Constants.area]
                             masterDataController.handleNoMatchingFile(adDoc = adModel, rawAd = item)
                             acIndexController.insert(rawAd=item)
             else:
                item = ADIndexController().insert(item)
         else:
            result = masterDataIndexController.isBuildingExistsInMasterDataIndex2(building = adModel.ad[Constants.building], city = adModel.ad[Constants.city])
            if result is not None:
                #There is MD document with the same building and city
                mdDoc = MDDocumentModel(result)
                masterDataController.handleAreaInBuildingMatching(mdDoc = mdDoc, adDoc = adModel, rawAd = item, shouldInsertToAd = False)
                masterDataController.handleCoordinatesInBuildingMatching(mdDoc = mdDoc, adDoc = adModel, rawAd = item)
            else:
                #MD doesn't have a document with the same building and city
                masterDataController.handleNoMatchingFile(adDoc = adModel, rawAd = item)
                acIndexController.insert(rawAd=item)