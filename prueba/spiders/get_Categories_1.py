import scrapy
import json

class MercadolibreCategorias_1_Spider(scrapy.Spider):
    name = 'categorias_1'

    def start_requests(self):
        with open('c:/Users/Impresos Salcedo/Desktop/python/ML/Scrapy/Learning/test/prueba/Categories_base.json', encoding='utf-8') as f:
            urls = json.load(f)
        for url in urls:
            nombre_base = url.get('nombre_categoria_base')
            link = url.get('url_categoria_base')
            if link:
                # Pasa el nombre de la categoría base en meta
                yield scrapy.Request(url=link, callback=self.parse, meta={'nombre_categoria_base': nombre_base})

    def parse(self, response):
        nombre_base = response.meta.get('nombre_categoria_base')
        categories_1 = response.xpath('.//div[contains(@class, "desktop__view-child")]')
        for categorie in categories_1:
            name = categorie.xpath('.//h3/a/div/text()').get()
            categorie_url = categorie.xpath('.//h3/a/@href').get()
            
            if name and categorie_url: # Asegúrate de que ambos valores no sean None
                yield {
                    'nombre_categoria_1': name,
                    'url_categoria_1': categorie_url,
                    'categoria_base': nombre_base,
                    }
