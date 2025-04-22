import base64
class CustomProxyMiddleware(object):
    # overwrite process request
    def process_request(self, request, spider):
        "pass"
        # Set the location of the proxy
        # if spider.name == 'apartments_rent_yzerproperty' or spider.name == 'apartments_sale_yzerproperty' or  spider.name == 'PropertyFinderApartmentsRent' or spider.name == 'PropertyFinderApartmentsSale':
        #     # print request.url
        #     # request.meta['proxy'] = "https://fr.proxymesh.com:31280"
        #     # # Use the following lines if your proxy requires authentication
        #     # proxy_user_pass = "bashar.z:Spiders123"
        #     # # setup basic authentication for the proxy
        #     # encoded_user_pass = base64.b64encode(proxy_user_pass)
        #     # request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
        # return None
