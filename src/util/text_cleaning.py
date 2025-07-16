import re
import spacy
import string
from nltk.corpus import stopwords

# Download stopwords if not already downloaded
import nltk
nltk.download('stopwords')

nlp = spacy.load("en_core_web_sm")
stop_words = set(stopwords.words('english'))

def clean_text(text):
    """
    Improved cleaner: keeps more context, avoids over-cleaning.
    """
    # Remove URLs
    text = re.sub(r'http\S+|www\S+|https\S+', '', text)

    # Remove markdown formatting (lightly)
    text = re.sub(r'[\*\[\]\(\)\>]', '', text)

    # Lowercase text
    text = text.lower()

    # Tokenize and lemmatize
    doc = nlp(text)
    cleaned = []
    for token in doc:
        # Keep alpha and alphanumeric tokens (to prevent loss of terms like 'gpt-3', 'ai123')
        if not token.is_stop and (token.is_alpha or token.is_ascii):
            cleaned.append(token.lemma_)
    
    return ' '.join(cleaned)
