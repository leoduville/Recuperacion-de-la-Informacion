import sys
import re
import string

def remove_accents(word):
    # Definimos un diccionario con los caracteres acentuados en minúsculas y sus equivalentes sin acento
    accents_mapping = {
        'á': 'a', 'é': 'e', 'í': 'i', 'ó': 'o', 'ú': 'u'
    }
    # Reemplazamos los caracteres acentuados por sus equivalentes sin acento
    for accented_char, unaccented_char in accents_mapping.items():
        word = word.replace(accented_char, unaccented_char)
    return word

def tokenize_and_count(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()

    # Utilizamos split para dividir el texto en palabras y convertimos a minúscula
    words = re.split(r'\W+', text.lower())
    # Eliminamos los acentos de las palabras
    words_without_accents = [remove_accents(word) for word in words]
    # Eliminamos los signos de puntuación
    translation_table = str.maketrans('', '', string.punctuation)
    words_without_punctuation = [word.translate(translation_table) for word in words_without_accents]

    # Contar términos totales y únicos
    total_terms = len(words_without_punctuation)
    unique_terms = len(set(words_without_punctuation))

    return total_terms, unique_terms

def write_results(total_terms, unique_terms, output_file):
    with open(output_file, 'w') as file:
        file.write(f"Terminos totales procesados: {total_terms}\n")
        file.write(f"Terminos unicos: {unique_terms}\n")

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py archivo_entrada archivo_salida")
        sys.exit(1)

    input_file = sys.argv[1]
    output_file = sys.argv[2]

    total_terms, unique_terms = tokenize_and_count(input_file)
    write_results(total_terms, unique_terms, output_file)

    print("Procesamiento completado. Resultados escritos en", output_file)
