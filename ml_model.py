from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline

# Sample training dataset
training_data = [
    ("I feel very stressed about exams", "Stress"),
    ("I am happy today", "Happy"),
    ("I feel lonely and sad", "Sad"),
    ("I am anxious about my future", "Anxiety"),
    ("Everything is going great", "Happy"),
    ("I feel depressed", "Sad"),
    ("I am worried about my results", "Anxiety"),
    ("I feel relaxed and calm", "Happy"),
    ("I feel overwhelmed", "Stress"),
]

texts, labels = zip(*training_data)

model = Pipeline([
    ('vectorizer', CountVectorizer()),
    ('classifier', MultinomialNB())
])

model.fit(texts, labels)

def predict_emotion(text):
    return model.predict([text])[0]
