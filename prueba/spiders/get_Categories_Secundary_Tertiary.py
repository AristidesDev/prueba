import scrapy

class GetCategorieBaseSpider(scrapy.Spider):
    name = "get_categories_primary_segundary"
    allowed_domains = ["www.mercadolibre.com.ve"]
    start_urls = ["https://www.mercadolibre.com.ve/c/alimentos-y-bebidas"]

    def parse(self, response):
        categories_primary = response.xpath('.//div[contains(@class, "andes-card")]/div/div')
        for category in categories_primary:
            name = category.xpath('.//h3[contains(@class, "category-list-item")]/a/div/text()').get()
            categorie_url = category.xpath('.//h3[contains(@class, "category-list-item")]/a/@href').get()
            
            # # Busca categorías secundaria dentro de la categoría primaria
            secundary = []
            for category_secundary in category.xpath('.//li[contains(@class, "category-list__item")]'):
                name_category_secundary = category_secundary.xpath('.//h4/a/div/text()').get()
                url_category_secundary = category_secundary.xpath('.//h4/a/@href').get()
                if name_category_secundary and url_category_secundary:
                    secundary.append({
                        'nombre_categoria_secundaria': name_category_secundary.strip(),
                        'url_categoria_secundaria': url_category_secundary,
                    })

            if name and categorie_url:
                yield {
                    'nombre_categoria_base': name.strip(),
                    'url_categoria_base': categorie_url,
                    'categoria_primary': secundary,
                }