import streamlit as st
import joblib
import pandas as pd
import numpy as np

# Page config
st.set_page_config(
    page_title="IVX Health - No-Show Predictor",
    page_icon="🏥",
    layout="centered"
)

# Load Model
@st.cache_resource
def load_model():
    artifacts = joblib.load('models/best_model.pkl')
    return artifacts

st.title("🏥 IVX Health: No-Show Prediction Dashboard")
st.markdown("Predict the likelihood of a patient missing their infusion appointment based on their details and history.")

try:
    artifacts = load_model()
    model = artifacts['model']
    scaler = artifacts['scaler']
    feature_cols = artifacts['feature_cols']
    best_model_name = artifacts.get('best_model_name', 'Trained Model')
    metrics = artifacts.get('metrics', {})
    
    st.sidebar.success(f"✅ Loaded: {best_model_name}")
    st.sidebar.info(f"Test Recall: {metrics.get('recall', 0)*100:.1f}%\n\nTest F1: {metrics.get('f1', 0):.3f}")
except Exception as e:
    st.error(f"Error loading model: {e}")
    st.stop()

# --- Input Form ---
with st.form("prediction_form"):
    st.header("Patient & Appointment Details")
    
    col1, col2 = st.columns(2)
    
    with col1:
        age = st.number_input("Patient Age", min_value=0, max_value=120, value=45)
        lead_time_days = st.number_input("Lead Time (Days from booking to appointment)", min_value=0, max_value=365, value=14)
        
        # We need appointment_day_of_week (0=Monday, 6=Sunday)
        day_of_week_name = st.selectbox("Appointment Day of Week", ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"])
        day_map = {"Monday": 0, "Tuesday": 1, "Wednesday": 2, "Thursday": 3, "Friday": 4, "Saturday": 5, "Sunday": 6}
        appointment_day_of_week = day_map[day_of_week_name]
        
        is_weekend = 1 if appointment_day_of_week in [5, 6] else 0
        
        sms_received = st.selectbox("SMS Reminder Received?", ["No", "Yes"])
        sms_val = 1 if sms_received == "Yes" else 0

    with col2:
        has_prior_conditions = st.selectbox("Chronic Conditions? (Diabetes, Hypertension, etc.)", ["No", "Yes"])
        cond_val = 1 if has_prior_conditions == "Yes" else 0
        
        total_prior_appointments = st.number_input("Total Prior Appointments", min_value=0, max_value=200, value=5)
        prior_no_shows = st.number_input("Prior No-Shows Count", min_value=0, max_value=total_prior_appointments, value=1)
        
        # Calculate rate automatically
        denom = 1 if total_prior_appointments == 0 else total_prior_appointments
        prior_no_show_rate = prior_no_shows / denom

    submitted = st.form_submit_button("Predict No-Show Likelihood")

# --- Prediction Logic ---
if submitted:
    # Build dataframe for prediction to match training
    input_data = pd.DataFrame([{
        'Age': age,
        'lead_time_days': lead_time_days,
        'appointment_day_of_week': appointment_day_of_week,
        'is_weekend': is_weekend,
        'SMS_received': sms_val,
        'has_prior_conditions': cond_val,
        'prior_no_shows': prior_no_shows,
        'total_prior_appointments': total_prior_appointments,
        'prior_no_show_rate': prior_no_show_rate
    }])
    
    # Ensure columns match exactly
    input_data = input_data[feature_cols]
    
    # Scale if we are using the Logistic Regression model
    if best_model_name == 'Logistic Regression':
        input_data_processed = scaler.transform(input_data)
    else:
        input_data_processed = input_data
        
    # Get probability of class 1 (No-Show)
    proba = model.predict_proba(input_data_processed)[0][1]
    prediction = model.predict(input_data_processed)[0]
    
    st.markdown("---")
    st.header("Prediction Results")
    
    col_res1, col_res2 = st.columns(2)
    
    with col_res1:
        if prediction == 1:
            st.error(f"🚨 High Risk: NO-SHOW")
        else:
            st.success(f"✅ Low Risk: WILL SHOW")
            
    with col_res2:
        st.metric(label="Probability of No-Show", value=f"{proba * 100:.1f}%")
        
    # Provide actionable insight
    st.markdown("### 💡 Recommended Action")
    if proba > 0.7:
        st.warning("- **Critical Risk:** Call the patient immediately. Consider double-booking this infusion chair.")
    elif proba > 0.4:
        st.info("- **Elevated Risk:** Send an additional personalized text message or email reminder 24 hours prior.")
    else:
        st.success("- **Standard Protocol:** Routine automated reminders are sufficient.")
