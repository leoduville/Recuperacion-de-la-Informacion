import itertools
from operator import itemgetter
import os
import struct
import re
from matplotlib import pyplot as plt
from tqdm import tqdm
import time
import pickle

def remove_accents(word):
    # Definimos un diccionario con los caracteres acentuados en minúsculas y sus equivalentes sin acento
    accents_mapping = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }
    # Reemplazamos los caracteres acentuados por sus equivalentes sin acento
    for accented_char, unaccented_char in accents_mapping.items():
        word = word.replace(accented_char, unaccented_char)
    return word

def tokenize(text):
    text = text.lower()
    intab = "áéíóú"
    outtab = "aeiou"
    str = text
    trantab = str.maketrans(intab, outtab)
    normalizado = str.translate(trantab)
    normalizado = re.sub(r'[^a-z0-9 ]','', normalizado)
    tokens = normalizado.split(" ")
    if "" in tokens:
        while "" in tokens:
            tokens.remove("")
    return tokens

def build_partial_index(doc_id, text, partial_index, dict_terms, freq):
    tokens = tokenize(text)
    term_freq = {}
    for token in tokens:
        if len(token) > 2:
            if freq:
                if token in term_freq:
                    term_freq[token] += 1
                else:
                    term_freq[token] = 1
            else:
                term_freq[token] = 1
    for term, freq in term_freq.items():
        partial_index.append((dict_terms[term], doc_id, freq))

def dump_partial_index(sorted_partial_index, filename):
    byte_data = struct.pack(f">{len(sorted_partial_index)}I", *sorted_partial_index)
    with open(filename, 'ab') as index_file:
        index_file.write(byte_data)

def read_partial_index(filename):
    tuples_list = []
    with open(filename, 'rb') as index_file:
        data = index_file.read()
        format_string = f">{len(data) // 4}I"
        unpacked_data = struct.unpack(format_string, data)
        for i in range(0, len(unpacked_data), 3):
            tuples_list.append((unpacked_data[i], unpacked_data[i+1], unpacked_data[i+2]))
    return tuples_list

def save_vocabulary(vocabulary):
    with open("vocabulary.pickle", "wb") as file:
        pickle.dump(vocabulary, file)

def merge_partial_indices(index_files, merged_index_filename):
    vocabulary = {}
    seek = 0
    tuples = []
    df = 0
    
    # Leer cada archivo parcial una vez y almacenar los datos en partial_data
    for partial_index in index_files:
        with open(partial_index, 'rb') as index_file:
            data = index_file.read()
            format_string = f">{len(data) // 4}I"
            unpacked_data = struct.unpack(format_string, data)
            for i in range(0, len(unpacked_data), 3):
                term_id, doc_id, freq = unpacked_data[i], unpacked_data[i+1], unpacked_data[i+2]
                tuples.append((term_id, doc_id, freq))

    tuples.sort(key=lambda x: x[0])

    # Calcular df y actualizar el vocabulario mientras fusionamos los datos parciales y escribimos en el archivo final
    with open(merged_index_filename, 'wb') as merged_index_file:
        for term, term_data in itertools.groupby(tuples, key=lambda x: x[0]):
            term_data = list(term_data)
            term_data = [(doc_id, freq) for _, doc_id, freq in term_data]  # Seleccionamos solo doc_id y freq
            term_data = list(itertools.chain(*term_data))
            df = len(term_data) // 2  # Calculamos df
            vocabulary[term] = [seek, df]  # Actualizamos el vocabulario
            seek += len(term_data) * 4  # Cada tupla ocupa 4 bytes en el archivo final
            term_data = struct.pack(f">{len(term_data)}I", *term_data)
            merged_index_file.write(term_data)
    save_vocabulary(vocabulary)

