from django.apps import AppConfig
import algoliasearch_django as algoliasearch
from algoliasearch_django import AlgoliaIndex


class PortalConfig(AppConfig):
    name = 'portal'

    def ready(self):
        Product = self.get_model('Product')
        algoliasearch.register(Product, ProductIndex)


class ProductIndex(AlgoliaIndex):
    fields = ('id', 'name', 'short_description', 'description', 'slug', 'price')
    settings = {'searchableAttributes': ['name', 'description']}
    index_name = 'product_index'
