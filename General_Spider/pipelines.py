# -*- encoding: utf-8 -*-
# -*- coding: utf-8 -*-
# encoding: utf-8
import json
import uuid
import csv
import re
import datetime
from General_Spider.actions.actions import Actions
from General_Spider.BuildingPipeline.Constants import Constants
from General_Spider.parsers.DataNormalisation import PaymentXMLParser
from General_Spider.parsers.DataNormalisation import PropertyXMLParser
from General_Spider.parsers.DataNormalisation import FurnishingXMLParser
class JsonWriterPipeline(object):
    def process_item(self, item, spider):
        ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, item['ad_link'].encode('utf-8'))) #get the uuid depending on the link thus we will have a unique identifier
        item['creating_date_time'] = str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        item['creating_date'] = str(datetime.datetime.now().strftime("%Y-%m-%d"))
        #During testing uncomment the lines between start and end, and when deploying on server, it is important to comment them.
        #start
        # fileName = str(item["category"]).lower()+'_'+str(item['source']).lower()+'_'+ID #get the file name which is category + source + ID
        # self.file = open("JSONFiles/"+ item["category"]+"/" + item["action"]+"/"+ item['source']+"/"+fileName + '.json', 'wb') #create a new json file with the name = fileName parameter
        # line = json.dumps(dict(item)) #change the item to a json format in one line
        # self.file.write(line) #write the item to the file
        # for key in item:
        #     try:
        #         item[key] = item[key].decode("utf-8")
        #     except:
        #         item[key] = item[key]
        # #end
        return item

class ActionsPipeline(object):
    def process_item(self, item, spider):
        for key in item:
            actions = ActionsPipeline.actionsXMLParser.actionsDictionary.get(key) #get all actions for that item
            if actions is not None: #checking if that item has actions or not.
                try:
                    value = item[key] 
                    for oneAction in actions:
                            value = getattr(Actions, oneAction)(value)
                    item[key] = value
                except:
                    if (ActionsPipeline.defaultValues[key] == "-1"):
                        item[key] = -1
                    else:
                        item[key] = ActionsPipeline.defaultValues[key]
        return item


    @staticmethod
    def setActionsXMLParser(actionsXMLParser):
        ActionsPipeline.actionsXMLParser = actionsXMLParser# Define your item pipelines here

    @staticmethod
    def setDefaultValues(defaultValues):
        ActionsPipeline.defaultValues = defaultValues;

# class CordinatesPipeline(object):
#     def process_item(self, item, spider):
#         location = item['building'] + " " + item['area'] + " "+ item["city"]
#         g = google_map()
#         result = g.get_long_lat(location)
#         if result is not None:
#             item["coordinates"] = "{0},{1}".format(result["latitude"], result["longitude"])
#         else:
#             item["coordinates"] = "{0},{1}".format(12.483324, 41.901180)
#         return item

class Yzerproperty(object): 
    def process_item(self, item, spider): 
        if item['source'] == "yzerproperty": 
            title = item['ad_title'] 
            title = title.strip() 
            title = title.lower() 
            if re.findall(r'studio (.*)', title)!= []: 
                item['bedrooms'] = 0 
        return item

class DubizzlePipeline(object):
    def process_item(self, item, spider):
        if item['source'] == "dubizzle":
            defaultValue = ""
            exceptionValue = "NA"
            building = item['building']
            building = building.strip()
            building = building.lower()
            try:
                if building == defaultValue or building == exceptionValue.lower():
                    buildingAndArea = item['buildingAndArea']
                    firstValue = buildingAndArea.split(',')[0]
                    secondValue = buildingAndArea.split(',')[1]
                    firstValue = ''.join([i if ord(i) < 128 else '' for i in firstValue])
                    secondValue = ''.join([i if ord(i) < 128 else '' for i in secondValue])
                    firstValue = firstValue.lower()
                    firstValue = firstValue.strip()
                    secondValue = secondValue.lower()
                    secondValue = secondValue.strip()
                    city = item['city']
                    city = city.lower()
                    city = city.strip()
                    if firstValue != city:  # case of area and buiilding state name , uae
                        if secondValue == city:
                            item['area'] = firstValue
                        else:
                            item['building'] = firstValue
                            item['area'] = secondValue
            except Exception as ee:
                errorMessage2 = "Error on {0}".format(str(ee))
                print errorMessage2
            # my_dict.pop('buildingAndArea', None)
        return item

class AddCombinedField(object):
    def process_item(self,item,spider):
        bedroomStr =""
        if item["bedrooms"]== 0:
            bedroomStr= "studio"
        elif item["bedrooms"]==1:
            bedroomStr = "1 one"
        elif item["bedrooms"] == 2:
            bedroomStr = "2 two"
        elif item["bedrooms"] == 3:
            bedroomStr = "3 three"
        elif item["bedrooms"] == 4:
            bedroomStr = "4 four"
        elif item["bedrooms"] == 5:
            bedroomStr = "5 five"
        elif item["bedrooms"] == 6:
            bedroomStr = "6 six"
        elif item["bedrooms"] == 7:
            bedroomStr = "7 seven"
        area = item["area"]
        building = item["building"]
        type = item["master_property_type"]
        price = str(item["price"])
        title = item["ad_title"]
        city = item["city"]
        action = item["action"]    
        combined = "city {0} area {1} building {2} property_type {3} bedroom BR bed  {4} price {5} ad_title {6} action {7}".format(city,area,building,type,bedroomStr,price,title,action)
        item["combined_field_Pho_Syn"]=combined
        return item


class DataNormalisation(object):
    def process_item(self, item, spider):
        if item[Constants.action].lower() == Constants.rent:
            payment_value = item[Constants.payment_type]
            property_type = item[Constants.type]
            furnished = item[Constants.furnished]
            area_value = item[Constants.area]
            result = DataNormalisation.mappingObject[Constants.payment_type].getMasterValue(payment_value.lower())
            if result != None:
                item['master_payment_type'] = result
            else :
                item['master_payment_type'] = 'na'

            propertyTypeResult = DataNormalisation.mappingObject[Constants.type].getMasterValue(property_type.lower())
            if propertyTypeResult != None:
                item['master_property_type'] = propertyTypeResult
            else:
                item['master_property_type'] = 'na'
            furnishingResult = DataNormalisation.mappingObject[Constants.furnished].getMasterValue(furnished.lower())
            if furnishingResult != None:
                item['master_furnished'] = furnishingResult
            else:
                item['master_furnished'] = 'na'
            areaResult = DataNormalisation.mappingObject[Constants.area].getMasterValue(area_value.lower())
            if areaResult !=None:
                item[Constants.area]= areaResult
            return item
        elif item[Constants.action].lower() == Constants.sale:
            property_type = item[Constants.type]
            area_value = item["area"]
            propertyTypeResult = DataNormalisation.mappingObject[Constants.type].getMasterValue(property_type.lower())
            if propertyTypeResult != None:
                item['master_property_type'] = propertyTypeResult
            else:
                item['master_property_type'] = 'na'
            areaResult = DataNormalisation.mappingObject[Constants.area].getMasterValue(area_value.lower())
            if areaResult != None:
                item[Constants.area] = areaResult
            return item


    @staticmethod
    def setMapping(mappingObject):
        DataNormalisation.mappingObject = mappingObject
