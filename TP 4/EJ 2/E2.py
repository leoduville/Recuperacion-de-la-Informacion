import struct
import pickle
import re
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

def search_term(term, dict_terms, vocabulary):
    with open("final_index.bin", "rb") as f:
        tuples_list = []
        term_id = dict_terms[term]
        seek, df = vocabulary[term_id]
        f.seek(seek)
        bytes_data = f.read(df * 8)  # Cada entrada ocupa 8 bytes (doc_id, freq)
        unpacked_data = struct.unpack(f">{len(bytes_data) // 4}I", bytes_data)
        for i in range(0, len(unpacked_data), 2):
            tuples_list.append((unpacked_data[i], unpacked_data[i+1]))
    return tuples_list

def create_tuples_from_keys(dictionary):
    tuples_list = []
    for key in dictionary.keys():
        tuples_list.append((key, 1))
    return tuples_list

def eliminar_parentesis(texto):
    return re.sub(r'\(|\)', '', texto)

def evaluate_query(query_tokens, dict_terms, dict_files, vocabulary):
    query_tokens = query_tokens.split()
    stack = []
    i = 0
    while i < len(query_tokens):
        token = query_tokens[i]
        token = eliminar_parentesis(token)
        if token in {"AND", "OR", "NOT"}:
            operator = token
            i += 1
            term = query_tokens[i]
            term = eliminar_parentesis(term)
            if operator == "NOT":
                merged_postings = []
                if stack:
                    postings = stack.pop()
                    prev_postings = search_term(term, dict_terms, vocabulary)
                else:
                    prev_postings = search_term(term, dict_terms, vocabulary)
                    postings = create_tuples_from_keys(dict_files)
                    postings.sort(key=lambda x: x[0], reverse=False)
                m = 0
                n = 0
                while m < len(postings) and n < len(prev_postings):
                    if postings[m][0] == prev_postings[n][0]:
                        m += 1
                        n += 1
                    elif postings[m][0] < prev_postings[n][0]:
                        merged_postings.append(postings[m])
                        m += 1
                    else:
                        n += 1
                merged_postings += postings[m:]
                merged_postings.sort(key=lambda x: x[0], reverse=False)
                stack.append(merged_postings)
            else:
                postings = search_term(term, dict_terms, vocabulary)
                if stack:
                    prev_postings = stack.pop()
                    if operator == "AND":
                        m = 0
                        n = 0                    
                        merged_postings = []
                        while m < len(postings) and n < len(prev_postings):
                            if postings[m][0] == prev_postings[n][0]:
                                merged_postings.append((postings[m][0], max(postings[m][1], prev_postings[n][1])))
                                m += 1
                                n += 1
                            elif postings[m][0] < prev_postings[n][0]:
                                m += 1
                            else:
                                n += 1
                        merged_postings.sort(key=lambda x: x[0], reverse=False)
                        stack.append(merged_postings)
                    elif operator == "OR":
                        m = 0
                        n = 0
                        merged_postings = []
                        while m < len(postings) and n < len(prev_postings):
                            if postings[m][0] == prev_postings[n][0]:
                                merged_postings.append((postings[m][0], max(postings[m][1], prev_postings[n][1])))
                                m += 1
                                n += 1
                            elif postings[m][0] < prev_postings[n][0]:
                                merged_postings.append(postings[m])
                                m += 1
                            else:
                                merged_postings.append(prev_postings[n])
                                n += 1
                        merged_postings += postings[m:] # Agregar los elementos restantes de postings1
                        merged_postings += prev_postings[n:] # Agregar los elementos restantes de postings2
                        merged_postings.sort(key=lambda x: x[0], reverse=False)
                        stack.append(merged_postings)
                else:
                    stack.append(postings)
            i += 1
        else:
            term = token
            postings = search_term(term, dict_terms, vocabulary)
            stack.append(postings)
            i += 1
    return stack.pop() if stack else []

vocabulary = load_vocabulary("vocabulary.pickle")
dict_terms = load_dict_terms("dict_terms.pickle")
dict_files = load_dict_files("dict_files.pickle")

# Ahora realizamos una búsqueda
query = input("Introduce tu consulta: ")
start_time = time.time()
search_result = evaluate_query(query, dict_terms, dict_files, vocabulary)
end_time = time.time()
elapsed_time = end_time - start_time
print("Documentos que contienen la consulta:", search_result, len(search_result))
print(f"Tiempo: {elapsed_time}")