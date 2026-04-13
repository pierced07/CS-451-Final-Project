# IVX Health No-Show Prediction

## Project Overview
Predicting patient no-shows to optimize infusion center scheduling. This project implements an end-to-end data science pipeline from raw data to deployed insight.

## Team
- Pierce Daugherty — Data pipeline, EDA, modeling, deployment

## Data
The raw dataset (`data/raw/Medical_Appointment_No_Shows.csv`) is included in this repository for reproducibility.

### Source
[Kaggle - Medical Appointment No Shows](https://www.kaggle.com/datasets/joniarroba/noshowappointments)

## Installation & Reproducibility

### Prerequisites
- Python 3.10+
- pip

### Setup
```bash
# Clone repository
git clone https://github.com/pierced07/ivx-no-shows.git
cd ivx-no-shows

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

### Run EDA Notebook
jupyter notebook notebooks/01_EDA.ipynb

### Cleaning Pipeline
python src/cleaning.py

### Streamlit App
streamlit run app.py