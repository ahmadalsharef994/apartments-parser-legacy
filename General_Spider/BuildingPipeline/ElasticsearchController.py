from elasticsearch import Elasticsearch
from Constants import Constants
import datetime
import json
import uuid
from General_Spider.configurations import *
class ElasticsearchController(object):
     def __init__(self):
         self.es = Elasticsearch([elasticSerachServerIP], port=elasticSearchServerPort, http_auth=(elasticSearchUsername, elasticSearchPassword))#68.168.100.142
    # def search(self, query, documentType, indexName):
     #    return es.search(index=indexName, doc_type = documentType, body={"query": query})
     def insert(self, query, documentType, indexName):
         self.es.index(index = indexName, doc_type = documentType, body = query )
     def clean(self, value):
        value = value.lower()
        value = value.strip()
        return value

class MasterDataIndexController(ElasticsearchController):
     def __init__(self):
         super(MasterDataIndexController, self).__init__()
         self.indexName = elasticSearchMasterIndexName
         self.documentType = Constants.doc
     def search(self, query):
         return self.es.search(index=self.indexName,  body = query)
     def insert(self, building, area, city, coordinates):
         body = dict()
         if building is not None:
            body[Constants.building] = building
         if area is not None:
            body[Constants.area] = area
         if city is not None:
            body[Constants.city] = city
         if coordinates is not None:
            body[Constants.coordinates] = coordinates
         creating_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
         body[Constants.creating_date_time] = creating_date_time
         creating_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
         body[Constants.creating_date] = creating_date
         self.es.index(index=self.indexName, doc_type = self.documentType, body = body)
     def updateArea(self, id, area):
         self.es.update(index = self.indexName, doc_type=self.documentType, id=id, body={"doc" : {"area": area}})
     def updateCoordinates(self, id, coordinates):
         self.es.update(index = self.indexName, doc_type=self.documentType, id=id, body={"doc" : {"coordinates" : coordinates}})
     def isBuildingExistsInMasterDataIndex2(self, building, city):
        building = self.clean(building)
        city = self.clean(city)
        query = {"query" : {"bool": {"filter": [{"term": {"building.raw": building}},{"term": {"city.raw": city}}]}}}
        result = self.search(query)
        total = result["hits"]["total"]
        if total == 0:
            return None
        else:
            return result["hits"]["hits"][0]
     def isBuildingExistsInMasterDataIndex(self, longitude, latitude):
        query = {"query" : {"bool": {"filter": [{"term": {"coordinates": "{0},{1}".format(latitude, longitude)}}]}}}
        result = self.search(query)
        total = result["hits"]["total"]
        if total == 0:
            return None
        else:
            return result["hits"]["hits"][0]
     def insertToMasterData(self, building, area, city, coordinates):
        building = self.clean(building)
        area = self.clean(area)
        city = self.clean(city)
        creating_date_time = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        creating_date = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        query = body = {"building": building, "city" : city, "area" : area, "coordinates" : coordinates, "creating_date" : creating_date, "creating_date_time" : creating_date_time}
        self.insert(query)

class ADIndexController(ElasticsearchController):
     def __init__(self):
         super(ADIndexController, self).__init__()
         self.indexName = elasticSearchIndexName
         self.documentType = "doc"
     def search(self, query):
         return self.search(index=self.indexName, doc_type = self.docuemntType, body = query)
     def insert(self, rawAd):
        if (Constants.coordinates not in rawAd):
            if (Constants.longitude in rawAd) and  (Constants.defaultValue != rawAd[Constants.longitude].strip().lower()) and  (Constants.exceptionValue != rawAd[Constants.longitude].strip().lower()) and (Constants.latitude in rawAd) and  (Constants.defaultValue != rawAd[Constants.latitude].strip().lower()) and  (Constants.exceptionValue != rawAd[Constants.latitude].strip().lower()) :
                rawAd[Constants.coordinates] = "{0},{1}".format(rawAd[Constants.latitude], rawAd[Constants.longitude])
        rawAd.pop(Constants.latitude, None)
        rawAd.pop(Constants.longitude, None)
        rawAd['creating_date_time'] = str(datetime.datetime.today().strftime("%Y-%m-%d %H:%M:%S"))
        rawAd['creating_date'] = str(datetime.datetime.today().strftime("%Y-%m-%d"))
        body = json.dumps(dict(rawAd), ensure_ascii=True)
        ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, rawAd['ad_link'].encode('utf-8')))
        action = rawAd['action']
        if action.lower() == Constants.sale:
            self.documentType = Constants.docSale
        else:
            self.documentType = Constants.doc
        self.es.index(index = self.indexName, doc_type = self.documentType, body = body, id = ID) #propertywebsites7, propertyrent, propertywebsitestest
        return rawAd




class ACIndexController(ElasticsearchController): #autoComplete index controller
    def __init__(self):
        super(ACIndexController, self).__init__()
        self.indexName = elasticSearchAutoCompleteIndex
        self.documentType = "doc"

    def insert(self, rawAd):
        data = dict()
        if (Constants.area in rawAd):
            data[Constants.area] = {"input": [rawAd[Constants.area]]}
        if (Constants.building in rawAd):
            data[Constants.building] = {"input": [rawAd[Constants.building]]}
        if ("combined_field_Pho_Syn" in rawAd):
            data[Constants.combined_field] = {"input": [rawAd["combined_field_Pho_Syn"]]}
        body = json.dumps(dict(data), ensure_ascii=True)
        ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, rawAd['ad_link'].encode('utf-8')))
        self.documentType = Constants.doc
        try:
            self.es.index(index=self.indexName, doc_type=self.documentType, body=body,
                      id=ID)  # propertywebsites7, propertyrent, propertywebsitestest
        except Exception as ee:
            print "Errorrrrrrrr on {0}".format(str(ee))
        return rawAd



     
