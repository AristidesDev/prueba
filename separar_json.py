import json
import os

# Cargar el archivo JSON original
with open('Categorias_2.json', 'r', encoding='utf-8') as f:
    datos = json.load(f)

# Crear un diccionario para agrupar por "nombre_categoria_base"
categorias = {}

for item in datos:
    categoria = item.get('nombre_categoria_base')
    if categoria:
        if categoria not in categorias:
            categorias[categoria] = []
        categorias[categoria].append(item)

# Crear una carpeta para los archivos separados
os.makedirs('categorias_json', exist_ok=True)

# Guardar cada grupo en un archivo separado
for categoria, items in categorias.items():
    nombre_archivo = f'categorias_json/{categoria.replace(" ", "_")}.json'
    with open(nombre_archivo, 'w', encoding='utf-8') as f:
        json.dump(items, f, ensure_ascii=False, indent=2)

print("¡Archivos separados correctamente!")