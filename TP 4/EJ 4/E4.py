import struct
import pickle
import math

# Función para cargar el vocabulario
def load_vocabulary(file_path):
    with open(file_path, "rb") as file:
        vocabulary = pickle.load(file)
    return vocabulary

# Función para cargar el diccionario de términos
def load_dict_terms(file_path):
    with open(file_path, "rb") as file:
        dict_terms = pickle.load(file)
    return dict_terms

# Función para cargar el diccionario de archivos
def load_dict_files(file_path):
    with open(file_path, "rb") as file:
        dict_files = pickle.load(file)
    return dict_files

# Función para leer las postings de un término
def read_postings(term_id, vocabulary):
    with open("final_index.bin", "rb") as f:
        seek, df = vocabulary[term_id]
        f.seek(seek)
        bytes_data = f.read(df * 8)  # Cada entrada ocupa 8 bytes (doc_id, freq)
        unpacked_data = struct.unpack(f">{len(bytes_data) // 4}I", bytes_data)
        postings = [(unpacked_data[i], unpacked_data[i+1]) for i in range(0, len(unpacked_data), 2)]
    return postings

# Función para calcular el puntaje TF-IDF de un término
def calculate_tf_idf(tf, df, N):
    idf = math.log(N / df)
    return tf * idf

# Función para calcular el puntaje de similitud entre la consulta y un documento
def calculate_similarity(query_vector, document_vector):
    score = 0
    for term_id, query_weight in query_vector.items():
        if term_id in document_vector:
            document_weight = document_vector[term_id]
            score += query_weight * document_weight
    return score

# Función para realizar la búsqueda DAAT (Document-At-A-Time)
def daat_query(query_terms, dict_terms, vocabulary, dict_files, k):
    query_vector = {}  # Vector de consulta
    N = len(dict_files)  # Número total de documentos
    scores = {}  # Almacena los puntajes de similitud entre la consulta y los documentos

    # Calcular el vector de consulta (TF-IDF)
    for term in query_terms:
        if term in dict_terms:
            term_id = dict_terms[term]
            postings = read_postings(term_id, vocabulary)
            df = len(postings)
            tf = 1 + math.log(1)  # Consideramos TF como 1 en consultas booleanas
            query_vector[term_id] = calculate_tf_idf(tf, df, N)
    
    # Recorrer los documentos
    for doc_id in dict_files.keys():
        document_vector = {}  # Vector del documento
        for term_id in query_vector.keys():
            postings = read_postings(term_id, vocabulary)
            for posting in postings:
                if posting[0] == doc_id:
                    document_vector[term_id] = calculate_tf_idf(posting[1], len(postings), N)
                    break
        # Calcular el puntaje de similitud y almacenarlo
        score = calculate_similarity(query_vector, document_vector)
        scores[doc_id] = score
    # Devolver los top-k documentos según el puntaje
    top_k_documents = sorted(scores.items(), key=lambda x: x[1], reverse=True)[:k]
    return top_k_documents

# Cargar los datos necesarios
vocabulary = load_vocabulary("vocabulary.pickle")
dict_terms = load_dict_terms("dict_terms.pickle")
dict_files = load_dict_files("dict_files.pickle")

# Realizar la búsqueda DAAT
query = input("Introduce tu consulta: ")
query_terms = query.split()  # Convertir la consulta en una lista de términos
k = 10  # Obtener los top-10 documentos
top_documents = daat_query(query_terms, dict_terms, vocabulary, dict_files, k)
print("Top-{} documentos relevantes:".format(k))
for doc_id, score in top_documents:
    print("Documento ID:", doc_id, "- Score:", score)
