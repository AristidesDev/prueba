import json

# Cargar los archivos
with open('Categorias_base_1_anidado.json', encoding='utf-8') as f1:
    categorias_base_1 = json.load(f1)

with open('Categorias_2.json', encoding='utf-8') as f2:
    categorias_2 = json.load(f2)

# Agrupar categorias_2 por categoria_1
cat2_dict = {}
for cat2 in categorias_2:
    key = cat2['categoria_1']
    cat2_dict.setdefault(key, []).append(cat2)

# Anidar categorias_2 en cada categoria_1 dentro de categorias_base_1
for base in categorias_base_1:
    for cat1 in base.get('categorias_1', []):
        nombre_cat1 = cat1['nombre_categoria_1']
        cat1['categorias_2'] = cat2_dict.get(nombre_cat1, [])

# Guardar el resultado
with open('Categorias_base_1_2_anidado.json', 'w', encoding='utf-8') as fout:
    json.dump(categorias_base_1, fout, ensure_ascii=False, indent=2)