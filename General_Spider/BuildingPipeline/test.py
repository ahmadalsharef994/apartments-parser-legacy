from elasticsearch import Elasticsearch
es=Elasticsearch(['68.168.100.142'], port=9200)
query={"query" : {"match_all" : {}}}
# scanResp= es.search(index="masterdatafinal", doc_type="doc",body=query, search_type="scan", scroll="0s")
#
# scrollId= scanResp['_scroll_id']
#
# response= es.scroll(scroll_id=scrollId, scroll= "10m")
# print response


import elasticsearch
# res = Elasticsearch.helpers.scan(es,query=query,index="masterdatafinal",doc_type="doc" )

# Initialize the scroll
page = es.search(
  index = 'propertyrent2',
  doc_type = 'doc',
  scroll = '2m',
  search_type = 'scan',
  size = 1000,
  body = query)
sid = page['_scroll_id']
scroll_size = page['hits']['total']

  # Start scrolling
while (scroll_size > 0):
    print "Scrolling..."
    data3Result = es.search(index="apartmentmasterdata3", body={"size": 2000, "query": {"match_all": {}}})
    page = es.scroll(scroll_id = sid, scroll = '2m')
    # Update the scroll ID
    sid = page['_scroll_id']
    # Get the number of results that we returned in the last scroll
    scroll_size = len(page['hits']['hits'])
    print "scroll size: " + str(scroll_size)
    # Do something with the obtained page