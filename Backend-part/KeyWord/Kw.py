import uuid
from  keybert import KeyBERT
from llama_cpp import Llama 

payload = {}
payload["id"] = uuid.uuid4()
payload["Content"] = """Supervised learning is the machine learning task of learning a function that
                        maps an input to an output based on example input-output pairs. It infers a
                        function from labeled training data consisting of a set of training examples.
                        In supervised learning, each example is a pair consisting of an input object
                        (typically a vector) and a desired output value (also called the supervisory signal).
                        A supervised learning algorithm analyzes the training data and produces an inferred function,
                        which can be used for mapping new examples. An optimal scenario will allow for the
                        algorithm to correctly determine the class labels for unseen instances. This requires
                        the learning algorithm to generalize from the training data to unseen situations in a
                        'reasonable' way (see inductive bias)."""
                        


def kewords(id,content):
    k = {}
    model_path = "bge-small-en-v1.5-q4_k_m.gguf"
    model = Llama(model_path, embedding=True) #path to the quantized model
    kw_model = KeyBERT(model=model)
    words = kw_model.extract_keywords(content, keyphrase_ngram_range = (1,1) ,stop_words ="english")
    k['id'] = id
    k['KeyWords'] = [i[0] for i in words]
    return k

ans = kewords(payload['id'],payload['Content'])
print(ans)