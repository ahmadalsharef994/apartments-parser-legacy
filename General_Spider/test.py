# import uuid
# ID = str(uuid.uuid5(uuid.NAMESPACE_DNS, "https://www.propsearch.ae//property/2725886/1-bedroom-apartment-for-sale-in-shakespeare-circus-1-uptown-motor-city".encode('utf-8'))) #get the uuid depending on the link thus we will have a unique identifier
# print ID

# import re
# value = "created 22.03.2016, updated 04.01.2018"
# updateDate = value.split(',')
# result = re.search('updated \s*(.*)', value).group(1)
# print  result

def getthatNextpage(value,currentMasterpage):
    #     http://getthat.comdsksakdaskdsd
    next = '&page='+currentMasterpage+1
    value= value+currentMasterpage+1
    return  value

