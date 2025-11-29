import scrapy
import json
from pathlib import Path

class MercadolibreCategorias1Spider(scrapy.Spider):
    name = 'categorias_2'

    def start_requests(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        json_file = base_path / 'Categorias_1.json'
        if not json_file.exists():
            self.logger.error(f"Archivo {json_file} no encontrado.")
            return
        try:
            with open(json_file, encoding='utf-8') as f:
                categorias = json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error al parsear JSON: {e}")
            return
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