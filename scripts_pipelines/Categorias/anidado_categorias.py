import json

def construir_arbol_categorias(categorias_planas):
    # Crear un diccionario para buscar categorías por su ruta jerárquica
    categorias_por_ruta = {}
    
    # Primero, indexar todas las categorías por su ruta completa
    for categoria in categorias_planas:
        ruta = tuple(categoria['jerarquia'])  # Convertir a tupla para usar como clave
        categorias_por_ruta[ruta] = categoria
    
    # Función recursiva para construir el árbol
    def construir_subarbol(ruta_actual):
        nodo_actual = categorias_por_ruta.get(ruta_actual)
        if not nodo_actual:
            return None
        
        # Buscar todos los hijos directos de este nodo
        hijos = []
        for ruta_completa, categoria in categorias_por_ruta.items():
            # Si la ruta tiene un elemento más y comienza con la ruta actual, es un hijo directo
            if (len(ruta_completa) == len(ruta_actual) + 1 and 
                ruta_completa[:len(ruta_actual)] == ruta_actual):
                
                hijo = construir_subarbol(ruta_completa)
                if hijo:
                    hijos.append(hijo)
        
        # Crear el nodo con sus hijos
        return {
            "nombre": nodo_actual["nombre"],
            "url": nodo_actual["url"],
            "hijos": hijos
        }
    
    # Encontrar todas las raíces (categorías con jerarquía de 1 elemento)
    arbol_completo = []
    for ruta, categoria in categorias_por_ruta.items():
        if len(ruta) == 1:
            arbol_raiz = construir_subarbol(ruta)
            if arbol_raiz:
                arbol_completo.append(arbol_raiz)
    
    return arbol_completo

# Cargar el JSON original
with open('categorias_para_arbol.json', 'r', encoding='utf-8') as f:
    categorias_planas = json.load(f)

# Construir el árbol anidado
arbol_anidado = construir_arbol_categorias(categorias_planas)

# Guardar el resultado en un nuevo archivo JSON
with open('arbol_categorias_anidadas.json', 'w', encoding='utf-8') as f:
    json.dump(arbol_anidado, f, ensure_ascii=False, indent=2)

print("Proceso completado. El archivo 'arbol_categorias_anidadas55.json' ha sido generado.")
print(f"Se encontraron {len(arbol_anidado)} categorías raíz.")

# Mostrar un ejemplo de la estructura resultante
if arbol_anidado:
    print("\nEjemplo de estructura anidada:")
    ejemplo = arbol_anidado[0]  # Primera categoría raíz
    print(f"Raíz: {ejemplo['nombre']}")
    if ejemplo['hijos']:
        print(f"  - Hijos directos: {len(ejemplo['hijos'])}")
        primer_hijo = ejemplo['hijos'][0]
        print(f"    • {primer_hijo['nombre']}")
        if primer_hijo['hijos']:
            print(f"      - Nietos: {len(primer_hijo['hijos'])}")