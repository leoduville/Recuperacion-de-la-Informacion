from collections import defaultdict
import time

def cargar_indice_invertido(archivo):
    indice_invertido = {}
    with open(archivo, 'r') as f:
        for line in f:
            term_id, df, doc_ids_str = line.strip().split(':')
            doc_ids = doc_ids_str.rstrip(',').split(',')
            indice_invertido[term_id] = doc_ids
    return indice_invertido

def calcular_puntaje_TAAT(consulta, indice_invertido):
    puntajes = defaultdict(int)
    documentos_relevantes_por_termino = {}
    
    # Calcular documentos relevantes para cada término
    for termino in consulta:
        if termino in indice_invertido:
            documentos_relevantes_por_termino[termino] = indice_invertido[termino]
            documentos_relevantes = documentos_relevantes_por_termino[termino]
            for doc_id in documentos_relevantes:
                puntajes[doc_id] += 1  # Incrementar el puntaje parcial
    return puntajes

def calcular_puntaje_DAAT(consulta, indice_invertido):
    puntajes = defaultdict(int)
    documentos_relevantes = set()

    # Obtener documentos relevantes para todos los términos de la consulta
    for termino in consulta:
        if termino in indice_invertido:
            documentos_relevantes.update(indice_invertido[termino])

    # Procesar cada documento relevante para cada término
    for doc_id in documentos_relevantes:
        for termino in consulta:
            if termino in indice_invertido and doc_id in indice_invertido[termino]:
                puntajes[doc_id] += 1  # Incrementar puntaje

    return puntajes

def ordenar_por_puntajes(puntajes):
    return sorted(puntajes.items(), key=lambda x: x[1], reverse=True)

# Uso del programa
archivo = 'dump10k.txt'
indice_invertido = cargar_indice_invertido(archivo)

consulta = input("Ingrese la consulta separando los términos por espacios: ").split()

inicio_taat = time.time()
puntajes_TAAT = calcular_puntaje_TAAT(consulta, indice_invertido)
fin_taat = time.time()
tiempo_taat = fin_taat - inicio_taat

inicio_daat = time.time()
puntajes_DAAT = calcular_puntaje_DAAT(consulta, indice_invertido)
fin_daat = time.time()
tiempo_daat = fin_daat - inicio_daat

# Ordenar los documentos por puntaje
puntajes_TAAT_ordenados = ordenar_por_puntajes(puntajes_TAAT)
puntajes_DAAT_ordenados = ordenar_por_puntajes(puntajes_DAAT)

print("Resultados:")
print("Puntajes TAAT:", puntajes_TAAT_ordenados)
print("Tiempo TAAT:", tiempo_taat)
print("Puntajes DAAT:", puntajes_DAAT_ordenados)
print("Tiempo DAAT:", tiempo_daat)
