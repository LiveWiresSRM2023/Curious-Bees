from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer

def extract_keywords(blog_text):
    # Step 1: Tokenize the text (split it into words)
    vectorizer = CountVectorizer()
    X = vectorizer.fit_transform([blog_text])
    words = vectorizer.get_feature_names_out()

    # Step 2: Calculate term frequencies
    transformer = TfidfTransformer()
    tfidf = transformer.fit_transform(X)

    # Step 3: Get words with their TF-IDF scores
    scores = tfidf.toarray()[0]
    word_scores = list(zip(words, scores))

    # Step 4: Sort words by TF-IDF score (higher score means more important)
    sorted_word_scores = sorted(word_scores, key=lambda x: x[1], reverse=True)

    # Step 5: Extract keywords (top keywords based on TF-IDF score)
    top_keywords = [word for word, score in sorted_word_scores[:5]]  # Adjust number of keywords as needed

    return top_keywords



# blog contains exactly 512 chars


# Example usage:
blog_text = """
    Machine learning is a branch of artificial intelligence that focuses on the development
      of algorithms allowing computers to learn from and make decisions based on data.
      It encompasses supervised learning, unsupervised learning, and reinforcement learning.
      Applications range from image recognition to natural language processing, revolutionizing
      industries like healthcare and finance.

    """

keywords = extract_keywords(blog_text)
print("Keywords:", keywords)

# results
# so poor in this method
# Keywords: ['learning', 'and', 'from', 'of', 'on']