# src/cleaning.py
import pandas as pd
from datetime import datetime
from pathlib import Path

def clean_appointment_data(df):
    """
    Cleans the medical appointment dataset and engineers features.
    
    Cleaning Steps:
    1. Drop duplicates
    2. Handle missing values (Age, SMS_received)
    3. Fix data inconsistencies (negative ages, future scheduled dates)
    4. Engineer temporal and behavioral features
    
    Returns:
        df_clean (pd.DataFrame): Cleaned dataset
        cleaning_log (dict): Summary of cleaning actions for report
    """
    # Make a copy to avoid SettingWithCopyWarning
    df_clean = df.copy()
    cleaning_log = {
        'original_rows': len(df_clean),
        'duplicates_removed': 0,
        'missing_values_handled': 0,
        'outliers_removed': 0,
        'final_rows': 0
    }
    
    # =========================================
    # STEP 1: Remove Duplicates
    # =========================================
    original_count = len(df_clean)
    df_clean = df_clean.drop_duplicates()
    cleaning_log['duplicates_removed'] = original_count - len(df_clean)
    
    # =========================================
    # STEP 2: Handle Missing Values
    # =========================================
    # Check for missing values
    missing_before = df_clean.isnull().sum().sum()
    
    # Drop rows with missing critical fields (e.g., Age, No-show status)
    df_clean = df_clean.dropna(subset=['Age', 'No-show'])
    
    # Fill missing SMS_received with 0 (assume no SMS if missing)
    if 'SMS_received' in df_clean.columns:
        df_clean['SMS_received'] = df_clean['SMS_received'].fillna(0)
    
    missing_after = df_clean.isnull().sum().sum()
    cleaning_log['missing_values_handled'] = missing_before - missing_after
    
    # =========================================
    # STEP 3: Fix Data Inconsistencies & Outliers
    # =========================================
    # Remove negative ages (data entry error)
    negative_age_count = (df_clean['Age'] < 0).sum()
    df_clean = df_clean[df_clean['Age'] >= 0]
    cleaning_log['outliers_removed'] += negative_age_count
    
    # Remove extreme ages (>100 is possible but rare, check your data)
    extreme_age_count = (df_clean['Age'] > 100).sum()
    df_clean = df_clean[df_clean['Age'] <= 100]
    cleaning_log['outliers_removed'] += extreme_age_count
    
    # Convert ScheduledDay and AppointmentDay to datetime
    df_clean['ScheduledDay'] = pd.to_datetime(df_clean['ScheduledDay'])
    df_clean['AppointmentDay'] = pd.to_datetime(df_clean['AppointmentDay'])
    
    # Remove appointments where ScheduledDay is AFTER AppointmentDay (impossible)
    invalid_dates = (df_clean['ScheduledDay'] > df_clean['AppointmentDay']).sum()
    df_clean = df_clean[df_clean['ScheduledDay'] <= df_clean['AppointmentDay']]
    cleaning_log['outliers_removed'] += invalid_dates
    
    # =========================================
    # STEP 4: Feature Engineering (Requirement: 3+ features)
    # =========================================
    
    # Feature 1: lead_time_days (days between scheduling and appointment)
    df_clean['lead_time_days'] = (df_clean['AppointmentDay'] - df_clean['ScheduledDay']).dt.days
    
    # Feature 2: appointment_day_of_week (0=Monday, 6=Sunday)
    df_clean['appointment_day_of_week'] = df_clean['AppointmentDay'].dt.dayofweek
    
    # Feature 3: is_weekend (1 if Saturday/Sunday, 0 otherwise)
    df_clean['is_weekend'] = df_clean['appointment_day_of_week'].isin([5, 6]).astype(int)
    
    # Feature 4: has_prior_conditions (1 if has Diabetes, Hypertension, or Alcoholism)
    condition_cols = ['Diabetes', 'Hypertension', 'Alcoholism']
    available_cols = [c for c in condition_cols if c in df_clean.columns]
    if available_cols:
        df_clean['has_prior_conditions'] = df_clean[available_cols].sum(axis=1).clip(0, 1)
    
    # Feature 5: age_group (categorical for analysis)
    df_clean['age_group'] = pd.cut(
        df_clean['Age'], 
        bins=[0, 18, 35, 60, 100], 
        labels=['Child', 'Young Adult', 'Adult', 'Senior']
    )
    
    # =========================================
    # STEP 5: Finalize Log
    # =========================================
    cleaning_log['final_rows'] = len(df_clean)
    
    return df_clean, cleaning_log


def save_cleaned_data(df, output_path='data/processed/cleaned_appointments.csv'):
    """
    Saves cleaned data to the processed folder.
    """
    project_root = Path(__file__).parent.parent
    full_path = project_root / output_path
    full_path.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(full_path, index=False)
    print(f"Cleaned data saved to {full_path}")


# Example usage when running this file directly
if __name__ == "__main__":
    from data_loader import load_raw_data
    
    df = load_raw_data()
    df_clean, log = clean_appointment_data(df)
    
    print("\n=== Cleaning Summary ===")
    for key, value in log.items():
        print(f"{key}: {value}")
    
    save_cleaned_data(df_clean)