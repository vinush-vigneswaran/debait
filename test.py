import cohere
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

with open('api_key.txt') as f:
    api_key = f.readlines()

co = cohere.Client(api_key[0])
response = co.embed(
  model='large',
  texts=["hello", "hi"])

vec = np.array(response.embeddings)

print(cosine_similarity([vec[0]], [vec[1]]))

