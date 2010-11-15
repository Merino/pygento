import xmlrpclib
import base64

class NotConnected(Exception):
    pass

class MagentoConnection(object):
    def __init__(self, url, username, apikey):
        self.url = url
        self.username = username
        self.apikey = apikey
        self.connect()
        
    def connect(self):
        '''Connect to Magento's xmlrpc'''
        self.server = xmlrpclib.ServerProxy(self.url)
        self.token = self.server.login(self.username, self.apikey)
        
    def _call(self, res, *args, **kwargs):
        if not self.token:
            raise NotConnected()
        return self.server.call(self.token, res, *args, **kwargs)
        
class Magento(MagentoConnection):
    
    #PRODUCT OPERATIONS
    def getProductInfo(self, sku):
        '''Gives the product info'''
        return self._call('catalog_product.info', [sku])

    def updateProductData(self, sku, productdata):
        '''Updates the products for the product with the given sku'''
        return self._call('catalog_product.update', [sku, productdata])
    
    #IMAGE OPERATIONS
    def getImagesOfProducts(self, sku):
        '''Retrieves all images of a product'''
        return self._call('catalog_product_attribute_media.list', [sku])
    
    def removeImageOfProduct(self, sku, image_location):
        '''Remove a image of a product'''
        return self._call('catalog_product_attribute_media.remove', [sku, image_location])
    
    def addImageToProduct(self, sku, image_path, exclude=False, position=0, types=[]):
        '''Adds an image to a product'''
        image_file = open(image_path, "rb")
        encoded_string = base64.b64encode(image_file.read())
        image_data = {'exclude': exclude,
                      'position': position,
                      'types': types,
                      'file': {'content': encoded_string, 
                               'mime': 'image/jpeg'}}
        return self._call('catalog_product_attribute_media.create', [sku, image_data])
            
if __name__ == "__main__":
    MAGENTO_XMLRPC_URL = 'http://www.yourmagento.com/index.php/api/xmlrpc/'

    magento = Magento(url=MAGENTO_XMLRPC_URL, 
                      username="username", 
                      apikey="apikey")
