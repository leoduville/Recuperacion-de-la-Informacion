import os
import re
import math
from collections import defaultdict
from nltk.stem import LancasterStemmer
from scipy.stats import spearmanr
import pyterrier as pt
import numpy as np

class InformationRetrievalEngine:
    def __init__(self):
        self.term_frequencies = defaultdict(dict)
        self.document_lengths = defaultdict(float)
        self.document_paths = {}
        self.num_documents = 0
        self.stemmer = LancasterStemmer()

    def process_text(self, text):
        text = re.sub(r"[^\w\s]", "", text.lower())
        return text.split()

    def index_document(self, document_path):
        with open(document_path, 'r', encoding='utf-8') as file:
            content = file.read()
            terms = self.process_text(content)
            document_id = self.num_documents
            self.document_paths[document_id] = document_path
            self.num_documents += 1
            
            for term in terms:
                term = self.stemmer.stem(term)
                if term in self.term_frequencies:
                    if document_id in self.term_frequencies[term]:
                        self.term_frequencies[term][document_id] += 1
                    else:
                        self.term_frequencies[term][document_id] = 1
                else:
                    self.term_frequencies[term] = {document_id: 1}
                self.document_lengths[document_id] += 1

    def index_directory(self, directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".html"):
                    file_path = os.path.join(root, file)
                    self.index_document(file_path)

    def calculate_tf_idf(self, idf):
        tf_idf = defaultdict(dict)
        for term, doc_freqs in self.term_frequencies.items():
            for doc_id, freq in doc_freqs.items():
                tf_idf[term][doc_id] = freq * idf.get(term, 0)
        return tf_idf

    def query(self, query_str, idf):
        query_terms = self.process_text(query_str)
        query = defaultdict(int)
        for term in query_terms:
            term = self.stemmer.stem(term)
            query[term] += 1

        query_tfidf = {}
        query_length = 0.0

        for term, freq in query.items():
            if term in idf:
                query_tfidf[term] = freq * idf[term]
                query_length += query_tfidf[term] ** 2

        query_length = math.sqrt(query_length)

        scores = defaultdict(float)
        tf_idf = self.calculate_tf_idf(idf)
        for term, weight in query_tfidf.items():
            for doc_id, doc_weight in tf_idf.get(term, {}).items():
                scores[doc_id] += weight * doc_weight

        ranked_docs = sorted(scores.items(), key=lambda x: x[1], reverse=True)
        return [(doc_id, score) for doc_id, score in ranked_docs]

def calculate_idf(term_frequencies, num_documents):
    idf = {}
    for term, doc_freqs in term_frequencies.items():
        idf[term] = math.log(num_documents / (1 + len(doc_freqs)), 10)
    return idf

# Ejemplo de uso:
engine = InformationRetrievalEngine()
engine.index_directory("en")
idf = calculate_idf(engine.term_frequencies, engine.num_documents)
query= "italian"
query_result = engine.query(query, idf)
for doc_id, score in query_result:
    print(f"Documento: {doc_id}, Puntuación: {score:.4f}, Ruta: {engine.document_paths[doc_id]}")

sorted_paths = [engine.document_paths[doc_id] for doc_id, score in query_result]
sorted_paths_np = np.array(sorted_paths)
print(sorted_paths)

if not pt.started():
    pt.init()

files = pt.io.find_files("en")
indexer = pt.FilesIndexer("C:/Users/leo_2/OneDrive/Documentos/GitHub/Recuperacion de la Informacion/Recuperacion-de-la-Informacion/TP 2/EJ 6/index", verbose=True, overwrite=True, meta={"docno":20, "filename":512})
indexref = indexer.index(files)
index = pt.IndexFactory.of(indexref)

br =  pt.BatchRetrieve(index, num_results=50, wmodel="TF_IDF", metadata=["filename"])
results = br.search(query)

tfidf = np.array(results["filename"])
print(tfidf)

spearmancoefficient, datos = spearmanr(tfidf[:5], sorted_paths_np[:5])
print("Coeficiente de correlación de Spearman 5 elementos:", spearmancoefficient,)

spearmancoefficient, datos = spearmanr(tfidf[:10], sorted_paths_np[:10])
print("Coeficiente de correlación de Spearman 10 elementos:", spearmancoefficient,)