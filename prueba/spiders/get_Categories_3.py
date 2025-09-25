import scrapy
import json

class MercadolibreCategorias1Spider(scrapy.Spider):
    name = 'categorias_3'
    # start_urls = ["https://listado.mercadolibre.com.ve/bebidas-aguas/", 
    # "https://listado.mercadolibre.com.ve/bebidas-blancas-licores/",
    # "https://listado.mercadolibre.com.ve/bebidas-deportivas/",
    # ]


    def start_requests(self):
        with open('c:/Users/Impresos Salcedo/Desktop/python/ML/Scrapy/Learning/test/prueba/categorias_2.json', encoding='utf-8') as f:
            categorias = json.load(f)
        for categoria in categorias:
            url = categoria.get('url_categoria_2')
            categoria_2 = categoria.get('nombre_categoria_2')
            categoria_1 = categoria.get('categoria_1')
            categoria_base = categoria.get('categoria_base')
            if url:
                yield scrapy.Request(
                    url=url,
                    callback=self.parse,
                    meta={
                        'nombre_categoria_2': categoria_2,
                        'nombre_categoria_1': categoria_1,
                        'categoria_base': categoria_base
                    }
                )

    def parse(self, response):
        categoria_2 = response.meta.get('nombre_categoria_2')
        categoria_1 = response.meta.get('nombre_categoria_1')
        categoria_base = response.meta.get('categoria_base')
        categories_3 = response.xpath('.//li[contains(@class, "ui-search-filter-container")]')
        for categorie_3 in categories_3:
            name = categorie_3.xpath('.//a/span/text()').get()
            categorie_url = categorie_3.xpath('.//a/@href').get()
            yield {
                'nombre_categoria_3': name,
                'url_categoria_3': categorie_url,
                'categoria_2': categoria_2,
                'categoria_1': categoria_1,
                'categoria_base': categoria_base,

            }