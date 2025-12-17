from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import os
from spam_detector import *

app = Flask(__name__)
CORS(app)

# =====================================================
# LOAD MODEL ONLY ONCE
# =====================================================

print("Loading spam detection model...")

MODEL_READY = False

def load_model():
    global all_trainWords, spam_trainWords, ham_trainWords
    global all_uniqueWords, spam_cond, ham_cond, p_spam, p_ham
    global MODEL_READY

    if MODEL_READY:
        return

    all_trainWords, spam_trainWords, ham_trainWords = trainWord_generator()
    all_uniqueWords = unique_words(all_trainWords)

    total_emails = number_of_allEmails()
    spam_emails = number_of_spamEmails()

    p_spam = spam_probability(total_emails, spam_emails)
    p_ham = ham_probability(total_emails, total_emails - spam_emails)

    delta = 1
    spam_bag, ham_bag = bagOfWords_genarator(
        all_uniqueWords, spam_trainWords, ham_trainWords
    )

    smoothed_spam, smoothed_ham = smoothed_bagOfWords(
        all_uniqueWords, spam_bag, ham_bag, delta
    )

    spam_cond = spam_condProbability(
        all_uniqueWords, spam_bag, smoothed_spam, delta
    )
    ham_cond = ham_condProbability(
        all_uniqueWords, ham_bag, smoothed_ham, delta
    )

    MODEL_READY = True
    print("Model loaded successfully!")

# Load once at startup
load_model()

# =====================================================
# PREDICTION LOGIC
# =====================================================

def predict_email(text):
    words = text_parser(text.lower())

    log_spam = np.log(p_spam)
    log_ham = np.log(p_ham)

    for w in words:
        if w in all_uniqueWords:
            log_spam += np.log(spam_cond.get(w, 1e-10))
            log_ham += np.log(ham_cond.get(w, 1e-10))

    prediction = "spam" if log_spam > log_ham else "ham"
    confidence = abs(log_spam - log_ham)

    return prediction, confidence

# =====================================================
# ROUTES
# =====================================================

@app.route("/")
def home():
    return "Backend is running"

@app.route("/predict", methods=["POST"])
def predict_api():
    data = request.get_json(force=True)

    text = (
        data.get("email")
        or data.get("text")
        or data.get("message")
        or ""
    ).strip()

    if not text:
        return jsonify({"error": "No email text provided"}), 400

    prediction, confidence = predict_email(text)

    return jsonify({
        "prediction": prediction,
        "confidence": round(confidence, 4),
        "is_spam": prediction == "spam"
    })

# =====================================================
# RUN SERVER (RENDER / PRODUCTION SAFE)
# =====================================================

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(
        host="0.0.0.0",
        port=port,
        debug=False,
        use_reloader=False
    )
