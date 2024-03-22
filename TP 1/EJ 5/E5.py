import numpy as np

# Función para cargar el conjunto de entrenamiento desde archivos
def cargar_conjunto_entrenamiento(ruta_archivos):
    conjunto_entrenamiento = {}
    for idioma, ruta_archivo in ruta_archivos.items():
        with open(ruta_archivo, 'r', encoding='latin1') as archivo:
            texto_entrenamiento = archivo.read()
            conjunto_entrenamiento[idioma] = texto_entrenamiento
    return conjunto_entrenamiento


# Función para calcular la frecuencia de letras en un texto
def calcular_frecuencia_letras(texto):
    texto = texto.lower()
    letras = [letra for letra in texto if letra.isalpha()]
    total_letras = len(letras)
    frecuencia_letras = {letra: letras.count(letra) / total_letras for letra in set(letras)}
    return frecuencia_letras

# Función para calcular la correlación entre dos distribuciones de frecuencia
def calcular_correlacion(frecuencia_texto, frecuencia_entrenamiento):
    letras_comunes = set(frecuencia_texto) & set(frecuencia_entrenamiento)
    frecuencia_texto_comun = np.array([frecuencia_texto[letra] for letra in letras_comunes])
    frecuencia_entrenamiento_comun = np.array([frecuencia_entrenamiento[letra] for letra in letras_comunes])
    correlacion = np.corrcoef(frecuencia_texto_comun, frecuencia_entrenamiento_comun)[0, 1]
    return correlacion

# Función para identificar el idioma
def identificar_idioma(texto_prueba, conj_entrenamiento):
    frecuencia_texto = calcular_frecuencia_letras(texto_prueba)
    mejor_correlacion = -1
    mejor_idioma = None
    for idioma, texto_entrenamiento in conj_entrenamiento.items():
        frecuencia_entrenamiento = calcular_frecuencia_letras(texto_entrenamiento)
        correlacion = calcular_correlacion(frecuencia_texto, frecuencia_entrenamiento)
        if correlacion > mejor_correlacion:
            mejor_correlacion = correlacion
            mejor_idioma = idioma
    return mejor_idioma

# Función para leer el archivo completo y determinar el idioma de cada línea
def identificar_idioma_por_linea(archivo_prueba, conj_entrenamiento):
    with open(archivo_prueba, 'r', encoding='latin1') as archivo:
        texto_prueba = archivo.read()
    
    lineas = texto_prueba.split('\n')
    for linea in lineas:
        linea = linea.strip()  # Eliminar espacios en blanco al inicio y al final de la línea
        if linea:  # Saltar líneas en blanco
            idioma_identificado = identificar_idioma(linea, conj_entrenamiento)
            print(idioma_identificado)

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
    archivo_prueba = 'languageIdentificationData/test'
    
    # Cargar el conjunto de entrenamiento
    conjunto_entrenamiento = cargar_conjunto_entrenamiento(ruta_archivos_entrenamiento)
    
    # Identificar el idioma de cada línea del archivo de prueba
    identificar_idioma_por_linea(archivo_prueba, conjunto_entrenamiento)

if __name__ == "__main__":
    main()
