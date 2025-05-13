from flask import Flask, request, jsonify, render_template
import pickle
import re

app = Flask(__name__)

# Load the trained model and vectorizer
def load_model():
    with open("logistic_regression_model.pkl", "rb") as model_file:
        loaded_model = pickle.load(model_file)
    with open("tfidf_vectorizer.pkl", "rb") as vectorizer_file:
        loaded_vectorizer = pickle.load(vectorizer_file)
    return loaded_model, loaded_vectorizer

loaded_model, loaded_vectorizer = load_model()

# Preprocessing function
def preprocess_url(url):
    if not isinstance(url, str):
        return ""
    url = re.sub(r"https?://", "", url)
    url = re.sub(r"[^a-zA-Z0-9./]", " ", url)
    return url.lower()

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    url = data.get("url", "")
    processed_url = preprocess_url(url)
    X_new = loaded_vectorizer.transform([processed_url])
    prediction = loaded_model.predict(X_new)
    result = "🚨 Phishing URL Detected!" if prediction[0] == 1 else "✅ Legitimate URL"
    return jsonify({"result": result})

@app.route("/", methods=["GET"])
def home():
    return render_template("webpage.html")

if __name__ == "__main__":
    app.run(debug=True)
