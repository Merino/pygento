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
        
    def updateImageOfProducts(self, sku, image_location, image_data):
        '''Update image data of a image'''
        return self._call('catalog_product_attribute_media.update', [sku, image_location, image_data])
    
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
        
    #CATEGORY OPERARTIONS
    def createCategory(self, parent_category_id, categorydata):
        '''Create a category'''
        return self._call('catalog_category.create', [parent_category_id, categorydata])
        
    def assignProduct(self, category_id, product_sku):
        '''Assign a product to a category'''
        return self._call('catalog_category.assignProduct', [category_id, product_sku])
        
    def updateCategory(self, category_id, categorydata):
        '''Update a category'''
        return self._call('catalog_category.update', [category_id, categorydata])
        
    def moveCategory(self, category_id, parent_id):
        '''Move category into another category'''
        return self._call('catalog_category.move', [category_id, parent_id])
        
    def treeCategory(self, parent_id):
        '''Retrieve category tree'''
        return self._call('catalog_category.tree', [parent_id,])
        
    def assignedProducts(self, category_id, store_id):
        '''Retrieve all assigned products'''
        return self._call('catalog_category.assignedProducts', [category_id, store_id])
                
        
if __name__ == "__main__":
    MAGENTO_XMLRPC_URL = 'http://www.yourmagento.com/index.php/api/xmlrpc/'

    magento = Magento(url=MAGENTO_XMLRPC_URL, 
                      username="username", 
                      apikey="apikey")
