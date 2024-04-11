def procesar_archivo_all(archivo_all, archivo_salida):
    with open(archivo_all, 'r', encoding='utf-8') as file:
        contenido = file.read()
    
    # Dividir el contenido en documentos
    documentos = contenido.split(".I ")[1:]
    
    # Escribir cada documento en el archivo de salida en formato TREC
    with open(archivo_salida, 'w', encoding='utf-8') as file:
        for i, documento in enumerate(documentos, start=1):
            # Agregar etiquetas TREC
            documento_trec = "<DOC>\n<DOCNO>" + str(i) + "</DOCNO>\n" + documento.strip() + "\n</DOC>\n\n"
            file.write(documento_trec)

# Rutas de los archivos de entrada y salida
archivo_all = "CISI/CISI.ALL"
archivo_salida = "archivo_salida.trec"

# Procesar el archivo .ALL y escribir el resultado en formato TREC
procesar_archivo_all(archivo_all, archivo_salida)

