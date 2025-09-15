import scrapy

class GetCategorieBaseSpider(scrapy.Spider):
    name = "get_categories_base"
    allowed_domains = ["www.mercadolibre.com.ve"]
    start_urls = ["https://www.mercadolibre.com.ve/categorias"] # URL de la página de categorías

    # Extrae las categorías base 
    def parse(self, response):
        categories_base = response.xpath('.//div[contains(@class, "categories__container")]') # este XPath obtine un div con la categoria base y las cotegorias primarias 
        for category_base in categories_base:
            name = category_base.xpath('.//h2[contains(@class, "categories__title")]/a/text()').get()
            categorie_url = category_base.xpath('.//h2[contains(@class, "categories__title")]/a/@href').get()
            
              # Busca categorías primarias dentro de la categoría base
#             primary = []
#             for category_primary in category_base.xpath('.//li[contains(@class, "categories__item")]'): # Ajusta el XPath según la estructura real de la página
#                 name_category_primary = category_base.xpath('.//a/h3/text()').get()
#                 url_category_primary = category_primary.xpath('.//a/@href').get()
#                 if name_category_primary and url_category_primary:
#                     primary.append({
#                         'nombre_categoria_secundaria': name_category_primary,
#                         'url_categoria_secundaria': url_category_primary,
#                     }) 

            if name and categorie_url: # Asegúrate de que ambos valores no sean None
                yield {
                    'nombre_categoria_base': name,
                    'url_categoria_base': categorie_url,
                    # 'categoria_primary': primary,
                    }       