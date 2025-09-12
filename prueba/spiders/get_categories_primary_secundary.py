import scrapy


class GetCategoriesPrimarySecundarySpider(scrapy.Spider):
    name = "get_categories_primary_secundary"
    allowed_domains = ["www.mercadolibre.com.ve"]
    start_urls = ["https://www.mercadolibre.com.ve/categorias#menu=categories"]

    # Extrae las categorías principales y secundarias       
    # Extrae las subcategorías
    def parse(self, response):
        contenedor_Categories = response.xpath('.//div[contains(@class, "categories__container")]') # Ajusta el XPath según la estructura real de la página   
        for category_primary in contenedor_Categories:        
            name_category_primary = category_primary.xpath('.//a/text()').get()
            url_category_primary = category_primary.xpath('.//a/@href').get()
            
            # Busca subcategorías dentro de la categoría primaria
            secundarias = []
            for category_secundary in category_primary:
                name_category_secundary = category_secundary.xpath('.//a/text()').get()
                url_category_secundary = category_secundary.xpath('.//a/@href').get()
                if name_category_secundary and url_category_secundary:
                    secundarias.append({
                        'nombre_categoria_secundaria': name_category_secundary,
                        'url_categoria_secundaria': url_category_secundary,
                    })
                    
            if name_category_primary and url_category_primary:
                yield {
                    'nombre': name_category_primary,
                    'url_categoria': url_category_primary,
                    'secundarias': secundarias,
                }   