# IVX Health No-Show Prediction

## Project Overview
Predicting patient no-shows to optimize infusion center scheduling. This project implements an end-to-end data science pipeline from raw data to deployed insight.

## Data
The raw dataset (`data/raw/appointments.csv`) is included in this repository for reproducibility. 
### Sources
[Kaggle - Medical Appointment No Shows](https://www.kaggle.com/datasets/joniarroba/noshowappointments)

## Installation & Reproducibility

### Prerequisites
- Python 3.10+
- Jupyter Notebook

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