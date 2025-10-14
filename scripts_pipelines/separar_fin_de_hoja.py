import json
from collections import defaultdict

def normalizar_jerarquia(jerarquia):
    """Normaliza la jerarquía removiendo 'Fin de Hoja' del final si está presente"""
    if jerarquia and jerarquia[-1] == "Fin de Hoja":
        return jerarquia[:-1]
    return jerarquia

def agregar_categorias_individuales(datos, categorias_fin_hoja, jerarquias_fin_hoja_vistas):
    """Agrega al diccionario urls_fin_hoja los elementos que solo tienen un elemento en la jerarquía"""
    for item in datos:
        jerarquia = item["jerarquia"]
        
        # Verificar si la jerarquía tiene solo un elemento
        if len(jerarquia) == 1:
            jerarquia_normalizada = tuple(jerarquia)
            
            # Si no hemos visto esta jerarquía normalizada antes, agregarla
            if jerarquia_normalizada not in jerarquias_fin_hoja_vistas:
                categorias_fin_hoja[len(categorias_fin_hoja)] = item
                jerarquias_fin_hoja_vistas.add(jerarquia_normalizada)
    
    return categorias_fin_hoja, jerarquias_fin_hoja_vistas

def separar_categorias(datos):
    # Diccionarios para almacenar las categorías separadas
    categorias_fin_hoja = {}
    categorias_sin_fin_hoja = {}
    
    # Conjuntos para verificar duplicados (usando jerarquías normalizadas)
    jerarquias_fin_hoja_vistas = set()
    jerarquias_sin_fin_hoja_vistas = set()
    
    # Primero, agregar las categorías con "Fin de Hoja" y las categorías especiales
    for item in datos:
        jerarquia = item["jerarquia"]
        jerarquia_normalizada = tuple(normalizar_jerarquia(jerarquia))
        
        # Verificar si es una categoría con 3 elementos y el tercero es "Fin de Hoja"
        es_categoria_especial = len(jerarquia) == 3 and jerarquia[-1] == "Fin de Hoja"
        
        # Para categorías con "Fin de Hoja"
        if "Fin de Hoja" in jerarquia:
            # Si no hemos visto esta jerarquía normalizada antes, agregarla
            if jerarquia_normalizada not in jerarquias_fin_hoja_vistas:
                categorias_fin_hoja[len(categorias_fin_hoja)] = item
                jerarquias_fin_hoja_vistas.add(jerarquia_normalizada)
        
        # Para categorías sin "Fin de Hoja" O categorías especiales
        if not "Fin de Hoja" in jerarquia or es_categoria_especial:
            # Si es una categoría especial, crear una versión modificada sin "Fin de Hoja"
            if es_categoria_especial:
                item_modificado = item.copy()
                item_modificado["jerarquia"] = jerarquia[:-1]  # Remover "Fin de Hoja"
                jerarquia_para_comparar = tuple(jerarquia[:-1])
            else:
                item_modificado = item
                jerarquia_para_comparar = tuple(jerarquia)
            
            # Si no hemos visto esta jerarquía antes, agregarla al archivo sin fin de hoja
            if jerarquia_para_comparar not in jerarquias_sin_fin_hoja_vistas:
                categorias_sin_fin_hoja[len(categorias_sin_fin_hoja)] = item_modificado
                jerarquias_sin_fin_hoja_vistas.add(jerarquia_para_comparar)
    
    # Ahora, agregar las categorías que solo tienen un elemento en la jerarquía
    categorias_fin_hoja, jerarquias_fin_hoja_vistas = agregar_categorias_individuales(
        datos, categorias_fin_hoja, jerarquias_fin_hoja_vistas
    )
    
    return categorias_fin_hoja, categorias_sin_fin_hoja

def guardar_archivos(categorias_fin_hoja, categorias_sin_fin_hoja):
    # Convertir los diccionarios a listas para guardar como JSON
    lista_fin_hoja = list(categorias_fin_hoja.values())
    lista_sin_fin_hoja = list(categorias_sin_fin_hoja.values())
    
    # Guardar archivo con categorías que tienen "Fin de Hoja"
    with open('urls_fin_hoja.json', 'w', encoding='utf-8') as f:
        json.dump(lista_fin_hoja, f, ensure_ascii=False, indent=2)
    
    # Guardar archivo con categorías que no tienen "Fin de Hoja"
    with open('categorias_para_arbol.json', 'w', encoding='utf-8') as f:
        json.dump(lista_sin_fin_hoja, f, ensure_ascii=False, indent=2)
    
    return len(lista_fin_hoja), len(lista_sin_fin_hoja)

# Cargar el archivo JSON original
with open('categorias_flat.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# Separar las categorías
categorias_fin_hoja, categorias_sin_fin_hoja = separar_categorias(datos)

# Guardar los archivos
cantidad_fin_hoja, cantidad_sin_fin_hoja = guardar_archivos(categorias_fin_hoja, categorias_sin_fin_hoja)

# Mostrar resumen
print("RESUMEN DE LA SEPARACIÓN:")
print(f"Total de elementos en el JSON original: {len(datos)}")
print(f"Elementos en 'urls_fin_hoja.json': {cantidad_fin_hoja}")
print(f"Elementos en 'categorias_para_arbol.json': {cantidad_sin_fin_hoja}")
print(f"Suma de ambos archivos: {cantidad_fin_hoja + cantidad_sin_fin_hoja}")
print(f"Elementos eliminados por duplicados: {len(datos) - (cantidad_fin_hoja + cantidad_sin_fin_hoja)}")

# Mostrar ejemplos de categorías especiales (con 3 elementos y tercero es "Fin de Hoja")
categorias_especiales = [item for item in datos if len(item["jerarquia"]) == 3 and item["jerarquia"][-1] == "Fin de Hoja"]
if categorias_especiales:
    print(f"\nSe encontraron {len(categorias_especiales)} categorías especiales (3 elementos con 'Fin de Hoja' como tercero):")
    for i, item in enumerate(categorias_especiales[:5]):  # Mostrar solo las primeras 5
        print(f"  {i+1}. Original: {' -> '.join(item['jerarquia'])}")
        # Buscar cómo aparece en cada archivo
        jerarquia_sin_fin_hoja = item["jerarquia"][:-1]
        print(f"     En 'categorias_para_arbol.json': {' -> '.join(jerarquia_sin_fin_hoja)}")

# Mostrar ejemplos de categorías individuales
categorias_individuales = [item for item in datos if len(item["jerarquia"]) == 1]
if categorias_individuales:
    print(f"\nSe encontraron {len(categorias_individuales)} categorías individuales (1 elemento en jerarquía):")
    for i, item in enumerate(categorias_individuales[:10]):  # Mostrar solo las primeras 10
        print(f"  {i+1}. {' -> '.join(item['jerarquia'])}")