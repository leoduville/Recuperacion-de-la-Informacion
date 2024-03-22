import os
import re
import sys
from collections import defaultdict
import string
from nltk.stem import PorterStemmer
import nltk
nltk.download('punkt')

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
    # Utilizamos split para dividir el texto en palabras y convertimos a minúscula
    words = re.split(r'\W+', text.lower())
    # Eliminamos los acentos de las palabras
    words_without_accents = [remove_accents(word) for word in words]
    # Eliminamos los signos de puntuación
    translation_table = str.maketrans('', '', string.punctuation)
    words_without_punctuation = [word.translate(translation_table) for word in words_without_accents]
    return words_without_punctuation

def process_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return tokenize(text)

def remove_stopwords(terms, stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return [term for term in terms if term not in stopwords]

def apply_stemming(terms):
    stemmer = PorterStemmer()
    return [stemmer.stem(term) for term in terms]

def generate_lexical_analysis(directory, stopwords_file=None, min_length=1, max_length=float('inf')):
    term_frequency = defaultdict(int)  # Frecuencia de términos
    document_frequency = defaultdict(int)  # Document Frequency

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            terms = process_document(file_path)

            if stopwords_file:
                terms = remove_stopwords(terms, stopwords_file)
            
            terms = apply_stemming(terms)

            for term in terms:
                if min_length <= len(term) <= max_length:
                    term_frequency[term] += 1

            for term in set(terms):
                if min_length <= len(term) <= max_length:
                    document_frequency[term] += 1

    # Ordenar términos alfabéticamente
    sorted_terms = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)

    # Escribir resultados en el archivo terminos.txt
    with open('terminos_stemming.txt', 'w', encoding='utf-8') as output_file:
        for term, cf in sorted_terms:
            output_file.write(f"{term} {cf} {document_frequency[term]}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python programa.py <directorio> [opcional: <archivo_stopwords>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    stopwords_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_lexical_analysis(directory, stopwords_file)
