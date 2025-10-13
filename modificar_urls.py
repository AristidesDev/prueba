import json

# Cargar el JSON
with open('categorias_con_fin_hoja.json', 'r', encoding='utf-8') as f:
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

# Modificar todas las URLs en el JSON
for item in data:
    if 'url' in item:
        item['url'] = modificar_url(item['url'])

# Guardar el JSON modificado
with open('categorias_con_fin_hoja_modificado.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("URLs modificadas exitosamente!")