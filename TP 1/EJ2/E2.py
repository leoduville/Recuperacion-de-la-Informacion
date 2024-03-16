import os
import re
from collections import defaultdict

def tokenize_grefenstette_tapanainen(text):
    # Expresiones regulares para tokenizar según los criterios especificados
    abbreviation_pattern = r'\b(?:[A-Za-z]\.)+[A-Za-z]?\.?'  # Abreviaturas
    email_url_pattern = r'\b(?:[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}|https?://\S+)'  # Correos electrónicos y URLs
    number_pattern = r'\b(?:\d{1,3}(?:,\d{3})*(?:\.\d+)?|\.\d+)\b'  # Números
    proper_name_pattern = r'\b(?:[A-Z][a-z]+(?: [A-Z][a-z]+)+)\b'  # Nombres propios

    # Tokenizar el texto según las expresiones regulares
    tokens = re.findall(abbreviation_pattern + '|' + email_url_pattern + '|' +
                        number_pattern + '|' + proper_name_pattern + '|[a-zA-Z]+', text)
    
    return tokens

def process_document(file_path, tokenizer):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return tokenizer(text)

def generate_lexical_analysis(directory, tokenizer, min_length=1, max_length=float('inf')):
    term_frequency = defaultdict(int)  # Frecuencia de términos
    document_frequency = defaultdict(int)  # Document Frequency

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            terms = process_document(file_path, tokenizer)

            for term in terms:
                if min_length <= len(term) <= max_length:
                    term_frequency[term] += 1

            for term in set(terms):
                if min_length <= len(term) <= max_length:
                    document_frequency[term] += 1

    # Escribir resultados en el archivo terminos.txt
    with open('terminos_grefenstette_tapanainen.txt', 'w', encoding='utf-8') as output_file:
        for term in sorted(term_frequency.keys()):
            output_file.write(f"{term} {term_frequency[term]} {document_frequency[term]}\n")

if __name__ == "__main__":
    directory = "C:/Users/leo_2/OneDrive/Documentos/GitHub/Recuperacion de la Informacion/Recuperacion-de-la-Informacion/TP 1/EJ 1/RI-tknz-data"
    tokenizer = tokenize_grefenstette_tapanainen

    generate_lexical_analysis(directory, tokenizer)
