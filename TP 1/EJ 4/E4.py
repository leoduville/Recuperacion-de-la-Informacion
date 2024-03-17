import sys
import time
import nltk
from nltk.stem import PorterStemmer, LancasterStemmer

# Función para cargar la colección CISI desde una ruta dada
def load_cisi_corpus(cisi_path):
    return nltk.corpus.CategorizedPlaintextCorpusReader(cisi_path, r'.*\.ALL|.*\.BLN|.*\.QRY|.*\.REL', cat_pattern=r'([\w\s]+)/.*')

# Función para tokenizar la colección CISI
def tokenize_corpus(cisi_corpus):
    return cisi_corpus.words()

# Función para aplicar un stemmer a una lista de tokens
def apply_stemmer(tokens, stemmer):
    return [stemmer.stem(token) for token in tokens]

# Función principal
def main(cisi_path):
    # Cargar la colección CISI
    cisi_corpus = load_cisi_corpus(cisi_path)

    # Tokenizar la colección CISI
    tokens = tokenize_corpus(cisi_corpus)

    # Inicializar stemmers Porter y Lancaster
    porter_stemmer = PorterStemmer()
    lancaster_stemmer = LancasterStemmer()

    # Medir tiempo de ejecución y obtener tokens únicos para stemmer Porter
    start_time_porter = time.time()
    porter_stemmed_tokens = apply_stemmer(tokens, porter_stemmer)
    unique_tokens_porter = set(porter_stemmed_tokens)
    end_time_porter = time.time()

    # Medir tiempo de ejecución y obtener tokens únicos para stemmer Lancaster
    start_time_lancaster = time.time()
    lancaster_stemmed_tokens = apply_stemmer(tokens, lancaster_stemmer)
    unique_tokens_lancaster = set(lancaster_stemmed_tokens)
    end_time_lancaster = time.time()

    # Comparar cantidad de tokens únicos resultantes
    print("Cantidad de tokens únicos resultantes:")
    print("Stemmer Porter:", len(unique_tokens_porter))
    print("Stemmer Lancaster:", len(unique_tokens_lancaster))

    # Comparar tiempo de ejecución
    print("\nTiempo de ejecución para toda la colección:")
    print("Stemmer Porter:", end_time_porter - start_time_porter, "segundos")
    print("Stemmer Lancaster:", end_time_lancaster - start_time_lancaster, "segundos")

if __name__ == "__main__":
    # Verificar que se proporcione la ruta de la colección CISI como argumento
    if len(sys.argv) != 2:
        print("Usage: python script.py path_to_cisi_collection")
        sys.exit(1)

    # Obtener la ruta de la colección CISI del primer argumento
    cisi_path = sys.argv[1]

    # Ejecutar la función principal con la ruta de la colección CISI como argumento
    main(cisi_path)
