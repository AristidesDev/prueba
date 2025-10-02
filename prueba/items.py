# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class CategoryItem(scrapy.Item):
    # Define los campos para tu item
    nombre = scrapy.Field()
    url = scrapy.Field()
    jerarquia = scrapy.Field() # Ej: ["Accesorios para Vehículos", "Audio para Vehículos", "Antenas"


