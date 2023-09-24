from sentence_transformers import SentenceTransformer, util

def compare_sentences(sentence1, sentence2):
    model = SentenceTransformer('paraphrase-MiniLM-L6-v2')

    # Encode sentences to get their embeddings
    embedding1 = model.encode(sentence1, convert_to_tensor=True)
    embedding2 = model.encode(sentence2, convert_to_tensor=True)

    # Compute cosine similarity between embeddings
    similarity = util.pytorch_cos_sim(embedding1, embedding2)[0][0].item()
    return similarity

# Example sentences
sentence1 = "My wife name is priyanka"
sentence2 = "I love my wife"

# Get similarity
similarity = compare_sentences(sentence1, sentence2)
print(f'Similarity: {similarity:.2f}')
