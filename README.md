# AI Spam Shield 🛡️

A modern, high-performance web application powered by Natural Language Processing (NLP) that accurately detects and flags SPAM SMS messages.

![AI Spam Shield Interface](https://via.placeholder.com/800x400.png?text=AI+Spam+Shield+UI)  
*(Add a screenshot of your web interface here!)*

## 🌟 Features
- **High Accuracy NLP Engine**: Utilizes an optimized Multinomial Naive Bayes model generating ~98% predictive accuracy.
- **Robust Text Preprocessing**: Incorporates NLTK for punctuation stripping, stop-word removal, and full lemmatization.
- **Premium User Interface**: Features "Motion UI" with smooth CSS animations, asynchronous loading states, and frosted-glass aesthetics (Glassmorphism).
- **Fast Inference Server**: Lightweight Flask REST API backend (`app.py`) built solely for serving inference requests quickly.

## 🛠️ Technology Stack
- **Backend / Machine Learning**: Python 3, scikit-learn, pandas, NLTK, joblib
- **Web Server API**: Flask
- **Frontend**: Vanilla HTML5, Vanilla CSS3, JavaScript (AJAX/Fetch)

---

## 🚀 Quick Start Guide

### 1. Clone the Repository
```bash
git clone https://github.com/your-username/Spam_detection_project.git
cd Spam_detection_project
```

### 2. Set Up the Virtual Environment
It is recommended to run this project inside an isolated virtual environment.
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows, use: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Train the Model (Optional)
The pre-trained model (`model.pkl`) may already be provided. However, to re-download the latest dataset, re-tune the NLP features, and generate a fresh `model.pkl` file, run the core script:
```bash
python3 spam_detector.py
```

### 5. Launch the Web Server
Start the Flask application. It runs on **Port 8000** by default (avoiding macOS port 5000 AirPlay conflicts).
```bash
python3 app.py
```

### 6. Use the App
Open your favorite web browser and navigate to:  
`http://127.0.0.1:8000`

---

## 🧠 How It Works (The NLP Pipeline)

If you are interested in the mathematical logic behind the spam detection, the project follows these steps:
1. **Data Cleaning**: Non-essential characters, common English 'stop-words', and casing are stripped away from raw SMS strings.
2. **Lemmatization**: Words are reduced to their base root structure (e.g., *running* → *run*).
3. **TF-IDF Vectorization**: Text is converted into numerical sequences. It highlights words that are frequent in a specific message (Term Frequency) but are mathematically penalized if they appear too often across all messages (Inverse Document Frequency).
4. **Naive Bayes Classification**: Uses Bayes' Theorem of probability to determine if the message clusters closer to known SPAM characteristics or HAM (safe) characteristics based on the isolated keywords.

## 🤝 Contributing
Contributions are more than welcome! 
1. Fork the project.
2. Create your feature branch (`git checkout -b feature/CoolFeature`).
3. Commit your changes (`git commit -m 'Add some CoolFeature'`).
4. Push to the branch (`git push origin feature/CoolFeature`).
5. Open a pull request.
