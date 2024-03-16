import os
import sys
import re
from collections import defaultdict

def tokenize(text):
    # Utilizamos una expresión regular para dividir el texto en palabras
    return re.findall(r'\w+', text.lower())

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
    token_count = 0 # Variables para estadisticas.txt
    term_count = 0
    term_lengths = []
    term_frequency_one = 0
    shortest_document = float('inf')
    longest_document = 0

    for filename in os.listdir(directory):
        if filename.endswith('.txt'):
            file_path = os.path.join(directory, filename)
            terms = process_document(file_path)
            token_count += len(terms)
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
        for term in sorted(term_frequency.keys()):
            output_file.write(f"{term} {term_frequency[term]} {document_frequency[term]}\n")

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