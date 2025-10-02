# prueba/spiders/pruebas.py

import scrapy
from prueba.items import CategoryItem

class CategoryTreeSpider(scrapy.Spider):
    name = "category_tree"

    allowed_domains = [
        "www.mercadolibre.com.ve",
        "listado.mercadolibre.com.ve",
        "vehiculos.mercadolibre.com.ve",
        "inmuebles.mercadolibre.com.ve",
        "servicios.mercadolibre.com.ve",
        "carros.mercadolibre.com.ve",
        "motos.mercadolibre.com.ve"
    ]
    start_urls = ["https://www.mercadolibre.com.ve/categorias"]

    def parse(self, response):
        """
        Punto de entrada. Extrae las categorías base (Nivel 0).
        """
        self.logger.info('Parseando la página principal de categorías...')
        
        for category_container in response.xpath('//div[contains(@class, "categories__container")]'):
            name = category_container.xpath('.//h2[contains(@class, "categories__title")]/a/text()').get()
            url = category_container.xpath('.//h2[contains(@class, "categories__title")]/a/@href').get()
            
            # testiar una categoria
            #-------------------------------------------
            # name = category_container.xpath('.//h2[contains(@class, "categories__title")]/a[contains(text(), "Alimentos ")]/text()').get()
            # url = category_container.xpath('.//h2[contains(@class, "categories__title")]/a[contains(text(), "Alimentos ")]/@href').get()
            # ------------------------------------------
            #Fin testiar una categoria

            if name and url:
                nombre_limpio = name.strip()
                jerarquia = [nombre_limpio]
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = jerarquia
                yield item

                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_level_1,
                    meta={'jerarquia': jerarquia}
                )

    def parse_level_1(self, response):
        """
        Extrae las categorías de Nivel 1 (las que están en los H3 de las tarjetas).
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando Nivel 1 para: {" > ".join(jerarquia_actual)}')

        categories_l1 = response.xpath('.//div[contains(@class, "desktop__view-child")]//h3/a')

        if not categories_l1:
            self.logger.warning(f"No se encontró el layout de H3 en {response.url}. Pasando a la lógica de filtros laterales.")
            yield from self.parse_subsequent_levels(response)
            return

        for category_link in categories_l1:
            name = category_link.xpath('string(.)').get()
            url = category_link.xpath('./@href').get()

            if name and url and name.strip():
                nombre_limpio = " ".join(name.strip().split())
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = nueva_jerarquia
                yield item
                
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_subsequent_levels,
                    meta={'jerarquia': nueva_jerarquia}
                )

    def parse_subsequent_levels(self, response):
        """
        Función recursiva que extrae subcategorías de los filtros laterales (Nivel 2, 3, 4...).
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando subniveles para: {" > ".join(jerarquia_actual)}')

        # **XPath CORREGIDO Y PRECISO (basado en tu sugerencia)**
        # Selecciona solo los 'li' dentro del div de filtros cuyo h3 contiene "Categor".
        selector_sidebar = './/div[@class="ui-search-filter-dl" and .//h3[contains(text(), "Categor")]]//li'
        
        categories_sidebar = response.xpath(selector_sidebar)
        
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
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = nueva_jerarquia
                yield item

                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_subsequent_levels,
                    meta={'jerarquia': nueva_jerarquia}
                )