import scrapy
from prueba.items import CategoryItem

class CategoryTreeSpider(scrapy.Spider):
    name = "catego"

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
            # name = category_container.xpath('.//h2[contains(@class, "categories__title")]/a[contains(text(), "Antigüedades")]/text()').get()
            # url = category_container.xpath('.//h2[contains(@class, "categories__title")]/a[contains(text(), "Antigüedades")]/@href').get()
            # ------------------------------------------
            #Fin testiar una categoria
           
            if name and url:
                nombre_limpio = name.strip()
                jerarquia = [nombre_limpio]
                
                item = CategoryItem(nombre=nombre_limpio, url=response.urljoin(url), jerarquia=jerarquia)
                yield item

                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_level_1,
                    meta={'jerarquia': jerarquia}
                )

    def parse_level_1(self, response):
        """
        Función MODIFICADA: Ahora parsea la estructura de Primarias (H3) y Secundarias (H4 en LI)
        e identifica si una primaria es una hoja.
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando Nivel 1 (estructura compleja) para: {" > ".join(jerarquia_actual)}')

        # CAMBIO REALIZADO: Corregido el selector base según tu indicación.
        # Ahora se itera sobre los bloques de filas DENTRO del contenedor principal 'desktop__view-child'.
        for block in response.xpath('.//div[contains(@class, "desktop__view-child")]'):
            
            primary_link = block.xpath('.//h3/a')
            primary_name = primary_link.xpath('string(.)').get()
            primary_url = primary_link.xpath('./@href').get()

            if not (primary_name and primary_url):
                continue

            nombre_primario_limpio = " ".join(primary_name.strip().split())
            jerarquia_primaria = jerarquia_actual + [nombre_primario_limpio]
            
            secondary_links = block.xpath('.//ul/li/h4/a')
            
            if secondary_links:
                # Si HAY secundarias, la primaria NO es una hoja.
                # Producimos el item normal para la categoría primaria.
                item_primario = CategoryItem(nombre=nombre_primario_limpio, url=response.urljoin(primary_url), jerarquia=jerarquia_primaria)
                yield item_primario
                
                self.logger.debug(f'Primaria "{nombre_primario_limpio}" tiene {len(secondary_links)} secundarias.')
                for sec_link in secondary_links:
                    sec_name = sec_link.xpath('string(./div)').get()
                    sec_url = sec_link.xpath('./@href').get()
                    
                    if sec_name and sec_url:
                        nombre_secundario_limpio = " ".join(sec_name.strip().split())
                        jerarquia_secundaria = jerarquia_primaria + [nombre_secundario_limpio]
                        
                        item_secundario = CategoryItem(nombre=nombre_secundario_limpio, url=response.urljoin(sec_url), jerarquia=jerarquia_secundaria)
                        yield item_secundario
                        
                        yield scrapy.Request(
                            url=response.urljoin(sec_url),
                            callback=self.parse_subsequent_levels,
                            meta={'jerarquia': jerarquia_secundaria}
                        )
            else:
                # CAMBIO REALIZADO: Si NO HAY secundarias, esta primaria es una hoja.
                self.logger.info(f'--- Hoja encontrada en Nivel 1: "{nombre_primario_limpio}" ---')
                
                # Añadimos el marcador "Fin de Hoja" a la jerarquía.
                jerarquia_primaria.append("Fin de Hoja")
                
                # Producimos el item para la categoría primaria MARCADA como hoja.
                item_primario_hoja = CategoryItem(nombre=nombre_primario_limpio, url=response.urljoin(primary_url), jerarquia=jerarquia_primaria)
                yield item_primario_hoja
                
                # IMPORTANTE: No hacemos un Request porque ya sabemos que es el final de la rama.

    def parse_subsequent_levels(self, response):
        """
        Función recursiva para filtros laterales. MODIFICADA para detectar hojas.
        """
        jerarquia_actual = response.meta['jerarquia']
        self.logger.info(f'Parseando subniveles para: {" > ".join(jerarquia_actual)}')

        selector_sidebar = './/div[@class="ui-search-filter-dl" and .//h3[contains(text(), "Categor")]]//li'
        categories_sidebar = response.xpath(selector_sidebar)
        
        # CAMBIO REALIZADO: Si el selector no encuentra ninguna subcategoría,
        # significa que la página actual es una hoja del árbol.
        if not categories_sidebar:
            self.logger.info(f'--- Hoja encontrada en Subnivel: {" > ".join(jerarquia_actual)} ---')
            
            # Creamos un item final para esta categoría, marcándola como hoja.
            # El nombre de la categoría es el último elemento de la jerarquía actual.
            nombre_hoja = jerarquia_actual[-1]
            jerarquia_hoja = jerarquia_actual + ["Fin de Hoja"]

            item_hoja = CategoryItem(nombre=nombre_hoja, url=response.url, jerarquia=jerarquia_hoja)
            yield item_hoja
            return # Detenemos la recursión para esta rama.

        # Si encontramos categorías, el proceso continúa como antes.
        for category_item in categories_sidebar:
            name = category_item.xpath('.//a/span/text()').get()
            url = category_item.xpath('.//a/@href').get()

            if name and url and name.strip():
                nombre_limpio = " ".join(name.strip().split())
                nueva_jerarquia = jerarquia_actual + [nombre_limpio]
                
                item = CategoryItem(nombre=nombre_limpio, url=response.urljoin(url), jerarquia=nueva_jerarquia)
                yield item

                yield scrapy.Request(
                    url=response.urljoin(url),
                    callback=self.parse_subsequent_levels,
                    meta={'jerarquia': nueva_jerarquia}
                )