import os
import sqlite3
import joblib
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify

app = Flask(__name__)
app.secret_key = 'telemedicine_kiosk_secret_key_rural_india'

# Default login credentials
DEFAULT_USER = 'admin'
DEFAULT_PASS = 'admin123'

# Disease Metadata Mapping for Predictions & Advice
DISEASE_DETAILS = {
    "Allergy": {
        "doctor": "Dr. Ramesh Patel (Allergist)",
        "medicines": "Cetirizine (10mg) once daily, Fluticasone Nasal Spray",
        "advice": "Identify and avoid allergen triggers. Wash bedding in hot water. Keep doors and windows closed during high pollen seasons.",
        "risk_level": "Safe",
        "risk_color": "success",
        "emergency_contact": "+91 98765 43210"
    },
    "Thyroid Disorder": {
        "doctor": "Dr. Sunita Sharma (Endocrinologist)",
        "medicines": "Levothyroxine (50mcg) on empty stomach, Selenium supplements",
        "advice": "Take thyroid medication daily at least 30 minutes before breakfast. Get thyroid profile blood tests every 3 months.",
        "risk_level": "Moderate",
        "risk_color": "warning",
        "emergency_contact": "+91 98765 43211"
    },
    "Influenza": {
        "doctor": "Dr. Anil Kumar (General Physician)",
        "medicines": "Oseltamivir (75mg), Paracetamol (650mg) for fever, Cough Lozenges",
        "advice": "Ensure plenty of bed rest and hydration. Stay isolated to avoid spreading the flu. Consume warm fluids like soups.",
        "risk_level": "Moderate",
        "risk_color": "warning",
        "emergency_contact": "+91 98765 43212"
    },
    "Stroke": {
        "doctor": "Dr. Rajesh Gupta (Neurologist)",
        "medicines": "Aspirin (under emergency supervision), Anti-hypertensives",
        "advice": "CRITICAL: Act FAST. A stroke is a medical emergency. Do not attempt home remedies. Head immediately to the nearest hospital with CT scan facility.",
        "risk_level": "Emergency",
        "risk_color": "danger",
        "emergency_contact": "102 / +91 98765 43213"
    },
    "Heart Disease": {
        "doctor": "Dr. K. S. Rao (Cardiologist)",
        "medicines": "Atorvastatin (20mg), Metoprolol (25mg), Nitroglycerin (under emergency sublingual)",
        "advice": "Monitor blood pressure regularly. Avoid fatty, high-cholesterol foods. Rest immediately if chest discomfort or shortness of breath occurs.",
        "risk_level": "Emergency",
        "risk_color": "danger",
        "emergency_contact": "102 / +91 98765 43214"
    },
    "Food Poisoning": {
        "doctor": "Dr. Meena Joshi (Gastroenterologist)",
        "medicines": "Oral Rehydration Salts (ORS), Loperamide (if diarrhea is severe), Probiotics",
        "advice": "Drink ORS solution continuously to prevent dehydration. Stick to a bland diet (banana, rice, applesauce, toast). Avoid dairy and fatty foods.",
        "risk_level": "Moderate",
        "risk_color": "warning",
        "emergency_contact": "+91 98765 43215"
    },
    "Bronchitis": {
        "doctor": "Dr. Vikas Saxena (Pulmonologist)",
        "medicines": "Levosalbutamol Inhaler, Guaifenesin expectorant, Warm steam inhalation",
        "advice": "Stay away from smoke and dust. Keep hydrated to help thin mucus in lungs. Perform steam inhalation twice daily.",
        "risk_level": "Moderate",
        "risk_color": "warning",
        "emergency_contact": "+91 98765 43216"
    },
    "COVID-19": {
        "doctor": "Dr. Anil Kumar (General Physician)",
        "medicines": "Paracetamol, Vitamin C, Zinc, Antivirals (if prescribed)",
        "advice": "Self-isolate immediately in a well-ventilated room. Wear a double mask. Measure body temperature and oxygen levels (SPO2) every 4 hours.",
        "risk_level": "Emergency",
        "risk_color": "danger",
        "emergency_contact": "1075 / +91 98765 43217"
    },
    "Dermatitis": {
        "doctor": "Dr. Priya Sen (Dermatologist)",
        "medicines": "Hydrocortisone Cream (1%), Cetirizine (10mg) for itching, Calamine lotion",
        "advice": "Apply moisturizer within 3 minutes of bathing. Avoid scratching the skin. Use mild, fragrance-free soaps.",
        "risk_level": "Safe",
        "risk_color": "success",
        "emergency_contact": "+91 98765 43218"
    },
    "Diabetes": {
        "doctor": "Dr. Sunita Sharma (Diabetologist)",
        "medicines": "Metformin (500mg) twice daily, Glimepiride (1mg)",
        "advice": "Control portion sizes, cut out white sugar, and increase fiber intake. Dedicate at least 30 minutes to walking daily. Regular foot care is vital.",
        "risk_level": "Moderate",
        "risk_color": "warning",
        "emergency_contact": "+91 98765 43219"
    },
    "Arthritis": {
        "doctor": "Dr. Sanjay Dutt (Rheumatologist)",
        "medicines": "Naproxen (500mg) as needed, Glucosamine, Topical pain-relief gel",
        "advice": "Engage in low-impact exercises like stretching or walking. Avoid heavy loading of painful joints. Apply hot packs for stiff joints.",
        "risk_level": "Safe",
        "risk_color": "success",
        "emergency_contact": "+91 98765 43220"
    },
    "Unknown": {
        "doctor": "Dr. Anil Kumar (General Physician)",
        "medicines": "Paracetamol (650mg) for general symptoms, ORS",
        "advice": "Monitor symptoms closely. If they worsen, seek professional medical attention at the nearest primary health center.",
        "risk_level": "Moderate",
        "risk_color": "warning",
        "emergency_contact": "+91 98765 43212"
    }
}

