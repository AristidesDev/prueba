import scrapy
import json
import os
from pathlib import Path

class MercadolibreCategorias1Spider(scrapy.Spider):
    name = 'categorias_3'
    # start_urls = ["https://listado.mercadolibre.com.ve/bebidas-aguas/", 
    # "https://listado.mercadolibre.com.ve/bebidas-blancas-licores/",
    # "https://listado.mercadolibre.com.ve/bebidas-deportivas/",
    # ]


    def start_requests(self):
        with open('c:/Users/Impresos Salcedo/Desktop/python/ML/Scrapy/Learning/test/prueba/Categorias_2.json', encoding='utf-8') as f:
            categorias = json.load(f)
        for categoria in categorias:
            url = categoria.get('url_categoria_2')
            categoria_2 = categoria.get('nombre_categoria_2')
            categoria_1 = categoria.get('categoria_1')
            categoria_base = categoria.get('categoria_base')
            print(f'Iniciando scraping de la categoría: {categoria_2} - {url} - {categoria_1} - {categoria_base}')
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
        # Asumimos que la carpeta 'categorias_json' está en el directorio raíz del proyecto Scrapy.
        # Path(__file__) se refiere a este archivo. .parent.parent.parent nos lleva a la raíz del proyecto.
        project_root = Path(__file__).resolve().parent.parent.parent
        json_dir = project_root / 'categorias_json'

        if not json_dir.exists():
            self.logger.error(f"El directorio '{json_dir}' no existe. Asegúrate de ejecutar primero el script para separar los JSON.")
            return

        for json_file in json_dir.glob('*.json'):
            with open(json_file, 'r', encoding='utf-8') as f:
                categorias = json.load(f)
            
            for categoria in categorias:
                url = categoria.get('url_categoria_2')
                categoria_2 = categoria.get('nombre_categoria_2')
                categoria_1 = categoria.get('categoria_1')
                categoria_base = categoria.get('categoria_base')
                self.logger.info(f'Iniciando scraping de la categoría: {categoria_2} - {url} - {categoria_1} - {categoria_base}')
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