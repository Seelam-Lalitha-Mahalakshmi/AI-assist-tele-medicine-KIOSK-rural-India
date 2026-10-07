# 🏥 AI-Powered Telemedicine Kiosk for Rural India

An AI-powered telemedicine application designed to assist people in rural areas with preliminary disease prediction and healthcare guidance.

The system allows healthcare workers to register patient information, enter symptoms, predict a possible disease using a Machine Learning model, and view suggested medical information through an easy-to-use web interface.

> ⚠️ **Disclaimer:** This project is intended for educational and demonstration purposes only. AI predictions should not replace diagnosis or treatment by qualified healthcare professionals.

---

## 🚀 Features

- 🔐 Secure login system
- 👤 Patient registration
- 📝 Patient information management
- 🤖 AI-based disease prediction
- 💾 SQLite database integration
- 👨‍⚕️ Doctor recommendation
- 💊 Suggested medicines and healthcare advice
- 🚨 Risk-level classification
- 📞 Emergency contact information
- 📊 Healthcare dashboard
- 🔎 Patient search functionality
- 🏷️ Disease-based filtering
- 📈 Disease-wise statistics
- 👥 Age-group statistics
- 🔄 Dynamic statistics API
- 🌐 Responsive web interface

---

## 🧠 How the System Works

```text
             ┌─────────────────────┐
             │       Patient       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Patient Registration│
             │  Name / Age / etc.  │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │  Enter Symptoms     │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Text Preprocessing  │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ ML Vectorizer       │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ ML Disease Model    │
             └──────────┬──────────┘
                        │
                        ▼
             ┌─────────────────────┐
             │ Disease Prediction  │
             └──────────┬──────────┘
                        │
              ┌─────────┴─────────┐
              ▼                   ▼
       ┌──────────────┐    ┌───────────────┐
       │ SQLite DB    │    │ Medical Advice│
       └──────────────┘    └───────────────┘
              │
              ▼
       ┌──────────────┐
       │  Dashboard   │
       └──────────────┘

Healthcare advice
