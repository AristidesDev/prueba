# prueba/spiders/category_tree_spider.py

import scrapy
from prueba.items import CategoryItem

class CategoryTreeSpider(scrapy.Spider):
    name = "category_tree"
    # allowed_domains = ["www.mercadolibre.com.ve"]
    start_urls = ["https://www.mercadolibre.com.ve/categorias"]

    def parse(self, response):
        """
        Punto de entrada: solo para la página principal de /categorias.
        Extrae las categorías base y lanza las primeras llamadas recursivas.
        """
        self.logger.info('Parseando la página raíz de categorías.')
        
        # Selector para las categorías base en la página principal
        categories_base = response.xpath('.//div[contains(@class, "categories__container")]//h2')
        
        for category in categories_base:
            name = category.xpath('.//a/text()').get()
            url = category.xpath('.//a/@href').get()
            
            if name and url:
                nombre_limpio = name.strip()
                jerarquia = [nombre_limpio]
                
                # Crea el item para la categoría base
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = response.urljoin(url)
                item['jerarquia'] = jerarquia
                yield item

                # Llama a la función recursiva para explorar esta categoría
                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_recursive,
                    meta={'jerarquia': jerarquia}
                )

    def parse_recursive(self, response):
        """
        Función recursiva que se encarga de cualquier página de categoría/subcategoría.
        Busca tanto el layout de "tarjetas" como el de "filtros laterales".
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando: {" > ".join(jerarquia_actual)}')

        # Usamos un set para no procesar la misma URL dos veces en una misma página
        urls_procesadas = set()

        # --- Selector 1: Para el layout de "tarjetas" ---
        selector_tarjetas = './/div[contains(@class, "desktop__view-child")]//a'
        for category in response.xpath(selector_tarjetas):
            name = category.xpath('.//div/text()').get() or category.xpath('.//h3/text()').get()
            url = category.xpath('./@href').get()

            if name and url:
                url_completa = response.urljoin(url)
                if url_completa in urls_procesadas:
                    continue
                urls_procesadas.add(url_completa)
                
                nombre_limpio = name.strip()
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]

                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = url_completa
                item['jerarquia'] = nueva_jerarquia
                yield item

                yield scrapy.Request(
                    url=url_completa,
                    callback=self.parse_recursive,
                    meta={'jerarquia': nueva_jerarquia}
                )

        # --- Selector 2: Para los filtros de la barra lateral ---
        # Usualmente el primer bloque de filtros es el de categorías
        selector_sidebar = '(//li[contains(@class, "ui-search-filter-container")])[1]//li//a'
        for category in response.xpath(selector_sidebar):
            name = category.xpath('.//span/text()').get()
            url = category.xpath('./@href').get()

            if name and url:
                url_completa = response.urljoin(url)
                if url_completa in urls_procesadas:
                    continue
                urls_procesadas.add(url_completa)

                nombre_limpio = name.strip()
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]
                
                item = CategoryItem()
                item['nombre'] = nombre_limpio
                item['url'] = url_completa
                item['jerarquia'] = nueva_jerarquia
                yield item
                
                yield scrapy.Request(
                    url=url_completa,
                    callback=self.parse_recursive,
                    meta={'jerarquia': nueva_jerarquia}
                )