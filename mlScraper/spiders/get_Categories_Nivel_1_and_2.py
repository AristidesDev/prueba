import scrapy
import json
from pathlib import Path

class MercadolibreCategorias_1_Spider(scrapy.Spider):
    name = 'categorias_nivel_1and2'

    def __init__(self, categoria_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categoria_base = categoria_base

    def start_requests(self):
        base_path = Path(__file__).resolve().parent.parent.parent
        json_file = base_path / 'categorias/base/categorias_base.json'
        if not json_file.exists():
            self.logger.error(f"Archivo {json_file} no encontrado.")
            return
        try:
            with open(json_file, encoding='utf-8') as f:
                urls = json.load(f)
        except json.JSONDecodeError as e:
            self.logger.error(f"Error al parsear JSON: {e}")
            return
        for url in urls:
            nombre_base = url.get('nombre_categoria_base')
            link = url.get('url_categoria_base')
            if link and (self.categoria_base is None or nombre_base == self.categoria_base):
                # Pasa el nombre de la categoría base en meta
                yield scrapy.Request(url=link, callback=self.parse, meta={'nombre_categoria_base': nombre_base})

    def parse(self, response):
        nombre_base = response.meta.get('nombre_categoria_base')
        categories_1 = response.xpath('.//div[contains(@class, "desktop__view-child")]')
        for categorie in categories_1:
            name = categorie.xpath('.//h3/a/div/text()').get()
            categorie_url = categorie.xpath('.//h3/a/@href').get()

            categorias_nivel_2 = []
            # Verificar si tiene hijos de nivel 2
            if categorie.xpath('./ul/li'):
                for li in categorie.xpath('./ul/li'):
                    child_name = li.xpath('.//a/div/text()').get()
                    child_url = li.xpath('.//a/@href').get()
                    if child_name and child_url:
                        categorias_nivel_2.append({
                            'nombre_categoria_2': child_name,
                            'url_categoria_2': child_url
                        })

            if name and categorie_url: # Asegúrate de que ambos valores no sean None
                yield {
                    'categoria_base': nombre_base,
                    'nombre_categoria_1': name,
                    'url_categoria_1': categorie_url,
                    'categorias_nivel_2': categorias_nivel_2
                }
