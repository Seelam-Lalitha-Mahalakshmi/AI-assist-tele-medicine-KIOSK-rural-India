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
🏥 Patient Registration

The patient registration form collects:

Patient name
Phone number
Age
Gender
Address
Symptoms
Medical history

After registration, the entered symptoms are processed by the Machine Learning model and a predicted disease is generated.

The patient information and prediction are then stored in the SQLite database.

📊 Dashboard

The dashboard provides:

Total number of patients
Disease-wise patient distribution
Age-group distribution
Patient records
Search functionality
Disease filtering
Recent patient registrations

Example age groups:

Under 18
18–45
46–60
Over 60
🗄️ Database

The application uses SQLite.

Patients Table
Field	Description
id	Unique patient ID
name	Patient name
phone	Patient phone number
age	Patient age
gender	Patient gender
address	Patient address
symptoms	Reported symptoms
medical_history	Previous medical history
predicted_disease	AI predicted disease
created_at	Registration timestamp
🔌 API Endpoint

The application provides a statistics API:

GET /api/stats

The endpoint returns disease-wise statistics in JSON format.

Example:

{
  "labels": [
    "Allergy",
    "Diabetes",
    "Influenza"
  ],
  "data": [
    5,
    3,
    4
  ]
}
🩺 Supported Disease Information

The application contains predefined medical information for diseases such as:

Allergy
Thyroid Disorder
Influenza
Stroke
Heart Disease
Food Poisoning
Bronchitis
COVID-19
Dermatitis
Diabetes
Arthritis

For each prediction, the application can display:

Recommended doctor/specialist
General medical information
Risk level
Emergency contact
Healthcare advice
