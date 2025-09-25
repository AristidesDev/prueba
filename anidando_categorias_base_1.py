import json

# Cargar los archivos
with open('Categories_base.json', encoding='utf-8') as f1:
    categorias_1 = json.load(f1)

with open('Categorias_1.json', encoding='utf-8') as f2:
    categorias_2 = json.load(f2)

# Agrupar categorias_2 por categoria_1
cat2_dict = {}
for cat2 in categorias_2:
    key = cat2['categoria_base']  # Usar 'categoria_base' para agrupar
    cat2_dict.setdefault(key, []).append(cat2)

# Anidar categorias_2 en categorias_1
for cat1 in categorias_1:
    nombre_cat1 = cat1['nombre_categoria_base']
    cat1['categorias_1'] = cat2_dict.get(nombre_cat1, [])

# Guardar el resultado
with open('Categorias_base_1_anidado.json', 'w', encoding='utf-8') as fout:
    json.dump(categorias_1, fout, ensure_ascii=False, indent=2)