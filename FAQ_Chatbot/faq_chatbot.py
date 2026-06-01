import pandas as pd
import nltk
import string

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

nltk.download('punkt', quiet=True)
nltk.download('stopwords', quiet=True)
nltk.download('punkt_tab', quiet=True)

data = pd.read_csv("faqs.csv")

questions = data["question"].tolist()
answers = data["answer"].tolist()

def preprocess(text):
    text = text.lower()

    words = word_tokenize(text)

    filtered_words = [
        word for word in words
        if word not in string.punctuation
        and word not in stopwords.words("english")
    ]

    return " ".join(filtered_words)

processed_questions = [preprocess(q) for q in questions]

vectorizer = TfidfVectorizer()
faq_vectors = vectorizer.fit_transform(processed_questions)

def chatbot(user_input):

    processed_input = preprocess(user_input)

    user_vector = vectorizer.transform([processed_input])

    similarity_scores = cosine_similarity(user_vector, faq_vectors)

    best_match_index = similarity_scores.argmax()

    best_score = similarity_scores[0][best_match_index]

    if best_score > 0.3:
        return answers[best_match_index]
    else:
        return "Sorry, I could not find a matching answer."

print("\n===== IPL 2026 FAQ CHATBOT =====")
print("Type 'exit' to quit.\n")

while True:

    user_question = input("You: ")

    if user_question.lower() == "exit":
        print("Chatbot: Goodbye!")
        break

    response = chatbot(user_question)

    print("Chatbot:", response)