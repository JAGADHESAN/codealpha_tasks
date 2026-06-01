import pandas as pd
import nltk
import string
import streamlit as st

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

st.set_page_config(
    page_title="IPL 2026 FAQ Chatbot",
    page_icon="🏏",
    layout="wide"
)
st.image("ipl_banner.jpg", use_container_width=True)

st.markdown("""
<style>
.main {
    background-color: #f8f9fa;
}

.title {
    text-align: center;
    color: #004ba0;
    font-size: 40px;
    font-weight: bold;
}

.subtitle {
    text-align: center;
    color: #ff6f00;
    font-size: 20px;
}

.answer-box {
    background-color: #e8f5e9;
    padding: 15px;
    border-radius: 10px;
    font-size: 18px;
}
</style>
""", unsafe_allow_html=True)

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

    similarity = cosine_similarity(user_vector, faq_vectors)

    best_match_index = similarity.argmax()

    best_score = similarity[0][best_match_index]

    if best_score > 0.3:
        return answers[best_match_index]
    else:
        return "Sorry, no matching IPL answer found."

st.markdown('<p class="title">🏏 IPL 2026 FAQ CHATBOT 🏏</p>',
            unsafe_allow_html=True)

st.markdown('<p class="subtitle">Cricket Insights & Predictions</p>',
            unsafe_allow_html=True)

st.sidebar.title("🏆 IPL 2026")

st.sidebar.info("""
💡 Try asking:

🏏 Which teams is been qualified for playoffs?

🏏 Which team is been eliminated first?

🏏 Who is the highest six hitter in IPL 2026?

🏏 Who has the impact bowling figures?

🏏 Will RCB win the consecutive back to back trophies?

🏏 Will Virat Kohli's 973 runs record be broken?
""")

st.sidebar.markdown("---")

st.sidebar.caption("Powered by NLP + TF-IDF + Cosine Similarity")

user_question = st.text_input(
    "💬 Ask your IPL question:"
)

if st.button("Get Answer"):

    if user_question:

        response = chatbot(user_question)

        st.markdown(
            f'<div class="answer-box"><b>Answer:</b> {response}</div>',
            unsafe_allow_html=True
        )

st.markdown("---")
st.markdown("🏏 Developed as an NLP FAQ Chatbot Project")