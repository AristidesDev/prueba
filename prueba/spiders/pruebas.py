# prueba/spiders/category_tree_spider.py

import scrapy
from prueba.items import CategoryItem

class CategoryTreeSpider(scrapy.Spider):
    name = "category_tree_1"
    # Hemos ampliado los dominios permitidos para incluir los subdominios que usa ML
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
        Punto de entrada. Extrae las categorías base (Nivel 0, Ej: "Accesorios para Vehículos").
        """
        self.logger.info('Parseando la página principal de categorías...')
        
        # Iteramos sobre cada bloque de categoría principal
        for category_container in response.xpath('//div[contains(@class, "categories__container")]'):
            name = category_container.xpath('.//h2[contains(@class, "categories__title")]/a/text()').get()
            url = category_container.xpath('.//h2[contains(@class, "categories__title")]/a/@href').get()
            
            if name and url:
                nombre_limpio = name.strip()
                # La jerarquía inicial solo contiene el nombre de la categoría base
                jerarquia = [nombre_limpio]
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = jerarquia
                yield item

                # Pasamos la jerarquía inicial a la siguiente función de parseo
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_level_1,
                    meta={'jerarquia': jerarquia}
                )

    def parse_level_1(self, response):
        """
        Extrae las categorías de Nivel 1 (Ej: "Audio para Vehículos") que se muestran como tarjetas.
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando Nivel 1 para: {" > ".join(jerarquia_actual)}')

        # Selector para las categorías que se muestran como "tarjetas"
        categories_l1 = response.xpath('.//div[contains(@class, "desktop__view-child")]')

        for category in categories_l1:
            name = category.xpath('.//h3/a/div/text()').get() # Usamos text() para obtener todo el texto
            url = category.xpath('..//h3/a/@href').get()

            if name and url and name.strip():
                nombre_limpio = " ".join(name.strip().split())
                # **CLAVE:** Creamos la nueva jerarquía añadiendo el nombre actual a la jerarquía del padre
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = nueva_jerarquia
                yield item
                
                # Pasamos la jerarquía COMPLETA Y ACTUALIZADA a la siguiente función
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

        # XPath mejorado para apuntar solo al filtro de "Categorías"
        selector_sidebar = [
        './/div[@class="ui-search-filter-dl"][./h3[contains(text(), "Categorías")]]/ul/li',
        './/div[@class="ui-search-filter-dl"][./h3[contains(text(), "Categorias")]]/ul/li',                 
        ]
        categories_sidebar = response.xpath(selector_sidebar)
        
        if not categories_sidebar:
            self.logger.info(f'--- Hoja final del árbol: {" > ".join(jerarquia_actual)} ---')
            return

        for category in categories_sidebar:
            name = category.xpath('.//span/text()').get()
            url = category.xpath('.//a/@href').get()

            if name and url and name.strip():
                nombre_limpio = " ".join(name.strip().split())
                # **CLAVE:** De nuevo, construimos la jerarquía completa
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = nueva_jerarquia
                yield item

                # **RECURSIÓN:** Llamamos a esta misma función, pasando la nueva jerarquía completa
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_subsequent_levels,
                    meta={'jerarquia': nueva_jerarquia}
                )