from sentence_transformers import SentenceTransformer
import scipy.spatial

class SimilarityChecker:

    

    def __init__(self):
        self.model = SentenceTransformer('bert-base-nli-mean-tokens')

    def check_news_similarity(self, article_text, sentence):
        sentence_l = [sentence]
        article_l = [article_text]
        text_embeddings = self.model.encode(article_l)
        sentence_embeddings = self.model.encode(sentence_l)

        distance = scipy.spatial.distance.cdist(sentence_embeddings, text_embeddings, "cosine")[0]
        results = zip(range(len(distance)), distance)
       
        results = sorted(results, key=lambda x: x[1])
       
        max_similarity = 1 - results[0][1]
        return max_similarity