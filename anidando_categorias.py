import json

# Carga los archivos
with open('Categories_base.json', encoding='utf-8') as f:
    categorias_base = json.load(f)

with open('cate1.json', encoding='utf-8') as f:
    categorias_1 = json.load(f)

# Crea un diccionario para acceso rápido por nombre de categoría base
base_dict = {base['nombre_categoria_base']: base for base in categorias_base}

# Anida las categorías 1 en su base correspondiente
for cat1 in categorias_1:
    nombre_base = cat1.get('nombre_categoria_base')
    if nombre_base in base_dict:
        base = base_dict[nombre_base]
        if 'categorias_1' not in base:
            base['categorias_1'] = []
        base['categorias_1'].append(cat1)

# Guarda el resultado anidado
with open('categorias_base_1.json', 'w', encoding='utf-8') as f:
    json.dump(list(base_dict.values()), f, ensure_ascii=False, indent=2)