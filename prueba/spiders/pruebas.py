import scrapy
import json

class MercadolibreCategorias1Spider(scrapy.Spider):
    name = 'prueba'

    # allowed_domains = ['www.mercadolibre.com.ve']
    # start_urls = ["https://listado.mercadolibre.com.ve/bebidas/#CATEGORY_ID=MLV178700&S=hc_alimentos-y-bebidas&c_tracking_id=0f111880-93f3-11f0-ae82-3db4a47c6659"] # URL de la página de categorías
    
    def start_requests(self):
        with open('c:/Users/Impresos Salcedo/Desktop/python/ML/Scrapy/Learning/test/prueba/categorias_1.json', encoding='utf-8') as f:
            categorias = json.load(f)
        for categoria in categorias:
            url = categoria.get('url_categoria_1')
            nombre_categoria_1 = categoria.get('nombre_categoria_1')
            categoria_base = categoria.get('categoria_base')
            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={
                        'nombre_categoria_1': nombre_categoria_1,
                        'categoria_base': categoria_base
                    }
                )

    def parse(self, response):
        categoria_1 = response.meta.get('nombre_categoria_1')
        categoria_base = response.meta.get('categoria_base')
        categories_2 = response.xpath('.//li[contains(@class, "ui-search-filter-container")]')
        for categorie_2 in categories_2:
            name = categorie_2.xpath('.//a/span/text()').get()
            categorie_url = categorie_2.xpath('.//a/@href').get()
            yield {
                'nombre_categoria_2': name,
                'url_categoria_2': categorie_url,
                'categoria_base': categoria_base,
                'categoria_1': categoria_1,

            }