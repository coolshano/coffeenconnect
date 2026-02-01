import numpy as np
from sentence_transformers import SentenceTransformer
from .models import Mentor


model = SentenceTransformer("all-MiniLM-L6-v2")

def get_embedding(text):
    return model.encode(text).tolist()

def cosine_similarity(a, b):
    if not a or not b:
        return 0

    a = np.array(a)
    b = np.array(b)

    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))

 # ensure this is imported

def match_mentors(mentee):
    field = mentee.user.userprofile.interested_field

    mentors = Mentor.objects.filter(
        user__userprofile__interested_field=field
    )

    results = []
    for mentor in mentors:
        if mentor.embedding and mentee.embedding:
            score = cosine_similarity(mentee.embedding, mentor.embedding)
            results.append((mentor, score))

    return sorted(results, key=lambda x: x[1], reverse=True)

