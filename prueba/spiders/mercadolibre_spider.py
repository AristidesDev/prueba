import scrapy

class MercadoLibreSpider(scrapy.Spider):
    name = 'mercadolibre_spider'
    
    start_urls = ['https://listado.mercadolibre.com.ve/comida-preparada/_CostoEnvio_Gratis']
    
    # Se agrega esta configuración para evitar el error 403 Forbidden.
    # Simula una solicitud de navegador web real.
    custom_settings = {
        'USER_AGENT': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/108.0.0.0 Safari/537.36'
    }

    def parse(self, response):
        # Selecciona el contenedor que agrupa cada producto.
        # Usa XPath para encontrar los elementos que representan cada producto en la lista.
        products = response.xpath('/html/body/main/div/div[2]/section/div[5]/ol/li')

        # Recorre cada producto en la lista.
        for product in products:
            # Extrae el nombre, el precio y la URL de la imagen de cada producto.
            # Los selectores se aplican de forma relativa al contenedor de cada producto.
            name = product.xpath('.//a[contains(@class, "poly-component__title")]/text()').get()
            price_full = product.xpath('.//span[contains(@class, "andes-money-amount__fraction")]/text()').get()
            product_url = product.xpath('.//a[contains(@class, "poly-component__title")]/@href').get()
            
            # Crea un diccionario con los datos extraídos para exportarlos.
            yield {
                'nombre': name,
                'precio': price_full,
                'url_producto': product_url,
            }

        # Lógica de paginación para pasar a la siguiente página.
        # Busca el enlace al botón "Siguiente" con el selector XPath corregido.
        next_page_link = response.xpath('//a[@title="Siguiente"]/@href').get()
        
        # Si el enlace a la siguiente página existe, crea una nueva solicitud para esa URL.
        if next_page_link:
            yield scrapy.Request(url=next_page_link, callback=self.parse)