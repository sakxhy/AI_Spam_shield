import pandas as pd
import numpy as np
import string
import warnings
import sys
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
from sklearn.pipeline import Pipeline
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report, accuracy_score
import joblib

# Download necessary NLTK datasets (only downloads if not already present)
try:
    nltk.download('stopwords', quiet=True)
    nltk.download('wordnet', quiet=True)
except Exception:
    pass

def explain_step(title, description):
    """Helper function to print clear explanations for the user."""
    print(f"\n[{title.upper()}]")
    print("-" * 50)
    print(description)
    print("-" * 50)

def clean_text(text):
    """
    Cleans and tunes the raw text data:
    1. Removes punctuation.
    2. Converts all text to lowercase.
    3. Removes common 'stop words' (e.g., 'the', 'is', 'in').
    4. Applies Lemmatization (converts words to their base form, e.g., 'running' -> 'run').
    """
    # 1. Remove punctuation
    nopunc = [char for char in text if char not in string.punctuation]
    nopunc = ''.join(nopunc)
    
    # 2. Lowercase and 3. Remove stopwords
    lemmatizer = WordNetLemmatizer()
    clean_words = []
    for word in nopunc.split():
        if word.lower() not in stopwords.words('english'):
            # 4. Lemmatization (base form)
            clean_words.append(lemmatizer.lemmatize(word.lower()))
            
    return " ".join(clean_words)

def train_model():
    explain_step("Step 1: Data Collection & Loading", 
                 "We are loading a dataset of ~5,500 SMS messages ('sms.tsv') "
                 "that has been hand-labeled as either 'ham' (safe/normal) or 'spam' (junk).")
                 
    try:
        # Load local dataset
        df = pd.read_csv("sms.tsv", sep='\t', header=None, names=['label', 'message'])
        print(f"✅ Successfully loaded {len(df)} messages.")
    except Exception as e:
        print(f"❌ Error loading dataset: {e}")
        return None
        
    # Convert labels to numerical format: 'ham' = 0, 'spam' = 1
    df['label_num'] = df.label.map({'ham':0, 'spam':1})
    
    explain_step("Step 2: Data Cleaning & Tuning", 
                 "Raw text is messy. It contains punctuation, uppercase/lowercase variations, "
                 "and common words ('the', 'a', 'is') that don't help detect spam. "
                 "\nWe created a 'clean_text' function to remove these and reduce words to their base form (Lemmatization).")
    
    print("⏳ Applying text cleaning to all messages (this might take a few seconds)...")
    # Apply our tuning function to the 'message' column to create clean data
    df['clean_message'] = df['message'].apply(clean_text)
    print("✅ Text cleaning complete.\n")
    print(f"Example Before: {df['message'].iloc[1]}\nExample After:  {df['clean_message'].iloc[1]}")
    
    
    explain_step("Step 3: Train / Test Split", 
                 "To evaluate our model properly, we must hold out some data it has NEVER SEEN before. "
                 "We split the dataset: 80% for training the model, and 20% for testing its accuracy.")
    
    X = df['clean_message']
    y = df['label_num']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    print(f"Training data size: {len(X_train)} | Testing data size: {len(X_test)}")
    
    
    explain_step("Step 4: Building the NLP Pipeline", 
                 "A machine learning model cannot understand text. It needs numbers. "
                 "\n1. TfidfVectorizer: Converts the cleaned text into numerical features. "
                 "It counts word frequencies but mathematically penalizes words that appear too often across all messages. "
                 "\n2. MultinomialNB: The Naive Bayes algorithm. It calculates the probability of a message being spam based on the words it contains.")
    
    # TfidfVectorizer combines the CountVectorizer and TfidfTransformer steps from earlier into one powerful step.
    pipeline = Pipeline([
        ('tfidf', TfidfVectorizer(max_features=5000)), # max_features limits the vocabulary to the top 5000 terms to speed up and reduce noise
        ('clf', MultinomialNB())
    ])
    
    print("⏳ Training the Naive Bayes model...")
    pipeline.fit(X_train, y_train)
    print("✅ Training complete.")
    
    
    explain_step("Step 5: Model Evaluation", 
                 "Now we test the model on the 20% data it has never seen to measure its accuracy, precision, and recall.")
    
    predictions = pipeline.predict(X_test)
    acc = accuracy_score(y_test, predictions)
    print(f"Overall Accuracy: {acc * 100:.2f}%\n")
    print(classification_report(y_test, predictions, target_names=['Ham (Safe)', 'Spam']))
    
    # Save the model
    explain_step("Step 6: Saving Model", 
                 "Saving the trained pipeline to 'model.pkl' for use in the web application.")
    joblib.dump(pipeline, 'model.pkl')
    print("✅ Model saved successfully as 'model.pkl'.\n")
    
    return pipeline

def detect_spam(model, message):
    """
    Detects if a given message is SPAM.
    Creates a prominent warning using the 'warnings' library if SPAM is detected.
    """
    prediction = model.predict([message])[0]
    
    if prediction == 1:
        # Spam detected: Issue a warning
        warning_msg = (
            f"\n\n🚨 *** SPAM WARNING *** 🚨\n"
            f"The following message has been flagged as SPAM:\n"
            f"'{message}'\n"
            f"Please exercise caution. Do not click on any suspicious links or provide personal information!\n"
        )
        warnings.warn(warning_msg, UserWarning)
        return True
    else:
        print(f"✅ Message is safe (Ham): '{message}'")
        return False

if __name__ == "__main__":
    print("==================================================")
    print(" 🛡️  NLP Spam Detector Initialization & Training ")
    print("==================================================")
    
    model = train_model()
    
    if model:
        explain_step("Step 6: Live Spam Detection Warning", 
                     "We will now test the final pipeline with sample messages. "
                     "If the model predicts a message is spam, we will issue a system alert using Python's 'warnings' library.")
        
        print("\n--- Test 1: Normal (Ham) Message ---")
        test_ham = "Hey! Are we still meeting for coffee at 4 PM?"
        detect_spam(model, test_ham)
        
        print("\n--- Test 2: Spam Message ---")
        test_spam = "CONGRATULATIONS! You have been selected to win a $1000 gift card! Click http://spam.link/claim to claim your prize IMMEDIATELY!"
        detect_spam(model, test_spam)
        
        print("\n✅ Detector tests completed successfully.\n")