def index_directory(docs_directory):

    """
    Indexa todos los archivos HTML en el directorio y sus subdirectorios.
    :param docs_directory: La ruta del directorio a indexar.
    """
    files_list = list_files(docs_directory)
    docs = {}
    for file_path in files_list:
        with open(file_path, 'r', encoding='utf-8') as f:
            doc_id = os.path.basename(file_path)  # Usamos el nombre del archivo como identificador del documento
            docs[doc_id] = f.read()
    return docs

def list_files(directory):
    """
    Lista todos los archivos en el directorio y sus subdirectorios.
    :param directory: La ruta del directorio a listar.
    :return: Una lista de rutas de archivos.
    """
    files_list = []
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            files_list.append(file_path)
    return files_list

def generate_termdict(docs):
    terms = {}
    i = 1
    for j, (doc_id, doc_content) in enumerate(tqdm((docs.items()), desc="Guardando id de terminos...")):
        tokens = tokenize(doc_content)
        for token in tokens:
            if len(token) > 2:
                if token not in terms:
                    terms[token] = i
                    i += 1
    with open("dict_terms.pickle", 'wb') as file:
        pickle.dump(terms, file)
    return terms

def sort_index_by_termId(index):
    index.sort(key=itemgetter(0))
    return index

def save_dict_files(dict_files):
    with open("dict_files.pickle", 'wb') as file:
        pickle.dump(dict_files, file)

def index_collection(collection_path, n, freq):
    partial_indices = []
    partial_index = []
    doc_count = 0
    dict_files = {}
    docs = index_directory(collection_path)
    dict_terms = generate_termdict(docs)
    start_time = time.time()
    for i, (doc_id, doc_content) in enumerate(tqdm((docs.items()), desc="Indexando documentos")):
        doc_count += 1
        dict_files[doc_count] = doc_id
        build_partial_index(doc_count, doc_content, partial_index, dict_terms, freq)
        if doc_count % n == 0:
            index_filename = f'partial_index_{doc_count // n}.bin'
            sorted_partial_index = sort_index_by_termId(partial_index)
            sorted_partial_index = list(itertools.chain(*sorted_partial_index)) 
            dump_partial_index(sorted_partial_index, index_filename)
            partial_indices.append(index_filename)
            partial_index.clear()
    if partial_index:
        index_filename = f'partial_index_{doc_count // n + 1}.bin'
        sorted_partial_index = sort_index_by_termId(partial_index)
        sorted_partial_index = list(itertools.chain(*sorted_partial_index)) 
        dump_partial_index(sorted_partial_index, index_filename)
        partial_indices.append(index_filename)
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Colección indexada correctamente. Tiempo: {elapsed_time}")
    save_dict_files(dict_files)
    start_time = time.time()
    merge_partial_indices(partial_indices, 'final_index.bin')
    end_time = time.time()
    elapsed_time = end_time - start_time
    print(f"Merge completado. Tiempo: {elapsed_time}")

def graficar_posting_lists(filename, top_n):
    with open(filename, "rb") as file:
        vocabulary = pickle.load(file)
    # Ordenar las claves del vocabulario según su frecuencia (df)
    sorted_keys = sorted(vocabulary, key=lambda x: vocabulary[x][1], reverse=True)
    
    # Obtener los valores de Document Frequency (df) correspondientes a las claves ordenadas
    dfs = [vocabulary[key][1] for key in sorted_keys[:top_n]]  # Tomar solo las frecuencias de los top_n términos
    
    # Graficar
    plt.bar(range(1, top_n + 1), dfs, align='center')
    plt.xlabel('Term ID')
    plt.ylabel('Tamaño de posting list')
    plt.title('Tamaño de posting para cada Term ID (Ordenadas por Frecuencia)')
    plt.show()

# Uso del script
collection_path = 'en'
n = 1000  # Ejemplo de tamaño de índice parcial
freq = True

index_collection(collection_path, n, freq)

vocabulary_name = "vocabulary.pickle"
graficar_posting_lists(vocabulary_name, 500)
