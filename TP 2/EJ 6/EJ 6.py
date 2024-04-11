import os
import re
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_documents(directory):
    documents = {}
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(".html"):
                filepath = os.path.join(root, filename)
                with open(filepath, "r", encoding="utf-8") as file:
                    content = file.read()
                    documents[filename] = content
    return documents

def preprocess_text(text):
    text = re.sub(r"[^\w\s]", "", text.lower())
    return text

def rank_documents(query, documents, n=10):
    vectorizer = TfidfVectorizer(preprocessor=preprocess_text)
    corpus = list(documents.values())
    X = vectorizer.fit_transform(corpus)
    query_vector = vectorizer.transform([query])
    similarities = cosine_similarity(X, query_vector)
    ranked_indices = similarities.argsort(axis=0)[::-1].flatten()
    ranked_documents = [(list(documents.keys())[i], similarities[i][0]) for i in ranked_indices[:n]]
    return ranked_documents

def main():
    directory = "en"
    documents = read_documents(directory)
    query = input("Ingrese su consulta: ")
    ranked_documents = rank_documents(query, documents)
    for doc_id, score in ranked_documents:
        print(f"Documento: {doc_id}, Puntaje: {score:.4f}")

if __name__ == "__main__":
    main()
