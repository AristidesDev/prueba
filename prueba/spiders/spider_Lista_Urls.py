import scrapy

class MercadolibreUrlsListSpider(scrapy.Spider):
    name = 'producto_urls'
    
    start_urls = [
        'https://listado.mercadolibre.com.ve/comida-preparada/_CostoEnvio_Gratis',
        'https://listado.mercadolibre.com.ve/comida-preparada/_CostoEnvio_Gratis_Desde_51',
        'https://listado.mercadolibre.com.ve/comida-preparada/_CostoEnvio_Gratis_Desde_101',
    ]

    # Se agrega esta configuración para evitar el error 403 Forbidden.
    # Simula una solicitud de navegador web real.

    def parse(self, response):
        products = response.xpath('//ol[contains(@class, "ui-search-layout")]/li')
        for product in products:
            name = product.xpath('.//h3[contains(@class, "poly-component__title-wrapper")]/a[contains(@class, "poly-component__title")]/text()').get()
            price_full = product.xpath('.//span[contains(@class, "andes-money-amount__fraction")]/text()').get()
            product_url = product.xpath('.//a[contains(@class, "poly-component__title")]/@href').get()
            
            yield {
                'nombre': name,
                'precio': price_full,
                'url_producto': product_url,
            }