import pickle
import struct
import time

def load_vocabulary(file_path):
    with open(file_path, "rb") as file:
        vocabulary = pickle.load(file)
    return vocabulary

def load_dict_terms(file_path):
    with open(file_path, "rb") as file:
        dict_terms = pickle.load(file)
    return dict_terms

def load_dict_files(file_path):
    with open(file_path, "rb") as file:
        dict_files = pickle.load(file)
    return dict_files

def read_index(directory, df, pointer):
    try:
        with open(directory, 'rb') as binary_file:
            binary_file.seek(pointer)
            byte_data = binary_file.read(df * 8)
        format_string = f">{len(byte_data) // 4}I"
        unpacked_data = struct.unpack(format_string, byte_data)
        grouped_data = [(unpacked_data[i], unpacked_data[i+1]) for i in range(0, len(unpacked_data), 2)]
        return grouped_data
    except FileNotFoundError:
        print(f"Error: File '{directory}' not found.")
        return None

def read_pickle(file_path):
    try:
        with open(file_path, "rb") as file:
            data = pickle.load(file)
        return data
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return None

def search(term,dictionary,vocabulary,directory):
    if term in dictionary:
        termId = dictionary[term]
        pointer, df = vocabulary[termId]
        result = read_index(directory, df, pointer)
        return result

def sort_docId(rank):
    sort = sorted(rank, key=lambda x: x[0])
    return sort

def crear_skip_lists(n, vocabulary, dictionary):
    skip_lists = {}
    for term, term_id in dictionary.items():
        block_num = 1
        skip_list = []
        docs = []
        frequency = []
        max_freq = 0
        docs_term = search(term, dictionary, vocabulary, 'final_index.bin')
        if docs_term:
            docs_term = sort_docId(docs_term)
            for doc_id, freq in docs_term:
                frequency.append(freq)
                docs.append(doc_id)
                max_freq = max(max_freq, freq)
                if block_num % n == 0:
                    skip_list.append(((doc_id, max_freq), docs, frequency))
                    frequency = []
                    docs = []
                    max_freq = 0
                block_num += 1
            if docs:
                skip_list.append(((doc_id, max_freq), docs, frequency))
        skip_lists[term_id] = skip_list
    return skip_lists

def operator_and(docs, skip_list):
    result = []
    for doc in docs:
        for max_val, doc_ids, _ in skip_list:
            if doc > max_val[0]:
                continue
            else:
                if doc in doc_ids:
                    result.append(doc)
                elif doc < min(doc_ids):
                    break
    return result

def search_query(query, dictionary, skip_lists):
    query_terms = query.split(" AND ")
    term_ids = []
    for term in query_terms:
        if term in dictionary:
            term_ids.append(dictionary[term])
        else:
            print(f"El término '{term}' no está en el diccionario.")
            return []

    if not term_ids:
        print("No se encontraron términos válidos en la consulta.")
        return []

    result = skip_lists[term_ids[0]]
    for term_id in term_ids[1:]:
        if term_id in skip_lists:
            result = operator_and([doc_id for _, doc_ids, _ in result for doc_id in doc_ids], skip_lists[term_id])
        else:
            print(f"No se encontró skip list para el término con term_id {term_id}.")
            return []

    return result

def menu():
    print("\nSeleccione una opción:")
    print("1. Crear Skip Lists")
    print("2. Realizar una consulta")
    print("3. Recuperar una Skip List para un término")
    print("4. Salir")

def main():
    vocabulary = read_pickle('vocabulary.pickle')
    dictionary = read_pickle('dict_terms.pickle')
    skip_lists = None

    while True:
        menu()
        opcion = input("Ingrese el número de la opción deseada: ")
        
        if opcion == "1":
            print("Creando Skip Lists...")
            skip_lists = crear_skip_lists(6, vocabulary, dictionary)
            print("Skip Lists creadas.")
        elif opcion == "2":
            if skip_lists:
                query = input("Ingrese la consulta: ")
                start_time = time.time()
                result = search_query(query, dictionary, skip_lists)
                end_time = time.time()
                elapsed_time = end_time - start_time
                print("Documentos que satisfacen la consulta:", result)
                print(f"Tiempo: {elapsed_time}")
            else:
                print("Primero debe crear las Skip Lists.")
        elif opcion == "3":
            term = input("Ingrese el término del cual desea recuperar la Skip List: ")
            if term in dictionary:
                term_id = dictionary[term]
                if skip_lists and term_id in skip_lists:
                    print(f"Skip List para el término '{term}':")
                    print(skip_lists[term_id])
                else:
                    print(f"No se encontró Skip List para el término '{term}'.")
            else:
                print(f"El término '{term}' no está en el diccionario.")
        elif opcion == "4":
            print("Saliendo...")
            break
        else:
            print("Opción no válida. Por favor, ingrese un número válido.")

if __name__ == "__main__":
    main()