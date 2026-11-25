from sentence_transformers import SentenceTransformer

print("Loading semantic model...")

model = SentenceTransformer("all-MiniLM-L6-v2")

sentences = [
    "Important concepts in machine learning",
    "Fundamental ideas behind computers learning from data",
    "How to cook delicious food"
]

embeddings = model.encode(sentences)

print("\nEmbedding shape:", embeddings.shape)

similarities = model.similarity(
    embeddings,
    embeddings
)

print("\nSimilarity scores:")
print(similarities)

print("\nSemantic model working!")
