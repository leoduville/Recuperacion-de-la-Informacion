import numpy as np

# Función para cargar el conjunto de entrenamiento desde archivos
def cargar_conjunto_entrenamiento(ruta_archivos):
    conjunto_entrenamiento = {}
    for idioma, ruta_archivo in ruta_archivos.items():
        with open(ruta_archivo, 'r', encoding='latin1') as archivo:
            texto_entrenamiento = archivo.read()
            conjunto_entrenamiento[idioma] = texto_entrenamiento
    return conjunto_entrenamiento

# Función para calcular la matriz de probabilidades de letras consecutivas
def calcular_probabilidades_consecutivas(texto):
    texto = texto.lower()
    letras = [letra for letra in texto if letra.isalpha()]
    alfabeto = sorted(set(letras))
    num_letras = len(alfabeto)
    matriz_probabilidades = np.zeros((num_letras, num_letras))
    letra_anterior = None
    for letra in letras:
        if letra_anterior is not None:
            indice_anterior = alfabeto.index(letra_anterior)
            indice_actual = alfabeto.index(letra)
            matriz_probabilidades[indice_anterior][indice_actual] += 1
        letra_anterior = letra
    # Normalizar las probabilidades
    matriz_probabilidades /= matriz_probabilidades.sum(axis=1, keepdims=True)
    return matriz_probabilidades, alfabeto

# Función para calcular la probabilidad de una cadena dada una matriz de probabilidades de transición
def calcular_probabilidad_cadena(cadena, matriz_probabilidades, alfabeto):
    probabilidad = 1.0
    for i in range(len(cadena) - 1):
        letra_actual = cadena[i]
        letra_siguiente = cadena[i + 1]
        if letra_actual in alfabeto and letra_siguiente in alfabeto:  # Verificar si ambas letras están en el alfabeto
            indice_actual = alfabeto.index(letra_actual)
            indice_siguiente = alfabeto.index(letra_siguiente)
            probabilidad_transicion = matriz_probabilidades[indice_actual][indice_siguiente]
            probabilidad *= probabilidad_transicion
    return probabilidad

# Función para identificar el idioma de cada línea del archivo de prueba
def identificar_idioma_por_linea(archivo_prueba, conj_entrenamiento):
    with open(archivo_prueba, 'r', encoding='latin1') as archivo:
        for linea in archivo:
            linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final de la línea
            if linea:  # Saltar líneas en blanco
                idioma_identificado = identificar_idioma_probabilidades_transicion(linea, conj_entrenamiento)
                print(idioma_identificado)

# Función para identificar el idioma basado en la probabilidad de transición de letras
def identificar_idioma_probabilidades_transicion(texto_prueba, conj_entrenamiento):
    probabilidades_entrenamiento = {}
    for idioma, texto_entrenamiento in conj_entrenamiento.items():
        matriz_probabilidades, alfabeto = calcular_probabilidades_consecutivas(texto_entrenamiento)
        probabilidades_entrenamiento[idioma] = matriz_probabilidades, alfabeto
    
    mejor_idioma = None
    mejor_probabilidad = 0
    for idioma, (matriz_probabilidades, alfabeto) in probabilidades_entrenamiento.items():
        probabilidad = calcular_probabilidad_cadena(texto_prueba, matriz_probabilidades, alfabeto)
        if probabilidad > mejor_probabilidad:
            mejor_probabilidad = probabilidad
            mejor_idioma = idioma
    return mejor_idioma

# Función principal
def main():
    # Rutas de los archivos de entrenamiento para cada idioma
    ruta_archivos_entrenamiento = {
        'Ingles': 'languageIdentificationData/training/English.txt',
        'Frances': 'languageIdentificationData/training/French.txt',
        'Italiano': 'languageIdentificationData/training/Italian.txt'
        # Agrega más idiomas con sus rutas correspondientes si es necesario
    }

    # Ruta del archivo de prueba
    archivo_prueba = '../languageIdentificationData/test'
    
    # Cargar el conjunto de entrenamiento
    conjunto_entrenamiento = cargar_conjunto_entrenamiento(ruta_archivos_entrenamiento)
    
    # Cargar el conjunto de entrenamiento
    conjunto_entrenamiento = cargar_conjunto_entrenamiento(ruta_archivos_entrenamiento)
    
    # Identificar el idioma de cada línea del archivo de prueba
    identificar_idioma_por_linea(archivo_prueba, conjunto_entrenamiento)

if __name__ == "__main__":
    main()
