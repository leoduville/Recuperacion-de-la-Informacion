import os
import re
import sys
from collections import defaultdict

def tokenize(text):
    # Tokeniza el texto utilizando diferentes reglas para extraer tokens específicos.
    tokens = extract_abbreviations(text)
    tokens.extend(extract_emails(text))
    tokens.extend(extract_urls(text))
    tokens.extend(extract_numbers(text))
    tokens.extend(extract_proper_names(text))
    
    return tokens

def extract_abbreviations(text):
    # Extrae abreviaturas del texto
    return re.findall(r'\b[A-Z][a-zA-Z\.]+\b', text)

def extract_emails(text):
    # Extrae direcciones de correo electrónico del texto
    return re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', text)

def extract_urls(text):
    # Extrae URLs del texto
    return re.findall(r'(http|ftp|https)://([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:/~+#-]*[\w@?^=%&/~+#-])?', text)

def extract_numbers(text):
    # Extrae números (cantidades, teléfonos) del texto
    return re.findall(r'\b\d+\b', text)

def extract_proper_names(text):
    # Extrae nombres propios (e.g., Villa Carlos Paz, Manuel Belgrano)
    return re.findall(r'\b[A-Z][a-z]+(?:\s[A-Z][a-z]+)*\b', text)

def process_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return tokenize(text)

def remove_stopwords(terms, stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return [term for term in terms if term not in stopwords]

def generate_lexical_analysis(directory, stopwords_file=None, min_length=1, max_length=float('inf')):
    term_frequency = defaultdict(int)  # Frecuencia de términos
    document_frequency = defaultdict(int)  # Document Frequency

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            terms = process_document(file_path)

            if stopwords_file:
                terms = remove_stopwords(terms, stopwords_file)

            for term in terms:
                if min_length <= len(term) <= max_length:
                    term_frequency[term] += 1

            for term in set(terms):
                if min_length <= len(term) <= max_length:
                    document_frequency[term] += 1

    # Ordenar términos alfabéticamente
    sorted_terms = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)

    # Escribir resultados en el archivo terminos.txt
    with open('terminos.txt', 'w', encoding='utf-8') as output_file:
        for term, cf in sorted_terms:
            output_file.write(f"{term} {cf} {document_frequency[term]}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python programa.py <directorio> [opcional: <archivo_stopwords>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    stopwords_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_lexical_analysis(directory, stopwords_file)
