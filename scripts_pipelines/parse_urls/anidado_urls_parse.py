import json

# Cargar el JSON original
with open('urls_para_parse.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# Función para construir el árbol jerárquico
def construir_arbol(datos):
    arbol = {}
    
    for item in datos:
        jerarquia = item["jerarquia"]
        nombre = item["nombre"]
        url = item["url"]
        
        # Comenzar desde la raíz del árbol
        nivel_actual = arbol
        
        # Recorrer cada nivel de la jerarquía
        for i, categoria in enumerate(jerarquia):
            # Si la categoría no existe en este nivel, crearla
            if categoria not in nivel_actual:
                nivel_actual[categoria] = {
                    "nombre": categoria,
                    "hijos": {},
                    "url": url if i == len(jerarquia) - 1 and categoria == nombre else None
                }
            
            # Si estamos en el último nivel y es el elemento actual, asegurar la URL
            if i == len(jerarquia) - 1 and categoria == nombre:
                nivel_actual[categoria]["url"] = url
            
            # Moverse al siguiente nivel
            nivel_actual = nivel_actual[categoria]["hijos"]
    
    return arbol

# Construir el árbol
arbol_jerarquico = construir_arbol(datos)

# Función para limpiar diccionarios vacíos de hijos
def limpiar_arbol(arbol):
    for key, value in list(arbol.items()):
        if isinstance(value, dict) and "hijos" in value:
            if value["hijos"]:
                limpiar_arbol(value["hijos"])
            else:
                del value["hijos"]
    return arbol

# Limpiar el árbol
arbol_limpio = limpiar_arbol(arbol_jerarquico)

# Convertir a lista para el formato final
def arbol_a_lista(arbol):
    resultado = []
    for key, value in arbol.items():
        item = {
            "nombre": value["nombre"],
            "url": value.get("url")
        }
        if "hijos" in value and value["hijos"]:
            item["hijos"] = arbol_a_lista(value["hijos"])
        resultado.append(item)
    return resultado

lista_final = arbol_a_lista(arbol_limpio)

# Guardar el resultado
with open('categorias_parse_anidadas.json', 'w', encoding='utf-8') as f:
    json.dump(lista_final, f, ensure_ascii=False, indent=2)

print("Proceso completado. Se ha generado el archivo 'categorias_anidadas.json'")