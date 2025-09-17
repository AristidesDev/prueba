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
            
            if name and categorie_url: # Asegúrate de que ambos valores no sean None
                yield {
                    'nombre_categoria_base': name,
                    'url_categoria_base': categorie_url,
                    # 'categoria_primary': primary,
                    }       