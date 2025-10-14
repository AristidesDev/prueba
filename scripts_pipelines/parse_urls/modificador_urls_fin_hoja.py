import json

# Cargar el JSON
with open('urls_fin_hoja.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Función para modificar la URL
def modificar_url(url):
    # Encontrar la última posición de "/"
    last_slash_index = url.rfind('/')
    
    if last_slash_index != -1:
        # Tomar la parte de la URL hasta el último "/"
        base_url = url[:last_slash_index + 1]
        # Agregar el sufijo requerido
        nueva_url = base_url + "_NoIndex_True?original_category_landing=true"
        return nueva_url
    else:
        # Si no hay "/", agregar el sufijo al final
        return url + "/_NoIndex_True?original_category_landing=true"

# Función para modificar la jerarquía
def modificar_jerarquia(jerarquia):
    # Eliminar "Fin de Hoja" si existe en la lista
    if "Fin de Hoja" in jerarquia:
        jerarquia.remove("Fin de Hoja")
    return jerarquia

# Función para cambiar URL a null cuando la jerarquía tiene solo un elemento
def modificar_url_jerarquia_unica(item):
    if 'jerarquia' in item and len(item['jerarquia']) == 1:
        item['url'] = None
    return item

# Modificar todas las URLs y jerarquías en el JSON
for item in data:
    if 'url' in item:
        item['url'] = modificar_url(item['url'])
    
    if 'jerarquia' in item:
        item['jerarquia'] = modificar_jerarquia(item['jerarquia'])

# Aplicar la modificación final para URLs con jerarquía de un solo elemento
for item in data:
    item = modificar_url_jerarquia_unica(item)

# Guardar el JSON modificado
with open('urls_para_parse.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("Todas las modificaciones aplicadas exitosamente!")