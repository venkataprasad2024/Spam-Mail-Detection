<p align="center"> 
  <img src="image/Email Logo.png" alt="Spam Detector Logo" width="90px" height="90px">
</p>

<h1 align="center">Spam Mail Detection System</h1>

<p align="center">
An end-to-end AI-powered spam email detection system built using Machine Learning, Flask, and React.
</p>

<p align="center">
🌐 Live Demo:  
<a href="https://spam-mail-detection-tau.vercel.app/" target="_blank">
https://spam-mail-detection-tau.vercel.app/
</a>
</p>

<p align="center"> 
<img src="gif/spam detector.gif" alt="Spam Detector Demo" height="380px">
</p>

---

## 📌 Project Overview

This project is a **full-stack spam email detection system** that classifies emails as **Spam** or **Ham (Not Spam)** using the **Naive Bayes classification algorithm**.

The backend is implemented using **Python & Flask**, where the Machine Learning model is trained and exposed via REST APIs.  
The frontend is built using **React (Vite)** and provides a clean, modern UI for users to test email content in real time.

---

## 🧠 Machine Learning Approach

- Algorithm: **Naive Bayes Classifier**
- Feature Extraction: **Bag of Words**
- Smoothing: **Laplace Smoothing**
- Classification: **Probabilistic text classification**

The model is trained once at server startup and reused for all incoming prediction requests to ensure optimal performance.

---

## 🏗️ Tech Stack

### Frontend
- React (Vite)
- Tailwind CSS
- Axios

### Backend
- Python
- Flask
- Flask-CORS
- NumPy

### Deployment
- **Frontend** → Vercel  
- **Backend** → Render

---

## 📁 Project Structure

Spam-Mail-Detection/
│
├── backend/
│   ├── app.py                # Flask API entry point
│   ├── spam_detector.py      # Core Naive Bayes logic
│   ├── train.py              # Model training script
│   ├── test.py               # Model evaluation script
│   ├── requirements.txt      # Backend dependencies
│   ├── train/                # Training email dataset
│   └── test/                 # Testing email dataset
│
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   │   └── SpamChecker.jsx   # Main UI component
│   │   ├── App.jsx
│   │   └── main.jsx
│   ├── public/
│   ├── index.html
│   ├── package.json
│   ├── vite.config.js
│   └── tailwind.config.js
│
├── gif/
│   └── spam detector.gif     # Demo animation
│
├── image/
│   ├── Email Logo.png
│   ├── 1.png
│   ├── 2.png
│   └── 3.png
│
└── README.md

## 🖥️ Local Setup Instructions

### Backend
cd backend
pip install -r requirements.txt
python app.py

### Frontend
cd frontend
npm install
npm run dev

## 🌍 Deployment

Frontend  → Vercel  
Backend   → Render  
Communication via HTTPS REST APIs

## 🎯 Future Enhancements

- Advanced NLP preprocessing
- Improved model accuracy
- Email file upload support
- User authentication
- Prediction history tracking
- Analytics dashboard

## 👨‍💻 Author

Venkata Prasad  
Full Stack Developer | Machine Learning Enthusiast  

GitHub: https://github.com/venkataprasad2024  
Live Demo: https://spam-mail-detection-tau.vercel.app/

⭐ If you like this project, don’t forget to star the repository!