# Load AI Model files
try:
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    label_encoder = joblib.load('label_encoder.pkl')
    print("AI Model loaded successfully.")
except Exception as e:
    print(f"Error loading AI model: {e}. Running training first...")
    import subprocess
    subprocess.run(['python', 'train.py'])
    model = joblib.load('model.pkl')
    vectorizer = joblib.load('vectorizer.pkl')
    label_encoder = joblib.load('label_encoder.pkl')

def get_db_connection():
    db_path = 'telemedicine.db'
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn

# Initialize Database
def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS patients (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            phone TEXT NOT NULL,
            age INTEGER NOT NULL,
            gender TEXT NOT NULL,
            address TEXT NOT NULL,
            symptoms TEXT NOT NULL,
            medical_history TEXT,
            predicted_disease TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    
    # Check if database is empty to insert sample mock patients for dashboard
    cursor.execute("SELECT COUNT(*) FROM patients")
    if cursor.fetchone()[0] == 0:
        print("Seeding database with sample patients for UI presentation...")
        sample_patients = [
            ("Aarav Mehta", "+91 98123 45678", 29, "Male", "Village Rampur, Sector 2", "fever, back pain, shortness of breath", "No history", "Allergy"),
            ("Priya Sharma", "+91 98234 56789", 76, "Female", "Village Sonpur, Gali 4", "insomnia, back pain, weight loss", "Hypertension", "Thyroid Disorder"),
            ("Rajesh Kumar", "+91 98345 67890", 78, "Male", "Village Haripur, Block B", "sore throat, vomiting, diarrhea", "Diabetes", "Influenza"),
            ("Sunita Devi", "+91 98456 78901", 55, "Female", "Village Rampur, Sector 1", "swelling, appetite loss, nausea", "None", "Heart Disease"),
            ("Amit Patel", "+91 98567 89012", 49, "Male", "Village Gopalpur, Sector 3", "vomiting, swelling, dizziness, fatigue", "High Cholesterol", "Heart Disease"),
            ("Vikram Singh", "+91 98678 90123", 69, "Male", "Village Haripur, Block A", "anxiety, shortness of breath, appetite loss, cough, back pain", "Asthma", "Food Poisoning"),
            ("Neha Verma", "+91 98789 01234", 25, "Female", "Village Sonpur, Gali 1", "sore throat, weight loss, chest pain, depression, anxiety, rash", "None", "Bronchitis"),
            ("Karan Johar", "+91 98890 12345", 11, "Male", "Village Gopalpur, Gali 2", "insomnia, diarrhea, swelling", "None", "COVID-19"),
            ("Anil Kapoor", "+91 98901 23456", 47, "Male", "Village Rampur, Sector 4", "joint pain, shortness of breath, runny nose", "None", "Dermatitis"),
            ("Meena Kumari", "+91 99012 34567", 72, "Female", "Village Sonpur, Gali 3", "back pain, diarrhea, nausea, runny nose, joint pain, shortness of breath, depression", "Diabetes", "Diabetes")
        ]
        cursor.executemany('''
            INSERT INTO patients (name, phone, age, gender, address, symptoms, medical_history, predicted_disease)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', sample_patients)
        conn.commit()
        print("Database seeding completed.")
    conn.close()

init_db()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        remember = request.form.get('remember')
        
        if username == DEFAULT_USER and password == DEFAULT_PASS:
            session['logged_in'] = True
            session['username'] = username
            flash('Successfully logged in!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password.', 'danger')
            return render_template('login.html')
            
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('Logged out successfully.', 'info')
    return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if not session.get('logged_in'):
        flash('Please login to register a patient.', 'warning')
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        name = request.form.get('name')
        phone = request.form.get('phone')
        age = int(request.form.get('age'))
        gender = request.form.get('gender')
        address = request.form.get('address')
        symptoms = request.form.get('symptoms')
        medical_history = request.form.get('medical_history', '')
        
        if not name or not phone or not age or not gender or not address or not symptoms:
            flash('Please fill in all required fields.', 'danger')
            return render_template('register.html')
        
        # ML Disease Prediction
        try:
            # Vectorize symptoms
            cleaned_symptoms = symptoms.lower().strip()
            symptom_vector = vectorizer.transform([cleaned_symptoms])
            
            # Predict encoded label
            prediction_encoded = model.predict(symptom_vector)[0]
            
            # Decode label to disease string
            predicted_disease = label_encoder.inverse_transform([prediction_encoded])[0]
        except Exception as e:
            print(f"Prediction error: {e}. Falling back to default.")
            predicted_disease = "Unknown"
            
        # Store in Database
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO patients (name, phone, age, gender, address, symptoms, medical_history, predicted_disease)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ''', (name, phone, age, gender, address, symptoms, medical_history, predicted_disease))
        patient_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        flash('Patient registered successfully and AI disease analysis complete!', 'success')
        return redirect(url_for('result', patient_id=patient_id))
        
    return render_template('register.html')

@app.route('/result/<int:patient_id>')
def result(patient_id):
    if not session.get('logged_in'):
        flash('Please login to view results.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    patient = conn.execute('SELECT * FROM patients WHERE id = ?', (patient_id,)).fetchone()
    conn.close()
    
    if not patient:
        flash('Patient record not found.', 'danger')
        return redirect(url_for('dashboard'))
        
    # Get doctor recommendation, suggested medicines, advice, risk level, and emergency contact
    disease = patient['predicted_disease']
    details = DISEASE_DETAILS.get(disease, DISEASE_DETAILS["Unknown"])
    
    return render_template('result.html', patient=patient, details=details)

@app.route('/dashboard')
def dashboard():
    if not session.get('logged_in'):
        flash('Please login to access the dashboard.', 'warning')
        return redirect(url_for('login'))
        
    conn = get_db_connection()
    
    # Statistics counts
    total_patients = conn.execute('SELECT COUNT(*) FROM patients').fetchone()[0]
    
    # Disease-wise breakdown
    disease_stats = conn.execute('''
        SELECT predicted_disease, COUNT(*) as count 
        FROM patients 
        GROUP BY predicted_disease
    ''').fetchall()
    
    # Convert list of rows to a dictionary
    disease_distribution = {row['predicted_disease']: row['count'] for row in disease_stats}
    
    # Age groups breakdown
    age_stats = conn.execute('''
        SELECT 
            CASE 
                WHEN age < 18 THEN 'Under 18'
                WHEN age BETWEEN 18 AND 45 THEN '18-45'
                WHEN age BETWEEN 46 AND 60 THEN '46-60'
                ELSE 'Over 60'
            END as age_group,
            COUNT(*) as count
        FROM patients
        GROUP BY age_group
    ''').fetchall()
    age_distribution = {row['age_group']: row['count'] for row in age_stats}
    
    # Search and filters handling
    search_query = request.args.get('search', '')
    disease_filter = request.args.get('disease', '')
    
    query = 'SELECT * FROM patients WHERE 1=1'
    params = []
    
    if search_query:
        query += ' AND (name LIKE ? OR phone LIKE ?)'
        params.extend([f'%{search_query}%', f'%{search_query}%'])
        
    if disease_filter:
        query += ' AND predicted_disease = ?'
        params.append(disease_filter)
        
    query += ' ORDER BY created_at DESC'
    patients_list = conn.execute(query, params).fetchall()
    
    # Unique diseases for the filter dropdown
    all_diseases = conn.execute('SELECT DISTINCT predicted_disease FROM patients').fetchall()
    
    conn.close()
    
    return render_template('dashboard.html', 
                           total_patients=total_patients,
                           disease_distribution=disease_distribution,
                           age_distribution=age_distribution,
                           patients=patients_list,
                           all_diseases=[d['predicted_disease'] for d in all_diseases],
                           search_query=search_query,
                           disease_filter=disease_filter)

# API Endpoint for AJAX stats updates (optional, for frontend dynamic updates)
@app.route('/api/stats')
def api_stats():
    if not session.get('logged_in'):
        return jsonify({'error': 'Unauthorized'}), 401
        
    conn = get_db_connection()
    disease_stats = conn.execute('''
        SELECT predicted_disease, COUNT(*) as count 
        FROM patients 
        GROUP BY predicted_disease
    ''').fetchall()
    
    labels = [row['predicted_disease'] for row in disease_stats]
    data = [row['count'] for row in disease_stats]
    
    conn.close()
    return jsonify({
        'labels': labels,
        'data': data
    })

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
