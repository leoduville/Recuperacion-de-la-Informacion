import re
import nltk
from nltk.corpus import stopwords as nltk_stopwords

# Descargar las stopwords de NLTK si no están disponibles
nltk.download('stopwords')

# Expresión regular para eliminar caracteres no alfanuméricos
regex_alpha_words = re.compile(r'[^a-zA-Z0-9áéíóúÁÉÍÓÚüÜñÑ]')

# Lista de stopwords de NLTK
stopwords = set(nltk_stopwords.words('spanish'))

# Diccionario para almacenar los términos únicos en cada consulta
unique_terms = {}

# Tokeniza una línea y opcionalmente cuenta las frecuencias de las palabras
def tokenize_line(line, frec, query_id):
    tokens = []
    for token in line.split():
        word = re.sub(regex_alpha_words, '', token.lower())
        if word and word not in stopwords:
            if frec:
                tokens.append(word)
            else:
                # Si no estamos contando frecuencias, verificamos si el término ya se ha agregado a esta consulta
                if word not in unique_terms.get(query_id, set()):
                    unique_terms.setdefault(query_id, set()).add(word)
                    tokens.append(word)
    return tokens

# Obtiene el tipo de tag de una línea
def get_tag(line):
    match = re.match(r'\.([ITAWXB])', line)
    return match.group(1) if match else None

# Obtiene el ID de consulta de una línea
def get_query_id(line):
    match = re.search(r'\.I\s+(\d+)', line)
    return match.group(1) if match else None

# Función principal
def main():
    filein = "../CISI/CISI.QRY"
    frec = True  # Indica si se deben contar las frecuencias
    with open(filein, 'r', encoding='utf-8') as fin, open("queriesfrec_CISI.trec", "w", encoding='utf-8') as fout:
        query_id = None
        in_query = False
        for line in fin:
            tag = get_tag(line)
            if tag == "I":
                # Escribir el inicio de la consulta y marcar que estamos dentro de una consulta
                if query_id:
                    fout.write("</TITLE>\n</TOP>\n")
                query_id = get_query_id(line)
                fout.write(f"<TOP>\n<NUM>{query_id}</NUM>\n<TITLE> ")
                in_query = True
                unique_terms[query_id] = set()  # Limpiar los términos únicos para esta consulta
            elif tag == "B":
                # Escribir el fin de la consulta y marcar que no estamos dentro de una consulta
                if in_query:
                    fout.write(" </TITLE>\n</TOP>\n")
                    in_query = False
            elif in_query and not line.startswith(('.W', '.T')):
                # Escribir el contenido de la consulta, ignorando líneas que comienzan con .W o .T
                tokens = tokenize_line(line, frec, query_id)
                if tokens:
                    fout.write(" ".join(tokens))
        
        # Verificar si quedó una consulta sin terminar
        if query_id and in_query:
            fout.write(" </TITLE>\n</TOP>\n")

if __name__ == '__main__':
    main()
