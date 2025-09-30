import json
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class NestedJsonPipeline:

    def open_spider(self, spider):
        """
        Se ejecuta cuando la araña se abre.
        Aquí inicializamos la estructura que contendrá nuestros datos anidados.
        """
        self.results = []
        # Usamos un set para rastrear las jerarquías ya agregadas y evitar duplicados.
        self.processed_hierarchies = set()

    def close_spider(self, spider):
        """
        Se ejecuta cuando la araña se cierra.
        Aquí guardamos la estructura de árbol completa en un archivo JSON.
        """
        # Abre el archivo de salida en modo escritura con codificación UTF-8
        with open('categorias_anidadas.json', 'w', encoding='utf-8') as f:
            # json.dump escribe la estructura de datos en el archivo.
            # ensure_ascii=False permite que se guarden caracteres como tildes correctamente.
            # indent=4 hace que el archivo JSON sea legible para los humanos.
            json.dump(self.results, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        """
        Se ejecuta para cada item que la araña produce (yield).
        Esta es la lógica principal para construir el árbol.
        """
        adapter = ItemAdapter(item)
        jerarquia = adapter.get('jerarquia', [])
        
        # Convertimos la jerarquía a una tupla para poder guardarla en el set
        jerarquia_tuple = tuple(jerarquia)
        if jerarquia_tuple in self.processed_hierarchies:
            # Si ya procesamos esta categoría exacta, la ignoramos.
            raise DropItem(f"Categoría duplicada encontrada: {jerarquia}")
        
        self.processed_hierarchies.add(jerarquia_tuple)

        # 'current_level' apunta a la lista de 'hijos' donde debemos buscar o insertar.
        # Al principio, apunta a la lista raíz `self.results`.
        current_level = self.results

        # Recorremos la jerarquía para encontrar el lugar correcto donde insertar el item
        for i, nombre_categoria in enumerate(jerarquia):
            # Buscamos si un nodo con este nombre ya existe en el nivel actual
            node = next((x for x in current_level if x.get('nombre') == nombre_categoria), None)

            if node is None:
                # Si el nodo no existe, lo creamos.
                node = {
                    'nombre': nombre_categoria,
                    'url': None, # La URL se asignará si este es el último nivel
                    'children': []
                }
                current_level.append(node)

            # Si estamos en el último elemento de la jerarquía, es nuestro item actual.
            # Actualizamos su URL, ya que la que creamos por defecto podría ser None.
            if i == len(jerarquia) - 1:
                node['url'] = adapter.get('url')

            # Movemos 'current_level' para que apunte a la lista de hijos del nodo actual,
            # preparándonos para la siguiente iteración del bucle.
            current_level = node['children']

        # Al final, levantamos DropItem para decirle a Scrapy que no continúe
        # procesando este item con otros pipelines o con el exportador de feeds.
        # Ya lo hemos "guardado" en nuestra estructura en memoria.
        raise DropItem("Item procesado y añadido a la estructura anidada.")