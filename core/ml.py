import numpy as np
from sentence_transformers import SentenceTransformer
from .models import Mentor

model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text).tolist()

def cosine(a, b):
    a = np.array(a)
    b = np.array(b)
    return np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))

def match_mentors(mentee):
    results = []

    for mentor in Mentor.objects.exclude(embedding=None):
        score = cosine(mentee.embedding, mentor.embedding)
        results.append((mentor, score))

    results.sort(key=lambda x: x[1], reverse=True)
    return results[:10]
