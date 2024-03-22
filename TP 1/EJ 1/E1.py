import os
import sys
import re
import string
from collections import defaultdict

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

def count_tokens(text):
    words = text.split(" ")
    return words

def process_document(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return tokenize(text)

def process_tokens(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
        return count_tokens(text)

def remove_stopwords(terms, stopwords_file):
    with open(stopwords_file, 'r', encoding='utf-8') as file:
        stopwords = set(file.read().splitlines())
    return [term for term in terms if term not in stopwords]

def generate_lexical_analysis(directory, stopwords_file=None, min_length=1, max_length=float('inf')):
    term_frequency = defaultdict(int)  # Frecuencia de términos
    document_frequency = defaultdict(int)  # Document Frequency
    token_count = 0 # Variables para estadisticas.txt
    term_count = 0
    term_lengths = []
    term_frequency_one = 0
    shortest_document = float('inf')
    longest_document = 0

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            tokens = process_tokens(file_path)
            token_count += len(tokens)
            terms = process_document(file_path)
            term_count += len(set(terms))
            term_lengths.extend(map(len, terms))
            shortest_document = min(shortest_document, len(terms))
            longest_document = max(longest_document, len(terms))

            if stopwords_file:
                terms = remove_stopwords(terms, stopwords_file)

            for term in terms:
                if min_length <= len(term) <= max_length:
                    term_frequency[term] += 1

            for term in set(terms):
                if min_length <= len(term) <= max_length:
                    document_frequency[term] += 1

    sorted_terms = sorted(term_frequency.items(), key=lambda x: x[1], reverse=True)
    for term, freq in term_frequency.items():
        if freq == 1:
            term_frequency_one += 1
        
    # Calcular estadísticas
    avg_token_per_document = token_count / len(os.listdir(directory))
    avg_term_per_document = term_count / len(os.listdir(directory))
    avg_term_length = sum(term_lengths) / len(term_lengths)

    # Escribir resultados en el archivo terminos.txt
    with open('terminos.txt', 'w', encoding='utf-8') as output_file:
         for term, cf in sorted_terms:
            output_file.write(f"{term} {cf} {document_frequency[term]}\n")

    # Escribir resultados en el archivo estadisticas.txt
    with open('estadisticas.txt', 'w', encoding='utf-8') as stats_file:
        stats_file.write(f"Cantidad de documentos procesados: {len(os.listdir(directory))}\n")
        stats_file.write(f"Cantidad de tokens extraídos: {token_count}\n")
        stats_file.write(f"Cantidad de términos extraídos: {term_count}\n")
        stats_file.write(f"Promedio de tokens por documento: {avg_token_per_document}\n")
        stats_file.write(f"Promedio de términos por documento: {avg_term_per_document}\n")
        stats_file.write(f"Largo promedio de un término: {avg_term_length}\n")
        stats_file.write(f"Cantidad de tokens del documento más corto: {shortest_document}\n")
        stats_file.write(f"Cantidad de tokens del documento más largo: {longest_document}\n")
        stats_file.write(f"Cantidad de términos que aparecen solo 1 vez: {term_frequency_one}\n")        

    # Escribir resultados en el archivo frecuencias.txt
    with open('frecuencias.txt', 'w', encoding='utf-8') as freq_file:
        freq_file.write("Los 10 términos más frecuentes y su CF (Collection Frequency):\n")
        for term, freq in sorted_terms[:10]:
            freq_file.write(f"{term} {freq}\n")

        freq_file.write("\nLos 10 términos menos frecuentes y su CF (Collection Frequency):\n")
        for term, freq in sorted_terms[-10:]:
            freq_file.write(f"{term} {freq}\n")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Uso: python programa.py <directorio> [opcional: <archivo_stopwords>]")
        sys.exit(1)
    
    directory = sys.argv[1]
    stopwords_file = sys.argv[2] if len(sys.argv) > 2 else None

    generate_lexical_analysis(directory, stopwords_file)
