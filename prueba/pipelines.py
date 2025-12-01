import json
import os
from itemadapter import ItemAdapter
from scrapy.exceptions import DropItem

class JsonPipeline:

    def open_spider(self, spider):
        if spider.name == 'categorias_base':
            self.items = []
        elif spider.name == 'categorias_subsecuentes_levels':
            self.items = []
        else:
            self.items_by_base = {}

    def close_spider(self, spider):
        if spider.name == 'categorias_base':
            filename = 'categorias/base/categorias_base.json'
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.items, f, ensure_ascii=False, indent=4)
        elif spider.name == 'categorias_subsecuentes_levels':
            filename = f"categorias/otros_niveles/{spider.categoria_base}.json"
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump(self.items, f, ensure_ascii=False, indent=4)
        else:
            for base, items in self.items_by_base.items():
                filename = f"categorias/nivel_1_2/{base}.json"
                os.makedirs(os.path.dirname(filename), exist_ok=True)
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(items, f, ensure_ascii=False, indent=4)

    def process_item(self, item, spider):
        if spider.name == 'categorias_base':
            self.items.append(dict(item))
        elif spider.name == 'categorias_subsecuentes_levels':
            self.items.append(dict(item))
        else:
            base = item.get('categoria_base')
            if base:
                if base not in self.items_by_base:
                    self.items_by_base[base] = []
                self.items_by_base[base].append(dict(item))
        return item

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
        with open('categorias_tree_alimentos.json', 'w', encoding='utf-8') as f:
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
                if adapter.get('is_leaf'):
                    node['is_leaf'] = True

            # Movemos 'current_level' para que apunte a la lista de hijos del nodo actual,
            # preparándonos para la siguiente iteración del bucle.
            current_level = node['children']

        # Al final, levantamos DropItem para decirle a Scrapy que no continúe
        # procesando este item con otros pipelines o con el exportador de feeds.
        # Ya lo hemos "guardado" en nuestra estructura en memoria.
        raise DropItem("Item procesado y añadido a la estructura anidada.")