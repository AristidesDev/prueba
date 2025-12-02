import scrapy
import json
from pathlib import Path
from ..items import CategoryItem

class MercadolibreCategorias1Spider(scrapy.Spider):
    name = 'categorias_subsecuentes_levels'

    def __init__(self, categoria_base=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.categoria_base = categoria_base
        self.processed_hierarchies = set()

    def start_requests(self):
        if not self.categoria_base:
            self.logger.error("Debe proporcionar el argumento categoria_base")
            return
        json_file = Path(__file__).resolve().parent.parent.parent / 'categorias' / 'nivel_1_2' / f'{self.categoria_base}.json'
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
            categoria_base = categoria.get('categoria_base')
            nombre_categoria_1 = categoria.get('nombre_categoria_1')
            url_categoria_1 = categoria.get('url_categoria_1')
            categorias_nivel_2 = categoria.get('categorias_nivel_2', [])
            if categorias_nivel_2:
                # Procesar todos los elementos de nivel 2
                for cat_2 in categorias_nivel_2:
                    nombre = cat_2.get('nombre_categoria_2')
                    url = cat_2.get('url_categoria_2')
                    jerarquia = [categoria_base, nombre_categoria_1, nombre]
                    if nombre and url:
                        yield scrapy.Request(url=url, callback=self.parse_subsequent_levels, meta={'jerarquia': jerarquia})
            else:
                nombre = nombre_categoria_1
                url = url_categoria_1
                jerarquia = [categoria_base, nombre]
                if nombre and url:
                    yield scrapy.Request(url=url, callback=self.parse_subsequent_levels, meta={'jerarquia': jerarquia})

    def parse_subsequent_levels(self, response):
        """
        Función recursiva que extrae subcategorías de los filtros laterales (Nivel 2, 3, 4...).
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando subniveles para: {" > ".join(jerarquia_actual)}')

        # **XPath CORREGIDO Y PRECISO (basado en tu sugerencia)**
        # Selecciona solo los 'li' dentro del div de filtros cuyo h3 contiene "Categor".
        selector_sidebar = './/div[@class="ui-search-filter-dl" and .//h3[contains(text(), "Categor")]]/ul/li'

        categories_sidebar = response.xpath(selector_sidebar)

        # Yield item for current page
        jerarquia_tuple = tuple(jerarquia_actual)
        if jerarquia_tuple not in self.processed_hierarchies:
            self.processed_hierarchies.add(jerarquia_tuple)
            item = CategoryItem()
            item['nombre'] = jerarquia_actual[-1]
            item['url'] = response.url
            item['jerarquia'] = jerarquia_actual
            item['is_leaf'] = not categories_sidebar
            yield item

        if not categories_sidebar:
            self.logger.info(f'--- Hoja final del árbol: {" > ".join(jerarquia_actual)} ---')
            return

        for category_item in categories_sidebar:
            # Ahora extraemos el enlace 'a' que está dentro del 'li'
            name = category_item.xpath('.//a/span/text()').get()
            url = category_item.xpath('.//a/@href').get()

            if name and url and name.strip():
                nombre_limpio = " ".join(name.strip().split())
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]
                jerarquia_tuple = tuple(nueva_jerarquia)

                if jerarquia_tuple not in self.processed_hierarchies:
                    yield scrapy.Request(
                        url=response.urljoin(url),
                        callback=self.parse_subsequent_levels,
                        meta={'jerarquia': nueva_jerarquia}
                    )