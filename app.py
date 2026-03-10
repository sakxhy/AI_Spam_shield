from flask import Flask, request, jsonify, render_template
import joblib
import os

app = Flask(__name__)

# Load the trained model
MODEL_PATH = "model.pkl"

if not os.path.exists(MODEL_PATH):
    print(f"Error: {MODEL_PATH} not found. Please run spam_detector.py to train and save the model first.")

@app.route('/')
def home():
    """Serves the main HTML page."""
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """API Endpoint to predict if a message is spam."""
    try:
        data = request.get_json()
        message = data.get('message', '')

        if not message.strip():
            return jsonify({'error': 'Message cannot be empty'}), 400

        # Load model on demand to ensure we always have the latest if retrained, 
        # though loading once at startup is faster in production.
        model = joblib.load(MODEL_PATH)
        
        # Predict: 1 for Spam, 0 for Ham
        prediction = model.predict([message])[0]
        
        result = {
            'is_spam': bool(prediction == 1),
            'message_checked': message
        }
        
        return jsonify(result)

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True, port=8000)
