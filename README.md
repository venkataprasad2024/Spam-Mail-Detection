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

