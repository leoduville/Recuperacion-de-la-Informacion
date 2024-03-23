import sys
import matplotlib.pyplot as plt
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

def tokenize_text(file_name):
    try:
        with open(file_name, 'r', encoding='utf-8') as file:
            text = file.read()
            # Utilizamos split para dividir el texto en palabras y convertimos a minúscula
            words = re.split(r'\W+', text.lower())
            # Eliminamos los acentos de las palabras
            words_without_accents = [remove_accents(word) for word in words]
            # Eliminamos los signos de puntuación
            translation_table = str.maketrans('', '', string.punctuation)
            words_without_punctuation = [word.translate(translation_table) for word in words_without_accents]
            return words_without_punctuation
    except FileNotFoundError:
        print("El archivo especificado no fue encontrado.")
        sys.exit(1)

def calcular_pares(tokens):
    total_tokens = len(tokens)
    unique_tokens = len(set(tokens))
    return total_tokens, unique_tokens

def verificar_ley_heaps(tokens):
    counts = {}
    x = []
    y = []
    total_tokens = 0
    
    for token in tokens:
        total_tokens += 1
        if token in counts:
            counts[token] += 1
        else:
            counts[token] = 1
        x.append(len(counts))
        y.append(total_tokens)
    
    plt.plot(y, x)
    plt.xlabel('Número total de palabras')
    plt.ylabel('Número de palabras unicas')
    plt.title('Ley de Heaps')
    plt.grid(True)
    plt.show()

def escribir_pares_en_archivo(total_tokens, unique_tokens, output_file):
    with open(output_file, 'w', encoding='utf-8') as file:
        file.write(f"Términos totales procesados: {total_tokens}\n")
        file.write(f"Términos únicos: {unique_tokens}\n")

def main(file_name, output_file):
    tokens = tokenize_text(file_name)
    total_tokens, unique_tokens = calcular_pares(tokens)
    print("Total de términos procesados:", total_tokens)
    print("Total de términos únicos:", unique_tokens)
    escribir_pares_en_archivo(total_tokens, unique_tokens, output_file)
    verificar_ley_heaps(tokens)

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Uso: python script.py <nombre_archivo> <archivo_salida>")
        sys.exit(1)
    file_name = sys.argv[1]
    output_file = sys.argv[2]
    main(file_name, output_file)
